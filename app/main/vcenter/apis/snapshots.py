# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.vcenter import control

parser = reqparse.RequestParser()

parser.add_argument('platform_id')  # 平台ID
parser.add_argument('snapshot_id')  # 快照ID
parser.add_argument('vm_uuid')  # 虚拟机uuid


class SnapshotManage(Resource):
    def get(self):
        args = parser.parse_args()
        try:
            data = control.snapshots.get_snapshot_list(platform_id=args['platform_id'], snapshot_id=args['snapshot_id'],
                                                       vm_uuid=args['vm_uuid'])
        except Exception as e:
            return set_return_val(False, [], str(e), 1529), 400
        return set_return_val(True, data, 'Snapshot gets success.', 1520)
