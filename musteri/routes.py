from .models import Musteri, Tahsilat, Odeme, Indirim
from . import musteri_bp
from flask_login import login_required, current_user
from flask import redirect, render_template, url_for, flash, request,send_file
from .forms import AddTahsilatForm, AddOdemeForm, IndirimForm, MusteriTutarForm
from werkzeug.utils import secure_filename
from company import db
from company.forms import ChangeAssistantForm
from company.globals import employees_name
from company.models import User
import os
from .helpers import get_tahsilat_shortcode
from services.tahsilats import submit_tahsilat_form
import requests
import json
from datetime import datetime
import secrets
from .forms import AddCustomerFom
from openpyxl import Workbook


@musteri_bp.route('/tahsilat/ekle/<int:musteri_id>', methods=['GET', 'POST'])
@login_required
def add_tahsilat(musteri_id):
    form = AddTahsilatForm()
    musteri = Musteri.query.get(musteri_id)
    if form.validate_on_submit():
        tutar = form.tutar.data
        aciklama = form.aciklama.data
        if form.dekont.data:
            f = form.dekont.data
            filename = secure_filename(f.filename)
            filename = secrets.token_hex(16) + '.' + filename.split('.')[1]
            print(os.getcwd(), 'static/dekonts', filename)
            print(os.getcwd())
            f.save(os.path.join(
                os.getcwd(), 'static/dekonts', filename
            ))
            shortcode = get_tahsilat_shortcode(current_user.shortcode)
            tahsilat = Tahsilat(tutar=tutar, aciklama=aciklama, dekont=filename, musteri_id=musteri_id,
                                shortcode=shortcode)
            db.session.add(tahsilat)
            db.session.commit()
        else:
            shortcode = get_tahsilat_shortcode(current_user.shortcode)
            tahsilat = Tahsilat(tutar=tutar, aciklama=aciklama, musteri_id=musteri_id, shortcode=shortcode)
            db.session.add(tahsilat)
            db.session.commit()
        flash(f"{musteri.isim} için {form.tutar.data} TL tutarında tahsilat oluşturuldu.", "success")
        return redirect(url_for('musteri.add_tahsilat', musteri_id=musteri_id))
    return render_template('tahsilat_ekle.html', form=form, musteri=musteri)


@musteri_bp.route('/tahsilat/sil/<int:tahsilat_id>', methods=['GET', 'POST'])
@login_required
def delete_tahsilat(tahsilat_id):
    tahsilat = Tahsilat.query.get(tahsilat_id)
    db.session.delete(tahsilat)
    db.session.commit()
    return redirect(url_for('musteri.list_pending_tahsilat'))


@musteri_bp.route('/tahsilat/duzenle/<int:tahsilat_id>', methods=['GET', 'POST'])
@login_required
def edit_tahsilat(tahsilat_id):
    tahsilat = Tahsilat.query.get(tahsilat_id)
    form = AddTahsilatForm()
    musteri = Musteri.query.get(tahsilat.musteri_id)
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
        flash(f"{musteri.isim} isim için girilen {tahsilat.shortcode} kısakodlu tahsilat başarıyla güncellendi.",
              "success")
        redirect(url_for('musteri.edit_tahsilat', tahsilat_id=tahsilat.id))
    elif request.method == 'GET':
        form.tutar.data = tahsilat.tutar
        form.aciklama.data = tahsilat.aciklama
    return render_template('tahsilat_ekle.html', form=form, musteri=musteri)


@musteri_bp.route('/tahsilat/onayla/<int:tahsilat_id>', methods=['GET', 'POST'])
@login_required
def approve_tahsilat(tahsilat_id):
    tahsilat = Tahsilat.query.get(tahsilat_id)
    tahsilat.durum = "Onaylandı"
    db.session.commit()
    return redirect(url_for('dashboard'))


@musteri_bp.route('/tahsilat/onayi-kaldir/<int:tahsilat_id>', methods=['GET', 'POST'])
@login_required
def decline_tahsilat(tahsilat_id):
    tahsilat = Tahsilat.query.get(tahsilat_id)
    tahsilat.durum = "Onay Bekliyor"
    db.session.commit()
    return redirect(url_for('dashboard'))


