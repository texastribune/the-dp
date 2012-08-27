var GradRatesChart = D3BarChart.extend();

GradRatesChart.prototype.get_layers = function(){
  // set up a layer for each series
  var self = this;
  var layers = self.plot.selectAll("g.layer")
    .data(this._data)
    .enter().append("g")
      .attr("class", "layer")
      .style("fill", function(d, i) { return self.options.color(i); });
  // shift grouped bars so they're adjacent to each other
  layers
    .attr("transform", function(d, i) {
      var offset = 20 - 10 * i;
      return "translate(" + offset + ",0)";
    });
  return layers;
};

GradRatesChart.prototype.get_bar_width = function(){
  var len_series = this._data.length; // m, i, rows
  var len_x = this._data[0].length;   // n, j, cols
  var bar_width = this.options.plot_box.w / len_x;  // bar_width is an outer width
  bar_width = bar_width - 20 - 10;
  return bar_width;
};


  var $section = $('#gradrates');
  var $source = $section.find('table');
  var data = $source.tabulate();
  data = [data[2], data[1], data[0]];  // reverse
  var colors = ['#99c', '#639', '#306'];
  colors = [colors[2], colors[1], colors[0]];

  var chart = new GradRatesChart($('<div class="chart" />').appendTo($section)[0],
        data,
        {
          'color': d3.scale.ordinal().range(colors)
        });

  chart.get_y_domain = function(){
    return [0, 100];
  };
  chart.refresh();
