(function() {
  // Global settings
  var el = "#admissions .d3-viz";
  var w = $(el).removeClass('loading').width(),  // HAHAHAHAHAHA
      h = 300,
      xPadding = 50,
      yPadding = 30
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
  var xScale = d3.scale.linear().domain([minYear, maxYear]).range([xPadding, w]);
  var yScale = d3.scale.linear().domain([0, maxApplicants]).range([h - yPadding, yPadding]);
  var barWidth = w / (maxYear - minYear) - 30;

  // Axes,
  var yearFormat = d3.format("4d");
  var xAxis = d3.svg.axis().scale(xScale).orient("bottom").tickSize(6, 1, 1).tickFormat(yearFormat);
  var yAxis = d3.svg.axis().scale(yScale).orient("left").ticks(5);

  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(" + (barWidth / 2 + 20) + ", " + (h - yPadding) + ")")
    .call(xAxis);

  svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(" + xPadding + ", 0)")
    .call(yAxis);

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
    .attr("fill", "#99CCFF")
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
    .attr("fill", "#3399CC")
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
    .attr("fill", "#003366")
    .attr("width", barWidth)
    .attr("height", height)
    .attr("x", function(d, i) { return xN(d, i, 2); })
    .attr("y", y)
    ;

  // Tooltip
  $('#admissions rect').tooltip({
    title: function(){
      var d = this.__data__;
      return d.series + " (" + d.x + "):<br><strong>" + d3.format(",.0f")(d.y) + "</strong>";
    }
  });

  // Render legend
  var legend = $('#admissions .legend')[0],
      series = [
          { name: "Applied", color: "#99CCFF" },
          { name: "Admitted", color: "#3399CC" },
          { name: "Enrolled", color: "#003366" }
      ];

  var items = d3.select(legend).append("ul")
        .attr("class", "nav nav-pills nav-stacked")
        .selectAll("li")
        .data(series)
        .enter()
          .insert("li")
            .attr('class', 'inactive')
            .append('a');
    items
      .append("span").attr("class", "legend-key")
        .html("&#9608;").style("color", function(d) { return d.color; });
    items
      .append("span").attr("class", "legend-value")
        .text(function(d) { return d.name; });
})();
