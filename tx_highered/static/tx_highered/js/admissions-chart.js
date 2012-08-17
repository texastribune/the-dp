// Global settings
var el = "#admissions .d3-viz";
var w = 760,
    h = 300
    ;

// Initialize SVG
var svg = d3.select(el)
  .append("svg:svg")
  .attr("width", "100%")
  .attr("height", "300")
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
var rScale = d3.scale.linear().domain([0, maxApplicants]).range([h, 0]);
var xScale = d3.scale.linear().domain([minYear, maxYear]).range([0, w]);
var yScale = d3.scale.linear().domain([0, maxApplicants]).range([h, 0]);

// Render applicants
svg.append("g")
  .selectAll("rect")
  .data(applicants)
  .enter()
  .append("rect")
  .attr("fill", "lightgray")
  .attr("width", 80)
  .attr("height", function(d) {
    return h - yScale(d.y);
  })
  .attr("x", function(d) {
    return xScale(d.x);
  })
  .attr("y", function(d) {
    return yScale(d.y);
  })
  ;

// Render admissions
svg.append("g")
  .selectAll("rect")
  .data(admissions)
  .enter()
  .append("rect")
  .attr("fill", "darkgray")
  .attr("width", 70)
  .attr("height", function(d) {
    return h - yScale(d.y);
  })
  .attr("x", function(d) {
    return xScale(d.x);
  })
  .attr("y", function(d) {
    return yScale(d.y);
  })
  ;

// Render enrollment
svg.append("g")
  .selectAll("rect")
  .data(enrollment)
  .enter()
  .append("rect")
  .attr("fill", "gray")
  .attr("width", 40)
  .attr("height", function(d) {
    return h - yScale(d.y);
  })
  .attr("x", function(d) {
    return xScale(d.x);
  })
  .attr("y", function(d) {
    return yScale(d.y);
  })
  ;
