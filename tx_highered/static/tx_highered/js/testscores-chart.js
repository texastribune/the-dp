
/* globals: d3 */

var TestScoresChart = function(){
  var url;
  var data;

  // PUBLIC
  function init(new_url){
    url = new_url;
    get_data_from_url(url);
  }

  function get_data_from_url(url){
    d3.json(url, function(new_data) {
      data = new_data;
    });
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
