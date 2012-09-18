var static_url = tt.media_url || '';

var map_institutions = function(data) {
  var template = Handlebars.compile($("#mapPopup").html()),
      $mapPopupContainer = $("#mapPopupContainer"),
      mapOptions = {
        center: [31.22219703210317, -99.9018131],
        zoom: 6,
        minZoom: 6,
        maxZoom: 17
      },
      map = L.map('mapCanvas', mapOptions),
      layer = new L.TileLayer("http://{s}.tiles.mapbox.com/v3/texastribune.map-3g2hqvcf/{z}/{x}/{y}.png", {
        subdomains: ["a", "b", "c", "d"]
      }).addTo(map),
      capIcon = L.icon({
        iconUrl: static_url + '/tx_highered/images/icon-cap.png',
        iconSize: [28, 21],
        iconAnchor: [14, 11.5],
        popupAnchor: [14, 11.5]
      }),
      points = {pub: [], pri:[]},  // technically these are layers
      navigationCanceled = false,
      hideAll = function(x){
        x.eachLayer(function(y){ y.setOpacity(0.1); });
      },
      showAll = function(x){
        x.eachLayer(function(y){ y.setOpacity(1); });
      };

  // Create a feature for each institution
  $.each(data, function(i, institution) {
    if (!institution.geojson) return;
    var point = L.geoJson(institution.geojson, {
      pointToLayer: function(feature, latlng) {
        var marker = L.marker(latlng, {icon: capIcon});
        return marker;
      },
      onEachFeature: function(feature, layer) {
        var data = feature.properties;
        layer.on("mouseover", function(_) {
          $mapPopupContainer.html(template({
            name: institution.name,
            city: institution.city
          }));
        });
        layer.on("mouseout", function(_) {
          $mapPopupContainer.html("<h4>Hover over a campus</h4>");
        });
        layer.on("click", function(e) {
          navigationCanceled = false;
          e = e.originalEvent;  // make e look like a standard event, not leaflet event
          setTimeout(function() {
            if (navigationCanceled !== true) {
              if (e.which && e.which == 2){
                window.open(institution.uri);
              } else {
                window.location.href = institution.uri;
              }
            }
          }, 500);
        },
        layer.on("dblclick", function() {
          navigationCanceled = true;
          map.zoomIn();
        }));
      }
    }).addTo(map);
    // store reference
    points[institution.is_private? 'pri' : 'pub'].push(point);
  });


  // selectively show/hide public/private institutions
  $('#view-map h2 a.btn').click(function(e){
    e.preventDefault();
    var $this = $(this);
    switch ($this.data('action')){
      case 'public':
        points.pri.forEach(hideAll);
        points.pub.forEach(showAll);
      break;
      case 'private':
        points.pub.forEach(hideAll);
        points.pri.forEach(showAll);
      break;
      default:
        points.pri.forEach(showAll);
        points.pub.forEach(showAll);
    }
    $this.addClass('active').siblings('.active').removeClass('active');
  });

  // Reset map when return button is clicked
  $("#statewideZoom").on("click", function() {
    map.setView(mapOptions.center, mapOptions.zoom);
  });

  // Add popup container
  $mapPopupContainer.appendTo("#mapCanvas").css("display", "inline");
};

