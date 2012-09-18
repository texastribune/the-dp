var autocomplete_trie = new Trie();

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
  $(".q").autocomplete({
    source: $.map(data, function(n) { return n.name; }),
    select: function(e, o) {
      var uri = urisByName[o.item.label];
      if (typeof(uri) !== "undefined") {
        location.href = uri;
      }
    }
  });
};

// Patch jQuery autocomplete to filter using fuzzy matching
$.ui.autocomplete.filter = function(array, term) {
  results = autocomplete_trie.search(term);
  return $.map(results, function(r) { return r.data.name; });
};
