/*globals $, d3, D3StackedBarChart, enrollment_chart_url, __extends */
var makeEnrollmentRaceChart = function() {
  "use strict";

  var COLORS = {
        "white_percent": "#F2841C",
        "total_percent_white": "#F2841C",
        "hispanic_percent": "#C3E683",
        "total_percent_hispanic": "#C3E683",
        "asian_percent": "#333333",
        "total_percent_asian": "#333333",
        "african_american_percent": "#FDFF81",
        "total_percent_black": "#FDFF81",
        "international_percent": "#F28386",
        "multiracial_percent": "#F7C184",
        "native_american_percent": "#91C1FF",
        "total_percent_native": "#91C1FF",
        "pacific_islander_percent": "#8FC2C1",
        "unknown_percent": "#CC0024",
        "total_percent_unknown": "#CC0024"
      };

  // similar to python's any
  function any(arr){
    return arr.reduce(function(a, b){ return a || b; });
  }

  var CustomChart = (function() {

    __extends(C, D3StackedBarChart);

    function C() {
      return C.__super__.constructor.apply(this, arguments);
    }

    C.prototype.getCleanData = function(new_data){
      // override to process data differently
      this.originalData = new_data;  // hold onto this
      var nested_dataset = d3.nest()
          .key(function(d) { return d.metric; })
          .entries(new_data);
      return C.__super__.getCleanData.call(this, nested_dataset);
    };

    C.prototype.getXScale = function(){
      // override to pull year range from original data
      var self = this,
          data = this.originalData;
      var yearRange = d3.extent(data, function(d) { return d.year; });
      return d3.scale.ordinal()
          .domain(d3.range(yearRange[0], yearRange[1] + 1))
          .rangeRoundBands([0, self._options.plotBox.width], 0.1, 0.1);
    };

    C.prototype.getMaxY = function(data){
      // pull max from original raw data
      return d3.max(this.originalData, function(d) { return d.enrollment; });
    };

    C.prototype.getX = function(){
      // override to use `d.year` instead of `d.x`
      var self = this;
      return function(d) { return self.xScale(d.year); };
    };

    C.prototype.getY = function(){
      // override to convert percent to value
      var self = this;
      return function(d) { return self.yScale((d.y0 + d.y) * d.enrollment / 100.0); };
    };

    C.prototype.getH = function(){
      // override to convert percent to value
      var self = this;
      return function(d) { return self.hScale(d.y * d.enrollment / 100.0); };
    };

    return C;
  })();

  var tooltipFmt = function(d){
        var guess = d3.format(",d")(Math.round(d.y * d.enrollment / 100));
        return guess + " (" + d.y + "%) " + d.race.substr(2);
      },
      _click = function(d, i, targetElem){
        // MAD HAXX AHEAD
        var self = this, filtered, targeted,
            evt = d3.event,
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
                return self._options.plotBox.height - self.h(d, i);
              })
              .attr("height", self.h);
        }
        if (self.yAxis){
          self.svg.select('.y.axis').transition().call(self.yAxis);
        }
      },
      options = {
        // 'color': d3.interpolateRgb("#001", "#eef"),  // does not actually reach maxima
        // 'color': d3.scale.pow().exponent(0.75).range(["#445", "#ccd"]),
        colors: COLORS,
        accessors: {
          bars: function(d) { return d.values; },
          colors: function(d, i) { return d.key; },
          y: function(d) { return d.value; }
        },
        tooltip: {
          enabled: true,
          format: function() { return tooltipFmt(this.__data__); }
        },
        xAxis: {
          enabled: true,
          title: "Year"
        },
        yAxis: {
          enabled: true,
          title: "Enrollment"
        },
        legend: {
          enabled: true,
          elem: $("#enrollment .legend"),
          reversed: true,
          click: _click,
          titleAccessor: function(d){ return d.values[0].race.substr(2); },
          postRender: function(el){
            $(el).find("li.inactive").removeClass('inactive');
          }
        },
        stackOrder: "big-bottom"
      };

  window.z = new CustomChart($("#enrollment .chart"), enrollment_chart_url, options);
};
