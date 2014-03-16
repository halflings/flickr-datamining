var map;
var lyon = new google.maps.LatLng(45.767, 4.833);
var markers = [];
var clusterCircles = [];
var cur_infowindow = null;

function initMap() {
  var mapOptions = {
    zoom: 15,
    center: lyon,
    styles: pale_dawn
  };

  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
}

function addMarker(picture) {
  var lat = picture['latitude'];
  var lng = picture['longitude'];
  var position = new google.maps.LatLng(lat, lng);

  var marker = new google.maps.Marker({
    map: map,
    draggable: false,
    animation: google.maps.Animation.DROP,
    position: position
  });

  var infowindow = new google.maps.InfoWindow({
    content: contentTemplate(picture)
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

function addCluster(cluster) {

  if (cluster.count < 10)
  {
    return;
  }

  color = Math.floor(Math.random() * 256.0 * 256.0 * 256.0);
  color = '#' + color.toString(16);

  var clusterOptions = {
    strokeColor: color,
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: color,
    fillOpacity: 0.35,
    map: map,
    center: new google.maps.LatLng(cluster.center[0], cluster.center[1]),
    radius: Math.min(400, 10 + Math.sqrt(cluster.count)*2)
  };

  var clusterCircle = new google.maps.Circle(clusterOptions);

  // Info Window / Click event
  var infowindow = new google.maps.InfoWindow({
    content: clusterTemplate(cluster)
  });


  google.maps.event.addListener(clusterCircle, 'click', function()  {
    if (cur_infowindow) {
      cur_infowindow.close();
    }
    cur_infowindow = infowindow;
    console.log(infowindow);
    infowindow.setPosition(clusterCircle.center);
    infowindow.open(map);

    $('#' + cluster.cluster + '-photos').on('click', function() {
      // hiding any infowindow
      cur_infowindow.close();
      cur_infowindow = null;

      // hiding current pictures
      $.each(markers, function(i, marker) {
        marker.setMap(null);
      });

      // loading the cluster's pictures
      loadClusterPictures(cluster.cluster);
    });

  });


  clusterCircles.push(clusterCircles);
  return clusterCircle;
}

function toggleBounce(marker) {
  if (marker.getAnimation() != null) {
    marker.setAnimation(null);
  } else {
    marker.setAnimation(google.maps.Animation.BOUNCE);
    setTimeout(function(){ marker.setAnimation(null); }, 1500);
  }
}

function loadPictures() {
  apiCall('/api/pictures', 'GET', {}, function(data) {
    console.log(data);
    $.each(data.pictures, function(i, picture) {
      addMarker(picture);
    });
  });
}

function loadClusterPictures(clusterId) {
  apiCall('/api/clusters/' + clusterId + '/pictures', 'GET', {}, function(data) {
    console.log(data);
    $.each(data.pictures, function(i, picture) {
      addMarker(picture);
    });
  });
}

function loadClusters() {
  apiCall('/api/clusters', 'GET', {}, function(data) {
    console.log(data);
    $.each(data.clusters, function(i, cluster) {
      addCluster(cluster);
    });
  });
}

google.maps.event.addDomListener(window, 'load', initMap);

$(document).ready(function() {
  contentTemplate = loadTemplate('#marker-content-template');
  clusterTemplate = loadTemplate('#cluster-template');
  loadClusters();
  //loadPictures();
});
