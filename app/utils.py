# utils.py
from flask import session, flash, redirect, url_for
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


def kdsid_hesapla(mvid, toplam_arsa_alani, birlesik_parsel_sayisi, is_site, bos_parsel_numaralari, parsel):
    kdsid = mvid  # Başlangıçta kdsid, mvid değeri ile aynıdır.
    
    # Eğer alan site ise koşulsuz %30 artış yapılır.
    if is_site:
        kdsid *= 1.30
    else:
        # 6 veya daha fazla parselin birleşmesi durumunda ve boş parsel varsa %15 artış
        # Boş parsel kontrolü
        if birlesik_parsel_sayisi >= 6 and parsel in bos_parsel_numaralari:
            if parsel in bos_parsel_numaralari:
                kdsid *= 1.15  # Boş parsel ise %15 artır
            else:
                kdsid *= 1.30  # Diğer parseller için %30 artır
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

