# -*- coding:utf-8 -*-
from app.main.vcenter import db
from pyVmomi import vmodl
from pyVmomi import vim

# from app.main.vcenter.control.datastores import sizeof_fmt
from app.main.vcenter.control.utils import get_mor_name


def images_list(image_id, name, ds_name, pgnum):
    images, pg = db.images.image_list(image_id, name, ds_name, pgnum)
    image_list = []
    for image in images:
        data = {
            'id': image.id,
            'iso_name': image.iso_name,
            'path': image.path,
            'ds_name': image.ds_name,
            'ds_mor_name': image.ds_mor_name,
            'size': image.size,
            'file_type': image.file_type,
            'last_change_time': image.last_change_time,
        }
        image_list.append(data)
    return image_list, pg


def match_files(ds, pattern):
    search = vim.HostDatastoreBrowserSearchSpec()
    search.matchPattern = pattern
    n = '[' + ds.summary.name + ']'
    search_ds = ds.browser.SearchDatastoreSubFolders_Task(n, search)
    while search_ds.info.state != "success":
        pass
    results = search_ds.info.result
    # print results
    for rs in results:
        # print rs
        dsfolder = rs.folderPath
        options = {}
        for f in rs.file:
            image_name = f.path
            path = dsfolder + image_name
            try:
                size = f.fileSize
                last_change_time = f.modification
            except Exception as e:
                size = '0kb'
                last_change_time = '0kb'
            options = {
                'image_name': image_name,
                'path': path,
                'size': size,
                'last_change_time': last_change_time,
            }
            yield options


def sync_image(platform, ds):
    image_list_match = match_files(ds, '*.iso')
    image_lists = db.images.get_image_name_by_platform_id(platform['id'], ds.name)

    # print(image_lists)
    image_list_db = []
    for image in image_lists:
        image_list_db.append(image.image_name)

    for image in image_list_match:

        if image['image_name'] in image_list_db:

            image_list_db.remove(image['image_name'])
            # print(image_list_db)
            db.images.update_image(platform_id=platform['id'], image_name=image['image_name'], path=image['path'],
                                   ds_name=ds.name, ds_mor_name=get_mor_name(ds), size=image['size'],
                                   last_change_time=image['last_change_time'])
        else:
            db.images.create_image(platform_id=platform['id'], image_name=image['image_name'], path=image['path'],
                                   ds_name=ds.name, ds_mor_name=get_mor_name(ds), size=image['size'],
                                   last_change_time=image['last_change_time'])
    # 删除为未在数据库中的image
    if image_list_db:
        for image_name in image_list_db:
            db.images.delete_image_by_image_name(image_name)
