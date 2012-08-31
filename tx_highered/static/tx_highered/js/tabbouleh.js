(function($) {
  var getCellValue = function(cell) {
        return (+ $(cell).data("value"));
      },

      getCellLabel = function(header, x, y) {
        return header + " " + x + " <strong>" + y + "</strong>";
      },

      tabulate = function(table) {
        var $table = $(table),
            // Use the first row as column headers
            headers = $table.find('thead th').map(function() {
              return $(this).text();
            }),
            // Initialize a list of data for each column except the first
            data = headers.slice(1).toArray().map(function() {
              return [];
            });

        $table.find('tbody > tr').each(function(_, row) {
          // Take the first cell as the x value
          var $rowChildren = $(row).children(),
              x = getCellValue($rowChildren.eq(0));

          // Append the remaining cells to their column data
          $rowChildren.slice(1).each(function(index, cell) {
            var y = getCellValue(cell);
            data[index].push({
              x: x,
              y: y,
              series: headers[index + 1],
              title: getCellLabel(headers[index + 1], x, y)
            });
          });
        });

        return data;
      };

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
})(jQuery);
