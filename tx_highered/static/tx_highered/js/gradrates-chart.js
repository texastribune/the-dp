(function(){
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

  // y-axis shows percentage
  GradRatesChart.prototype.get_y_domain = function(){
    return [0, 100];
  };

  // BEGIN
  var $section = $('#gradrates');
  var $source = $section.find('table');
  var data = $source.tabulate().toArray().reverse();
  var colors = ['#99c', '#639', '#306'];

  var chart = new GradRatesChart(
        $section.placeChartContainer(),
        data,
        {
          'color': colors,
          'tooltip': function(){
            var d = this.__data__;
            return d.series + " bachelor's graduation rate<br><b>" +
              d3.format(",.2f")(this.__data__.y) + "%</b>";
          }
        });

})();