@musteri_bp.route('/tahsilat/onay-bekleyenler')
@login_required
def list_pending_tahsilat():
    tahsilatlar = Tahsilat.query.filter_by(durum="Onay Bekliyor").join(Musteri, Tahsilat.musteri_id == Musteri.id).join(
        User, Musteri.user_id == current_user.id).all()
    return render_template("tahsilat_pending.html", tahsilatlar=tahsilatlar)


@musteri_bp.route('/tahsilat/onaylananlar')
@login_required
def approved_tahsilat():
    tahsilatlar = Tahsilat.query.filter_by(durum="Onaylandı").join(Musteri, Tahsilat.musteri_id == Musteri.id).join(
        User, Musteri.user_id == current_user.id).all()
    return render_template("tahsilat_pending.html", tahsilatlar=tahsilatlar)


@musteri_bp.route('/musteriler')
@login_required
def list_musteri():
    if current_user.role == "Finance":
        musteriler = Musteri.query.all()
        return render_template('musteriler_all.html', musteriler=musteriler)
    else:
        musteriler = Musteri.query.all()
        return render_template('musteriler.html', musteriler=musteriler)


@musteri_bp.route('/musteriler/duzenle/<int:musteri_id>', methods=['GET', 'POST'])
@login_required
def edit_musteri(musteri_id):
    musteri = Musteri.query.get(musteri_id)
    old_assistant = User.query.get(musteri.user_id)
    form = ChangeAssistantForm()
    form.assistans.choices = [(str(value), str(key)) for key, value in employees_name.items()]
    if form.validate_on_submit():
        new_assistant = User.query.get(int(form.assistans.data))
        musteri.user_id = int(form.assistans.data)
        old_assistant.kirkbes_bakiye -= musteri.bakiye
        new_assistant.kirkbes_bakiye += musteri.bakiye
        db.session.commit()
        flash(f"{musteri.isim} isimli müşterinin temsilcisi başarıyla değiştirildi.", "success")
        return redirect(url_for('musteri.edit_musteri', musteri_id=musteri.id))
    elif request.method == 'GET':
        form.assistans.data = str(musteri.user_id)
    return render_template('edit_musteri.html', form=form, musteri=musteri)
    return render_template('edit_musteri.html', form=form, musteri=musteri)


@musteri_bp.route('/musteriler/tutar-duzenle/<int:musteri_id>', methods=['GET', 'POST'])
@login_required
def musteri_tutar_duzenleme(musteri_id):
    musteri = Musteri.query.get(musteri_id)
    user = User.query.get(musteri.user_id)
    form = MusteriTutarForm()
    if form.validate_on_submit():
        yeni_tutar = form.tutar.data
        musteri.isim = form.isim.data
        if yeni_tutar != musteri.bakiye:
            if musteri.bakiye > yeni_tutar:
                user.kirkbes_bakiye = user.kirkbes_bakiye - (musteri.bakiye - yeni_tutar)
                musteri.bakiye = yeni_tutar
            if musteri.bakiye < yeni_tutar:
                user.kirkbes_bakiye = user.kirkbes_bakiye + (yeni_tutar - musteri.bakiye)
                musteri.bakiye = yeni_tutar
                musteri.bakiye = yeni_tutar
        else:
            musteri.bakiye = form.tutar.data
        flash(f"{musteri.isim} adlı müşteri için yapılan değişiklikler başarıyla güncellendi.",
              "success")
        db.session.commit()
    return render_template('musteri_tutar_duzenleme.html', form=form, musteri=musteri)

@musteri_bp.route('/musteri/grafik', methods=['GET', 'POST'])
@login_required
def grafik():
    users = User.query.all()
    user = User.query.get(26)
    print(user.id)
    print(user.name)
    return render_template("rapor.html", user=user)

