# utils.py
from flask import session, flash, redirect, url_for
from app.models import db, Veri, Harita
from functools import wraps

def check_authenticated():
    return 'user_id' in session

def authenticated_required(view_func):
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        if not check_authenticated():
            flash("Bu işlemi gerçekleştirmek için giriş yapmalısınız.", "danger")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return decorated_function


def kdsid_hesapla(mvid, toplam_arsa_alani, birlesik_parsel_sayisi, is_site, bose_parsel_numaralari, parsel):
    kdsid = mvid  # Başlangıçta kdsid, mvid değeri ile aynıdır.

    # bose_parsel_numaralari string'ini virgülle ayrılmış parsel numaralarının listesine dönüştür
    bose_parsel_listesi = bose_parsel_numaralari.split(',')

    # parsel değerini string'e çevir
    parsel_str = str(parsel)
    
    # Eğer alan site ise koşulsuz %30 artış yapılır.
    if is_site:
        kdsid *= 1.30
    else:
        # 6 veya daha fazla parselin birleşmesi ve toplam arsa alanı 1000m2 üzerinde ise
        if birlesik_parsel_sayisi >= 6 and toplam_arsa_alani > 1000:
            # Boş parsel ise %15 artır, değilse %30 artır
            kdsid *= 1.15 if parsel_str in bose_parsel_listesi else 1.30
        else:
            # Diğer alan büyüklüğüne göre artış yüzdeleri
            if toplam_arsa_alani > 3000:
                kdsid *= 1.30
            elif toplam_arsa_alani > 2000:
                kdsid *= 1.25
            elif toplam_arsa_alani > 1000:
                kdsid *= 1.20
            elif toplam_arsa_alani > 750:
                kdsid *= 1.15
            elif toplam_arsa_alani > 500:
                kdsid *= 1.10

    return kdsid

def harita_kdalan_guncelle():
    veri_kayitlari = db.session.query(Veri.ada, Veri.parsel).distinct().all()
    for ada, parsel in veri_kayitlari:
        ada_parsel = f"{ada}/{parsel}"
        harita_kaydi = Harita.query.filter_by(text_data=ada_parsel).first()
        if harita_kaydi:
            harita_kaydi.kdalan = True
    db.session.commit()
