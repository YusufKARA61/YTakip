document.addEventListener("DOMContentLoaded", function () {
  var carousel = document.getElementById("carouselBasicExample");
  var carouselInstance = new bootstrap.Carousel(carousel);

  var prevButton = document.querySelector('[data-mdb-slide="prev"]');
  var nextButton = document.querySelector('[data-mdb-slide="next"]');

  prevButton.addEventListener("click", function () {
    carouselInstance.prev();
  });

  nextButton.addEventListener("click", function () {
    carouselInstance.next();
  });
});

document.addEventListener("DOMContentLoaded", function() {
  // Tablodaki satırlara tıklama olayını ekle
  var rows = document.querySelectorAll("table tbody tr[data-href]");
  rows.forEach(function(row) {
      row.addEventListener("click", function() {
          window.location.href = row.dataset.href;
      });
      row.style.cursor = "pointer"; // Satıra imleci göster
      row.addEventListener("mouseover", function() {
          row.style.backgroundColor = "#f5f5f5"; // Hover efekti
      });
      row.addEventListener("mouseout", function() {
          row.style.backgroundColor = ""; // Hover efektini kaldır
      });
  });
});

function setCookieConsent(accepted) {
  var expiryDate = new Date();
  expiryDate.setDate(expiryDate.getDate() + 30); // 30 gün boyunca geçerli
  document.cookie = "cookieConsent=" + (accepted ? "true" : "false") + "; expires=" + expiryDate.toUTCString() + "; path=/";
}

document.addEventListener("DOMContentLoaded", function() {
  var cookieConsent = document.getElementById("cookie-consent");
  var cookieConsentButton = document.querySelector("#cookie-consent button");

  cookieConsentButton.addEventListener("click", function() {
    cookieConsent.style.display = "none";
    setCookieConsent(true); // Kullanıcı kabul etti
  });

  // Çerez kabul durumuna göre pop-up'ı göster veya gizle
  var isCookieAccepted = document.cookie.includes("cookieConsent=true");
  if (!isCookieAccepted) {
    cookieConsent.style.display = "block";
  }
});

$(document).ready(function() {
  $(".talep-iptal-btn").click(function() {
      $("#talepIptalModal").modal('show');
  });

  $(".talep-iptal-onayla-btn").click(function() {
      $(".talep-iptal-form").submit();
  });
});

$(document).ready(function() {
  $(".talep-olustur-btn").click(function() {
    $("#talepOlusturulduModal").modal('show');
  });

  $(".talep-onay-btn").click(function() {
    $(".talep-onay-form").submit();
  });
});

$(document).ready(function() {
  $(".satis-iptal-btn").click(function() {
      $("#satisIptalModal").modal('show');
  });

  $(".satis-iptal-onayla-btn").click(function() {
      $(".satis-iptal-form").submit();
  });
});

$(document).ready(function() {
  $(".satis-olustur-btn").click(function() {
    $("#satisOlusturulduModal").modal('show');
  });

  $(".satis-onay-btn").click(function() {
    $(".satis-onay-form").submit();
  });
});

// Yıldızlara tıklanınca derecelendirme yapılmasını sağlayın
document.querySelectorAll('.star').forEach(function(star) {
  star.addEventListener('click', function() {
    var rating = this.getAttribute('data-rating');
    
    // Derecelendirmeyi sunucuya göndermek veya başka bir işlem yapmak için
    // AJAX veya başka bir yöntem kullanabilirsiniz.
    // Örnek olarak, kullanıcıya bir mesaj gösterilebilir:
    alert('Derecelendirmeniz: ' + rating);
  });
});

var acceptTermsCheckbox = document.getElementById("acceptTerms");
var registerButton = document.querySelector(".btn.btn-primary");

acceptTermsCheckbox.addEventListener("change", function() {
    if (this.checked) {
            // Kullanıcı sözleşmesini kabul ettiyse kayıt düğmesini etkinleştirin.
            registerButton.removeAttribute("disabled");
    } else {
            // Kullanıcı sözleşmesini kabul etmediyse kayıt düğmesini devre dışı bırakın.
            registerButton.setAttribute("disabled", "disabled");
    }
});












