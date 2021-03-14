from . import app, bcrypt, db
from .forms import LoginForm, ChangeAssistantForm
from .models import User
from .globals import employees_name
from flask import render_template, redirect, url_for
from musteri.models import Tahsilat, Musteri, Odeme
from musteri.forms import AddCustomerFom
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import func
import datetime
from services.users import *
from guncel_modul.models import Siparis
from sqlalchemy import extract
from datetime import datetime
from sqlalchemy import extract, or_, and_


@app.template_filter('assistantname')
def assistantname(user_id):
    return list(employees_name.keys())[list(employees_name.values()).index(user_id)]


@app.template_filter('customername')
def customername(customer_id):
    musteri = Musteri.query.get(customer_id)
    return musteri.isim


@app.template_filter('siparisname')
def siparisname(siparis_id):
    siparis = Siparis.query.get(siparis_id)
    return siparis.musteri_adi


@app.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():

    if current_user.role == "Finance":
        bekleyenler = Tahsilat.query.filter_by(durum="Onay Bekliyor").all()
        onaylananlar = Tahsilat.query.filter_by(durum="Onaylandı").all()
        musteriler = Musteri.query.all()
        return render_template('dashfinans.html', bekleyenler=bekleyenler, onaylananlar=onaylananlar,
                               musteriler=musteriler)
    elif current_user.role == "Manager":
        son_odeme_ay = datetime.today().month

        siparisler = Siparis.query.filter(extract('month', Siparis.son_odeme_tarihi) == son_odeme_ay).filter_by(
            onceki_aydan_kalan=0).all()
        return render_template("siparis_list.html", siparisler=siparisler)
    elif current_user.role == "Employee":
        son_odeme_ay = datetime.today().month
        son_odeme_yil = datetime.today().year
        son_odeme_ay = datetime.today().month
        siparisler = Siparis.query.filter(and_(extract('month', Siparis.son_odeme_tarihi) == son_odeme_ay),
                                          extract('year', Siparis.son_odeme_tarihi) == son_odeme_yil).all()

        return render_template("siparis_list.html", siparisler=siparisler)
    # elif current_user.role == "Manager":
    #     total_graph = get_total_graph()
    #     users = User.query.all()
    #     graph_dict = get_users_payments_daily()
    #     musteriler = Musteri.query.all()
    #     form = AddCustomerFom()
    #     form.temsilci.choices = [(str(value), str(key)) for key, value in employees_name.items()]
    #     if form.validate_on_submit():
    #         musteri = Musteri(isim=form.isim.data, telefon=form.telefon.data, bakiye=form.bakiye.data,
    #                           parasut_no=form.parasut_no.data, parasut_odeme_linki=form.parasut_odeme_linki.data,
    #                           user_id=form.temsilci.data)
    #         db.session.add(musteri)
    #         db.session.commit()
    #     return render_template('dashman.html', musteriler=musteriler, users=users, form=form, graph_dict=graph_dict, total_graph=total_graph)
    # elif current_user.role == "Admin":
    #     total_graph = get_total_graph()
    #     users = User.query.all()
    #     graph_dict = get_users_payments_daily()
    #     musteriler = Musteri.query.all()
    #     form = AddCustomerFom()
    #     form.temsilci.choices = [(str(value), str(key)) for key, value in employees_name.items()]
    #     if form.validate_on_submit():
    #         musteri = Musteri(isim=form.isim.data, telefon=form.telefon.data, bakiye=form.bakiye.data,
    #                           parasut_no=form.parasut_no.data, parasut_odeme_linki=form.parasut_odeme_linki.data,
    #                           user_id=form.temsilci.data)
    #         db.session.add(musteri)
    #         db.session.commit()
    #     return render_template('dashadmin.html', musteriler=musteriler, users=users, form=form, graph_dict=graph_dict, total_graph=total_graph)


@app.route('/giris', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/cikis')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




