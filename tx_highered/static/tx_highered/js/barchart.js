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


// inclusive range
function irange(min, max){
  var a = [];
  for (var i = min; i <= max; i++){
    a.push(i);
  }
  return a;
}


var D3Chart = Class.extend({});

// override this if data needs to be scrubbed before getting charted
D3Chart.prototype.init_data = function(data){ return data; };

// get or set data
D3Chart.prototype.data = function(new_data){
  var self = this, data;
  if (typeof new_data === "undefined"){
    return this._data;
  }

  data = this.init_data(new_data);

  // reset height ceiling
  this.rescale(this.find_ceiling(data));

  // update layers data
  this._layers.data(data);
  // update bars data :(
  this._layers.selectAll("rect.bar")
    .data(function(d) { return d; })
    .transition()
      .attr("y", self.y)
      .attr("height", function(d) { return self.height_scale(d.y); });
};

// get or set option
D3Chart.prototype.option = function(name, newvalue){
  if (typeof newvalue === "undefined"){
    return this.options[name];
  }
  this.options[name] = newvalue;
};


var D3BarChart = D3Chart.extend({});

D3BarChart.prototype.init = function(el, data, options){
  this.elem = el;
  this._data = data;
  this._init(options);
  this._main();
};

D3BarChart.prototype._init = function(options){
  // merge user options and default options
  var self = this;
  var defaultOptions = {
      color: d3.scale.category10(),
      style: 'stacked',
      height: 300,
      width: 940,
      tooltip: function(){ return this.__data__.title || this.__data__.y; },
      enable_axis_x: true,
      enable_axis_y: true,
      margin: [10, 50, 30, 50]
  };
  self.options = $.extend({}, defaultOptions, options);

  // plot box
  var plot_box = {
        w: self.options.width - self.options.margin[1] - self.options.margin[3],
        h: self.options.height - self.options.margin[0] - self.options.margin[2]
      };
  self.options.plot_box = plot_box;


  var data = this.init_data(this._data);

  // setup x and y extents
  console.log(data);
  var len_x = data[0].length,   // n, j, cols
      min_x = data[0][0].x,
      max_x = data[0][len_x - 1].x;

  // plot x and y
  this.x_scale = d3.scale.ordinal()
              .domain(irange(min_x, max_x))
              .rangeRoundBands([0, plot_box.w], 0.1, 0.1);
  this.x_axis = null;
  this.x = function(d) { return self.x_scale(d.x); };
  this.height_scale = d3.scale.linear().range([0, plot_box.h]);
  this.y_scale = d3.scale.linear().range([plot_box.h, 0]);
  this.y_axis = null;
  this.y = null;
};

D3BarChart.prototype._main = function(){
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

  this.bar_width = this.get_bar_width();

  self.y = self.get_y();
  this.rescale(this.find_ceiling(this._data));

  this._layers = this.get_layers();
  this.bars();

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

D3BarChart.prototype.find_ceiling = function(data){
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

D3BarChart.prototype.rescale = function(data_ceiling){
  var self = this;
  self.height_scale.domain([0, data_ceiling]);
  self.y_scale.domain([0, data_ceiling]);
  if (self.yAxis){
    self.svg.select('.y.axis').transition().call(self.yAxis);
  }
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
D3BarChart.prototype.bars = function(){
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
        .attr("height", function(d) { return self.height_scale(d.y); });
};

D3BarChart.prototype.get_bar_width = function(){
  var len_series = this._data.length; // m, i, rows
  var len_x = this._data[0].length;   // n, j, cols
  bar_width = this.options.plot_box.w / len_x;  // bar_width is an outer width
  return bar_width;
};


var D3StackedBarChart = D3BarChart.extend();

D3StackedBarChart.prototype.init_data = function(new_data){
  // process add stack offsets
  this._data = d3.layout.stack()(new_data);
  return this._data;
};

D3StackedBarChart.prototype.find_ceiling = function(data){
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


var D3GroupedBarChart = D3BarChart.extend();

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
      var offset = bar_width * 0.9 * i;
      return "translate(" + offset + ",0)";
    });
  return layers;
};

D3GroupedBarChart.prototype.get_bar_width = function(){
  var len_series = this._data.length; // m, i, rows
  var len_x = this._data[0].length;   // n, j, cols
  bar_width = this.options.plot_box.w / len_x;  // bar_width is an outer width
  bar_width = bar_width / len_series;
  return bar_width;
};

