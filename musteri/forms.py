from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, SelectField, FloatField, TextAreaField, DateField


class AddTahsilatForm(FlaskForm):
    tutar = FloatField("Tahsilat Tutarı")
    musteri = StringField("Müşteri Adı")
    dekont = FileField("Dekont Yükle")
    aciklama = TextAreaField("Açıklama")
    submit = SubmitField("Tahsilatı Onaya Gönder")
    submit2 = SubmitField("Tahsilatı Düzenle")


class IndirimForm(FlaskForm):
    indirim_tutari = FloatField("Yapılacak İndirim Tutarı")
    submit = SubmitField("İndirim Ekle")
    musteri = StringField("Müşteri Adı")
    bakiye = FloatField("Güncel Bakiye")
    devreden_bakiye = FloatField("Devreden Bakiye")


class AddCustomerFom(FlaskForm):
    isim = StringField("Müşteri Adı")
    telefon = StringField("Telefon")
    bakiye = FloatField("Bakiye")
    tutar = FloatField("Tutar")
    parasut_no = StringField("Paraşüt No")
    parasut_odeme_linki = StringField("Paraşüt Ödeme Linki")
    temsilci = SelectField("Temsilci Adı")
    submit = SubmitField("Müşteri Ekle")


class MusteriTutarForm(FlaskForm):
    isim = StringField("Müşteri Adı")
    tutar = FloatField("Tutar")
    submit2 = SubmitField("Müşteri Düzenle")
    bakiye = FloatField("Bakiye")


class AddOdemeForm(FlaskForm):
    tutar = FloatField("Ödeme Tutarı")
    create_date = DateField("Ödeme Tarihi", format='%d/%m/%Y')
    musteri = StringField("Müşteri Adı")
    submit = SubmitField("Ödeme Ekle")
    submit2 = SubmitField("Ödeme Düzenle")
