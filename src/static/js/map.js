var lyon = new google.maps.LatLng(45.767, 4.833);
var dummy_point = new google.maps.LatLng(45.867, 4.863);
var map;
var markers = [];

function initialize() {
  var mapOptions = {
    zoom: 13,
    center: lyon,
    styles: pale_dawn
  };

  map = new google.maps.Map(document.getElementById('map-canvas'),
          mapOptions);

  addMarker(dummy_point);
}

function addMarker(position) {
  var marker = new google.maps.Marker({
    map:map,
    draggable:true,
    animation: google.maps.Animation.DROP,
    position: position
  });

  google.maps.event.addListener(marker, 'click', toggleBounce);
  markers.push(marker);
}

function toggleBounce() {
  if (marker.getAnimation() != null) {
    marker.setAnimation(null);
  } else {
    marker.setAnimation(google.maps.Animation.BOUNCE);
  }
}

google.maps.event.addDomListener(window, 'load', initialize);


function loadMarkers() {
    apiCall('/api/points', 'GET', {}, function(data) {
        console.log(data);
        $.each(data.points, function (i, point) {
            var lat = point['latitude'];
            var lng = point['longitude'];
            addMarker(new google.maps.LatLng(lat, lng));
        });
    });
}

$(document).ready(function() {
    loadMarkers();
});
