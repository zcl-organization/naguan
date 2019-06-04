# -*- coding:utf-8 -*-
from app.exts import db
from app.models import VCenterImage


def get_image_path(image_id):
    query = db.session.query(VCenterImage).get(image_id)
    if query:
        path = query.path
        return path


def image_list(image_id, name, ds_name, pgnum):
    query = db.session.query(VCenterImage)

    if image_id:
        query = query.filter_by(id=image_id)
    if name:
        query = query.filter_by(iso_name=name)
    if ds_name:
        query = query.filter_by(ds_name=ds_name)
    if pgnum:  # 默认获取分页获取所有日志
        query = query.paginate(page=int(pgnum), per_page=10, error_out=False)

    try:
        results = query.items

        pg = {
            'has_next': query.has_next,
            'has_prev': query.has_prev,
            'page': query.page,
            'pages': query.pages,
            'total': query.total,
        }
        return results, pg
    except Exception as e:
        raise Exception('Database operation exception')


def get_image_by_image_id(image_id):
    return db.session.query(VCenterImage).filter_by(id=image_id).first()


def get_image_by_platform_id(platform_id):
    images = db.session.query(VCenterImage).filter_by(platform_id=platform_id).all()
    return images


def get_image_name_by_platform_id(platform_id, ds_name):
    return db.session.query(VCenterImage.iso_name.label('image_name')).filter_by(ds_name=ds_name).filter_by(
        platform_id=platform_id).all()


def delete_image_by_image_name(image_name):
    image = db.session.query(VCenterImage).filter_by(iso_name=image_name).first()
    if image:
        db.session.delete(image)
        db.session.commit()


def create_image(platform_id, image_name, path, ds_name, ds_mor_name, size, last_change_time):
    new_image = VCenterImage()
    new_image.platform_id = platform_id
    new_image.iso_name = image_name
    new_image.path = path
    new_image.ds_name = ds_name
    new_image.ds_mor_name = ds_mor_name
    new_image.size = size
    new_image.last_change_time = last_change_time
    db.session.add(new_image)
    db.session.commit()


def update_image(platform_id, image_name, path, ds_name, ds_mor_name, size, last_change_time):
    image = db.session.query(VCenterImage).filter_by(iso_name=image_name).first()

    image.platform_id = platform_id
    image.iso_name = image_name
    image.path = path
    image.ds_name = ds_name
    image.ds_mor_name = ds_mor_name
    image.size = size
    image.last_change_time = last_change_time
    db.session.add(image)
    db.session.commit()
