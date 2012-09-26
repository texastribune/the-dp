/*globals $, d3, D3StackedBarChart, enrollment_chart_url */
(function() {
  "use strict";

  // private functions from
  // https://raw.github.com/mbostock/d3/master/src/layout/stack.js
  // for re-ordering data
  function d3_layout_stackReduceSum(d) {
    return d.reduce(d3_layout_stackSum, 0);
  }

  function d3_layout_stackSum(p, d) {
    return p + d[1];
  }

  // similar to python's any
  function any(arr){
    return arr.reduce(function(a, b){ return a || b; });
  }

  var Chart = D3StackedBarChart.extend({
    initData: function(new_data){
      // override to process data differently
      this.originalData = new_data;  // hold onto this
      var nested_dataset = d3.nest()
          .key(function(d) { return d.metric; })
          .entries(new_data);
      var stackOrder,
          stack = d3.layout.stack()
          .offset("zero")  // default
          .order(function(data) {
            var n = data.length,
                sums = data.map(d3_layout_stackReduceSum);
            stackOrder = d3.range(n).sort(function(a, b) { return sums[b] - sums[a]; });
            return stackOrder;
          })
          .values(function(d) { return d.values; })
          .x(function(d) { return d.year; })  // this doesn't seem to work
          .y(function(d) { return d.value; });
      var stacked_dataset = stack(nested_dataset);
      // actually sort the data too so colors are applied in sort order
      var return_data = [];
      for (var i = 0; i < stackOrder.length; i++){
        return_data.push(stacked_dataset[stackOrder[i]]);
      }
      // slower but terser alternative
      // return stackOrder.map(function(x){ return stacked_dataset[x]; });
      return return_data;
    },
    getXScale: function(){
      // override to pull year range from original data
      var self = this,
          data = this.originalData;
      var yearRange = d3.extent(data, function(d) { return d.year; });
      return d3.scale.ordinal()
          .domain(d3.range(yearRange[0], yearRange[1] + 1))
          .rangeRoundBands([0, self.options.plot_box.w], 0.1, 0.1);
    },
    getMaxY: function(data){
      // pull max from original raw data
      return d3.max(this.originalData, function(d) { return d.enrollment; });
    },
    getLayerFillStyle: function(){
      var self = this,
          n = self._data.length ;
      return function(d, i) { return self.options.color(i / n); };
    },
    getX: function(){
      // override to use `d.year` instead of `d.x`
      var self = this;
      return function(d) { return self.x_scale(d.year); };
    },
    getY: function(){
      // override to convert percent to value
      var self = this;
      return function(d) { return self.y_scale((d.y0 + d.y) * d.enrollment / 100.0); };
    },
    getH: function(){
      // override to convert percent to value
      var self = this;
      return function(d) { return self.height_scale(d.y * d.enrollment / 100.0); };
    },
    getBarWidth: function(){
      // override to get `len_x` a different way TODO can probably port this back into super
      // bar_width is an outer width
      return this.options.plot_box.w / this.x_scale.domain().length;
    },
    getBars: function(){
      // override to fix different data structure, array of objects instead of array of arrays
      var self = this;
      return this._layers.selectAll("rect.bar")
        .data(function(d) { return d.values; })
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

    postRenderLegend: function(el){
      $(el).find("li.inactive").removeClass('inactive');
    },

    legendActivateSeries: function(idx, targetElem){
      var self = this, filtered, targeted,
          $target = $(targetElem).parent(),
          $set = $target.parent().children(':not(.reset)'),
          reset = function(){
            self.rescale(self.getYDomain());  // TODO cache original outside this method
            self._layers.selectAll("rect.bar")
              .transition()
                .attr("y", self.y)
                .attr("height", self.h);
            var $resetCtl = $set.next('.reset');
            $resetCtl.hide(500, function(){ $resetCtl.remove(); });
          },
          addResetCtl = function(){
            if ($target.parent().children('.reset').length) { return; }
            var $resetCtl = $('<li class="reset"><a href="#">&times; Reset</a></li>');
            $resetCtl.click(function(){
              $set.filter('.active').removeClass('active');
              self._layers.attr("display", null);  // XXX
              reset();
              // $resetCtl.hide(500, function(){ $resetCtl.remove(); });  // do not delete
            });
            $resetCtl.find('a').click(function(e){ e.preventDefault(); });
            $target.parent().append($resetCtl);
          };

      // Interaction and UI
      // TODO allow multiple elements to be active
      var MODE; // DELETEME
      if ($target.hasClass('active')){
        $set.filter('.active').removeClass('active');
        MODE = "blur";
      } else {
        $set.filter('.active').removeClass('active');
        $target.addClass('active');
        addResetCtl();
        MODE = "focus";
      }

      // determine which layers to show
      // activeMask is the mask of what series are active: [true, false, false, ...]
      var activeMask = $set.map(function(i, x){ return $(x).hasClass('active'); }).toArray().reverse();
      if (!any(activeMask)){
        activeMask = activeMask.map(function(){ return true; });
      }

      // sort layers into two groups and toggle visiblity
      targeted = this._layers.filter(function(d, i){ return activeMask[i]; });
      targeted.attr("display", null);
      filtered = this._layers.filter(function(d, i){ return !activeMask[i]; });
      filtered.attr("display", "none");

      // redraw
      // TODO show multiple layers, this involves re-calculating everything
      // which is expensive
      if (MODE == "blur"){
        reset();
      } else {
        var max = d3.max(targeted.data()[0].values.map(function(a){ return a.value * a.enrollment / 100; }));
        self.rescale([0, max]);
        targeted.selectAll("rect.bar")
          .transition()
            .attr("y", function(d, i){
              // send thee to the bottom of the sea!
              return self.options.plot_box.h - self.h(d, i);
            })
            .attr("height", self.h);
      }
      if (self.yAxis){
        self.svg.select('.y.axis').transition().call(self.yAxis);
      }
    },

    getLegendSeriesTitle: function(d, i){
      return d.values[0].race.substr(2);
    }
  });

  var options = {
    'color': d3.interpolateRgb("#001", "#eef"),  // does not actually reach maxima
    // 'color': d3.scale.pow().exponent(0.75).range(["#445", "#ccd"]),
    'tooltip': function() { return this.__data__.y + " " + this.__data__.race; },
    'legendElem': $("#enrollment .legend")
  };

  new Chart($("#enrollment .chart"), enrollment_chart_url, options);
})();
