// TODO cache using localStorage?
(function($, Trie, exports){
"use strict";


// configuration
var $elem = $(".q");
var $ctl = $elem.nextAll();


var autocomplete_tries = [new Trie(), new Trie(), new Trie()];
var _data = [[], [], []];
var activeIdx = 0;

// prebuild data source
var build_sources = function(data){
  var newdata = _data, inst, namelower;
  for (var i = 0; i < data.length; i++){
    inst = data[i];
    newdata[0].push(inst.name);
    newdata[1 + inst.is_private].push(inst.name);
    // Insert institutions to trie
    namelower = inst.name.toLowerCase();
    autocomplete_tries[0].insert(namelower, data[i]);
    autocomplete_tries[1 + inst.is_private].insert(namelower, data[i]);
  }
  return newdata;
};

// jQuery UI autocomplete
var autocomplete_institutions = function(data) {
  _data = build_sources(data);

  // Map intitution names to URIs
  var urisByName = {};
  $.map(data, function(o) {
    urisByName[o.name] = o.uri;
  });

  // Initialize autocomplete
  $elem.autocomplete({
    source: ["foo", "bar", "baz"],  // source does nothing, but pass in an array to trick it
    select: function(e, o) {
      var uri = urisByName[o.item.label];
      if (typeof(uri) !== "undefined") {
        location.href = uri;
      }
    }
  });

  $elem.on("keydown", function(e){
    if (e.which == 9) {  // TAB
      e.preventDefault();
      activeIdx = (activeIdx + 1) % 3;
      $ctl.eq(activeIdx).addClass('active').siblings('.active').removeClass('active');
      // $elem.autocomplete('option', 'source', _data[activeIdx]);  // does nothing
      $elem.autocomplete('search', $elem.val());
    }

  });
};

// Patch jQuery autocomplete to filter using fuzzy matching
$.ui.autocomplete.filter = function(array, term) {
  var results = autocomplete_tries[activeIdx].search(term);
  return $.map(results, function(r) { return r.data.name; });
};


// TODO camelCase
exports.autocomplete_institutions = autocomplete_institutions;


})(jQuery, Trie, window);
