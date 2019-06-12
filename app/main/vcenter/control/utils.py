# -*- coding:utf-8 -*-
from pyVmomi import vmodl
from pyVmomi import vim
from pyVim import connect
from app.main.base.control import cloud_platform
import atexit


def get_mor_name(obj):
    obj_info = '%s' % obj
    obj_mor = obj_info.replace("'", "").split(':', 1)[1]
    return obj_mor


def wait_for_tasks(s, tasks):
    """Given the service instance si and tasks, it returns after all the
   tasks are complete
   """
    property_collector = s.content.propertyCollector
    task_list = [str(task) for task in tasks]
    # Create filter
    obj_specs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task)
                 for task in tasks]
    property_spec = vmodl.query.PropertyCollector.PropertySpec(type=vim.Task,
                                                               pathSet=[],
                                                               all=True)
    filter_spec = vmodl.query.PropertyCollector.FilterSpec()
    filter_spec.objectSet = obj_specs
    filter_spec.propSet = [property_spec]
    pcfilter = property_collector.CreateFilter(filter_spec, True)
    try:
        version, state = None, None
        # Loop looking for updates till the state moves to a completed state.
        while len(task_list):
            update = property_collector.WaitForUpdates(version)
            for filter_set in update.filterSet:
                for obj_set in filter_set.objectSet:
                    task = obj_set.obj
                    for change in obj_set.changeSet:
                        if change.name == 'info':
                            state = change.val.state
                        elif change.name == 'info.state':
                            state = change.val
                        else:
                            continue

                        if not str(task) in task_list:
                            continue

                        if state == vim.TaskInfo.State.success:
                            # Remove task from taskList
                            task_list.remove(str(task))
                        elif state == vim.TaskInfo.State.error:
                            raise task.info.error
            # Move to next version
            version = update.version

    finally:
        if pcfilter:
            pcfilter.Destroy()
    # return task.info.result


def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def get_obj_by_mor_name(content, vimtype, mor_name):
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        c_mor_name = get_mor_name(c)
        if c_mor_name == mor_name:
            obj = c
            break
    return obj


def connect_server(host, user, password, port, ssl=True):
    # print time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time()))
    if ssl:
        service_instance = connect.SmartConnectNoSSL(host=host,
                                                     user=user,
                                                     pwd=password,
                                                     port=int(port))
    else:
        service_instance = connect.SmartConnect(host=host,
                                                user=user,
                                                pwd=password,
                                                port=int(port))
    return service_instance


def get_connect(platform_id):
    options = {
        'id': platform_id
    }
    platforms = cloud_platform.platform_list(id=platform_id)
    if platforms:
        platform = platforms[0]
        s = connect_server(platform['ip'], platform['name'], platform['password'], platform['port'])
        atexit.register(connect.Disconnect, s)
    else:
        raise Exception('unable to find platform')
    content = s.RetrieveContent()
    return s, content, platforms[0]


def validate_input(name):
    return str(name).replace("@", " ")
