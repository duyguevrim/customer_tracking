from company import db
from werkzeug.utils import secure_filename
import os, secrets
from musteri.models import Tahsilat
from musteri.helpers import get_tahsilat_shortcode
from flask_login import current_user


def submit_tahsilat_form(form, musteri_id):
    """
    Tahsilat ekleme formunun valide olması durumunda çalıştırılır. Form verilerine göre veritabanına tahsilat ekler.
    :param form: Tahsilat ekleme formu
    :param musteri_id: Path fonksiyonuna argument olarak verilir.
    :return: VOID
    """
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
