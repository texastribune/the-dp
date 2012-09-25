/*global $, d3, normalizeFirst, D3StackedBarChart, D3GroupedBarChart */
(function(){
  "use strict";

  var $section = $('#pricetrends');
  var $source = $section.find('table.data-source');
  var data = $source.tabulate();
  data = [data[0], data[1], data[3], data[2]];  // make sure books is last

  // store

                   // instate, outstate, roomboard, books
  var price_colors = ['#39c', '#066', '#9c6', '#E63'];
  var zeroes = data[0].map(function(a){ return {x: a.x, y: 0}; });
  var chart = new D3StackedBarChart($section.find(".chart:eq(0)"),
      [data[0], zeroes, data[2], data[3]],
      {
        'color': price_colors,
        'tooltip': function(){
          var d = this.__data__;
          return d.series + " " + d.x + " <b>$" + d3.format(",.0f")(d.y) + "</b>";
        }
      });
  $('#pricetrends .chart-help a').click(function(e){
    e.preventDefault();
    var $this = $(this);
    $this.parent().parent().find('.active').removeClass('active');
    $this.parent().addClass('active');
    var idx = $(this).data('idx');
    var copy = $.extend([], data);  // shallow copy, passing true/false won't
                                    // work because jquery is too smart for
                                    // itself and starts copying prototypes so
                                    // Arrays turn into Objects
    copy[idx] = zeroes;
    chart.data(copy);
  });

  var chart2 = new D3GroupedBarChart($section.find(".chart:eq(1)"),
              [data[0], data[1]],
              {
                'color': price_colors
              });

/* disabled
  var normData = normalizeFirst([data[0], data[1]], 0);
  var chart3 = new D3GroupedBarChart($section.find(".chart:eq(2)"),
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
*/

})();
