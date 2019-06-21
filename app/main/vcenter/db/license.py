from app.exts import db
from app.models import Licenses


def find_license(platform_id):
    return db.session.query(Licenses).filter_by(platform_id=platform_id).all()


def create_license(platform_id, name, license_key, edition_key, used, total):
    license = Licenses()
    license.platform_id = platform_id
    license.name = name
    license.licenseKey = license_key
    license.editionKey = edition_key
    license.used = used
    license.total = total
    db.session.add(license)
    db.session.commit()


def get_license_by_id(license_id):
    return db.session.query(Licenses).get(license_id)
