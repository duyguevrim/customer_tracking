from . import guncel_modul
from .models import Siparis, Guncel_Tahsilat, GuncelOdeme, TumMusteriTahsilatlari
from flask_login import login_required, current_user
from flask import redirect, render_template, url_for, flash, request
from company.models import User
from company import db
from services.users import *
from .forms import SiparisForm, TahsilatForm, TahsilatFormm
from werkzeug.utils import secure_filename
import os
from company.models import User
from musteri.forms import AddTahsilatForm
import secrets
from musteri.forms import AddOdemeForm
from company.globals import employees_name
from company.forms import ChangeAssistantForm
from datetime import datetime
from sqlalchemy import extract, or_, and_

@guncel_modul.route('/siparisler/odeme-ekle/<int:siparis_id>', methods=['GET', 'POST'])
@login_required
def add_odeme(siparis_id):
    siparis = Siparis.query.get(siparis_id)
    # user = User.query.get(siparis.user_id)
    form = AddOdemeForm()
    user = User.query.get(25)
    if form.validate_on_submit():
        tutar = form.tutar.data
        date = form.create_date.data
        guncel_odeme = GuncelOdeme(tutar=tutar, siparis_id=siparis.id, create_date=date)
        siparis.tahsilat += form.tutar.data
        user.toplam_siparis_tahsilati += form.tutar.data
        db.session.add(guncel_odeme)
        db.session.commit()
        return redirect(url_for('guncel_modul.siparis_list', siparis_id=siparis.id))
    return render_template('odeme_ekle.html', siparis=siparis, form=form)


@guncel_modul.route('/siparis-ekle', methods=['GET', 'POST'])
@login_required
def add_siparis():
    form = SiparisForm()
    form.assistans.choices = [(str(value), str(key)) for key, value in employees_name.items()]
    if form.validate_on_submit():
        proje_no = form.proje_no.data
        musteri_adi = form.isim.data
        siparis_tutari = form.tutar.data
        son_odeme_tarihi = form.son_odeme_tarihi.data
        isin_alinma_tarihi = form.isin_alinma_tarihi.data
        siparis_son_durum = form.siparis_son_durum.data
        user_id = int(form.assistans.data)
        siparis = Siparis(proje_no=proje_no, musteri_adi=musteri_adi, siparis_tutari=siparis_tutari,
                          son_odeme_tarihi=son_odeme_tarihi, isin_alinma_tarihi=isin_alinma_tarihi,
                          siparis_son_durum=siparis_son_durum, user_id=user_id)
        db.session.add(siparis)
        db.session.commit()
        user = User.query.get(siparis.user_id)
        user.toplam_siparis_tutari += siparis.siparis_tutari
        db.session.commit()
        return redirect(url_for("guncel_modul.add_siparis"))
    return render_template("siparis_ekle.html", form=form)


@guncel_modul.route('/guncel-odeme/sil/<int:odeme_id>', methods=['GET', 'POST'])
@login_required
def delete_odeme(odeme_id):
    guncel_odeme = GuncelOdeme.query.get(odeme_id)
    siparis = Siparis.query.get(guncel_odeme.siparis_id)
    user = User.query.get(siparis.user_id)
    siparis.tahsilat -= guncel_odeme.tutar
    user.toplam_siparis_tahsilati -= guncel_odeme.tutar
    db.session.delete(guncel_odeme)
    db.session.commit()
    return redirect(url_for("guncel_modul.list_guncel_odeme"))


@guncel_modul.route('/siparisler', methods=['GET', 'POST'])
@login_required
def siparis_list():
    son_odeme_ay = datetime.today().month
    son_odeme_yil = datetime.today().year
    if current_user.role == "Finance":
        siparisler = Siparis.query.filter(and_(extract('month', Siparis.son_odeme_tarihi) == son_odeme_ay), extract('year', Siparis.son_odeme_tarihi) == son_odeme_yil).all()
        return render_template('siparisler_all.html', siparisler=siparisler)
    else:
        siparisler = Siparis.query.filter(and_(extract('month', Siparis.son_odeme_tarihi) == son_odeme_ay), extract('year', Siparis.son_odeme_tarihi) == son_odeme_yil).all()
        return render_template("satis_tum_siparisler.html", siparisler=siparisler)

