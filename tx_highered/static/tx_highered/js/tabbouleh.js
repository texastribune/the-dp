;(function($, window) {
  function getCellValue(cell) {
    return (+ $(cell).data("value"));
  }

  function getCellLabel(header, x, y) {
    return header + " " + x + " <strong>" + y + "</strong>";
  }

  function tabulate(table) {
    var $table = $(table);

    // Use the first row as column headers
    var headers = $table.find('thead th').map(function() {
      return $(this).text();
    });

    // Initialize a list of data for each column except the first
    var data = headers.slice(1).toArray().map(function() {
      return [];
    });

    $table.find('tbody > tr').each(function(_, row) {
      // Take the first cell as the x value
      var x = getCellValue($(row).children().eq(0));

      // Append the remaining cells to their column data
      $(row).children().slice(1).each(function(index, cell) {
        var y = getCellValue(cell);
        data[index].push({
          x: x,
          y: y,
          label: getCellLabel(headers[index], x, y)
        });
      });
    });

    return data;
  }

  /**
   * The jQuery.tabulate plugin.
   *
   * @param {object} options
   *    An object containing default option overrides.
   *
   * @return {object}
   *    A list of datasets retrieved from the tables.
   */
  $.fn.tabulate = function(options) {
    return this.map(function(i, table) {
      return tabulate(table);
    });
  };
})(jQuery, window);
