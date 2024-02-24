function showConfirmation(button) {
  var projeId = $(button).data('proje-id');
  
  if (projeId) {
    $('#delete-button').data('proje-id', projeId); // Bu satırı kaldırın
    $('#silmeOnayModal').modal('show');
    $('#silmeOnayModal').data('proje-id', projeId); // Proje ID'sini modalın kendisine ekleyin
  } else {
    alert('Proje ID alınamadı.');
  }
}

function cancelDeletion() {
  $('#silmeOnayModal').modal('hide');
}

function deleteItem() {
  var projeId = $('#silmeOnayModal').data('proje-id');

  if (projeId) {
    var deleteURL = "/sil_proje/" + projeId;

    $.ajax({
      url: deleteURL,
      method: "POST",
      data: JSON.stringify({ proje_id: projeId }),
      contentType: "application/json",
      success: function(response) {
        $('#silmeOnayModal').modal('hide'); // Silme onay modalını kapat
        showMessageModal(response.message);
        setTimeout(function(){ 
          window.location.reload(); // 1 saniye sonra sayfayı yenile
        }, 1000);
      },
      error: function(xhr, status, error) {
        console.log(error);
      }
    });
  } else {
    console.error('Proje ID tanımsız!');
  }
}



function showMessageModal(message) {
  $('#message-modal .modal-body').text(message);
  $('#message-modal').modal('show');
}

function closeMessageModal() {
  $('#message-modal').modal('hide');
  window.location.reload(); // Sayfayı yenile
}

function showUserConfirmation(button) {
  var userId = $(button).data('user-id');
  
  if (userId) {
    $('#silmeOnayModal').modal('show');
    $('#silmeOnayModal').data('user-id', userId);
  } else {
    alert('Kullanıcı ID alınamadı.');
  }
}

function cancelUserDeletion() {
  $('#silmeOnayModal').modal('hide');
}

function deleteUserItem() {
  var userId = $('#silmeOnayModal').data('user-id');

  if (userId) {
    var deleteURL = "/sil_kullanici/" + userId;

    $.ajax({
      url: deleteURL,
      method: "POST",
      data: JSON.stringify({ user_id: userId }),
      contentType: "application/json",
      success: function(response) {
        $('#silmeOnayModal').modal('hide');
        showMessageModal(response.message);
        setTimeout(function(){ 
          window.location.reload();
        }, 1000);
      },
      error: function(xhr, status, error) {
        console.error('Kullanıcı ID tanımsız!');
      }
    });
  } else {
    console.error('Kullanıcı ID tanımsız!');
  }
}

function initMap() {
  var vectorSource = new ol.source.Vector({
      format: new ol.format.GeoJSON(),
      url: 'http://34.118.84.26:8080/geoserver/wfs?service=WFS&' +
          'version=1.1.0&request=GetFeature&typename=bbgis:harita&' +
          'outputFormat=application/json&srsname=EPSG:3857',
      strategy: ol.loadingstrategy.bbox
  });

  var vectorLayer = new ol.layer.Vector({
    source: vectorSource,
    style: function(feature) {
        var ybizdenChecked = document.getElementById('ybizdenCheckbox').checked;
        var ortahasarChecked = document.getElementById('ortahasarCheckbox').checked;
        var kdalanChecked = document.getElementById('kdalanCheckbox').checked;

        // Varsayılan renk
        var color = 'rgba(0, 0, 255, 0.1)';

        if (kdalanChecked && feature.get('kdalan') === true) {
            color = 'blue';
        }
        if (ybizdenChecked && feature.get('ybizden') === 'Evet') {
            color = 'green';
        }
        if (ortahasarChecked && feature.get('ortahasar') === 'Evet') {
            color = 'red';
        }

        return new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: 'black',
                width: 1
            }),
            fill: new ol.style.Fill({
                color: color
            })
        });
    }
});



  var map = new ol.Map({
      layers: [
          new ol.layer.Tile({
              source: new ol.source.OSM()
          }),
          vectorLayer
      ],
      target: 'map',
      view: new ol.View({
          center: ol.proj.fromLonLat([30, 40]),
          zoom: 6
      })
  });

  document.getElementById('ybizdenCheckbox').addEventListener('change', function() {
      vectorLayer.getSource().refresh(); // Refresh the layer
  });

  document.getElementById('ortahasarCheckbox').addEventListener('change', function() {
      vectorLayer.getSource().refresh(); // Refresh the layer
  });

  document.getElementById('kdalanCheckbox').addEventListener('change', function() {
    vectorLayer.getSource().refresh(); // Refresh the layer
});
}

document.addEventListener('DOMContentLoaded', initMap);