@musteri_bp.route('/musteri/rapor', methods=['GET', 'POST'])
@login_required
def rapor():
    wb = Workbook()
    sheet = wb.active
    musteriler = Musteri.query.all()
    index = 2

    output = excel.make_response(wb)
    for musteri in musteriler:
        print(musteri.isim)
        sheet["A" + str(index)].value = musteri.isim
        sheet["B" + str(index)].value = musteri.telefon
        sheet["C" + str(index)].value = musteri.bakiye
        sheet["D" + str(index)].value = musteri.tahsilat
        sheet["E" + str(index)].value = musteri.guncel_bakiye
        index += 1
        print(index)

    wb.headers["Content-Disposition"] = "attachment; filename=" + \
                                            "sheet.xlsx"
    wb.headers["Content-type"] = \
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    file_name = 'Ekim 2020 Tahsilat Hedefi-raporr.xlsx'
    wb.save(file_name)
    print("burd")
    return send_file(file_name, attachment_filename=file_name, as_attachment=True)

@musteri_bp.route('/ekle/<int:musteri_id>', methods=['GET', 'POST'])
@login_required
def add_odeme(musteri_id):
    musteri = Musteri.query.get(musteri_id)
    user = User.query.get(musteri.user_id)
    form = AddOdemeForm()
    user = User.query.get(26)
    print("lkfdşlksdşf")
    if form.validate_on_submit():
        print("kjkfjdsf")
        tutar = form.tutar.data
        date = form.create_date.data
        odeme = Odeme(tutar=tutar, musteri_id=musteri.id, create_date=date)
        musteri.tahsilat += form.tutar.data
        user.toplam_siparis_tahsilati += form.tutar.data
        db.session.add(odeme)
        db.session.commit()
        flash(f"{musteri.isim} için {tutar} değerinde ödeme oluşturuldu.", "success")
        return redirect(url_for('musteri.list_musteri', musteri_id=musteri.id))
    return render_template('add_odeme.html', musteri=musteri, form=form)




@musteri_bp.route('/musteriler/indirim-ekle/<int:musteri_id>', methods = ['GET','POST'])
@login_required
def indirim_ekle(musteri_id):
    musteri = Musteri.query.get(musteri_id)
    user = User.query.get(musteri.user_id)
    indirim_form = IndirimForm()
    print(musteri.isim)
    if indirim_form.validate_on_submit():
        indirim_tutari = indirim_form.indirim_tutari.data
        user.kirkbes_bakiye -= indirim_tutari
        musteri.bakiye -= indirim_tutari
        db.session.commit()
        indirim = Indirim(indirim_tutari=indirim_tutari, musteri_id=musteri_id)
        db.session.add(indirim)
        db.session.commit()
        return redirect(url_for('musteri.indirim_ekle', musteri_id=musteri.id))
    return render_template('indirim_duzeltme_ekle.html', indirim_form=indirim_form, musteri=musteri, user=user)


@musteri_bp.route('/indirim-list', methods=['GET', 'POST'])
@login_required
def indirim_list():
    indirimler = Indirim.query.all()
    return render_template('indirim_duzeltmeler.html', indirimler=indirimler)


@musteri_bp.route('/odeme/sil/<int:odeme_id>', methods=['GET', 'POST'])
@login_required
def delete_odeme(odeme_id):
    odeme = Odeme.query.get(odeme_id)
    musteri = Musteri.query.get(odeme.musteri_id)
    user = User.query.get(musteri.user_id)
    musteri.tahsilat -= odeme.tutar
    user.kirkbes_tahsilat -= odeme.tutar
    db.session.delete(odeme)
    db.session.commit()
    return redirect(url_for("musteri.list_odeme"))


@musteri_bp.route('/indirim/sil/<int:indirim_id>', methods=['GET', 'POST'])
@login_required
def delete_indirim(indirim_id):
    indirim = Indirim.query.get(indirim_id)
    musteri = Musteri.query.get(indirim.musteri_id)
    user = User.query.get(musteri.user_id)
    user.kirkbes_bakiye += indirim.indirim_tutari
    musteri.bakiye += indirim.indirim_tutari
    db.session.delete(indirim)
    db.session.commit()
    return render_template("indirim_duzeltmeler.html")


@musteri_bp.route('/odeme-listesi')
@login_required
def list_odeme():
    odemeler = Odeme.query.all()
    return render_template('odemeler.html', odemeler=odemeler)