@guncel_modul.route('/siparisler-finans', methods=['GET', 'POST'])
@login_required
def siparis_list_finance():
    son_odeme_ay = datetime.today().month - 1
    siparisler = Siparis.query.filter_by(user_id = 21).all()
    return render_template("siparis_list.html", siparisler=siparisler)


@guncel_modul.route('/tum-siparisler', methods=['GET', 'POST'])
@login_required
def siparisler_all():
    son_odeme_ay = datetime.today().month
    siparisler = Siparis.query.filter(extract('month', Siparis.son_odeme_tarihi) == son_odeme_ay).all()
    return render_template('siparisler_all.html', siparisler=siparisler)


@guncel_modul.route('/siparisler/sil/<int:siparis_id>', methods=['GET', 'POST'])
@login_required
def delete_siparis(siparis_id):
    siparis = Siparis.query.get(siparis_id)
    user = User.query.get(siparis.user_id)

    user.toplam_siparis_tutari -= siparis.siparis_tutari
    user.toplam_siparis_tahsilati -= siparis.tahsilat
    siparis__id = siparis.id
    # odeme = GuncelOdeme.query.filter_by(siparis_id=siparis__id).first()
    # db.session.delete(odeme)
    # db.session.commit()

    db.session.delete(siparis)
    db.session.commit()
    return redirect(url_for('guncel_modul.siparis_list'))


@guncel_modul.route('/guncel-odeme')
@login_required
def list_guncel_odeme():
    month = datetime.today().month-1
    guncel_odemeler = GuncelOdeme.query.filter(GuncelOdeme.id > int(7132)).all()
    return render_template('guncel_odemeler.html', guncel_odemeler=guncel_odemeler)



@guncel_modul.route('/guncel/rapor', methods=['GET', 'POST'])
@login_required
def tablo():
    users = User.query.all()
    user = User.query.get(25)

    return render_template("rapor.html", user=user)


@guncel_modul.route('/guncel-tablo', methods=['GET', 'POST'])
@login_required
def temsilci_tablosu():
    if current_user.role == "Manager":
        users = User.query.filter(and_(User.id< 18, User.id != 10, User.id != 11, User.id != 12 , User.id != 14, User.id != 16 )).all()
        return render_template("temsilci_tablosu.html", users=users)
    elif current_user.id == 26:
        users = User.query.filter(User.id > 21).all()
        for user in users:
            print(user)
        return render_template("temsilci_tablosu.html", users=users)

@guncel_modul.route('/Siparisler/duzenle/<int:siparis_id>', methods=['GET', 'POST'])
@login_required
def siparis_duzenle(siparis_id):
    siparis = Siparis.query.get(siparis_id)
    user = User.query.get(siparis.user_id)
    form = SiparisForm()
    if form.validate_on_submit():
        yeni_tutar = form.tutar.data
        siparis.musteri_adi = form.isim.data
        siparis.proje_no = form.proje_no.data
        if yeni_tutar != siparis.siparis_tutari:
            if siparis.siparis_tutari > yeni_tutar:
                user.toplam_siparis_tutari = user.toplam_siparis_tutari - (siparis.siparis_tutari - yeni_tutar)
                siparis.siparis_tutari = yeni_tutar
            if siparis.siparis_tutari < yeni_tutar:
                user.toplam_siparis_tutari = user.toplam_siparis_tutari + (yeni_tutar - siparis.siparis_tutari)
                siparis.siparis_tutari = yeni_tutar
        else:
            siparis.siparis_tutari = form.tutar.data
        flash(f"{siparis.musteri_adi} adlı sipariş için yapılan değişiklikler başarıyla güncellendi.",
              "success")
        db.session.commit()
    return render_template('siparis_duzenle.html', form=form, siparis=siparis)


