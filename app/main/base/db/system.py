from app import SystemConfig
from app.exts import db


def system_config_list():
    # systems = SystemConfig.query.all()
    systems = db.session.query(SystemConfig).first()
    return systems


def system_config_update(platform_name, version_information, copyright, user_authentication_mode, debug):
    try:
        system_config = db.session.query(SystemConfig).first()
        if platform_name:
            system_config.platform_name = unicode(platform_name)
        if version_information:
            system_config.version_information = unicode(version_information)
        if copyright:
            system_config.copyright = unicode(copyright)
        if user_authentication_mode:
            system_config.user_authentication_mode = user_authentication_mode
        if debug == 1:
            system_config.debug = True
        elif debug == 2:
            system_config.debug = False
        db.session.commit()
    except Exception as e:
        raise Exception('Database operation exception')


def system_config_create(platform_name, version_information, copyright, user_authentication_mode, debug):
    try:
        system_config = SystemConfig()
        system_config.platform_name = unicode(platform_name)
        system_config.version_information = version_information
        system_config.copyright = copyright
        system_config.user_authentication_mode = user_authentication_mode

        if debug == 1:
            system_config.debug = True
        elif debug == 2:
            system_config.debug = False
        db.session.add(system_config)
        db.session.commit()
    except Exception as e:
        raise Exception('Database operation exception')


def system_config_update_logo(log_path):
    try:
        system_config = db.session.query(SystemConfig).first()
        system_config.logo = log_path
        db.session.commit()
    except Exception as e:
        raise Exception('Database operation exception')
