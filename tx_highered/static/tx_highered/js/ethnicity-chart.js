function render_enrollment_chart(dataset) {
  var margin = {top: 20, right: 0, bottom: 30, left: 60},
      width = 760 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

  // Scales
  var yearFormat = d3.format("4d");
  var yearRange = d3.extent(dataset, function(d) { return d.year; });
  var barWidth = width / (yearRange[1] - yearRange[0] + 1) - 10;
  var enrollmentMax = d3.max(dataset, function(d) { return d.enrollment; });
  var x = d3.scale.linear()
    .domain(yearRange)
    .range([0, width - barWidth]);
  var y = d3.scale.linear()
    .domain([0, enrollmentMax])
    .range([height, 0]);
  var height_scale = d3.scale.linear()
    .domain([0, enrollmentMax])
    .range([0, height]);
  var colors = {
    'total_percent_unknown': '#E30033',
    'total_percent_black': '#FF6633',
    'total_percent_hispanic': '#D6E985',
    'total_percent_native': '#006666',
    'total_percent_asian': '#3399CC',
    'total_percent_white': '#993399'
  };

  // Axes
  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")
      .tickFormat(yearFormat);

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left");

  // Stacking
  var nested_dataset = d3.nest()
      .key(function(d) { return d.metric; })
      .entries(dataset);

  var stack = d3.layout.stack()
      .offset("zero")
      .values(function(d) { return d.values; })
      .x(function(d) { return d.year; })
      .y(function(d) { return d.value; });

  var stacked_dataset = stack(nested_dataset);

  // Render
  var svg = d3.select("#enrollment .chart").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");

  var layers = svg.selectAll("g.layer")
    .data(nested_dataset)
    .enter()
      .append("g")
      .attr("class", "layer")
      .style("fill", function(d) {
        return colors[d.key];
      });

  var bars = layers.selectAll("rect")
    .data(function(d, i) { return d.values; })
    .enter()
      .append("rect")
      .attr("width", barWidth)
      .attr("x", function(d) {
        return x(d.year);
      })
      .attr("y", function(d) {
        return height - height_scale(d.y0 * d.enrollment / 100.0) - height_scale(d.y * d.enrollment / 100.0);
      })
      .attr("height", function(d) {
        return height_scale(d.y * d.enrollment / 100.0);
      });

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(" + barWidth / 2 + ", " + height + ")")
      .call(xAxis)
      .selectAll("text")
        .style("text-anchor", "middle");

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

  $('#enrollment rect').tooltip({
    title: function(){
      return this.__data__.y + " " + this.__data__.race;
    }
  });
}

function init_enrollment_chart(options) {
  d3.json(options.url, function(dataset) {
    render_enrollment_chart(dataset);
  });
}
