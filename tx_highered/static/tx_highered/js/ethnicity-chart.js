function render_enrollment_chart(dataset) {
  var margin = {top: 20, right: 20, bottom: 30, left: 50},
      width = 760 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

  // Scales
  var yearFormat = d3.format("4d");
  var yearRange = d3.extent(dataset, function(d) { return d.year; });
  var enrollmentMax = d3.max(dataset, function(d) { return d.enrollment; });
  var x = d3.scale.linear()
      .domain(yearRange)
      .range([0, width]);
  var y = d3.scale.linear()
      .domain([0, enrollmentMax])
      .range([height, 0]);
  var colors = {
    'unknown': '#E30033',
    'black': '#FF6633',
    'hispanic': '#D6E985',
    'native': '#006666',
    'asian': '#3399CC',
    'white': '#993399'
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
  var stack = d3.layout.stack()
      .offset("zero")
      .values(function(d) { return d.values; })
      .x(function(d) { return d.year; })
      .y(function(d) { return d.value; });

  // Render
  var svg = d3.select("#enrollment").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var nest = d3.nest()
      .key(function(d) { return d.race; });

  var layers = stack(nest.entries(dataset));

  var area = d3.svg.area()
      .x(function(d) { return x(d.year); })
      .y0(function(d) {
        return y(d.y0 * d.enrollment / 100.0);
      })
      .y1(function(d) {
        return y((d.y0 + d.y) * d.enrollment / 100.0);
      });

  svg.selectAll(".layer")
      .data(layers)
    .enter().append("path")
      .attr("class", "layer")
      .attr("d", function(d) { return area(d.values); })
      .style("fill", function(d) {
        return colors[d.key];
      })
      .style("fill-opacity", "0.8");

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);
}

function init_enrollment_chart(options) {
  d3.json(options.url, function(dataset) {
    render_enrollment_chart(dataset);
  });
}
