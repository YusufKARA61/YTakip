$(function () {


    // ------------------------------------------------------- //
    // Sidebar
    // ------------------------------------------------------ //
    $('.sidebar-toggler').on('click', function () {
        $('.sidebar').toggleClass('shrink show');
    });



    // ------------------------------------------------------ //
    // For demo purposes, can be deleted
    // ------------------------------------------------------ //

    var stylesheet = $('link#theme-stylesheet');
    $( "<link id='new-stylesheet' rel='stylesheet'>" ).insertAfter(stylesheet);
    var alternateColour = $('link#new-stylesheet');

    if ($.cookie("theme_csspath")) {
        alternateColour.attr("href", $.cookie("theme_csspath"));
    }

    $("#colour").change(function () {

        if ($(this).val() !== '') {

            var theme_csspath = 'css/style.' + $(this).val() + '.css';

            alternateColour.attr("href", theme_csspath);

            $.cookie("theme_csspath", theme_csspath, { expires: 365, path: document.URL.substr(0, document.URL.lastIndexOf('/')) });

        }

        return false;
    });

});

function confirmDelete() {
    if (confirm("Silmek istediğinizden emin misiniz?")) {
        // Silme işlemi için gerekli olan kodu buraya ekleyin
    }
}

Cookies.set('active', 'true');

$(document).ready(function() {
    $('#myTabs a').on('click', function (e) {
      e.preventDefault();
      $(this).tab('show');
    });
  });

  document.addEventListener('DOMContentLoaded', function() {
    var checkboxes = document.querySelectorAll('input[name="onay_durumu_checkbox"]');

    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            var veriId = checkbox.value;
            var isChecked = checkbox.checked; // Doğrudan boolean değer olarak kullan

            console.log('veriId:', veriId, 'isChecked:', isChecked);

            // Veritabanını güncellemek için AJAX isteği gönder
            fetch('/update_onay_durumu', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ projectId: veriId, isChecked: isChecked })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Veritabanı başarıyla güncellendi:', data);
            })
            .catch(error => {
                console.error('Hata:', error);
            });
        });
    });
});

