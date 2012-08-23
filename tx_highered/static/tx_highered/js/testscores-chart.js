
/* globals: d3 */

var TestScoresChart = function(){
  var url;
  var _data;
  var data;

  // PUBLIC
  function init(new_url){
    url = new_url;
    get_data_from_url(url);
  }

  function get_data_from_url(url){
    d3.json(url, function(new_data) {
      data = new_data;
      _data = data;  // save reference to original raw data;
      process_data(data);
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
    data = processed_data;
    return data;
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
