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

var map;
var vectorSource;

function initMap() {
    vectorSource = new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: 'https://bbgis.xyz/geoserver/wfs?service=WFS&' +
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

            // Zoom seviyesine bağlı olarak metin stilini ayarla
        var zoom = map.getView().getZoom();
        var text;
        var textStyle;

        // Örneğin, zoom seviyesi 12'den büyük olduğunda metni göster
        if (zoom > 18) {
            text = feature.get('text_data') || ''; // text_data yoksa boş string kullan
            textStyle = new ol.style.Text({
                font: '14px Calibri,sans-serif',
                text: text,
                fill: new ol.style.Fill({
                    color: '#000'
                }),
                stroke: new ol.style.Stroke({
                    color: '#fff',
                    width: 3
                }),
                overflow: true,
                offsetX: 0,
                offsetY: -15 // Metni geometrinin biraz üstünde göstermek için
            });
        }

            return new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: 'black',
                    width: 1
                }),
                fill: new ol.style.Fill({
                    color: color
                }),
                text: textStyle // Metin stilini burada belirt
            });
        }
    });

    map = new ol.Map({
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM()
            }),
            vectorLayer
        ],
        target: 'map',
        view: new ol.View({
            center: ol.proj.fromLonLat([28.84, 41.04]),
            zoom: 15
        })

    
        
    });

    // Popup div'ini oluştur
    var popup = document.createElement('div');
    popup.className = 'popup';
    popup.style.position = 'absolute';
    popup.style.backgroundColor = 'white';
    popup.style.padding = '10px';
    popup.style.border = '1px solid black';
    popup.style.borderRadius = '5px';
    popup.style.boxShadow = '0 1px 4px rgba(0,0,0,0.3)';
    popup.style.display = 'none';

    // Çarpı butonunu oluştur
    var closeButton = document.createElement('div');
    closeButton.innerHTML = '&times;'; // HTML entity for a multiplication sign (times)
    closeButton.style.position = 'absolute';
    closeButton.style.top = '5px';
    closeButton.style.right = '10px';
    closeButton.style.cursor = 'pointer';
    closeButton.style.fontSize = '20px';
    closeButton.style.color = 'black';

    // Çarpı butonuna tıklama olayı ekle
    closeButton.onclick = function() {
        popup.style.display = 'none'; // Popup'ı gizle
    };

    // Popup içeriğini tutacak bir div oluşturun
    var popupContent = document.createElement('div');
    popup.appendChild(popupContent); // Bu div'i popup'a ekleyin

    // Çarpı butonunu popup'a ekle
    popup.appendChild(closeButton);

    // Popup'ı body'ye ekle
    document.body.appendChild(popup);


    // Haritaya tıklama olayı ekle
    map.on('singleclick', function(evt) {
      map.forEachFeatureAtPixel(evt.pixel, function(feature, layer) {
          var geometry = feature.getGeometry();
          var area = geometry.getArea(); // Geometrinin alanını hesapla
          var correctedArea = area / 1.76; // %76 artışı düzeltmek için
          var coord = evt.coordinate; // Tıklanan koordinat
          var coordPx = map.getPixelFromCoordinate(coord); // Koordinatı piksel cinsine çevir
  
          // Ybizden değerini kontrol et
          var ybizdenDurumu = feature.get('ybizden') === 'Evet' ? 'Var' : 'Yok';
          // Orta Hasar değerini kontrol et
          var ortahasarDurumu = feature.get('ortahasar') === 'Evet' ? 'Var' : 'Yok';
          // Çalışma alanı kontrol et
          var kdalanDurumu = feature.get('kdalan') === true ? 'Var' : 'Yok';
  
          // Popup içeriğini ayarla ve göster
          // Popup içeriğini ayarla ve göster
          // Sekmeler için HTML yapısını oluştur
popupContent.innerHTML = `
<div class="tabs">
  <div class="tab-headers">
    <div class="tab-header active" data-tab="tab1">Bina Bilgisi</div>
    <div class="tab-header" data-tab="tab2">Parsel Bilgisi</div>
  </div>
  <div class="tab-content active" id="tab1">
    <!-- Bina bilgisi içeriği -->
    <p>İmar Durumu: ${ybizdenDurumu}</p>
    <p>Yapı Ruhsat Tarihi: ${ybizdenDurumu}</p>
    <p>Bağımsız Bölüm Sayısı: ${ybizdenDurumu}</p>
  </div>
  <div class="tab-content" id="tab2">
    <!-- Parsel bilgisi içeriği -->
    <p>Ada/Parsel: ${feature.get('text_data') || 'Bilgi Yok'}</p>
    <p>Alan: ${correctedArea.toFixed(2)} m²</p>
    <p>Kentsel Dönüşüm Çalışması: ${kdalanDurumu}</p>
    <p>Orta Hasar Var Mı: ${ortahasarDurumu}</p>
  </div>
</div>
`;

// Sekme başlıklarına tıklama olaylarını ekle
document.querySelectorAll('.tab-header').forEach(header => {
header.addEventListener('click', function() {
  // Tüm başlıkları ve içerikleri pasif yap
  document.querySelectorAll('.tab-header').forEach(header => header.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
  
  // Aktif başlık ve içeriği ayarla
  this.classList.add('active');
  document.getElementById(this.dataset.tab).classList.add('active');
});
});

// CSS stilleri
var style = document.createElement('style');
style.innerHTML = `
.tabs { border: 1px solid #ccc; }
.tab-headers { display: flex; }
.tab-header { padding: 10px; cursor: pointer; border-bottom: 3px solid transparent; }
.tab-header.active { border-bottom-color: blue; }
.tab-content { display: none; padding: 10px; }
.tab-content.active { display: block; }
`;
document.head.appendChild(style);


          popup.style.display = 'block';
          popup.style.left = evt.pixel[0] + 'px';
          popup.style.top = evt.pixel[1] + 'px';
          return true; // İlk bulunan özelliği işle
      });
  
      // Eğer tıklanan noktada herhangi bir özellik yoksa, popup'ı gizle
      if (!map.hasFeatureAtPixel(evt.pixel)) {
          popup.style.display = 'none';
      }
  });
  

    document.getElementById('ybizdenCheckbox').addEventListener('change', function() {
        vectorLayer.getSource().refresh();
    });

    document.getElementById('ortahasarCheckbox').addEventListener('change', function() {
        vectorLayer.getSource().refresh();
    });

    document.getElementById('kdalanCheckbox').addEventListener('change', function() {
        vectorLayer.getSource().refresh();
    });
}

function searchFeature() {
    var searchText = document.getElementById('search-box').value;
    vectorSource.forEachFeature(function(feature) {
        if (feature.get('text_data') === searchText) {
            var featureGeometry = feature.getGeometry();
            var featureCenter = ol.extent.getCenter(featureGeometry.getExtent());
            map.getView().animate({center: featureCenter, zoom: 19});
        }
    });
}

document.addEventListener('DOMContentLoaded', initMap);


