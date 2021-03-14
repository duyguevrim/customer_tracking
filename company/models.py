from . import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    shortcode = db.Column(db.String, nullable=False)
    kirkbes_bakiye = db.Column(db.Float)
    kirkbes_tahsilat = db.Column(db.Float, default=0.0)
    musteriler = db.relationship('Musteri', backref='user', lazy=True)
    siparisler = db.relationship('Siparis', backref='user', lazy=True)
    tamsilcioranlari = db.relationship('TemsilciOranlari', backref='user', lazy=True)
    toplam_siparis_tutari = db.Column(db.Float, default=0.0)
    toplam_siparis_tahsilati = db.Column(db.Float, default=0)
    tahsilatlar = db.relationship('TumMusteriTahsilatlari', backref='user', lazy=True)
