from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from app.models import Proje, Veri, User
from app.utils import kdsid_hesapla  # utils modülünden kdsid_hesapla fonksiyonunu içe aktarın
from app.forms import ProjeForm
import openpyxl
import pandas as pd
from sqlalchemy import func, case
from flask import current_app
from app import db

proje = Blueprint('proje', __name__)

@proje.route('/proje_ekle', methods=['GET', 'POST'])
def proje_ekle():
    form = ProjeForm()

    if form.validate_on_submit():
        # Formdan gelen bilgileri al
        proje_adi = form.proje_adi.data
        koordinator_id = form.koordinator_sec.data
        excel_file = request.files['excel_file']
        bose_parsel_numaralari = form.bose_parsel_numaralari.data
        is_site = form.is_site.data  # Site durumu için checkbox

        # Yeni proje oluştur
        yeni_proje = Proje(proje_adi=proje_adi, user_id=koordinator_id, is_site=is_site)  # Site durumu ekleniyor
        db.session.add(yeni_proje)
        db.session.flush()  # Veritabanına henüz kaydetmeden ID almak için

        # Excel dosyasını işle
        if excel_file:
            workbook = openpyxl.load_workbook(excel_file)
            sheet = workbook.active

            # Excel dosyasını oku
            df = pd.read_excel('your_excel_file.xlsx')

            # 'ada' ve 'parsel' sütunlarına göre grupla
            grouped = df.groupby(['ada', 'parsel'])

            # Grup sayısını hesapla
            birlesik_parsel_sayisi = len(grouped)

            for row in sheet.iter_rows(min_row=2, values_only=True):
                # Satırdaki verileri al (excel dosyanıza göre düzenleyin)
                isim, telefon, tcno, mvid, _, arsaalan, kisiarsaalan, hisseoran, ada, parsel = row

                # Hesaplamalar
                hisseoran = kisiarsaalan / arsaalan if arsaalan > 0 else 0

                # Kdsid hesapla
                kdsid = kdsid_hesapla(mvid, arsaalan, birlesik_parsel_sayisi, is_site, bose_parsel_numaralari)

                # Veri tablosuna veri ekle
                yeni_veri = Veri(proje_id=yeni_proje.proje_id, isim=isim, telefon=telefon, tcno=tcno, mvid=mvid, kdsid=kdsid, arsaalan=arsaalan, kisiarsaalan=kisiarsaalan, hisseoran=hisseoran, ada=ada, parsel=parsel)

                db.session.add(yeni_veri)

        db.session.commit()
        flash('Proje başarıyla eklendi!', 'success')
        return redirect(url_for('proje.projeler'))

    return render_template('admin/proje_ekle.html', form=form)



@proje.route('/projeler')
def projeler():
    projeler = db.session.query(Proje, User).join(User, Proje.user_id == User.user_id).all()
    return render_template('admin/projeler.html', projeler=projeler)


@proje.route('/proje_detay/<int:proje_id>')
def proje_detay(proje_id):
    # Proje bilgisini çek
    proje = Proje.query.get_or_404(proje_id)

    # Proje ile ilişkilendirilmiş kdsid verilerini çek
    veriler = db.session.query(
        Veri.ada, 
        Veri.parsel,
        func.sum(Veri.kdsid).label('kdsid_toplam'),
        func.sum(case([(Veri.onay_durumu == True, Veri.kdsid)], else_=0)).label('kdsid_onayli_toplam')
    ).filter(Veri.proje_id == proje_id).group_by(Veri.ada, Veri.parsel).all()

    # Proje ile ilişkilendirilmiş diğer detaylı verileri çek (mvid_hisseoran hesaplaması dahil)
    fizveriler = db.session.query(
        Veri.ada,
        Veri.parsel,
        Veri.mvid,
        Veri.hisseoran,
        (Veri.mvid * Veri.hisseoran).label('mvid_hisseoran'),
        # Diğer gerekli sütunlar...
    ).filter(Veri.proje_id == proje_id).all()

    # Şablonu verilerle birlikte render et
    return render_template('admin/proje_detay.html', proje=proje, veriler=veriler, fizveriler=fizveriler)


@proje.route('/sil_proje/<int:proje_id>', methods=['POST'])
def sil_proje(proje_id):
    # Proje ID'si ile ilişkili olan proje ve verileri bul
    proje = Proje.query.get_or_404(proje_id)
    veriler = Veri.query.filter_by(proje_id=proje_id).all()

    # Önce ilgili Veri objelerini sil
    for veri in veriler:
        db.session.delete(veri)

    # Sonra Proje objesini sil
    db.session.delete(proje)

    # Değişiklikleri veritabanına kaydet
    db.session.commit()

    return jsonify(message="Proje ve ilişkili veriler başarıyla silindi.")


