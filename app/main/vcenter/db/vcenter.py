# -*- coding:utf-8 -*-
from app.models import VCenterTree
from app.exts import db


# 添加vcenter tree 信息
def vcenter_tree_create(tree_type, platform_id, name, dc_host_folder_mor_name=None, dc_mor_name=None, dc_oc_name=None,
                        dc_vm_folder_mor_name=None, mor_name=None, cluster_mor_name=None, cluster_oc_name=None):
    # print(options)
    new_vcenter = VCenterTree()
    new_vcenter.type = tree_type
    new_vcenter.platform_id = platform_id
    new_vcenter.dc_host_folder_mor_name = dc_host_folder_mor_name
    new_vcenter.dc_mor_name = dc_mor_name
    new_vcenter.dc_oc_name = dc_oc_name
    new_vcenter.dc_vm_folder_mor_name = dc_vm_folder_mor_name
    new_vcenter.mor_name = mor_name
    new_vcenter.name = name
    new_vcenter.cluster_mor_name = cluster_mor_name
    new_vcenter.cluster_oc_name = cluster_oc_name

    # print(new_vcenter)
    db.session.add(new_vcenter)
    db.session.commit()
    # pass


def vcenter_tree_get_by_platform(platform_id, platform_name, tree_type):
    query = db.session.query(VCenterTree)
    query = query.filter(VCenterTree.platform_id == platform_id).filter(VCenterTree.type == tree_type).filter(
        VCenterTree.name == platform_name).filter(VCenterTree.dc_mor_name.is_(None))
    return query.first()


def vcenter_tree_get_by_dc(platform_id, dc_mor_name, tree_type):
    query = db.session.query(VCenterTree)
    query = query.filter(VCenterTree.platform_id == platform_id).filter(VCenterTree.type == tree_type).filter(
        VCenterTree.dc_mor_name == dc_mor_name)
    return query.first()


def vcenter_tree_get_by_cluster(platform_id, cluster_mor_name, tree_type):
    query = db.session.query(VCenterTree)
    query = query.filter(VCenterTree.platform_id == platform_id).filter(VCenterTree.type == tree_type).filter(
        VCenterTree.cluster_mor_name == cluster_mor_name)
    return query.first()


def vcenter_tree_get_by_cluster(platform_id, host_mor_name, tree_type):
    query = db.session.query(VCenterTree)
    query = query.filter(VCenterTree.platform_id == platform_id).filter(VCenterTree.type == tree_type).filter(
        VCenterTree.mor_name == host_mor_name)
    return query.first()


# 更新vcenter tree信息
def vcenter_tree_update(tree_type, platform_id, mor_name, name=None, dc_host_folder_mor_name=None,
                        dc_mor_name=None, dc_oc_name=None, dc_vm_folder_mor_name=None, cluster_mor_name=None,
                        cluster_oc_name=None):
    if tree_type == 1:
        vcenter_info = db.session.query(VCenterTree).filter_by(platform_id=platform_id).filter_by(type=tree_type).first()
    else:
        vcenter_info = db.session.query(VCenterTree).filter_by(platform_id=platform_id).filter_by(
            type=tree_type).filter_by(mor_name=mor_name).first()
    if name:
        vcenter_info.name = name
    if dc_host_folder_mor_name:
        vcenter_info.dc_host_folder_mor_name = dc_host_folder_mor_name
    if dc_mor_name:
        vcenter_info.dc_mor_name = dc_mor_name
    if dc_oc_name:
        vcenter_info.dc_oc_name = dc_oc_name
    if dc_vm_folder_mor_name:
        vcenter_info.dc_vm_folder_mor_name = dc_vm_folder_mor_name
    if cluster_mor_name:
        vcenter_info.cluster_mor_name = cluster_mor_name
    if cluster_oc_name:
        vcenter_info.cluster_oc_name = cluster_oc_name
    db.session.commit()


# 根据获取所有
def vcenter_tree_get_all_id(platform_id):
    result = db.session.query(VCenterTree.id).filter_by(platform_id=platform_id).all()
    return result


# 根据id删除tree信息
def vcenter_tree_delete_by_id(id):
    query = db.session.query(VCenterTree)
    tree_willdel = query.filter_by(id=id).first()
    db.session.delete(tree_willdel)
    db.session.commit()
    return True


def vcenter_tree_list_by_platform_id(platform_id):
    result = db.session.query(VCenterTree).filter_by(platform_id=platform_id).all()
    return result


def vcenter_tree_by_id(id):
    result = db.session.query(VCenterTree).filter_by(id=id).first()
    return result
