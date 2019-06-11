from app.main.vcenter import db
from app.main.vcenter.control.instances import Instance


class InstanceVmTemplate:

    def __init__(self, platform_id, uuid):
        self.instance = Instance(platform_id=platform_id, uuid=uuid)
        self.vm = self.instance.vm

    def template_create_vm(new_vm_name, ds_id, dc_id, resourcepool=None):
        # # RelocateSpec
        # relospec = vim.vm.RelocateSpec()
        # relospec.datastore = datastore
        # relospec.pool = resource_pool
        #
        # # ConfigSpec
        # configSpec = vim.vm.ConfigSpec()
        # configSpec.annotation = "This is the annotation for this VM"
        #
        # # CloneSpec
        # clonespec = vim.vm.CloneSpec()
        # clonespec.location = relospec
        # clonespec.powerOn = power_on
        # clonespec.config = configSpec
        #
        # print ("cloning VM...")
        # task = template.Clone(folder=destfolder, name=vm_name, spec=clonespec)
        # wait_for_task(task)
        pass


