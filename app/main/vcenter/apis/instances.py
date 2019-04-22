# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.main.vcenter.control import instances as instance_manage

parser = reqparse.RequestParser()
parser.add_argument('platform_id')
parser.add_argument('host')
parser.add_argument('vm_name')
parser.add_argument('action')
parser.add_argument('uuid')
ret_status = {
    'ok': True,
    'code': 200,
    'msg': '创建成功',
    'data': {}
}


class InstanceManage(Resource):
    def post(self):
        """
         操作 vm 信息
        ---
        tags:
          - instances
        parameters:
          - in: query
            name: action
            type: string
            description: '操作云主机 start stop suspend remove restart'
          - in: query
            name: vmname
            type: string
            description: 云主机名称
          - in: query
            name: platform_id
            type: string
            description: 云平台id
          - in: query
            name: cpu
            type: string
            description: cpu
          - in: query
            name: memory
            type: string
            description: memory
          - in: query
            name: dc_mor_name
            type: string
            description: datacenter mor name
          - in: query
            name: image_type
            type: string
            description: 镜像类型
          - in: query
            name: arrDiskInputJson
            type: string
            description: '[{"diskInput":"1"}]'
          - in: query
            name: arrIsThinJson
            type: string
            description: '[{"isThin":"true"}]'
          - in: query
            name: arrDiskOcNameJson
            type: string
            description: '[{"diskOcName":"Local_62"}]'
          - in: query
            name: arrNetNameJson
            type: string
            description: '[{"netName":"VM Network"}]'
          - in: query
            name: hostOcName
            type: string
            description: host name
        responses:
          200:
            description: vCenter tree 信息
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                  default: "操作成功"
                data:
                  type: array
                  items:
                    properties:
                      id:
                        type: string
                        default: 1
                      vmtitle:
                        type: string
                      vmMorName:
                        type: string
                      vmOcName:
                        type: string
                      toolsVersion:
                        type: string
                      toolsRun:
                        type: string
                      sys:
                        type: string
                      poolMorName:
                        type: string
                      poolOcName:
                        type: string
                      kvmVVType:
                        type: string
                      isThin:
                        type: string
                      ip:
                        type: string
                      hostMorName:
                        type: string
                      hostOcName:
                        type: string
                      hSpace:
                        type: string
                      dSpace:
                        type: string
                      cpuHzRate:
                        type: string
                      cpuHzOverhead:
                        type: string
                      cpu:
                        type: string
                      State:
                        type: string
                      Network:
                        type: string
                      MemoryRate:
                        type: string
                      Memory:
                        type: string
                      DiskRate:
                        type: string
          400:
            description: 获取失败
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                  default: False
                code:
                  type: "integer"
                  format: "int64"
                  default: 1302
                msg:
                  type: string
                  default: "获取失败"
                data:
                  type: array
                  items:
                    properties:
        """
        args = parser.parse_args()
        print(args)
        try:

            if args['action'] in ['start', 'stop', 'suspend', 'restart']:
                instance_manage.power_action(action=args['action'], platform_id=args['platform_id'], uuid=args['uuid'])
                pass
            else:
                pass
        except Exception as e:
            print('raise ', e)
        return "操作成功"

    # 获取 instance 列表
    def get(self):
        """
         获取 instance 信息
        ---
        tags:
          - instances
        parameters:
          - in: query
            name: mor_name
            type: string
            description: host 名称
          - in: query
            name: platform_id
            type: string
            description: 平台id
          - in: query
            name: vm_name
            type: string
            description: vmOcName
        responses:
          200:
            description: vCenter tree 信息
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
                      id:
                        type: string
                        default: 1
                      vmtitle:
                        type: string
                      vmMorName:
                        type: string
                      vmOcName:
                        type: string
                      toolsVersion:
                        type: string
                      toolsRun:
                        type: string
                      sys:
                        type: string
                      poolMorName:
                        type: string
                      poolOcName:
                        type: string
                      kvmVVType:
                        type: string
                      isThin:
                        type: string
                      ip:
                        type: string
                      hostMorName:
                        type: string
                      hostOcName:
                        type: string
                      hSpace:
                        type: string
                      dSpace:
                        type: string
                      cpuHzRate:
                        type: string
                      cpuHzOverhead:
                        type: string
                      cpu:
                        type: string
                      State:
                        type: string
                      Network:
                        type: string
                      MemoryRate:
                        type: string
                      Memory:
                        type: string
                      DiskRate:
                        type: string
          400:
            description: 获取失败
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                  default: False
                code:
                  type: "integer"
                  format: "int64"
                  default: 1302
                msg:
                  type: string
                  default: "获取失败"
                data:
                  type: array
                  items:
                    properties:
        """
        args = parser.parse_args()
        try:
            data = instance_manage.vm_list_all(platform_id=args['platform_id'], host=args['host'],
                                               vm_name=args['vm_name'])
            ret_status['ok'] = True
            ret_status['code'] = 1111
            ret_status['data'] = data
            ret_status['msg'] = '查询成功'
        except Exception as e:
            ret_status['ok'] = False
            ret_status['code'] = 1111
            ret_status['data'] = {}
            ret_status['msg'] = '查询失败'
            return ret_status, 400
        return ret_status

    def delete(self, id, uuid):
        """
         操作 vm 信息
        ---
        tags:
          - instances
        parameters:
          - in: path
            name: id
            type: string
            description: platform_id
          - in: path
            name: uuid
            type: string
            description: uuid
        responses:
          200:
            description: vCenter tree 信息
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                  default: "删除成功"
                data:
                  type: array
                  items:
                    properties:
          400:
            description: 删除失败
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                  default: False
                code:
                  type: "integer"
                  format: "int64"
                  default: 1302
                msg:
                  type: string
                  default: "删除失败"
                data:
                  type: array
                  items:
                    properties:
        """
        args = parser.parse_args()
        data = instance_manage.vm_delete(platform_id=id,
                                         uuid=uuid)

        return '删除成功'

    def put(self):
        """
         更新 vm 信息
        ---
        tags:
          - instances
        parameters:
          - in: path
            name: id
            type: string
            description: platform_id
          - in: path
            name: vmname
            type: string
            description: vmmorname
          - in: query
            name: arrDiskOcNameJson
            type: string
            description: '[{"diskOcName":"Local_62"}]'
          - in: query
            name: arrNetNameJson
            type: string
            description: '[{"netName":"VM Network"}]'
          - in: query
            name: cpu
            type: string
            description: cpu
          - in: query
            name: memory
            type: string
            description: memory
        responses:
          200:
            description: vCenter tree 信息
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                  default: "操作成功"
                data:
                  type: array
                  items:
                    properties:
                      id:
                        type: string
                        default: 1
                      vmtitle:
                        type: string
                      vmMorName:
                        type: string
                      vmOcName:
                        type: string
                      toolsVersion:
                        type: string
                      toolsRun:
                        type: string
                      sys:
                        type: string
                      poolMorName:
                        type: string
                      poolOcName:
                        type: string
                      kvmVVType:
                        type: string
                      isThin:
                        type: string
                      ip:
                        type: string
                      hostMorName:
                        type: string
                      hostOcName:
                        type: string
                      hSpace:
                        type: string
                      dSpace:
                        type: string
                      cpuHzRate:
                        type: string
                      cpuHzOverhead:
                        type: string
                      cpu:
                        type: string
                      State:
                        type: string
                      Network:
                        type: string
                      MemoryRate:
                        type: string
                      Memory:
                        type: string
                      DiskRate:
                        type: string
          400:
            description: 获取失败
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                  default: False
                code:
                  type: "integer"
                  format: "int64"
                  default: 1302
                msg:
                  type: string
                  default: "获取失败"
                data:
                  type: array
                  items:
                    properties:
        """

        pass
