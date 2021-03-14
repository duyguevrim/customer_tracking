from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField,FloatField,FileField,TextAreaField,DateField

class SiparisForm(FlaskForm):
    isim = StringField("Sipariş Adı")
    proje_no = StringField("Proje No")
    tutar = FloatField("Tutar")
    son_odeme_tarihi = DateField("Son Ödeme Tarihi")
    siparis_son_durum = StringField("Sipariş Son Durumu")
    isin_alinma_tarihi = DateField("İşin Alındığı Tarih")
    submit = SubmitField("Sipariş Düzenle")
    submit2 = SubmitField("Sipariş Oluştur")
    assistans = SelectField("Temsilci Adı")


class TahsilatForm(FlaskForm):
    tutar = FloatField("Tahsilat Tutarı")
    isim = StringField("Müşteri Adı")
    dekont = FileField("Dekont Yükle")
    aciklama = TextAreaField("Açıklama")
    submit = SubmitField("Tahsilatı Onaya Gönder")
    submit2 = SubmitField("Tahsilat Düzenle")


class TahsilatFormm(FlaskForm):
    tutar = FloatField("Tahsilat Tutarı")
    isim = StringField("Müşteri Adı")
    dekont = FileField("Dekont Yükle")
    crm_kodu = FileField("CRM Müşteri Kodu**")
    aciklama = TextAreaField("Açıklama")
    submit = SubmitField("Tahsilatı Onaya Gönder")
    submit2 = SubmitField("Tahsilat Düzenle")
