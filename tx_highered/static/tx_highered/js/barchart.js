// data processor TODO move awaaaaay
function normalizeFirst(data, idx){
  data = $.extend(true, [], data);  // make a deep copy of data
  idx = idx || 0;
  // var max_first = data
  var max_value = Math.max.apply(null, data.map(function(d){ return d[idx].y; }));
  var set, factor;
  for (var i = 0; i < data.length; i++){
    set = data[i];
    factor = max_value / set[idx].y;
    for (var j = 0; j < set.length; j++){
      set[j].y *= factor / max_value * 100;
    }
  }
  return data;
}


/*
  Based on:
  http://mbostock.github.com/d3/ex/stack.html
*/
var d3BarChart = function(el, data, options){
  // merge user options and default options
  var defaultOptions = {
    color: d3.scale.category10(),
    style: 'stacked',
    tooltip: function(){ return this.__data__.title || this.__data__.y; }
  };
  var enable_axis_x = true;
  var enable_axis_y = true;
  var margin = [10, 50, 10, 50];
  options = $.extend({}, defaultOptions, options);

  // data pre-processor
  if (options.style == "stacked"){
    // transform data, pre-calculate y0 bar stack offset
    data = d3.layout.stack()(data);
  }

  // configure svg box
  var width = 940;
  var height = 300;
  // setup svg DOM
  var svg = d3.select(el)
            .append("svg")
            .attr("width", "100%")
            .attr("height", "100%")
            .attr("viewBox", [0, 0, width, height].join(" "))
            .attr("preserveAspectRatio", "xMinYMin meet");


  // configure plot box
  var left_axis_width = enable_axis_y ? 40 : 0;
  var bottom_axis_height = enable_axis_x ? 30 : 0;
  var plot_box = {
        w: width - margin[1] - margin[3] - left_axis_width,
        h: height - margin[0] - margin[2] - bottom_axis_height
      },
      bar_width;
  // setup plot DOM
  var plot = svg
            .append("g")
            .attr("class", "plot")
            .attr("width", plot_box.w)
            .attr("height", plot_box.h)
            .attr("transform", "translate(" + (margin[3] + left_axis_width) + "," + margin[0] + ")");

  // d3 configuration
  var len_series = data.length; // m, i, rows
  var len_x = data[0].length,   // n, j, cols
      min_x = data[0][0].x,
      max_x = data[0][len_x - 1].x,
      // TODO refactor to generate with or without d.y0 constant dyanamically
      find_ceiling = function(data){
        return d3.max(data, function(d) {
          return d3.max(d, function(d) {
            return d.y;
          });
        });
      },
      find_ceiling_stacked = function(data){
        return d3.max(data, function(d) {
          return d3.max(d, function(d) {
            return d.y + d.y0;
          });
        });
      },
      x_scale = d3.scale.linear()
                  .domain([min_x, max_x])
                  .range([0, plot_box.w]),
      x_axis,
      x = function(d) { return x_scale(d.x); },
      height_scale_stack = d3.scale.linear().range([0, plot_box.h]),
      y_scale = d3.scale.linear().range([plot_box.h, 0]),
      y_axis,
      y;

  // sets global height and scales
  function rescale(data_ceiling){
    height_scale_stack.domain([0, data_ceiling]);
    y_scale.domain([0, data_ceiling]);
    if (y_axis){
      svg.select('.y.axis').transition().call(y_axis);
    }
  }

  bar_width = plot_box.w / len_x;  // bar_width is an outer width
  if (options.style == "grouped") {
    // subdivide bar_width further
    bar_width = bar_width / len_series;
  }

  if (options.style == "stacked"){
    find_ceiling = find_ceiling_stacked;
    y = function(d) { return y_scale(d.y + d.y0); };
  } else {
    y = function(d) { return y_scale(d.y); };
  }
  rescale(find_ceiling(data));

  // set up a layer for each series
  var layers = plot.selectAll("g.layer")
    .data(data)
    .enter().append("g")
      .attr("class", "layer")
      .style("fill", function(d, i) { return options.color(i / (len_series - 1)); });
  // shift grouped bars so they're adjacent to each other
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
      .attr("width", bar_width * 0.9)
      .attr("x", x)
      .attr("y", plot_box.h)
      .attr("height", 0)
      .attr("transform", "translate(" + (-bar_width / 2) + ", 0)")
      .transition()
        .delay(function(d, i) { return i * 10; })
        // .attr("y", function(d) { return height_scale_stack(d.y0); })  // inverse
        .attr("y", y)
        .attr("height", function(d) { return height_scale_stack(d.y); });

  // tooltip
  $('rect.bar', svg[0]).tooltip({
    // manually call because options.tooltip can change
    title: function(){ return options.tooltip.call(this); }
  });

  // draw axes
  if (enable_axis_x) {
    x_axis = d3.svg.axis()
             .scale(x_scale)
             .tickSize(6, 1, 1)
             .tickFormat(function(a){ return a; });
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(" + (margin[3] + left_axis_width) + "," + (height - margin[2] - bottom_axis_height) + ")")
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

  // PUBLIC METHOD
  function set_or_get_data(new_data){
    if (new_data === void 0) {
      return data;
    }

    // process add stack offsets
    data = d3.layout.stack()(new_data);

    // reset height ceiling
    rescale(find_ceiling(data));

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

  // PUBLIC METHOD
  function set_or_get_option(name, newvalue){
    if (newvalue === void 0){
      return options[name];
    }
    options[name] = newvalue;
  }

  return {
    // properties
    elem: el,
    svg: svg,
    plot: plot,
    xAxis: x_axis,
    yAxis: y_axis,

    // methods
    setData: set_or_get_data,
    option: set_or_get_option
  };
};
