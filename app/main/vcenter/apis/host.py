# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from app.main.base.apis.auth import basic_auth
from app.common.tool import set_return_val
from app.main.vcenter.control.host import Host

parser = reqparse.RequestParser()
parser.add_argument('platform_id')  # 平台ID
parser.add_argument('host_name')  # host名称
parser.add_argument('esxi_username')  # 用户名
parser.add_argument('esxi_password')  # 密码

parser.add_argument('folder_name')  # 存储文件夹
parser.add_argument('cluster_id')  # 集群ID
parser.add_argument('resource_pool')  # 资源池ID
parser.add_argument('license_id')  # 许可证id
parser.add_argument('fetch_ssl_thumbprint')  # ssl???
parser.add_argument('esxi_ssl_thumbprint')  # ssl???


class ResourceHostManage(Resource):

    @basic_auth.login_required
    def get(self):
        """
         获取 Host 信息
        ---
       tags:
          - vCenter Host
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: query
            name: platform_id
            type: integer
            required: true
       responses:
          200:
            description: vCenter vSwitch 信息
            schema:
              properties:
                ok:
                  type: boolean
                  description: status
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
                      nics:
                        type: list
                        default: ['vemic0',]
                        description: nics
                      num_of_port:
                        type: string
                        default: 128
                        description: numPorts
                      mtu:
                        type: integer
                        default: 1500
                        description: mtu
                      host_name:
                        type: string
                        default: 192.168.12.203
                        description: host_name
                      host_mor_name:
                        type: string
                        default: 'hostsystem-890'
                        description: host_mor_name
                      name:
                        type: string
                        default: mu_test
                        description: name
                      platform_id:
                        type: interger
                        default: 1
                        description: platform_id
                      id:
                        type: string
                        default: 1
                        description: id
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
                  default: 3001
                msg:
                  type: string
                  default: ""
                data:
                  type: array
                  items:
                    properties:
        """
        try:
            args = parser.parse_args()
            if not args['platform_id']:
                raise RuntimeError('Parameter Error!')
            # TODO 功能未做
        except Exception as e:
            return set_return_val(False, {}, str(e), 3001), 400
        return set_return_val(True, [], 'Get Info Success!', 3000)

    @basic_auth.login_required
    def post(self):
        """
          创建Host
        ---
       tags:
          - vCenter Host
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: body
            name: body
            required: true
            schema:
              required:
              - platform_id
              - host_name
              - esxi_username
              - esxi_password
              properties:
                platform_id:
                  type: integer
                  default: 1
                  description: 平台id
                  example: 1
                host_name:
                  type: string
                  default: 192.168.12.203
                  description: 主机名称
                  example: 192.168.12.203
                esxi_username:
                  type: string
                  default: root
                  description: 用户名
                  example: root
                esxi_password:
                  type: string
                  default: kpy2019
                  description: 密码
                  example: kpy2019
                folder_name:
                  type: string
                  default: kpy2019
                  description: 存储文件夹
                  example: kpy2019
                cluster_id:
                  type: integer
                  default: 1
                  description: 集群id
                  example: 1
                esxi_license:
                  type: string
                  default: HV4WC-01087-1ZJ48-031XP-9A843
                  description: 许可证
                  example: HV4WC-01087-1ZJ48-031XP-9A843
                resource_pool:
                  type: integer
                  default: 1
                  description: 资源池
                  example: 1

       responses:
          200:
            description: vCenter Host 创建
            schema:
              properties:
                ok:
                  type: boolean
                  description: status
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                data:
                  type: array
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
                  default: 3002
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
        """
        try:
            args = parser.parse_args()

            if not all([args['platform_id'], args['host_name'],
                        args['esxi_username'], args['esxi_password']]):
                raise ValueError('Parameter Error!')
            if not args['folder_name'] and not args['cluster_id']:
                raise ValueError('Parameter Error!')
            host = Host(args['platform_id'])
            host.add_host(host_name=args['host_name'], esxi_username=args['esxi_username'],
                          esxi_password=args['esxi_password'], folder_name=args['folder_name'],
                          cluster_id=args['cluster_id'],
                          license_id=args['license_id'], resource_pool=args['resource_pool'],
                          fetch_ssl_thumbprint=args['fetch_ssl_thumbprint'],
                          esxi_ssl_thumbprint=args['esxi_ssl_thumbprint'])
        except Exception as e:
            return set_return_val(False, [], str(e), 3001), 400

        return set_return_val(True, [], 'Create Host Success!!!', 3000)

    @basic_auth.login_required
    def delete(self):
        """
         删除Host
        ---
       tags:
          - vCenter vSwitch
       security:
       - basicAuth:
          type: http
          scheme: basic
       parameters:
          - in: query
            name: platform_id
            type: integer
            required: true
            description: '1 -- platform_id'
          - in: path
            name: vswiter_id
            type: integer
            required: true
            description: '8 -- vswiter_id'
       responses:
          200:
            description: vCenter vSwitch 信息
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
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
        """
        try:
            args = parser.parse_args()
            if not all([args['platform_id'], args['host_name']]):
                raise RuntimeError('Parameter Error!!!')
            host = Host(args['platform_id'])
            host.remove_host(args['host_name'])
        except Exception as e:
            return set_return_val(False, [], str(e), 3001), 400

        return set_return_val(True, [], 'Delete Success!!!', 3000)

    # @basic_auth.login_required
    def put(self):  # TODO   license的创建，vCenter同步需要
        args = parser.parse_args()
        host = Host(args['platform_id'])
        host.sync_licenses()
        print 'success.'


