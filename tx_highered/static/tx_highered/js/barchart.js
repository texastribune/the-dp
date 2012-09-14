/*global $, d3, tt */
(function($, d3, tt, exports){
  "use strict";
// begin file-iffy, unindent


// data processor TODO move awaaaaay
exports.normalizeFirst = function(data, idx){
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
};

/***************** CHART ******************/
var D3Chart = exports.D3Chart = tt.Class.extend({
  // override this if data needs to be scrubbed before getting charted
  initData: function(data){ return data; },

  // get or set data
  data: function(new_data){
    var data;
    if (typeof new_data === "undefined"){
      return this._data;
    }

    this._data = this.initData(new_data);
    this.refresh();
    return this;
  },

  // get or set data
  refresh: function(){
    return this;
  },

  // get or set option
  option: function(name, newvalue){
    if (typeof newvalue === "undefined"){
      return this.options[name];
    }
    this.options[name] = newvalue;
    return this;
  }

});


/***************** BAR CHART ******************/
var D3BarChart = exports.D3BarChart = D3Chart.extend({
  init: function(el, data, options){
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
        self._data = self.initData(new_data);
        self.setUp(options);
        self.render();
      });
    } else {
      this._data = this.initData(data);
      this.setUp(options);
      this.render();
    }
  },

  setUp: function(options){
    // merge user options and default options
    var self = this,
        data = this._data;
    var defaultOptions = {
          color: d3.scale.category10(),
          height: 300,
          width: 940,
          margin: [10, 0, 30, 50],
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

    self.layerFillStyle = self.getLayerFillStyle();

    // setup x scales
    this.x_scale = self.getXScale();
    self.x_axis = null;
    self.x = self.getX();

    // setup y scales
    self.height_scale = d3.scale.linear().range([0, plot_box.h]);
    self.y_scale = d3.scale.linear().range([plot_box.h, 0]);
    self.y_axis = null;
    self.y = self.getY();
    self.h = self.getH();

    // setup bar width
    self.bar_width = this.getBarWidth();
  },

  render: function(){
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

    this.rescale(self.getYDomain());

    this._layers = this.getLayers();
    this.getBars();

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
      if (self.options.yAxisTickFormat) {
        y_axis.tickFormat(self.options.yAxisTickFormat);
      }
      svg.append("g")
          .attr("class", "y axis")
          .attr("transform", "translate(" + self.options.margin[3] + "," + self.options.margin[0] + ")")
          .call(y_axis);
      self.yAxis = y_axis;
    }
    if (self.options.legendElem) {
      // only one chart has a legend, as we add more, this will naturally
      // get refactored into something that makes sense
      self.renderLegend(self.options.legendElem);
    }
  },

  getXScale: function(){
    // TODO this makes a lot of assumptions about how the input data is
    // structured and ordered, replace with d3.extent
    var self = this,
        data = this._data;
    var len_x = data[0].length,
        min_x = data[0][0].x,
        max_x = data[0][len_x - 1].x;
    return d3.scale.ordinal()
        .domain(d3.range(min_x, max_x + 1))
        .rangeRoundBands([0, self.options.plot_box.w], 0.1, 0.1);
  },

  getYDomain: function(){
     return [0, this.getMaxY(this._data)];
  },

  refresh: function(){
    var self = this,
        data = self._data;

    // reset height ceiling
    self.rescale(self.getYDomain());

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
  },

  getMaxY: function(data){
    return d3.max(data, function(d) {
      return d3.max(d, function(d) {
        return d.y;
      });
    });
  },

  getLayerFillStyle: function(){
    var self = this;
    return function(d, i) { return self.options.color(i); };
  },

  getX: function(){
    var self = this;
    return function(d) { return self.x_scale(d.x); };
  },

  getY: function(){
    var self = this;
    return function(d) { return self.y_scale(d.y); };
  },

  getH: function(){
    var self = this;
    return function(d) { return self.height_scale(d.y); };
  },

  rescale: function(extent){
    // TODO get rid of this method
    this.height_scale.domain([0, extent[1] - extent[0]]);
    this.y_scale.domain(extent);
    return this;
  },

  getLayers: function(){
    // set up a layer for each series
    var self = this;
    var layers = self.plot.selectAll("g.layer")
      .data(this._data)
      .enter().append("g")
        .attr("class", "layer")
        .style("fill", self.layerFillStyle);
    return layers;
  },

  // setup a bar for each point in a series
  getBars: function(){
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
  },

  getBarWidth: function(){
    var len_series = this._data.length; // m, i, rows
    var len_x = this._data[0].length;   // n, j, cols
    var bar_width = this.options.plot_box.w / len_x;  // bar_width is an outer width
    return bar_width;
  },

  getLegendSeriesTitle: function(d, i){
    return "lol";
  },

  renderLegend: function(el){
    var self = this;
    if (el.jquery) {  // todo what about things like zepto?
      this.$legend = el;
      this.legend = el[0];
    } else if (typeof el == "string"){
      this.legend = document.getElementById(el);
    } else {
      this.legend = el;
    }
    var items = d3.select(this.legend).append("ul")
      .attr("class", "nav nav-pills nav-stacked")
      .selectAll("li")
        .data(this._data)
        // bars are built bottom-up, so build the legend the same way
        .enter().insert("li", ":first-child")
          .append('a').attr("href", "#");
    items
      .append("span").attr("class", "legend-key")
      // TODO use an element that can be controlled with CSS better but is also printable
      .html("&#9608;").style("color", this.layerFillStyle);
    items
      .append("span").attr("class", "legend-value")
      .text(self.getLegendSeriesTitle);
    // events
    items.on("click", function(d, i){
      d3.event.preventDefault();
      if (self.legendActivateSeries){
        self.legendActivateSeries(i, this);
      }
    });
  }
});


/***************** STACKED BAR CHART ******************/
var D3StackedBarChart = exports.D3StackedBarChart = D3BarChart.extend({

  initData: function(new_data){
    // process add stack offsets
    return d3.layout.stack()(new_data);
  },

  getMaxY: function(data){
    return d3.max(data, function(d) {
      return d3.max(d, function(d) {
        return d.y + d.y0;
      });
    });
  },

  getY: function(){
    var self = this;
    return function(d) { return self.y_scale(d.y + d.y0); };
  }
});


/***************** GROUPED BAR CHART ******************/
var D3GroupedBarChart = exports.D3GroupedBarChart = D3BarChart.extend({

  getLayers: function(){
    // set up a layer for each series
    var self = this;
    var layers = self.plot.selectAll("g.layer")
      .data(this._data)
      .enter().append("g")
        .attr("class", "layer")
        .style("fill", self.layerFillStyle);
    // shift grouped bars so they're adjacent to each other
    layers
      .attr("transform", function(d, i) {
        return "translate(" + self.getLayerOffset(i) + ",0)";
      });
    return layers;
  },

  getLayerOffset: function(i) {
    return this.bar_width * 0.9 * i;
  },

  getBarWidth: function(){
    var len_series = this._data.length; // m, i, rows
    var len_x = this._data[0].length;   // n, j, cols
    var bar_width = this.options.plot_box.w / len_x;  // bar_width is an outer width
    bar_width = bar_width / len_series;
    return bar_width;
  }
});

// end file iffy
})(jQuery, d3, tt, window);
