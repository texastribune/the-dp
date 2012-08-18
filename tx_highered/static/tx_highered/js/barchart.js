/*
  Based on:
  http://mbostock.github.com/d3/ex/stack.html
*/

var d3BarChart = function(el, data, options){
  var defaultOptions = {
    style: 'stacked'
  };
  var color = d3.scale.category10();
  var width = 940;
  var height = 300;
  var margin = [10, 50, 10, 50];
  var enable_axis_x = true;
  var enable_axis_y = true;
  var bottom_axis_height = enable_axis_x ? 30 : 0;
  var left_width = enable_axis_y ? 40 : 0;

  options = $.extend({}, defaultOptions, options);

  // configure plot area
  var plot = {
    w: width - margin[1] - margin[3] - left_width,
    h: height - margin[0] - margin[2] - bottom_axis_height
  };


  // transform data, pre-calculate y0 bar stack offset
  data = d3.layout.stack()(data);

  // continue d3 configuration
  var len_series = data.length;
  var len_x = data[0].length,
      min_x = data[0][0].x,
      max_x = data[0][len_x - 1].x,
      bar_width = plot.w / len_x * 0.9,
      max_totaly = d3.max(data, function(d) {
        return d3.max(d, function(d) {
          return d.y0 + d.y;
        });
      }),
      // max_y = d3.max(data, function(d) {
      //   return d3.max(d, function(d) {
      //     return d.y;
      //   });
      // }),
      // map x value
      x_scale = d3.scale.linear()
                  .domain([min_x, max_x])
                  .range([0, plot.w]),
      x = function(d) { return x_scale(d.x); },
      height_scale_stack,  // scaler for mapping height
      y_scale,
      y;

  // sets global height and scales
  function rescale(new_height){
    height_scale_stack = d3.scale.linear()
                      .domain([0, new_height])
                      .range([0, plot.h]);
    y_scale = d3.scale.linear()
        .domain([0, new_height])
        .range([plot.h, 0]);
  }
  rescale(max_totaly);

  if (options.style == "grouped") {
    bar_width = bar_width / len_series;
  }

  if (options.style == "stacked"){
    y = function(d) { return y_scale(d.y + d.y0); };
  } else {
    y = function(d) { return y_scale(d.y); };
  }


  // setup d3 canvas
  var svg = d3.select(el)
            .append("svg:svg")
            .attr("width", "100%")
            .attr("height", "100%")
            .attr("viewBox", [0, 0, width, height].join(" "))
            .attr("preserveAspectRatio", "xMinYMin meet");

  // setup d3 plot area
  var vis = svg
            .append("g")
            .attr("class", "vis")
            .attr("width", plot.w)
            .attr("height", plot.h)
            .attr("transform", "translate(" + (margin[3] + left_width) + "," + margin[0] + ")");

  // set up a layer for each series
  var layers = vis.selectAll("g.layer")
    .data(data)
    .enter().append("g")
      .attr("class", "layer")
      .style("fill", function(d, i) { return color(i / (len_series - 1)); });

  if (options.style == "grouped") {
    layers
      .attr("transform", function(d, i) {
        // only tested for len_series == 2
        var offset = bar_width * (0.5 + i - len_series / 2);
        return "translate(" + offset + ",0)";
      });
  }

  // setup a bar for each point in a series
  var bars = layers.selectAll("rect.bar")
    .data(function(d) { return d; })
    .enter().append("rect")
      .attr("class", "bar")
      .attr("width", bar_width)
      .attr("x", x)
      .attr("y", plot.h)
      .attr("height", 0)
      .attr("transform", "translate(" + (-bar_width/2) + ",0)")
      .transition()
        .delay(function(d, i) { return i * 10; })
        // .attr("y", function(d) { return height_scale_stack(d.y0); })  // inverse
        .attr("y", y)
        .attr("height", function(d) { return height_scale_stack(d.y); });

  // tooltip
  $('rect.bar', svg.$elem).tooltip({title: function(){ return this.__data__.title; }});

  if (enable_axis_x) {
    x_axis = d3.svg.axis()
             .scale(x_scale)
             .tickSize(6, 1, 1)
             .tickFormat(function(a){ return a; });
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(" + (margin[3] + left_width) + "," + (height - margin[2] - bottom_axis_height) + ")")
        .call(x_axis);
  }

  if (enable_axis_y) {
    y_axis = d3.svg.axis()
             .scale(y_scale)
             .orient("left");
    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + margin[3] + "," + margin[0] + ")")
        .call(y_axis);
  }

  // interaction, new data api
  function set_data(new_data){
    // process add stack offsets
    data = d3.layout.stack()(new_data);

    // reset height ceiling
    ceiling = d3.max(data, function(d) {
      return d3.max(d, function(d) {
        return d.y0 + d.y;
      });
    });
    // if (ceiling > max_totaly) {
    //   rescale(ceiling);
    // }
    rescale(ceiling);

    // update layers data
    layers.data(data);
    // update bars data :(
    layers.selectAll("rect.bar")
      .data(function(d) { return d; })
      .transition()
        .attr("y", y)
        .attr("height", function(d) { return height_scale_stack(d.y); });
    return layers;
  }

  return {
    // properties
    elem: el,

    // methods
    setData: set_data
  };
};
