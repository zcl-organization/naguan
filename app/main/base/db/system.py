from app import SystemConfig
from app.exts import db


def system_list():
    systems = SystemConfig.query.all()
    return systems


def system_save_db(system):
    db.session.add(system)
    db.session.commit()


def system_get(sysconfig):
    all_config = {
        'platform_name': sysconfig.platform_name,
        'version_information': sysconfig.version_information,
        'logo': sysconfig.logo,
        'copyright': sysconfig.copyright,
        'user_authentication_mode': sysconfig.user_authentication_mode,
        'debug': sysconfig.debug,
        'store_log': sysconfig.store_log
    }
    return all_config




