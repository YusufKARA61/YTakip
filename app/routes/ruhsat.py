from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.forms import RuhsatBilgileriForm
from app.models import RuhsatBilgileri
from app.utils import harita_ruhsat_guncelle  # utils modülünden ruhsat güncelle fonksiyonunu içe aktarın

ruhsat = Blueprint('ruhsat', __name__)

@ruhsat.route('/ruhsatlar')
@login_required
def ruhsat_listele():
    ruhsatlar = RuhsatBilgileri.query.all()
    return render_template('admin/ruhsat/ruhsat_listele.html', ruhsatlar=ruhsatlar)

@ruhsat.route('/ruhsat-ekle', methods=['GET', 'POST'])
@login_required
def ruhsat_ekle():
    form = RuhsatBilgileriForm()
    if form.validate_on_submit():
        yeni_ruhsat = RuhsatBilgileri(
            yapi_adi=form.yapi_adi.data,
            ruhsat_tarihi=form.ruhsat_tarihi.data,
            zabıt_tarih=form.zabıt_tarih.data,
            imar_barisi=form.imar_barisi.data,
            mahalle=form.mahalle.data,
            ada=form.ada.data,
            parsel=form.parsel.data,
            parsel_turu=form.parsel_turu.data,
            mevcut_insaat_alan=form.mevcut_insaat_alan.data,
            tapu_alani=form.tapu_alani.data,
            blok_sayi=form.blok_sayi.data,
            konut_bb_sayi=form.konut_bb_sayi.data,
            ticari_bb_sayi=form.ticari_bb_sayi.data,
            toplam_bb_sayi=form.toplam_bb_sayi.data,
            toplam_insaat_alan=form.toplam_insaat_alan.data
        )
        db.session.add(yeni_ruhsat)
        db.session.commit()
        flash('Ruhsat başarıyla eklendi.', 'success')

        # Harita tablosunu güncelle
        harita_ruhsat_guncelle()  # Fonksiyonu çağır

        return redirect(url_for('ruhsat.ruhsat_listele'))
    return render_template('admin/ruhsat/ruhsat_ekle.html', form=form)

@ruhsat.route('/ruhsat-duzenle/<int:id>', methods=['GET', 'POST'])
@login_required
def ruhsat_duzenle(id):
    ruhsat = RuhsatBilgileri.query.get_or_404(id)
    form = RuhsatBilgileriForm(obj=ruhsat)
    if form.validate_on_submit():
        ruhsat.yapi_adi = form.yapi_adi.data
        ruhsat.ruhsat_tarihi = form.ruhsat_tarihi.data
        ruhsat.zabıt_tarih = form.zabıt_tarih.data
        ruhsat.imar_barisi = form.imar_barisi.data
        ruhsat.mahalle = form.mahalle.data
        ruhsat.ada = form.ada.data
        ruhsat.parsel = form.parsel.data
        ruhsat.parsel_turu = form.parsel_turu.data
        ruhsat.mevcut_insaat_alan = form.mevcut_insaat_alan.data
        ruhsat.tapu_alani = form.tapu_alani.data
        ruhsat.blok_sayi = form.blok_sayi.data
        ruhsat.konut_bb_sayi = form.konut_bb_sayi.data
        ruhsat.ticari_bb_sayi = form.ticari_bb_sayi.data
        ruhsat.toplam_bb_sayi = form.toplam_bb_sayi.data
        ruhsat.toplam_insaat_alan = form.toplam_insaat_alan.data
        db.session.commit()
        flash('Ruhsat başarıyla güncellendi.', 'success')
        return redirect(url_for('ruhsat.ruhsat_listele'))
    return render_template('admin/ruhsat/ruhsat_duzenle.html', form=form)

@ruhsat.route('/ruhsat-sil/<int:id>', methods=['POST'])
@login_required
def ruhsat_sil(id):
    ruhsat = RuhsatBilgileri.query.get_or_404(id)
    db.session.delete(ruhsat)
    db.session.commit()
    flash('Ruhsat başarıyla silindi.', 'success')
    return redirect(url_for('ruhsat.ruhsat_listele'))

