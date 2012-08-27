  var $section = $('#gradrates');
  var $source = $section.find('table');
  var data = $source.tabulate();

  var chart = new D3GroupedBarChart($('<div class="chart" />').appendTo($section)[0],
        data,
        {
          'color': d3.scale.ordinal().range(['#99c', '#639', '#306'])
        });

  chart.get_y_domain = function(){
    return [0, 100];
  };
  chart.refresh();
