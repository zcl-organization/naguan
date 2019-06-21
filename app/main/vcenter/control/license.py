from app.main.vcenter import db
from app.main.vcenter.control.utils import get_connect


def find_license(platform_id):
    licenses = db.license.find_license(platform_id)
    license_list = []
    for license in licenses:
        data = dict(
            platform_id=license.platform_id,
            name=license.name,
            licenseKey=license.licenseKey,
            editionKey=license.editionKey,
            used=license.used,
            total=license.total
        )
        license_list.append(data)
    return license_list


def create_licenses(platform_id):
    si, content, platform = get_connect(platform_id)
    licenses = si.content.licenseManager.licenses
    for license in licenses:
        data = dict(
            platform_id=platform_id,
            name=license.name,
            license_key=license.licenseKey,
            edition_key=license.editionKey,
            used=license.used,
            total=license.total,
        )
        db.license.create_license(**data)
