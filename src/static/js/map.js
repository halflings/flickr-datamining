var lyon = new google.maps.LatLng(45.767, 4.833);
var dummy_point = new google.maps.LatLng(45.867, 4.863);
var map;
var markers = [];
var cur_infowindow = null;

function initMap() {
  var mapOptions = {
    zoom: 13,
    center: lyon,
    styles: pale_dawn
  };

  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  addMarker(dummy_point);
}

function addMarker(picture) {
  var infowindow = new google.maps.InfoWindow({
    content: contentTemplate(picture)
  });

  var lat = picture['latitude'];
  var lng = picture['longitude'];
  var position = new google.maps.LatLng(lat, lng);

  var marker = new google.maps.Marker({
    map: map,
    draggable: false,
    animation: google.maps.Animation.DROP,
    position: position
  });

  google.maps.event.addListener(marker, 'click', function()  {
    if (cur_infowindow) {
      cur_infowindow.close();
    }
    cur_infowindow = infowindow;
    toggleBounce(marker);
    infowindow.open(map, marker);
  });

  markers.push(marker);
}

function toggleBounce(marker) {
  if (marker.getAnimation() != null) {
    marker.setAnimation(null);
  } else {
    marker.setAnimation(google.maps.Animation.BOUNCE);
    setTimeout(function(){ marker.setAnimation(null); }, 1500);
  }
}

google.maps.event.addDomListener(window, 'load', initMap);


function loadMarkers() {
  apiCall('/api/pictures', 'GET', {}, function(data) {
    console.log(data);
    $.each(data.pictures, function(i, picture) {
      addMarker(picture);
    });
  });
}

$(document).ready(function() {
  contentTemplate = loadTemplate('#marker-content-template');
  loadMarkers();
});
