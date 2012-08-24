
/* globals: d3, $ */

var TestScoresChart = D3GroupedBarChart.extend();

TestScoresChart.prototype.init_data = function(new_data){
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
      y_min: datum.sat.verbal[0],
      y_max: datum.sat.verbal[1]
    });
    processed_data.math.push({
      x: datum.year,
      y: datum.sat.math[0],
      y_min: datum.sat.math[0],
      y_max: datum.sat.math[1]
    });
    processed_data.writing.push({
      x: datum.year,
      y: datum.sat.writing[0],
      y0: datum.sat.writing[1] - datum.sat.writing[0],
      y_min: datum.sat.writing[0],
      y_max: datum.sat.writing[1]
    });
  }
  var data = [processed_data.verbal, processed_data.math, processed_data.writing];
  this._data = data;
  return data;
};

TestScoresChart.prototype.find_ceiling = function(){
  return 800;
};

// setup a bar for each point in a series
TestScoresChart.prototype.bars = function(){
  var self = this;
  return this._layers.selectAll("rect.bar")
    .data(function(d) { return d; })
    .enter().append("rect")
      .attr("class", "bar")
      .attr("width", self.bar_width * 0.9)
      .attr("x", self.x)
      .attr("y", self.options.plot_box.h)
      .attr("height", 0)
      .transition()
        .delay(function(d, i) { return i * 10; })
        // .attr("y", function(d) { return height_scale_stack(d.y0); })  // inverse
        .attr("y", self.y)
        .attr("height", function(d) { return self.height_scale(d.y_max - d.y_min); });
};
