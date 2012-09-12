
// jQuery UI autocomplete
var autocomplete_institutions = function(data) {
  // Map intitution names to URIs
  var urisByName = {};
  $.map(data, function(o) {
    urisByName[o.name] = o.uri;
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
  term = $.ui.autocomplete.escapeRegex(term);
  var matcher = new RegExp(term.split('').join('.*'), 'i');
  return $.grep( array, function(value) {
    return matcher.test( value.label || value.value || value );
  });
};

