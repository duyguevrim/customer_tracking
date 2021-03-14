from company.models import User
from musteri.models import Odeme, Musteri, Tahsilat
from company import db
import datetime
from sqlalchemy import func
from flask_login import current_user


def get_users_payments_daily():
    """
    Bütün kullanıcılara ait günlük tahsilat verilerini döndürür.
    Döndürülen veri dict tipinde ve key değeri kullanıcı id'sidir.
    Value tarafı ise 0. elemanda tarih listesini, 1. elemanda toplam tahsilat tutarlarını içeren bir listedir.
    :return:
    """
    users = User.query.all()
    graph_dict = {}
    for user in users:
        custids = [musteri.id for musteri in user.musteriler]
        veriler = db.session.query(Odeme.create_date, func.sum(Odeme.tutar)).filter(
            Odeme.musteri_id.in_(custids)).filter(Odeme.create_date <= datetime.date.today()).order_by(
            Odeme.create_date).group_by(Odeme.create_date).all()
        graph_dict[user.id] = [[veri[0].strftime('%d/%m/%Y') for veri in veriler], [veri[1] for veri in veriler]]
    return graph_dict


def get_total_graph():
    """
    Her gün yapılan toplam tahsilat tutarını döndürür.
    Gelen veri 0. elemanda tarih listesi, 1. elemanda tutar listesi içeren bir listedir.
    :return:
    """
    total_graph = db.session.query(Odeme.create_date, func.sum(Odeme.tutar)).filter(
        Odeme.create_date <= datetime.date.today()).order_by(Odeme.create_date).group_by(Odeme.create_date).all()
    total_graph = [[veri[0].strftime('%d/%m/%Y') for veri in total_graph], [veri[1] for veri in total_graph]]
    return total_graph


def get_current_user_graph():
    """
    Bir kişiye ait günlük tahsilat verilerini döndürür.
    :return:
    """
    user = User.query.get(current_user.id)
    sample = [musteri.id for musteri in user.musteriler]
    veriler = db.session.query(Odeme.create_date, func.sum(Odeme.tutar)).filter(
        Odeme.musteri_id.in_(sample)).filter(Odeme.create_date <= datetime.date.today()).order_by(
        Odeme.create_date).group_by(Odeme.create_date).all()
    return veriler
