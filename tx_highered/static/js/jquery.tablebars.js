// jquery tablebars plugin
// version 0.3
// usage: $('table').tablebars()
// to turn on bars for a column, add the 'data-tablebars=1' class to the corresponding
// header. By default, the bars have no style. An example css declartion is:
//
//      .ui-tablebar { color: #333; background: #DACD99; }
//
// limitations: table must have a thead, data must be simple
jQuery.fn.tablebars = function(){
  this.each(function(i, table){
    var $table = $(table);

    // decide which columns get tablebars
    function pickColumns($table){
      var columns = [];
      $table.find('thead > tr:eq(0)').children().each(function(i, cell){
        if ($(cell).attr('data-tablebars')) columns.push(i);
      });
      return columns;
    }

    function processColumn(set){
      var data = [],
          rawdata = [],
          max = 0,
          width = set.eq(0).width();

      // wrap cells in set with a container div
      if (set.children('div.ui-tablebar-outer').length === 0) {
        set.wrapInner('<div class="ui-tablebar-outer" style="position: relative;"/>');
      }
      set = set.children();

      set.each(function(i, cell){
        var rawvalue = rawdata[i] = $(cell).html();
        var value = data[i] = Math.max(0, parseFloat(rawvalue.replace(/[^0-9.\-]+/g, '')));
        if (rawvalue[rawvalue.length - 1] == "%") {
          // TODO this percent logic is O(N) when it only needs to be O(1)
          max = 100;
          return;
        }
        if (!isNaN(value) && value > max){
          max = value;
        }
      });
      if (!max) max = 1;
      set.each(function(i, cell){
        var $cell = $(cell),
            $bar = $cell.find('span.ui-tablebar');
        if (!$bar.length) {
          $bar = $('<span class="ui-tablebar" style="overflow:hidden; position:absolute; width:0;"></span>');
          $cell.prepend($bar);
        }
        $bar.width(width * data[i] / max).html(rawdata[i]);
      });
    }

    function collectCells(columns){
      columns.forEach(function(index){
        var set = $table.find('tbody > tr > td:nth-child(' + (index + 1) + ')');
        processColumn(set);
      });
    }

    collectCells(pickColumns($table));
  });
  return this;
};
