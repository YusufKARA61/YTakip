# app/routes/main.py
from flask import Blueprint, render_template, request, flash
from app import db
from app.models import Veri
from app.forms import SorguForm

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def home():
    form = SorguForm()
    if request.method == 'POST' and form.validate_on_submit():
        tcno = form.tcno.data
        raw_results = Veri.query.filter_by(tcno=tcno).all()

        # mvid_hisseoran ve kdsid_hisseoran değerlerini hesapla
        sorgu_sonuclari = []
        for result in raw_results:
            mvid_hisseoran = result.mvid * result.hisseoran
            kdsid_hisseoran = result.kdsid * result.hisseoran
            sorgu_sonuclari.append({
                'isim': result.isim,
                'ada': result.ada,
                'parsel': result.parsel,
                'arsaalan': result.arsaalan,
                'kisiarsaalan': result.kisiarsaalan,
                'mvid_hisseoran': mvid_hisseoran,
                'kdsid_hisseoran': kdsid_hisseoran
                # Diğer alanlarınız buraya eklenebilir
            })

        if sorgu_sonuclari:
            return render_template('frontend/sorgu_sonuc.html', sorgu_sonuclari=sorgu_sonuclari)
        else:
            flash('Bu TCNO ile eşleşen veri bulunamadı.', 'error')
    return render_template('frontend/home.html', form=form)

@main.route('/map')
def show_map():
    return render_template('frontend/map.html')
