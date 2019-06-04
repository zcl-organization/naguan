from app.models import VCenterDisk
from app.exts import db


def get_disk_uuid_by_vm_uuid(platform_id, vm_uuid):
    device_info = db.session.query(VCenterDisk.disk_uuid).filter_by(
        platform_id=platform_id).filter_by(vm_uuid=vm_uuid).all()
    return device_info


def disk_create(platform_id, vm_uuid, label, disk_size, disk_file, level, shares, iops, cache, disk_type, sharing,
                disk_mode, disk_uuid):
    new_disk = VCenterDisk()
    new_disk.platform_id = platform_id
    new_disk.vm_uuid = vm_uuid
    new_disk.label = label
    new_disk.disk_size = disk_size
    new_disk.disk_file = unicode(disk_file)
    new_disk.level = level
    new_disk.shares = shares
    new_disk.iops = iops
    new_disk.cache = cache
    new_disk.disk_type = disk_type
    new_disk.sharing = sharing
    new_disk.disk_mode = disk_mode
    new_disk.disk_uuid = disk_uuid

    db.session.add(new_disk)
    db.session.commit()


def disk_update(platform_id, vm_uuid, label, disk_size, disk_file, level, shares, iops, cache, disk_type, sharing,
                disk_mode, disk_uuid):
    disk_info = db.session.query(VCenterDisk).filter_by(platform_id=platform_id).filter_by(
        disk_uuid=disk_uuid).first()
    disk_info.vm_uuid = vm_uuid
    disk_info.disk_size = disk_size
    disk_info.disk_file = unicode(disk_file)
    disk_info.label = label
    disk_info.level = level
    disk_info.shares = shares
    disk_info.iops = iops
    disk_info.cache = cache
    disk_info.disk_type = disk_type
    disk_info.sharing = sharing
    disk_info.disk_mode = disk_mode

    db.session.commit()


def device_delete_by_uuid(platform_id, disk_uuid):
    query = db.session.query(VCenterDisk)
    disk_willdel = query.filter_by(platform_id=platform_id).filter_by(disk_uuid=disk_uuid).first()
    db.session.delete(disk_willdel)
    db.session.commit()


def device_delete_by_vm_uuid(platform_id, vm_uuid):
    query = db.session.query(VCenterDisk)
    disk_middle = query.filter_by(platform_id=platform_id).filter_by(vm_uuid=vm_uuid).delete(
        synchronize_session=False)
    db.session.commit()


def get_disk_by_vm_uuid(platform_id, vm_uuid, pgnum):
    query = db.session.query(VCenterDisk).filter_by(platform_id=platform_id).filter_by(vm_uuid=vm_uuid)

    if pgnum:
        query = query.paginate(page=int(pgnum), per_page=10, error_out=False)

    results = query.items
    pg = {
        'has_next': query.has_next,
        'has_prev': query.has_prev,
        'page': query.page,
        'pages': query.pages,
        'total': query.total,
    }
    return results, pg
    # return db.session.query(VCenterDisk).filter_by(platform_id=platform_id).filter_by(vm_uuid=vm_uuid).all()


def get_disk_by_disk_id(disk_id):
    return db.session.query(VCenterDisk).filter_by(id=disk_id).first()
