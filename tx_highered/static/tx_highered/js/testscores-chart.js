/*global D3GroupedBarChart */
(function(){
  "use strict";
// begin file-iffy, unindent


/***************** TEST SCORES BAR CHART ******************/
var TestScoresChart = D3GroupedBarChart.extend();
window.TestScoresChart = TestScoresChart;

TestScoresChart.prototype.initData = function(new_data){
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
      y_max: datum.sat.verbal[1]
    });
    processed_data.math.push({
      x: datum.year,
      y: datum.sat.math[0],
      y_max: datum.sat.math[1]
    });
    processed_data.writing.push({
      x: datum.year,
      y: datum.sat.writing[0],
      y_max: datum.sat.writing[1]
    });
  }
  var data = [processed_data.verbal, processed_data.math, processed_data.writing];
  this._data = data;
  return data;
};

TestScoresChart.prototype.getYDomain = function(){
  return [200, 800];
};

TestScoresChart.prototype.getY = function(){
  var self = this;
  return function(d) { return self.y_scale(d.y_max); };
};

TestScoresChart.prototype.getH = function(){
  var self = this;
  return function(d) { return self.height_scale(d.y_max - d.y); };
};

var series = ["verbal", "math", "writing"];

TestScoresChart.prototype.getLegendSeriesTitle = function(d, i){
  return series[i];
};

// end file iffy
})();
