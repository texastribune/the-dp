/*
  Based on:
  http://mbostock.github.com/d3/ex/stack.html
*/

function buildTableData($table){
  // build data
  var $headings = $table.find('thead th').map(function(){ return $(this).text(); });
  var $rows = $table.find('tbody > tr');
  var data = $headings.slice(1).toArray().map(function(){ return []; });
  $rows.each(function(_, row){
    var $cells = $(row).children();
    var xVal = +$cells.eq(0).text();
    $cells.slice(1).each(function(idx, cell){
      data[idx].push({
        x: xVal,
        y: $(cell).data('value'),
        title: "" + $headings[idx + 1] + " " + xVal + " <strong>" + $.trim($(cell).text()) + "</strong>"
      });
    });
  });
  return data;
}

var stackedBarChart = function(el, data){
  var color = d3.interpolateRgb("#aad", "#556");
  var height = 300;
  var margin = [10, 50, 10, 50];
  var x_axis_height = 30;

  // transform data, pre-calculate y0 bar stack offset
  data = d3.layout.stack()(data);

  // insert DOM
  var $canvas = $('<div class="chart" />').insertAfter(el);

  // derived configuration
  var width = $canvas.width();

  // setup d3
  var svg = d3.select($canvas[0])
            .append("svg:svg")
            .attr("width", width)
            .attr("height", height);

  w = width - margin[1] - margin[3];
  h = height - margin[0] - margin[2] - x_axis_height;
  var vis = svg
            .append("g")
            .attr("class", "vis")
            .attr("width", w)
            .attr("height", h)
            .attr("transform", "translate(" + margin[3] + "," + margin[0] + ")");

  // continue d3 configuration
  var len_series = data.length;
  var len_x = data[0].length,
      min_x = data[0][0].x,
      max_x = data[0][len_x - 1].x,
      bar_width = w / len_x * 0.9,
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
                  .range([0, w]),
      x = function(d) { return x_scale(d.x); },
      height_scale_stack,  // scaler for mapping height
      y_scale_stack,  // scaler for mapping y position
      y_stack;  // scaler for mapping y position considering stacked offset

  // sets global height and scales
  function rescale(new_height){
    max_totaly = new_height;
    height_scale_stack = d3.scale.linear()
                      .domain([0, max_totaly])
                      .range([0, h]);
    y_scale_stack = d3.scale.linear()
                      .domain([0, max_totaly])
                      .range([h, 0]);
    y_stack = function(d) { return y_scale_stack(d.y + d.y0); };
  }

  rescale(max_totaly);

  vis.attr("transform", "translate(" + (margin[3] - bar_width / 2) + "," + margin[0] + ")");

  // set up a layer for each series
  var layers = vis.selectAll("g.layer")
    .data(data)
    .enter().append("g")
      .attr("class", "layer")
      .style("fill", function(d, i) { return color(i / (len_series - 1)); });

  // setup a bar for each point in a series
  var bars = layers.selectAll("rect.bar")
    .data(function(d) { return d; })
    .enter().append("rect")
      .attr("class", "bar")
      .attr("width", bar_width)
      .attr("x", x)
      .attr("y", h)
      .attr("height", 0)
      .transition()
        .delay(function(d, i) { return i * 10; })
        // .attr("y", function(d) { return height_scale_stack(d.y0); })  // inverse
        .attr("y", function(d) { return y_scale_stack(d.y + d.y0); })
        .attr("height", function(d) { return height_scale_stack(d.y); });

  $canvas.find('rect.bar').tooltip({title: function(){
    return this.__data__.title;
  }});

  // FIXME formatter is wrong, assumes this is a number instead of a year
  x_axis = d3.svg.axis().scale(x_scale).tickSize(6, 1, 1);
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(" + (margin[3]) + "," + (height - margin[2] - x_axis_height) + ")")
      .call(x_axis);

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
        .attr("y", function(d) { return y_scale_stack(d.y + d.y0); })
        .attr("height", function(d) { return height_scale_stack(d.y); });
    return layers;
  }

  return {
    setData: set_data
  };
};
