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
  console.log(el, color);
  var height = 300;

  // transform data, pre-calculate y0 bar stack offset
  data = d3.layout.stack()(data);

  // insert DOM
  var $canvas = $('<div class="chart" />').insertAfter(el);

  // derived configuration
  var width = $canvas.width();

  // setup d3
  var vis = d3.select($canvas[0])
            .append("svg")
            .attr("width", width)
            .attr("height", height);

  // continue d3 configuration
  var len_series = data.length;
  var len_x = data[0].length,
      min_x = data[0][0].x,
      max_x = data[0][len_x - 1].x,
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
                  .domain([min_x, max_x + 1])
                  .range([0, width]);
      x = function(d) { return x_scale(d.x); },
      y_scale_stack = d3.scale.linear()
                        .domain([0, max_totaly])
                        .range([0, height]);
      y_scale_stack2 = d3.scale.linear()
                        .domain([0, max_totaly])
                        .range([height, 0]);
      // map bottom y value
      // y0_stack = function(d) { return height * (1 - d.y0 / max_totaly); },
      // map top y value
      y_stack = function(d) { return y_scale_stack(d.y + d.y0); },
      // map y value
      // y = function(d) { return height * d.y / max_totaly; };
      bar_width = width / len_x * 0.9;

  // set up a layer for each series
  var layers = vis.selectAll("g.layer")
    .data(data)
    .enter().append("g")
      .attr("class", "layer")
      .style("fill", function(d, i) { return color(i / (len_series - 1)); });

  // setup a bar for each point in a series
  var bars = layers.selectAll("g.bar")
    .data(function(d) { return d; })
    .enter().append("g")
      .attr("class", "bar");

  // set the bar width and height
  bars.append("rect")
    .attr("width", bar_width)
    .attr("x", x)
    .attr("y", height)
    .attr("height", 0)
    .transition()
      .delay(function(d, i) { return i * 10; })
      // .attr("y", function(d) { return y_scale_stack(d.y0); })  // inverse
      .attr("y", function(d) { return y_scale_stack2(d.y + d.y0); })
      .attr("height", function(d) { return y_scale_stack(d.y); });

  $canvas.find('g.bar > rect').tooltip({title: function(){
    return this.__data__.title;
  }});

  return {
  };
};

var $source = $('#pricetrends table');
var data = buildTableData($source);
var chart = stackedBarChart($source[0], data);
