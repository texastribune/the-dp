/*global $, d3, normalizeFirst, D3StackedBarChart, D3GroupedBarChart */
(function(){
  "use strict";

  var $section = $('#pricetrends');
  var $source = $section.find('table');
  var data = $source.tabulate();

  // store

  var price_colors = ['#39c', '#066', '#9c6', '#9cc'];
                                               // instate, outstate, roomboard, books
  var zeroes = data[0].map(function(a){ return {x: a.x, y: 0}; });
  var chart = new D3StackedBarChart($section.placeChartContainer(),
      [data[0], zeroes, data[3], data[2]],
      {
        'color': price_colors,
        'tooltip': function(){
          var d = this.__data__;
          return d.series + " " + d.x + " <b>$" + d3.format(",.0f")(d.y) + "</b>";
        }
      });
  $source.find('th:eq(1)').click(function(){
    chart.data([data[0], zeroes, data[3], data[2]]);
  });
  $source.find('th:eq(2)').click(function(){
    chart.data([zeroes, data[1], data[3], data[2]]);
  });

  var chart2 = new D3GroupedBarChart($section.placeChartContainer(),
              [data[0], data[1]],
              {
                'color': price_colors
              });

  var normData = normalizeFirst([data[0], data[1]], 0);
  var chart3 = new D3GroupedBarChart($section.placeChartContainer(),
        normData,
        {
          'color': price_colors,
          'style': 'grouped',
          'tooltip': function(){
            var d = this.__data__;
            return d.series + " <b>" + d3.format(",.2f")(this.__data__.y - 100) + "%</b>";
          }
        });
  // change yaxis tick format
  chart3.yAxis.tickFormat(function(a){ return a - 100 + '%'; });
  // add sea-level line
  var s = chart3.yAxis.scale();
  chart3.plot.selectAll('line.sealevel')
    .data([100, 200, 300, 400])
      .enter().append('line').attr('class', 'sealevel')
        .attr('x1', 0)
        .attr('x2', '100%')
        .attr('y1', 0)
        .attr('y2', 0)
        .attr('stroke-opacity', 0)
        .attr("transform", function(d){ return "translate(0, " + s(d) + ")"; })
        .transition()
          .attr("transform", function(d){ return "translate(0, " + s(d) + ")"; })
          .attr('stroke-opacity', 100);
  chart3.refresh();

  var x_array = data[0].map(function(a){ return a.x; });
  chart3.plot.selectAll('rect.bar').on("click", function(){
    var idx = x_array.indexOf(this.__data__.x);
    if (idx === -1) { return; }
    var normData = normalizeFirst([data[0], data[1]], idx);
    chart3.data(normData);
    chart3.plot.selectAll('line.sealevel')  // called after .enter() AND updates
      .transition()
        .attr("transform", function(d){ return "translate(0, " + s(d) + ")"; })
        .attr('stroke-opacity', 100);
  });

})();
