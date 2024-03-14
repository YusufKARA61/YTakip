from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required
from app.forms import RiskliForm  # Riskli yapılar için form
from app import db
from app.models import Riskli

riskli = Blueprint('riskli', __name__)

@riskli.route('/riskli')
@login_required
def listele():
    form = RiskliForm()
    riskli_binalar = Riskli.query.all()
    return render_template('admin/riskli/riskli_liste.html', form=form, riskli_binalar=riskli_binalar)


@riskli.route('/riskli/ekle', methods=['GET', 'POST'])
@login_required
def ekle():
    form = RiskliForm()
    if form.validate_on_submit():
        yeni_riskli = Riskli(
            YKN=form.YKN.data,
            ADI=form.ADI.data,
            ADA=form.ADA.data,
            PARSEL=form.PARSEL.data,
            MAHALLE=form.MAHALLE.data,
            CADDE=form.CADDE.data,
            SOKAK=form.SOKAK.data,
            BINA_NO=form.BINA_NO.data,
            DURUMU=form.DURUMU.data,
            TESISAT_KESIM_TARIHI=form.TESISAT_KESIM_TARIHI.data,
            YIKIM_TARIHI=form.YIKIM_TARIHI.data,
            PERSONEL=form.PERSONEL.data,
            BASVURU_TARIHI=form.BASVURU_TARIHI.data,
            BASVURU_NO=form.BASVURU_NO.data,
            KAT_SAYISI=form.KAT_SAYISI.data,
            BETON_BASINC_DAYANIMI_MPA=form.BETON_BASINC_DAYANIMI_MPA.data,
            OZEL_NOT=form.OZEL_NOT.data
        )
        db.session.add(yeni_riskli)
        db.session.commit()
        flash('Riskli yapı başarıyla eklendi.', 'success')
        return redirect(url_for('riskli.listele'))
    return render_template('admin/riskli/riskli_ekle.html', form=form)

@riskli.route('/riskli/sil/<int:id>', methods=['POST'])
@login_required
def sil(id):
    riskli = Riskli.query.get_or_404(id)
    db.session.delete(riskli)
    db.session.commit()
    flash('Riskli yapı başarıyla silindi.', 'success')
    return redirect(url_for('riskli.listele'))

@riskli.route('/riskli/düzenle/<int:id>', methods=['GET', 'POST'])
@login_required
def duzenle(id):
    riskli = Riskli.query.get_or_404(id)
    form = RiskliForm(obj=riskli)
    
    if form.validate_on_submit():
        form.populate_obj(riskli)
        db.session.commit()
        flash('Riskli yapı başarıyla güncellendi.', 'success')
        return redirect(url_for('riskli.listele'))
    
    return render_template('admin/riskli/riskli_duzenle.html', form=form)


