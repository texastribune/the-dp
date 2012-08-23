
/* globals: d3, $ */

var TestScoresChart = function(){
  var url;
  var _data;
  var data;
  var defaultOptions = {
    color: d3.scale.category10(),
    style: 'stacked',
    tooltip: function(){ return this.__data__.title || this.__data__.y; }
  };
  var enable_axis_x = true;
  var enable_axis_y = true;
  var margin = [10, 50, 30, 50];
  var options;

  // PUBLIC
  function init(new_url, new_options){
    url = new_url;
    get_data_from_url(url);
    options = $.extend({}, defaultOptions, new_options);
  }

  function get_data_from_url(url){
    d3.json(url, function(new_data) {
      data = new_data;
      _data = data;  // save reference to original raw data;
      process_data(data);
      insert_chart();
    });
  }

  function process_data(new_data){
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
        y_min: datum.sat.verbal[0],
        y_max: datum.sat.verbal[1]
      });
      processed_data.math.push({
        x: datum.year,
        y_min: datum.sat.math[0],
        y_max: datum.sat.math[1]
      });
      processed_data.writing.push({
        x: datum.year,
        y_min: datum.sat.writing[0],
        y_max: datum.sat.writing[1]
      });
    }
    data = [processed_data.verbal, processed_data.math, processed_data.writing];
    return data;
  }

  function insert_chart(){
    // TODO remove jquery and DOM manipulation
    var $elem = $('<div class="chart">');
    $('#testing').append($elem);

    // configure svg box
    var width = 940;
    var height = 300;
    // setup svg DOM
    var svg = d3.select($elem[0])
                .append("svg")
                .attr("width", "100%")
                .attr("height", "100%")
                .attr("viewBox", [0, 0, width, height].join(" "))
                .attr("preserveAspectRatio", "xMinYMin meet");

    // configure plot box
    var plot_box = {
          w: width - margin[1] - margin[3],
          h: height - margin[0] - margin[2]
        },
        bar_width;
    // setup plot DOM
    var plot = svg
              .append("g")
              .attr("class", "plot")
              .attr("width", plot_box.w)
              .attr("height", plot_box.h)
              .attr("transform", "translate(" + margin[3] + "," + margin[0] + ")");


    // d3 configuration
    var len_series = data.length; // m, i, rows
    var len_x = data[0].length,   // n, j, cols
        min_x = data[0][0].x,
        max_x = data[0][len_x - 1].x,
        // TODO refactor to generate with or without d.y0 constant dyanamically
        find_ceiling = function(data){
          return d3.max(data, function(d) {
            return d3.max(d, function(d) {
              return d.y;
            });
          });
        },
        find_ceiling_stacked = function(data){
          return d3.max(data, function(d) {
            return d3.max(d, function(d) {
              return d.y + d.y0;
            });
          });
        },
        x_scale = d3.scale.ordinal()
                    .domain(irange(min_x, max_x))
                    .rangeRoundBands([0, plot_box.w], 0.1, 0.1),
        x_axis,
        x = function(d) { return x_scale(d.x); },
        height_scale_stack = d3.scale.linear().range([0, plot_box.h]),
        y_scale = d3.scale.linear().range([plot_box.h, 0]),
        y_axis,
        y;

    // sets global height and scales
    function rescale(data_ceiling){
      height_scale_stack.domain([0, data_ceiling]);
      y_scale.domain([0, data_ceiling]);
      if (y_axis){
        svg.select('.y.axis').transition().call(y_axis);
      }
    }

    bar_width = plot_box.w / len_x / len_series;  // bar_width is an outer width

    y = function(d) { return y_scale(d.y_min); };
    // rescale(find_ceiling(data));
    rescale(800);

    // set up a layer for each series
    var layers = plot.selectAll("g.layer")
      .data(data)
      .enter().append("g")
        .attr("class", "layer")
        .style("fill", function(d, i) { return options.color(i); })
        .attr("transform", function(d, i) {
          var offset = bar_width * 0.9 * i;
          return "translate(" + offset + ",0)";
        });

    // setup a bar for each point in a series
    var bars = layers.selectAll("rect.bar")
      .data(function(d) { return d; })
      .enter().append("rect")
        .attr("class", "bar")
        .attr("width", bar_width * 0.9)
        .attr("x", x)
        .attr("y", plot_box.h)
        .attr("height", 0)
        .transition()
          .delay(function(d, i) { return i * 10; })
          .attr("y", y)
          .attr("height", function(d) { return height_scale_stack(d.y_max - d.y_min); });

    // tooltip
    // $('rect.bar', svg[0]).tooltip({
    //   // manually call because options.tooltip can change
    //   title: function(){ return options.tooltip.call(this); }
    // });

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
  }

  // PUBLIC
  function get_or_set_data(new_data){
    if (typeof new_data === "undefined"){
      return data;
    }
    data = new_data;
  }

  return {
    // properties

    // methods
    init: init,
    data: get_or_set_data
  };
}();