@guncel_modul.route('/tahsilat-ekle-crm', methods=['GET', 'POST'])
@login_required
def tahsilat_ekle_crm():
    form = TahsilatFormm()
    if form.validate_on_submit():
        musteri_adi_crm = form.isim.data
        crm_kodu = form.crm_kodu.data
        tahsilat_tutari = form.tutar.data
        aciklama = form.aciklama.data
        user_id = current_user.id
        if form.dekont.data:
            f = form.dekont.data
            filename = secure_filename(f.filename)
            filename = secrets.token_hex(16) + '.' + filename.split('.')[1]
            print(os.getcwd(), 'static/dekonts', filename)
            print(os.getcwd())
            f.save(os.path.join(
                os.getcwd(), 'static/dekonts', filename
            ))
            tahsilat = TumMusteriTahsilatlari(tahsilat_tutari=tahsilat_tutari, musteri_adi_crm=musteri_adi_crm,
                                              aciklama=aciklama,
                                              dekont=filename, user_id=user_id, crm_kodu=crm_kodu)
            db.session.add(tahsilat)
            db.session.commit()
        else:
            tahsilat = TumMusteriTahsilatlari(tahsilat_tutari=tahsilat_tutari, musteri_adi_crm=musteri_adi_crm,
                                              aciklama=aciklama, user_id=user_id, crm_kodu=crm_kodu)
            db.session.add(tahsilat)
            db.session.commit()
        flash(f"{tahsilat.musteri_adi_crm} için {form.tutar.data} TL tutarında tahsilat oluşturuldu.", "success")
        return redirect(url_for('guncel_modul.tahsilat_ekle_crm'))
    return render_template('tahsilat_ekle_crm.html', form=form)


@guncel_modul.route('/tahsilat-durumu/sil/<int:tahsilat_id>', methods=['GET', 'POST'])
@login_required
def delete_crm_tahsilat(tahsilat_id):
    tahsilat = TumMusteriTahsilatlari.query.get(tahsilat_id)
    db.session.delete(tahsilat)
    db.session.commit()
    return redirect(url_for('guncel_modul.crm_onay_bekleyen'))


@guncel_modul.route('/tahsilat-durumu', methods=['GET', 'POST'])
@login_required
def tahsilat_durum():
    bekleyenler = TumMusteriTahsilatlari.query.filter_by(durum="Onay Bekliyor").all()
    onaylananlar = TumMusteriTahsilatlari.query.filter_by(durum="Onaylandı").all()
    return render_template('finans_crm_tahsilat.html', bekleyenler=bekleyenler, onaylananlar=onaylananlar)


@guncel_modul.route('/tahsilat-durumu/onayla/<int:tahsilat_id>', methods=['GET', 'POST'])
@login_required
def crm_tahsilat_onayla(tahsilat_id):
    tahsilat = TumMusteriTahsilatlari.query.get(tahsilat_id)
    tahsilat.durum = "Onaylandı"
    db.session.commit()
    return redirect('tahsilat-durumu')


@guncel_modul.route('/tahsilat-durumu/onayi-kaldir/<int:tahsilat_id>', methods=['GET', 'POST'])
@login_required
def crm_tahsilat_onay_kaldir(tahsilat_id):
    tahsilat = TumMusteriTahsilatlari.query.get(tahsilat_id)
    tahsilat.durum = "Onay Bekliyor"
    db.session.commit()
    return redirect('tahsilat-islem')


@guncel_modul.route('/crm-onay-bekleyenler')
@login_required
def crm_onay_bekleyen():
    tahsilatlar = TumMusteriTahsilatlari.query.filter_by(durum="Onay Bekliyor").join(
        User, TumMusteriTahsilatlari.user_id == current_user.id).all()
    return render_template("crm_tahsilat_onay.html", tahsilatlar=tahsilatlar)


@guncel_modul.route('/crm-onaylananlar')
@login_required
def crm_onaylanan():
    tahsilatlar = TumMusteriTahsilatlari.query.filter_by(durum="Onaylandı").join(
        User, TumMusteriTahsilatlari.user_id == current_user.id).all()
    return render_template("crm_tahsilat_onay.html", tahsilatlar=tahsilatlar)


@guncel_modul.route('/Siparisler/tahsilat/ekle/<int:siparis_id>', methods=['GET', 'POST'])
@login_required
def tahsilat_ekle(siparis_id):
    form = TahsilatForm()
    siparis = Siparis.query.get(siparis_id)
    if form.validate_on_submit():
        tutar = form.tutar.data
        aciklama = form.aciklama.data
        user_id = current_user.id
        if form.dekont.data:
            f = form.dekont.data
            filename = secure_filename(f.filename)
            filename = secrets.token_hex(16) + '.' + filename.split('.')[1]
            print(os.getcwd(), 'static/dekonts', filename)
            print(os.getcwd())
            f.save(os.path.join(
                os.getcwd(), 'static/dekonts', filename
            ))
            tahsilat = Guncel_Tahsilat(tutar=tutar, aciklama=aciklama, dekont=filename, siparis_id=siparis_id)
            db.session.add(tahsilat)
            db.session.commit()
        else:
            tahsilat = Guncel_Tahsilat(tutar=tutar, aciklama=aciklama, siparis_id=siparis_id)
            db.session.add(tahsilat)
            db.session.commit()
        flash(f"{siparis.musteri_adi} için {form.tutar.data} TL tutarında tahsilat oluşturuldu.", "success")
        return redirect(url_for('guncel_modul.tahsilat_ekle', siparis_id=siparis_id))
    return render_template('guncel_tahsilat_ekle.html', form=form, siparis=siparis)


