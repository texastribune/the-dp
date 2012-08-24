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


function D3BarChart(el, data, options){
  this.elem = el;
  this._data = data;
  this._init(options);


  // setup svg DOM
  var svg = d3.select(el)
              .append("svg")
              .attr("width", "100%")
              .attr("height", "100%")
              .attr("viewBox", [0, 0, this.options.width, this.options.height].join(" "))
              .attr("preserveAspectRatio", "xMinYMin meet");
  this.svg = svg;

  // setup plot DOM
  var plot = svg
            .append("g")
            .attr("class", "plot")
            .attr("width", this.options.plot_box.w)
            .attr("height", this.options.plot_box.h)
            .attr("transform", "translate(" + this.options.margin[3] + "," + this.options.margin[0] + ")");
  this.plot = plot;

  // d3 configuration
      // find_ceiling_stacked = function(data){
      //   return d3.max(data, function(d) {
      //     return d3.max(d, function(d) {
      //       return d.y + d.y0;
      //     });
      //   });
      // };
  var self = this;


  var len_series = this._data.length; // m, i, rows
  var len_x = this._data[0].length;   // n, j, cols
  bar_width = this.options.plot_box.w / len_x;  // bar_width is an outer width
  // if (options.style == "grouped") {
    // subdivide bar_width further
    bar_width = bar_width / len_series;
  // }
  this.bar_width = bar_width;

  // if (this.options.style == "stacked"){
  //   find_ceiling = find_ceiling_stacked;
  //   y = function(d) { return y_scale(d.y + d.y0); };
  // } else {
  self.y = function(d) { return self.y_scale(d.y); };
  // }
  this.rescale(this.find_ceiling(data));

  // set up a layer for each series
  var layers = plot.selectAll("g.layer")
    .data(data)
    .enter().append("g")
      .attr("class", "layer")
      .style("fill", function(d, i) { return self.options.color(i); });
  // shift grouped bars so they're adjacent to each other
  // if (options.style == "grouped") {
    layers
      .attr("transform", function(d, i) {
        var offset = bar_width * 0.9 * i;
        return "translate(" + offset + ",0)";
      });
  // }
  this._layers = layers;
  this.bars();

  /*
  // tooltip
  $('rect.bar', svg[0]).tooltip({
    // manually call because options.tooltip can change
    title: function(){ return options.tooltip.call(this); }
  });

  // draw axes
  if (enable_axis_x) {
    x_axis = d3.svg.axis()
    .orient("bottom")
             .scale(x_scale)
             .tickSize(6, 1, 1)
             .tickFormat(function(a){ return a; });
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(" + margin[3] + "," + (height - margin[2]) + ")")
        .call(x_axis);
  }
  if (enable_axis_y) {
    y_axis = d3.svg.axis()
             .scale(y_scale)
             .orient("left");
    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + margin[3] + "," + margin[0] + ")")
        .call(y_axis);
  }
  */

}

  // sets global height and scales
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

  // setup x and y extents
  var data = self._data;
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

D3BarChart.prototype.find_ceiling = function(data){
  return d3.max(data, function(d) {
    return d3.max(d, function(d) {
      return d.y;
    });
  });
};

D3BarChart.prototype.rescale = function(data_ceiling){
  var self = this;
  self.height_scale.domain([0, data_ceiling]);
  self.y_scale.domain([0, data_ceiling]);
  if (self.y_axis){
    self.svg.select('.y.axis').transition().call(self.y_axis);
  }
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


// get or set data
D3BarChart.prototype.data = function(new_data){
  var self = this;
  if (typeof new_data === "undefined"){
    return this._data;
  }

  // process add stack offsets
  var data = d3.layout.stack()(new_data);

  // reset height ceiling
  this.rescale(this.find_ceiling(data));

  // update layers data
  this._layers.data(data);
  // update bars data :(
  this._layers.selectAll("rect.bar")
    .data(function(d) { return d; })
    .transition()
      .attr("y", y)
      .attr("height", function(d) { return self.height_scale(d.y); });

  this._data = data;
  return layers;
};

// get or set option
D3BarChart.prototype.option = function(name, newvalue){
  if (typeof newvalue === "undefined"){
    return this.options[name];
  }
  this.options[name] = newvalue;
};
