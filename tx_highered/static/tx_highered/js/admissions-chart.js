// Global settings
var el = "#admissions .d3-viz";
var w = $('#admissions .d3-viz').width(),
    h = 300,
    yPadding = 20
    ;

// Initialize SVG
var svg = d3.select(el)
  .append("svg:svg")
  .attr("width", "100%")
  .attr("height", "100%")
  .attr("viewBox", "0 0 " + w + " " + h)
  .attr("preserveAspectRatio", "xMinYMin meet")
  ;

// Datasets
var datasets = $("#admissions table.table").tabulate();
var applicants = datasets[0];
var admissions = datasets[1];
var enrollment = datasets[2];

// Scales
var minYear = d3.min(applicants, function(d) { return d.x; });
var maxYear = d3.max(applicants, function(d) { return d.x; });
var maxApplicants = d3.max(applicants, function(d) { return d.y; });
var minAdmissions = d3.min(admissions, function(d) { return d.y; });
var maxAdmissions = d3.max(admissions, function(d) { return d.y; });
var rScale = d3.scale.linear().domain([0, maxAdmissions]).range([h - yPadding, yPadding]);
var xScale = d3.scale.linear().domain([minYear, maxYear]).range([0, w]);
var yScale = d3.scale.linear().domain([0, maxApplicants]).range([h - yPadding, yPadding]);
var barWidth = w / (applicants.length + 1) - 10;

// Axes,
var yearFormat = d3.format("4d");
var xAxis = d3.svg.axis().scale(xScale).orient("bottom").tickSize(6, 1, 1).tickFormat(yearFormat);

svg.append("g")
  .attr("class", "axis")
  .attr("transform", "translate(" + (barWidth / 2 + 20) + ", " + (h - yPadding) + ")")
  .call(xAxis);

// Attrs
function xN(d, i, n) {
  return xScale(d.x) + (n * 10);
}

function y(d) {
  return yScale(d.y) - yPadding;
}

function height(d) {
  return h - yScale(d.y);
}

function rY(d) {
  return rScale(d.y) - yPadding;
}

function rHeight(d) {
  return h - rScale(d.y);
}

var applicantsG = svg.append("g");

// Render applicants
applicantsG
  .selectAll("rect")
  .data(applicants)
  .enter()
  .append("rect")
  .attr("fill", "lightgray")
  .attr("width", barWidth)
  .attr("height", height)
  .attr("x", function(d, i) { return xN(d, i, 0); })
  .attr("y", y)
  ;

// Render admissions
svg.append("g")
  .selectAll("rect")
  .data(admissions)
  .enter()
  .append("rect")
  .attr("fill", "darkgray")
  .attr("width", barWidth)
  .attr("height", height)
  .attr("x", function(d, i) { return xN(d, i, 1); })
  .attr("y", y)
  ;

// Render enrollment
svg.append("g")
  .selectAll("rect")
  .data(enrollment)
  .enter()
  .append("rect")
  .attr("fill", "gray")
  .attr("width", barWidth)
  .attr("height", height)
  .attr("x", function(d, i) { return xN(d, i, 2); })
  .attr("y", y)
  ;


$("#admissions a.zoom").toggle(function(e) {
  e.preventDefault();
  svg.selectAll("rect")
    .transition()
    .duration(1000)
    .attr("y", rY)
    .attr("height", rHeight);
  $(this).children("i").attr("class", "icon-minus");
}, function(e) {
  e.preventDefault();
  svg.selectAll("rect")
    .transition()
    .attr("y", y)
    .attr("height", height);
  $(this).children("i").attr("class", "icon-plus");
});
