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

function initMap() {
  var map = new ol.Map({
    target: 'mapContainer',
    layers: [
      new ol.layer.Tile({
        source: new ol.source.OSM()
      })
    ],
    view: new ol.View({
      center: ol.proj.fromLonLat([28.8547, 41.0345]), // İstanbul'un koordinatları
      zoom: 13 // Yakınlaştırma seviyesi
    })
  });
}

document.addEventListener('DOMContentLoaded', function() {
  initMap();
});

function initMap() {
  // Harita
  var map = new ol.Map({
    target: 'mapContainer',
    layers: [
      new ol.layer.Tile({
        source: new ol.source.OSM()
      }),
      new ol.layer.Vector({
        source: new ol.source.Vector({
          format: new ol.format.GeoJSON(),
          url: 'URL_TO_YOUR_POSTGIS_VECTOR_DATA' // PostGIS veritabanınızın URL'sini buraya ekleyin
        }),
        style: new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: 'blue',
            width: 2
          }),
          fill: new ol.style.Fill({
            color: 'rgba(0, 0, 255, 0.1)'
          })
        })
      })
    ],
    view: new ol.View({
      center: ol.proj.fromLonLat([28.8547, 41.0345]), // İstanbul'un koordinatları
      zoom: 13 // Yakınlaştırma seviyesi
    })
  });

  // Harita üzerinde ada parsellerini göstermek için uygun bir stil ve kaynak kullanın.
  // Burada stil ve kaynak ayarlarını PostGIS veritabanınıza ve ada parsellerinin formatına göre özelleştirmeniz gerekecektir.
}

document.addEventListener('DOMContentLoaded', function() {
  initMap();
});




