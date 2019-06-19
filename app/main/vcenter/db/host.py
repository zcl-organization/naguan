from app.exts import db
from app.models import Licenses
from app.models import VCenterHost


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


def add_host(name, mor_mame, port, power_state, connection_state, maintenance_mode, platform_id,
             uuid, cpu, ram, used_ram, rom, used_rom, cpu_mhz, cpu_model, version, image, build,
             full_name, boot_time, uptime):

    new_host = VCenterHost()
    new_host.name = name
    new_host.mor_name = mor_mame
    new_host.port = port
    new_host.power_state = power_state
    new_host.connection_state = connection_state
    new_host.maintenance_mode = maintenance_mode
    new_host.platform_id = platform_id
    new_host.uuid = uuid
    new_host.cpu = cpu
    new_host.ram = ram
    new_host.used_ram = used_ram
    new_host.rom = rom
    new_host.used_rom = used_rom
    new_host.cpu_mhz = cpu_mhz
    new_host.cpu_model = cpu_model
    new_host.version = version
    new_host.image = image
    new_host.build = build
    new_host.full_name = full_name
    new_host.boot_time = boot_time
    new_host.uptime = uptime
    db.session.add(new_host)
    db.session.commit()


def get_host(name):
    return db.session.query(VCenterHost).filter_by(name=name).first()


def del_host(name):
    host = db.session.query(VCenterHost).filter_by(name=name).first()
    db.session.delete(host)
    db.session.commit()



