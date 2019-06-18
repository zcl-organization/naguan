from app.exts import db
from app.models import Licenses


def create_license(name, license_key, edition_key, used, total):
    license = Licenses()
    license.name = name
    license.licenseKey = license_key
    license.editionKey = edition_key
    license.used = used
    license.total = total
    db.session.add(license)
    db.session.commit()


def get_license_by_id(license_id):
    return db.session.query(Licenses).get(license_id)



