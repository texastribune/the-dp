// TODO cache using localStorage?
(function($, Trie, exports){
"use strict";


// configuration
var $elem = $(".q");
var $ctl = $('#view-map a.btn');


var autocomplete_trie = new Trie();
var _data = [[], [], []];
var activeIdx = 0;

// prebuild data source
var build_sources = function(data){
  var newdata = _data, inst;
  for (var i = 0; i < data.length; i++){
    inst = data[i];
    newdata[0].push(inst.name);
    newdata[1 + !inst.is_private].push(inst.name);
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

  // Insert institutions to trie
  $.each(data, function(i, o) {
    autocomplete_trie.insert(o.name.toLowerCase(), o);
  });

  // Initialize autocomplete
  $elem.autocomplete({
    source: _data[0],
    select: function(e, o) {
      var uri = urisByName[o.item.label];
      if (typeof(uri) !== "undefined") {
        location.href = uri;
      }
    }
  });

  $elem.on("keydown", function(e){
    if (e.which == 9) {  // TAB
      activeIdx = (activeIdx + 1) % 3;
      $elem.autocomplete('option', 'source', _data[activeIdx]);
      $elem.autocomplete('search', $elem.val());
      $ctl.eq(activeIdx).addClass('active').siblings('.active').removeClass('active');
      e.preventDefault();
    }

  });
};

// Patch jQuery autocomplete to filter using fuzzy matching
$.ui.autocomplete.filter = function(array, term) {
  var results = autocomplete_trie.search(term);
  return $.map(results, function(r) { return r.data.name; });
};


// TODO camelCase
exports.autocomplete_institutions = autocomplete_institutions;


})(jQuery, Trie, window);
