from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify,send_file
from app.models import Proje, Veri, User
from app.utils import kdsid_hesapla, harita_kdalan_guncelle  # utils modülünden kdsid_hesapla fonksiyonunu içe aktarın
from app.forms import ProjeForm
from flask_login import current_user, login_required
import openpyxl
import pandas as pd
from io import BytesIO
from sqlalchemy import func, case
from flask import current_app
from app import db
from flask_mail import Message
import os
from werkzeug.utils import secure_filename
from collections import defaultdict
from app import mail


proje = Blueprint('proje', __name__)

@proje.route('/proje_ekle', methods=['GET', 'POST'])
@login_required
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
            # Dosya adını güvenli bir şekilde al
            filename = secure_filename(excel_file.filename)
            # Dosyayı bir yere kaydet (örneğin 'uploads' klasörüne)
            filepath = os.path.join('uploads', filename)
            excel_file.save(filepath)

            workbook = openpyxl.load_workbook(filepath)
            sheet = workbook.active

            # Dosyayı kaydettikten sonra pandas ile oku
            df = pd.read_excel(filepath)

            # 'ada' ve 'parsel' sütunlarına göre grupla
            grouped = df.groupby(['ada', 'parsel'])['arsaalan'].first()

            # Toplam arsa alanını bir sözlükte sakla
            toplam_arsa_alani_dict = defaultdict(float)
            for (ada, parsel), total_area in grouped.items():
                toplam_arsa_alani_dict[(ada, parsel)] = total_area

            # Grup sayısını hesapla
            birlesik_parsel_sayisi = len(grouped)

            for row in sheet.iter_rows(min_row=2, values_only=True):
                # Satırdaki verileri al (excel dosyanıza göre düzenleyin)
                isim, telefon, tcno, mvid, _, arsaalan, kisiarsaalan, hisseoran, ada, parsel = row

                # Hesaplamalar
                hisseoran = kisiarsaalan / arsaalan if arsaalan > 0 else 0

                # Gruplanmış verilerin 'arsaalan' değerlerini topla ve sonucu toplam_arsa_alani değişkenine aktar
                toplam_arsa_alani = grouped.sum()

                # Kdsid hesapla
                kdsid = 1.3 * kdsid_hesapla(mvid, toplam_arsa_alani, birlesik_parsel_sayisi, is_site, bose_parsel_numaralari, parsel)

                # Veri tablosuna veri ekle
                yeni_veri = Veri(proje_id=yeni_proje.proje_id, isim=isim, telefon=telefon, tcno=tcno, mvid=mvid, kdsid=kdsid, arsaalan=arsaalan, kisiarsaalan=kisiarsaalan, hisseoran=hisseoran, ada=ada, parsel=parsel)

                db.session.add(yeni_veri)

        db.session.commit()
        flash('Proje başarıyla eklendi!', 'success')

        # Harita tablosunu güncelle
        harita_kdalan_guncelle()  # Fonksiyonu çağır

        # Seçilen koordinatörün bilgilerini alın
        koordinator = User.query.get(koordinator_id)

        # Seçilen koordinatöre bir e-posta gönderin
        if koordinator:
            msg = Message('Yeni Proje Eklendi',
                    sender=current_app.config['MAIL_DEFAULT_SENDER'],
                    recipients=[koordinator.email])  # User modelinizde 'email' adında bir özellik olduğunu varsayalım

            msg.body = f"Merhaba {koordinator.first_name},\n\nYeni bir proje eklendi: {proje_adi}.\n\nDetaylar için sisteme giriş yapınız."

            try:
                mail.send(msg)
            except Exception as e:
                flash(f'E-posta gönderirken bir hata oluştu: {str(e)}', 'danger')
        return redirect(url_for('proje.projeler'))

    return render_template('admin/proje_ekle.html', form=form)

