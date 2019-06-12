# -*- coding:utf-8 -*-
from flask import g
from flask_restful import Resource, reqparse
from app import set_return_val
from app.main.vcenter import control
from app.main.base import control as base_control


parser = reqparse.RequestParser()
parser.add_argument('platform_id')
parser.add_argument('pgnum')  # 翻页
parser.add_argument('pgsort')
parser.add_argument('host')
parser.add_argument('vm_name')

parser.add_argument('template_uuid')
parser.add_argument('dc_id')  # 数据中心
parser.add_argument('ds_id')  # 数据存储
parser.add_argument('resource_pool_id')  # 资源中心
parser.add_argument('host_id')  # host


class InstanceTemplateManage(Resource):

    def get(self):
        args = parser.parse_args()
        try:
            if not args['platform_id']:
                raise Exception('Parameter error')
            instance = control.instances.Instance(platform_id=args['platform_id'])

            pgnum = args['pgnum'] if args['pgnum'] else 1

            data, pg = instance.list(host=args['host'], vm_name=args['vm_name'], pgnum=pgnum,
                                     pgsort=args['pgsort'], template=True)
        except Exception as e:
            return set_return_val(False, [], str(e), 2031), 400
        return set_return_val(True, data, 'instance gets success.', 2030, pg), 200

    def post(self):
        args = parser.parse_args()
        data = dict(
            type='instance_template',
            result=True,
            resources_id='',
            event=unicode('模板创建虚拟机'),
            submitter=g.username,
        )
        try:
            if not all([args['platform_id'], args['template_uuid'], args['vm_name'],
                        args['ds_id'], args['dc_id']]):
                raise Exception('Parameter error')
            instance_vm_template = control.instance_template.InstanceVmTemplate(
                platform_id=args['platform_id'], uuid=args['template_uuid'])
            instance_vm_template.template_create_vm(new_vm_name=args['vm_name'], ds_id=args['ds_id'],
                                                    dc_id=args['dc_id'], resource_pool_id=args.get('resource_pool_id'),
                                                    host_id=args.get('host_id'))
        except Exception as e:
            data['result'] = False
            return set_return_val(False, [], str(e), 2031), 400
        finally:
            data['resources_id'] = args.get('template_uuid')
            base_control.event_logs.eventlog_create(**data)
        return set_return_val(True, [], 'Template to virtual machine success.', 2030), 200

    def delete(self, vm_uuid):
        pass