@guncel_modul.route('/guncel-tahsilat/duzenle/<int:tahsilat_id>', methods=['GET', 'POST'])
@login_required
def edit_tahsilat(tahsilat_id):
    tahsilat = Guncel_Tahsilat.query.get(tahsilat_id)
    form = TahsilatForm()
    siparis = Siparis.query.get(tahsilat.siparis_id)
    if form.validate_on_submit():
        tahsilat.tutar = form.tutar.data
        tahsilat.aciklama = form.aciklama.data
        if form.dekont.data:
            f = form.photo.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(
                'static/dekontlar', filename
            ))
            tahsilat.dekont = filename
        db.session.commit()
        flash(f"{siparis.musteri_adi} için girilen tahsilat başarıyla güncellendi.",
              "success")
        redirect(url_for('guncel_modul.onay_bekleyen', tahsilat_id=tahsilat.id))
    elif request.method == 'GET':
        form.tutar.data = tahsilat.tutar
        form.aciklama.data = tahsilat.aciklama
    return render_template('guncel_tahsilat_ekle.html', form=form, siparis=siparis)


@guncel_modul.route('/tahsilat-islemler/sil/<int:tahsilat_id>', methods=['GET', 'POST'])
@login_required
def delete_tahsilat(tahsilat_id):
    tahsilat = Guncel_Tahsilat.query.get(tahsilat_id)
    db.session.delete(tahsilat)
    db.session.commit()
    return redirect(url_for('guncel_modul.onaylanan'))


@guncel_modul.route('/tahsilat-islem', methods=['GET', 'POST'])
@login_required
def tahsilat_islem():
    bekleyenler = Guncel_Tahsilat.query.filter_by(durum="Onay Bekliyor").all()
    onaylananlar = Guncel_Tahsilat.query.filter_by(durum="Onaylandı").all()
    siparisler = Siparis.query.all()
    return render_template('finans_tahsilat_onay.html', bekleyenler=bekleyenler, onaylananlar=onaylananlar,
                           siparisler=siparisler)


@guncel_modul.route('/tahsilat-islemler/onayla/<int:tahsilat_id>', methods=['GET', 'POST'])
@login_required
def tahsilat_onayla(tahsilat_id):
    tahsilat = Guncel_Tahsilat.query.get(tahsilat_id)
    tahsilat.durum = "Onaylandı"
    db.session.commit()
    return redirect('tahsilat-islem')


@guncel_modul.route('/tahsilat-islemler/onayi-kaldir/<int:tahsilat_id>', methods=['GET', 'POST'])
@login_required
def onay_kaldir(tahsilat_id):
    tahsilat = Guncel_Tahsilat.query.get(tahsilat_id)
    tahsilat.durum = "Onay Bekliyor"
    db.session.commit()
    return redirect('tahsilat-islem')


@guncel_modul.route('/guncel-tahsilat/onay-bekleyenler')
@login_required
def onay_bekleyen():
    tahsilatlar = Guncel_Tahsilat.query.filter_by(durum="Onay Bekliyor").join(Siparis,
                                                                              Guncel_Tahsilat.siparis_id == Siparis.id).join(
        User, Siparis.user_id == current_user.id).all()
    return render_template("guncel_tahsilat_onay.html", tahsilatlar=tahsilatlar)


@guncel_modul.route('/guncel-tahsilat/onaylananlar')
@login_required
def onaylanan():
    tahsilatlar = Guncel_Tahsilat.query.filter_by(durum="Onaylandı").join(Siparis,
                                                                          Guncel_Tahsilat.siparis_id == Siparis.id).join(
        User, Siparis.user_id == current_user.id).all()
    return render_template("guncel_tahsilat_onay.html", tahsilatlar=tahsilatlar)