@proje.route('/projeler')
@login_required
def projeler():
    # Admin veya şef rolüne sahipse tüm projeleri al
    if current_user.has_role('admin') or current_user.has_role('sef'):
        projeler = db.session.query(Proje, User).join(User, Proje.user_id == User.user_id).all()
    # Koordinatör rolüne sahipse sadece kendi projelerini al
    elif current_user.has_role('koordinator'):
        projeler = db.session.query(Proje, User).join(User, Proje.user_id == User.user_id).filter(Proje.user_id == current_user.user_id).all()

    return render_template('admin/projeler.html', projeler=projeler)




@proje.route('/proje_detay/<int:proje_id>')
@login_required
def proje_detay(proje_id):
    # Proje bilgisini çek
    proje = Proje.query.get_or_404(proje_id)

    # Proje ile ilişkilendirilmiş kdsid verilerini çek
    veriler = db.session.query(
        Veri.ada, 
        Veri.parsel,
        func.sum(Veri.kdsid).label('kdsid_toplam'),
        func.sum(case((Veri.onay_durumu == True, Veri.kdsid), else_=0)).label('kdsid_onayli_toplam')
    ).filter(Veri.proje_id == proje_id).group_by(Veri.ada, Veri.parsel).order_by(Veri.ada, Veri.parsel).all()

    # Proje ile ilişkilendirilmiş diğer detaylı verileri çek (mvid_hisseoran hesaplaması dahil)
    fizveriler = db.session.query(
        Veri.ada,
        Veri.veri_id,
        Veri.isim,
        Veri.tcno,
        Veri.arsaalan,
        Veri.parsel,
        Veri.mvid,
        Veri.hisseoran,
        Veri.kisiarsaalan,
        Veri.onay_durumu,
        (Veri.mvid * Veri.hisseoran).label('mvid_hisseoran'),
        (Veri.kdsid * Veri.hisseoran).label('kdsid_hisseoran'),
        # Diğer gerekli sütunlar...
    ).filter(Veri.proje_id == proje_id).order_by(Veri.ada, Veri.parsel).all()

    # Şablonu verilerle birlikte render et
    return render_template('admin/proje_detay.html', proje=proje, veriler=veriler, fizveriler=fizveriler)

@proje.route('/export_excel', methods=['POST'])
def export_excel():
    proje_id = request.form.get('proje_id')
    if proje_id is None:
        return "Proje ID'si eksik.", 400  # Kullanıcıya hata mesajı döndür

    # Veritabanından ilgili verileri çek
    sorgu_sonuclari = Veri.query.filter_by(proje_id=proje_id).all()

    # Sorgu sonuçlarını bir pandas DataFrame'ine dönüştür
    data = [{
        'Ada': veri.ada,
        'Parsel': veri.parsel,
        'TcNo': veri.tcno,
        'İsim': veri.isim,
        'Arsa Alanı': veri.arsaalan,
        'Kişi Arsa Alanı': veri.kisiarsaalan,
        'Mvid': veri.mvid,
        'Kdsid': veri.kdsid,
        'Onay Durumu': 'Evet' if veri.onay_durumu else 'Hayır'
    } for veri in sorgu_sonuclari]

    df = pd.DataFrame(data)

    # DataFrame'i bir Excel dosyasına yaz
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Fizibilite Verileri', index=False)
        
    
    output.seek(0)

    # Oluşturulan Excel dosyasını indirme olarak sun
    return send_file(
    output,
    as_attachment=True,
    download_name=f"fizibilite_{proje_id}.xlsx",  # Flask 2.0 ve sonrası için
    # Flask 1.x için attachment_filename=f"fizibilite_{proje_id}.xlsx",
    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
@proje.route('/update_onay_durumu', methods=['POST'])
def update_onay_durumu():
    data = request.get_json()
    veri_id = data.get('projectId')
    isChecked = data.get('isChecked')

    # veri_id'yi integer'a dönüştür
    try:
        veri_id = int(veri_id)
    except ValueError:
        # Eğer veri_id integer'a dönüştürülemezse hata döndür
        return jsonify({'status': 'error', 'message': 'Invalid veri_id'})

    try:
        veri = Veri.query.get(veri_id)
        if veri:
            veri.onay_durumu = isChecked
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Kayıt bulunamadı'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)})



@proje.route('/sil_proje/<int:proje_id>', methods=['POST'])
@login_required
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


