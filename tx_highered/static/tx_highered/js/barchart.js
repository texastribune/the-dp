/*global $, d3, Class */
(function(){
  "use strict";
// begin file-iffy, unindent


// data processor TODO move awaaaaay
function normalizeFirst(data, idx){
  data = $.extend(true, [], data);  // make a deep copy of data
  idx = idx || 0;
  // var max_first = data
  var max_value = Math.max.apply(null, data.map(function(d){ return d[idx].y; }));
  var set, factor;
  for (var i = 0; i < data.length; i++){
    set = data[i];
    factor = max_value / set[idx].y;
    for (var j = 0; j < set.length; j++){
      set[j].y *= factor / max_value * 100;
    }
  }
  return data;
}
window.normalizeFirst = normalizeFirst;

// shortcut for adding a chart to the given container element
$.fn.placeChartContainer = function(){
  var elem = $('<div class="chart d3-viz chart-viz"/>');
  this.append(elem);
  return elem;
};

/***************** CHART ******************/
var D3Chart = Class.extend({});
window.D3Chart = D3Chart;

// override this if data needs to be scrubbed before getting charted
D3Chart.prototype.init_data = function(data){ return data; };

// get or set data
D3Chart.prototype.data = function(new_data){
  var data;
  if (typeof new_data === "undefined"){
    return this._data;
  }

  this._data = this.init_data(new_data);
  this.refresh();
  return this;
};


// get or set data
D3Chart.prototype.refresh = function(){
  return this;
};
// get or set option
D3Chart.prototype.option = function(name, newvalue){
  if (typeof newvalue === "undefined"){
    return this.options[name];
  }
  this.options[name] = newvalue;
  return this;
};


/***************** BAR CHART ******************/
var D3BarChart = D3Chart.extend({});
window.D3BarChart = D3BarChart;

D3BarChart.prototype.init = function(el, data, options){
  var self = this;
  if (el.jquery) {  // todo what about things like zepto?
    this.elem = el[0];
    this.$elem = el;
  } else if (typeof el == "string"){
    this.elem = document.getElementById(el);
  } else {
    this.elem = el;
  }
  if (typeof data == "string"){  // if data is url
    d3.json(data, function(new_data) {
      self._data = self.init_data(new_data);
      self.setUp(options);
      self.render();
    });
  } else {
    this._data = this.init_data(data);
    this.setUp(options);
    this.render();
  }
};

D3BarChart.prototype.setUp = function(options){
  // merge user options and default options
  var self = this,
      data = this._data;
  var defaultOptions = {
        color: d3.scale.category10(),
        height: 300,
        width: 940,
        margin: [0, 0, 30, 50],
        tooltip: function(){ return this.__data__.title || this.__data__.y; },
        enable_axis_x: true,
        enable_axis_y: true
      };

  // set up box dimensions based on the parent element
  if (!self.$elem) { self.$elem = $(self.elem); }
  defaultOptions.height = self.$elem.height();
  defaultOptions.width = self.$elem.width();

  self.options = $.extend({}, defaultOptions, options);

  // allow an array of hex values for convenience
  if ($.isArray(self.options.color)) {
    self.options.color = d3.scale.ordinal().range(self.options.color);
  }

  // pre-calculate plot box dimensions
  var plot_box = {
        w: self.options.width - self.options.margin[1] - self.options.margin[3],
        h: self.options.height - self.options.margin[0] - self.options.margin[2]
      };
  self.options.plot_box = plot_box;

  // setup x scales
  var len_x = data[0].length,
      min_x = data[0][0].x,
      max_x = data[0][len_x - 1].x;
  this.x_scale = d3.scale.ordinal()
      .domain(d3.range(min_x, max_x + 1))
      .rangeRoundBands([0, plot_box.w], 0.1, 0.1);
  self.x_axis = null;
  self.x = function(d) { return self.x_scale(d.x); };

  // setup y scales
  self.height_scale = d3.scale.linear().range([0, plot_box.h]);
  self.y_scale = d3.scale.linear().range([plot_box.h, 0]);
  self.y_axis = null;
  self.y = self.get_y();
  self.h = self.get_h();

  // setup bar width
  self.bar_width = this.get_bar_width();
};

D3BarChart.prototype.render = function(){
  var self = this, svg, plot, x_axis, y_axis;

  // setup svg DOM
  svg = d3.select(this.elem)
          .append("svg")
          .attr("width", "100%")
          .attr("height", "100%")
          .attr("viewBox", [0, 0, this.options.width, this.options.height].join(" "))
          .attr("preserveAspectRatio", "xMinYMin meet");
  this.svg = svg;

  // setup plot DOM
  plot = svg
           .append("g")
           .attr("class", "plot")
           .attr("width", this.options.plot_box.w)
           .attr("height", this.options.plot_box.h)
           .attr("transform", "translate(" + this.options.margin[3] + "," + this.options.margin[0] + ")");
  this.plot = plot;

  this.rescale(self.get_y_domain());

  this._layers = this.get_layers();
  this.get_bars();

  // tooltip
  $('rect.bar', svg[0]).tooltip({
    // manually call because options.tooltip can change
    title: function(){ return self.options.tooltip.call(this); }
  });

  // draw axes
  if (self.options.enable_axis_x) {
    x_axis = d3.svg.axis()
      .orient("bottom")
      .scale(self.x_scale)
      .tickSize(6, 1, 1)
      .tickFormat(function(a){ return a; });
    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(" + self.options.margin[3] + "," + (self.options.height - self.options.margin[2]) + ")")
      .call(x_axis);
    self.xAxis = x_axis;
  }
  if (self.options.enable_axis_y) {
    y_axis = d3.svg.axis()
             .scale(self.y_scale)
             .orient("left");
    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + self.options.margin[3] + "," + self.options.margin[0] + ")")
        .call(y_axis);
    self.yAxis = y_axis;
  }
};

D3BarChart.prototype.get_y_domain = function(){
   return [0, this.get_max_y(this._data)];
};

D3BarChart.prototype.refresh = function(){
  var self = this,
      data = self._data;

  // reset height ceiling
  self.rescale(self.get_y_domain());

  // update layers data
  self._layers.data(data);
  // update bars data :(
  self._layers.selectAll("rect.bar")
    .data(function(d) { return d; })
    .transition()
      .attr("y", self.y)
      .attr("height", self.h);

  if (self.yAxis){
    self.svg.select('.y.axis').transition().call(self.yAxis);
  }
  return this;
};

D3BarChart.prototype.get_max_y = function(data){
  return d3.max(data, function(d) {
    return d3.max(d, function(d) {
      return d.y;
    });
  });
};

D3BarChart.prototype.get_y = function(){
  var self = this;
  return function(d) { return self.y_scale(d.y); };
};

D3BarChart.prototype.get_h = function(){
  var self = this;
  return function(d) { return self.height_scale(d.y); };
};

D3BarChart.prototype.rescale = function(extent){
  // TODO get rid of this method
  this.height_scale.domain([0, extent[1] - extent[0]]);
  this.y_scale.domain(extent);
  return this;
};

D3BarChart.prototype.get_layers = function(){
  // set up a layer for each series
  var self = this;
  var layers = self.plot.selectAll("g.layer")
    .data(this._data)
    .enter().append("g")
      .attr("class", "layer")
      .style("fill", function(d, i) { return self.options.color(i); });
  return layers;
};

// setup a bar for each point in a series
D3BarChart.prototype.get_bars = function(){
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
        .attr("y", self.y)
        .attr("height", self.h);
};

D3BarChart.prototype.get_bar_width = function(){
  var len_series = this._data.length; // m, i, rows
  var len_x = this._data[0].length;   // n, j, cols
  var bar_width = this.options.plot_box.w / len_x;  // bar_width is an outer width
  return bar_width;
};


/***************** STACKED BAR CHART ******************/
var D3StackedBarChart = D3BarChart.extend();
window.D3StackedBarChart = D3StackedBarChart;

D3StackedBarChart.prototype.init_data = function(new_data){
  // process add stack offsets
  return d3.layout.stack()(new_data);
};

D3StackedBarChart.prototype.get_max_y = function(data){
  return d3.max(data, function(d) {
    return d3.max(d, function(d) {
      return d.y + d.y0;
    });
  });
};

D3StackedBarChart.prototype.get_y = function(){
  var self = this;
  return function(d) { return self.y_scale(d.y + d.y0); };
};


/***************** GROUPED BAR CHART ******************/
var D3GroupedBarChart = D3BarChart.extend();
window.D3GroupedBarChart = D3GroupedBarChart;

D3GroupedBarChart.prototype.get_layers = function(){
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
      var offset = self.bar_width * 0.9 * i;
      return "translate(" + offset + ",0)";
    });
  return layers;
};

D3GroupedBarChart.prototype.get_bar_width = function(){
  var len_series = this._data.length; // m, i, rows
  var len_x = this._data[0].length;   // n, j, cols
  var bar_width = this.options.plot_box.w / len_x;  // bar_width is an outer width
  bar_width = bar_width / len_series;
  return bar_width;
};

// end file iffy
})();
