from company import db
from company.models import User
from datetime import datetime


class Siparis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proje_no = db.Column(db.String)
    musteri_adi = db.Column(db.String, nullable=False)
    siparis_tutari = db.Column(db.Float, nullable=False)
    son_odeme_tarihi = db.Column(db.Date)
    isin_alinma_tarihi = db.Column(db.Date)
    tahsilat = db.Column(db.Float, default=0)
    onceki_aydan_kalan = db.Column(db.Integer, default=0)
    siparis_son_durum = db.Column(db.String)
    evrak_cikis_tarihi = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tahsilatlar = db.relationship('Guncel_Tahsilat', backref='siparis', lazy=True)
    odeme = db.relationship('GuncelOdeme', backref='sipariss', lazy=True)


class Guncel_Tahsilat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutar = db.Column(db.Float)
    tahsilat_tarihi = db.Column(db.Date)
    aciklama = db.Column(db.String)
    dekont = db.Column(db.String, nullable=True)
    siparis_id = db.Column(db.Integer, db.ForeignKey('siparis.id'),nullable=False)
    durum = db.Column(db.String, nullable=False, default="Onay Bekliyor")


class GuncelOdeme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutar = db.Column(db.Float, nullable=False)
    create_date = db.Column(db.Date, nullable=False)
    siparis_id = db.Column(db.Integer, db.ForeignKey('siparis.id'), nullable=False)


class TemsilciOranlari(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    siparis_date = db.Column(db.Date, nullable=False)
    toplam_siparis_miktari = db.Column(db.Integer, default=0.0)
    toplam_siparis_tahsilati = db.Column(db.Integer, default=0.0)


class TumMusteriTahsilatlari(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    musteri_adi_crm = db.Column(db.String)
    crm_kodu = db.Column(db.String)
    tahsilat_tutari = db.Column(db.Float)
    durum = db.Column(db.String, nullable=False, default="Onay Bekliyor")
    tahsilat_tarihi = db.Column(db.Date)
    aciklama = db.Column(db.String)
    dekont = db.Column(db.String, nullable=True)
    create_date = db.Column(db.Date, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
