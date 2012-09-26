(function(exports, d3, D3GroupedBarChart){
  "use strict";
// begin file-iffy, unindent


/***************** TEST SCORES BAR CHART ******************/
var series = ["Critical Reading", "Math", "Writing"];

var TestScoresChart = exports.TestScoresChart = D3GroupedBarChart.extend({
  initData: function(new_data){
    // only do SAT
    /*
      from:
      [{year: 2011, sat:{verbal: [530, 730], act:{}}}]

      to:
      [{x: 2011, y_min: 530, y_max: 730, type: 'verbal'}]
    */
    var processed_data = {verbal:[], math:[], writing:[]};
    for (var i = 0; i < new_data.length; i++){
      var datum = new_data[i];
      processed_data.verbal.push({
        x: datum.year,
        y: datum.sat.verbal[0],
        y_max: datum.sat.verbal[1],
        n: 2 + !!datum.sat.writing[0]
      });
      processed_data.math.push({
        x: datum.year,
        y: datum.sat.math[0],
        y_max: datum.sat.math[1],
        n: 2 + !!datum.sat.writing[0]
      });
      processed_data.writing.push({
        x: datum.year,
        y: datum.sat.writing[0],
        y_max: datum.sat.writing[1],
        n: 2 + !!datum.sat.writing[0]
      });
    }
    var data = [processed_data.verbal, processed_data.math, processed_data.writing];
    this._data = data;
    return data;
  },

  // set to the range of valid SAT scores
  getYDomain: function(){
    return [200, 800];
  },

  getY: function(){
    var self = this;
    return function(d) { return self.y_scale(d.y_max); };
  },

  getH: function(){
    var self = this;
    return function(d) { return self.height_scale(d.y_max - d.y); };
  },

  // series data isn't in the data, grab it externally
  getLegendSeriesTitle: function(d, i){
    return series[i];
  },

  // hack so we can conditionally set bar width
  getBars: function(){
    var self = this;
    var bars = this._layers.selectAll("rect.bar")
      .data(function(d) { return d; })
      .enter().append("rect")
        .attr("class", "bar")
        .attr("width", function(d, i){
          var f = d.n == 2 ? 1.5 : 1;
          return f * self.bar_width * 0.9; })
        .attr("x", self.x)
        .attr("y", self.options.plot_box.h)
        .attr("height", 0)
        .transition()
          .delay(function(d, i) { return i * 10; })
          .attr("y", self.y)
          .attr("height", self.h);
    // now shift second series's bars to the right
    d3.select(self._layers[0][1]).selectAll("rect.bar")
        .attr("transform", function(d, i){
          var dx = d.n == 2 ? self.bar_width / 2 * 0.9 : 0;
          return "translate(" + dx + ", 0)";
        });
    return bars;
  }

});

// end file iffy
})(window, d3, D3GroupedBarChart);
