from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app import db
from app.models import FirmaBilgileri
from app.forms import FirmaBilgileriForm

firma = Blueprint('firma', __name__)

@firma.route('/firma-bilgileri', methods=['GET', 'POST'])
@login_required
def firma_bilgileri():
    form = FirmaBilgileriForm()
    if form.validate_on_submit():
        firma = FirmaBilgileri(firma_ad=form.firma_ad.data,
                               vergi_no=form.vergi_no.data,
                               yetkili_tc=form.yetkili_tc.data,
                               yetkili_ad=form.yetkili_ad.data,
                               firma_adres=form.firma_adres.data,
                               tel_no=form.tel_no.data,
                               email=form.email.data,
                               iban_no=form.iban_no.data,
                               mut_sinif=form.mut_sinif.data)
        db.session.add(firma)
        db.session.commit()
        flash('Firma bilgileri başarıyla kaydedildi.', 'success')
        return redirect(url_for('firma_bilgileri'))
    return render_template('frontend/firma_bilgileri.html', form=form)