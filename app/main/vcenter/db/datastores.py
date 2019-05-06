from app.exts import db
from app.models import VCenterDataStore


def get_datastore_by_platform_id(platform_id):
    return db.session.query(VCenterDataStore).filter_by(platform_id=platform_id).all()


def get_datastore_ds_name_by_platform_id(platform_id,dc_name):
    data_stores = db.session.query(VCenterDataStore).filter_by(platform_id=platform_id).filter_by(dc_name=dc_name).all()
    data_store_list = []
    for data_store in data_stores:
        data_store_list.append(data_store.ds_name)
    return data_store_list


def create_datastore(platform_id, ds_name, ds_mor_name, dc_name, dc_mor_name, capacity, used_capacity, free_capacity,
                     type, version, uuid, ssd, local, host):
    new_datastore = VCenterDataStore()
    new_datastore.platform_id = platform_id
    new_datastore.ds_name = ds_name
    new_datastore.ds_mor_name = ds_mor_name
    new_datastore.dc_name = dc_name
    new_datastore.dc_mor_name = dc_mor_name
    new_datastore.capacity = capacity
    new_datastore.used_capacity = used_capacity
    new_datastore.free_capacity = free_capacity
    new_datastore.type = type
    new_datastore.version = version
    new_datastore.uuid = uuid
    new_datastore.ssd = ssd
    new_datastore.local = local
    new_datastore.host = host
    db.session.add(new_datastore)
    db.session.commit()


def update_datastore(platform_id, ds_name, ds_mor_name, dc_name, dc_mor_name, capacity, used_capacity, free_capacity,
                     type, version, uuid, ssd, local, host):
    datastore = db.session.query(VCenterDataStore).filter_by(ds_name=ds_name).first()
    datastore.platform_id = platform_id
    # new_datastore.ds_name = ds_name
    datastore.ds_mor_name = ds_mor_name
    datastore.dc_name = dc_name
    datastore.dc_mor_name = dc_mor_name
    datastore.capacity = capacity
    datastore.used_capacity = used_capacity
    datastore.free_capacity = free_capacity
    datastore.type = type
    datastore.version = version
    datastore.uuid = uuid
    datastore.ssd = ssd
    datastore.local = local
    datastore.host = host
    db.session.add(datastore)
    db.session.commit()


def delete_datastore_by_ds_name(ds_name):
    data_store = db.session.query(VCenterDataStore).filter_by(ds_name=ds_name).first()
    if data_store:
        db.session.delete(data_store)
        db.session.commit()
