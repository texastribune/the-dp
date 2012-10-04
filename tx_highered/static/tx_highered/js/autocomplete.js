// TODO cache using localStorage?
(function($, Trie, exports){
"use strict";


// configuration
var $elem = $(".q");
var $ctl = $elem.nextAll();


var autocomplete_trie = new Trie();
var activeIdx = 0,
    setActiveIdx = function(idx){
      activeIdx = idx;
      $ctl.eq(activeIdx).addClass('active').siblings('.active').removeClass('active');
      // $elem.autocomplete('option', 'source', _data[activeIdx]);  // does nothing
      $elem.autocomplete('search', $elem.val());
    };

// jQuery UI autocomplete
var autocomplete_institutions = function(data) {
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
    source: [], // source does nothing but requires an array
    select: function(e, o) {
      var uri = urisByName[o.item.label];
      if (typeof(uri) !== "undefined") {
        location.href = uri;
      }
    }
  });

  // interaction for changing target list of institutions to search
  $ctl.on("click", function(e){
    setActiveIdx($ctl.index(this));
  });
  $elem.on("keydown", function(e){
    if (e.which == 9) {  // TAB
      e.preventDefault();
      setActiveIdx((activeIdx + 1) % 3);
    }
  });
};

// Patch jQuery autocomplete to filter using fuzzy matching
$.ui.autocomplete.filter = function(array, term) {
  var results = autocomplete_trie.search(term.toLowerCase());
  if (activeIdx == 1) {
    results = $.map(results, function(r, i) { return r.data.is_private ? null: r; });
  } else if (activeIdx == 2) {
    results = $.map(results, function(r, i) { return r.data.is_private ? r : null; });
  }
  return $.map(results, function(r) { return r.data.name; });
};


// TODO camelCase
exports.autocomplete_institutions = autocomplete_institutions;


})(jQuery, Trie, window);
