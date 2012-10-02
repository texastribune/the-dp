(function(exports, d3, D3GroupedBarChart, __extends){
  "use strict";
// begin file-iffy, unindent


/***************** TEST SCORES BAR CHART ******************/
exports.TestScoresChart = (function() {

  __extends(C, D3GroupedBarChart);

  function C(){
    return C.__super__.constructor.apply(this, arguments);
  }

  C.prototype.getCleanData = function(new_data){
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
  };

  C.prototype.getY = function(){
    var self = this;
    return function(d) { return self.yScale(d.y_max); };
  };

  C.prototype.getH = function(){
    var self = this;
    return function(d) { return self.hScale(d.y_max - d.y); };
  };

  // hack so we can conditionally set bar width
  C.prototype.getBars = function(){
    var self = this;
    var bars = this._layers.selectAll("rect.bar")
      .data(function(d) { return d; })
      .enter().append("rect")
        .attr("class", "bar")
        .attr("width", function(d, i){
          var f = d.n == 2 ? 1.5 : 1;
          return f * self.bar_width * 0.9; })
        .attr("x", self.x)
        .attr("y", self._options.plotBox.height)
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
  };

  return C;
})();

// end file iffy
})(window, d3, D3GroupedBarChart, __extends);
