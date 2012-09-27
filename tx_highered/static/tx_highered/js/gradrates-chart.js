(function(){

  // boilerplate
  var Chart = D3GroupedBarChart.extend({
    getLayerOffset: function(i) {
      return 20 - 10 * i;
    },

    getBarWidth: function(){
      var len_series = this._data.length; // m, i, rows
      var len_x = this._data[0].length;   // n, j, cols
      var bar_width = this.options.plot_box.w / len_x;  // bar_width is an outer width
      bar_width = bar_width - 20 - 10;
      return bar_width;
    },

    // y-axis shows percentage
    getYDomain: function(){
      return [0, 100];
    },

    getLegendSeriesTitle: function(d, i){
      return d[0].series;
    }
  });


  var $section = $('#gradrates'),
      data = $section.find('table.data-source').tabulate().toArray().reverse(),
      options = {
        color: ['#99c', '#639', '#306'],
        tooltip: function() {
          // TODO: replace with Handlebars
          return this.__data__.series + " bachelor's graduation rate<br><b>" +
            d3.format(",.1f")(this.__data__.y) + "%</b>";
        },
        xAxis: {
          enabled: true,
          title: "Year"
        },
        yAxis: {
          enabled: true,
          title: "Percent",
          tickFormat: function(a){ return a + '%'; }
        },
        legendElem: $section.find('.legend')
      };

  new Chart($section.find('.d3-viz'), data, options);
})();
