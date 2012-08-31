(function(){
  var $section = $('#gradrates'),
      $source = $section.find('table'),
      data = $source.tabulate().toArray().reverse(),
      colors = ['#99c', '#639', '#306'],
      options = {
        'color': colors,
        'tooltip': function() {
          // TODO: replace with Handlebars
          return this.__data__.series + " bachelor's graduation rate<br><b>" +
            d3.format(",.2f")(this.__data__.y) + "%</b>";
        }
      },
      Chart = D3BarChart.extend({
        get_layers: function(){
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
        },

        get_bar_width: function(){
          var len_series = this._data.length; // m, i, rows
          var len_x = this._data[0].length;   // n, j, cols
          var bar_width = this.options.plot_box.w / len_x;  // bar_width is an outer width
          bar_width = bar_width - 20 - 10;
          return bar_width;
        },

        // y-axis shows percentage
        get_y_domain: function(){
          return [0, 100];
        }
      });

  new Chart($section.find('.d3-viz'), data, options);

})();
