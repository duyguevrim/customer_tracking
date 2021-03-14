from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField


class LoginForm(FlaskForm):
    email = StringField("E-Posta Adresiniz")
    password = PasswordField("Parolanız")
    submit = SubmitField("Giriş Yap")


class ChangeAssistantForm(FlaskForm):
    assistans = SelectField("Görevli Satış Temsilcisi")
    submit = SubmitField("Temsilciyi Değiştir")
