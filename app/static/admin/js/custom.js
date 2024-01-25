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
  var styleFunction = function(feature) {
    return new ol.style.Style({
      stroke: new ol.style.Stroke({
        color: 'blue',
        width: 2
      }),
      fill: new ol.style.Fill({
        color: 'rgba(0, 0, 255, 0.1)'
      }),
      text: new ol.style.Text({
        text: feature.get('text_data'), // text_data özelliğini kullan
        scale: 1.2,
        fill: new ol.style.Fill({
          color: '#000'
        })
      })
    });
  };

  var map = new ol.Map({
    target: 'mapContainer',
    layers: [
      new ol.layer.Tile({
        source: new ol.source.OSM()
      }),
      new ol.layer.Vector({
        source: new ol.source.Vector({
          format: new ol.format.GeoJSON(),
          url: '/api/mapdata'
        }),
        style: styleFunction // Özel stil fonksiyonunu kullan
      })
    ],
    view: new ol.View({
      center: ol.proj.fromLonLat([28.8547, 41.0345]),
      zoom: 13
    })
  });
}

document.addEventListener('DOMContentLoaded', function() {
  initMap();
});

