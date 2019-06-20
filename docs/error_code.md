# 错误码定义

## login (错误码范围:1000~1009)

#### 登录 (1000~1009)

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1000 | 登录成功 | Login Success |
| 1001 | 登录失败 | Login Failed |
| 1002 | 参数错误 | Login parameter error |
| 1003 | 无对应用户 | No corresponding user |
| 1004 | 密码错误 | Password error |

## cloudplatform (错误码范围: 1010~1059)

#### 获取云平台信息 (1010~1019)

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1010 | 获取平台信息成功 | Failure to control access to platform information |
| 1011 | 获取平台信息失败 | Successful Control Acquisition Platform Information |

#### 新增云平台（1020～1029）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1020 | 添加新平台成功 | Successful addition of new platform |
| 1021 | 添加新平台失败 | Failure to add a new platform |
| 1022 | 添加新平台参数错误 | Errors in adding new platform parameters |
| 1023 | 平台已存在 | Platform already exists |

#### 更新云平台 （1030～1039）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1030 | 更新平台信息成功 | Update Platform Information Successfully |
| 1031 | 更新平台信息失败 | Failure to update platform information |
| 1032 | 无对应待更新平台数据 | No corresponding platform data to be updated |

#### 删除云平台 （1040～1049）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1040 | 删除云平台成功 | Delete Cloud Platform Successfully |
| 1041 | 删除云平台失败 | Failed to delete cloud platform |
| 1042 | 无对应待删除平台数据 | No corresponding platform data to be deleted |

## cloudplatformtype （错误码范围1060～1190）

#### 获取云平台类型信息（1060～1069）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1060 | 获取云平台类型信息成功 | Successful Access to Cloud Platform Type Information |
| 1061 | 获取云平台类型信息失败 | Failed to obtain cloud platform type information |

#### 创建云平台类型信息（1070～1079）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1070 | 创建云平台类型信息成功 | Successful Creation of Cloud Platform Type Information |
| 1071 | 创建云平台类型信息失败 | Failure to create cloud platform type information |
| 1072 | 创建云平台类型参数错误 | Error in creating cloud platform type parameters |
| 1073 | 创建云平台类型已存在 | Creating cloud platform types already exists |

#### 更新云平台类型信息（1080～1089）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1080 | 更新云平台类型信息成功 | Successful updating of cloud platform type information |
| 1081 | 更新云平台类型信息失败 | Failed to update cloud platform type information |
| 1082 | 更新云平台类型参数错误 | Error updating cloud platform type parameters |
| 1083 | 无对应平台类型待更新数据 | Data to be updated without corresponding platform type |

#### 删除云平台类型信息（1090～1099）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1090 | 删除云平台类型信息成功 | Successful deletion of cloud platform type information |
| 1091 | 删除云平台类型信息失败 | Failed to delete cloud platform type information |
| 1092  | 无对应平台类型待删除数据 | Data to be deleted without corresponding platform type |

## User （错误码范围1110～1209）

#### 获取用户信息 （1110～1129）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1110 | 获取用户信息成功 | Successful access to user information |
| 1111 | 获取用户信息失败 | Failed to obtain user information |

#### 新增用户信息  （1130～1149）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1130 | 新增用户信息成功 | Successful Addition of User Information |
| 1131 | 新增用户信息失败 | Failure to add user information |
| 1132 | 用户信息参数错误 | Error in User Information Parameters |
| 1133 | 用户已存在 | User already exists |

#### 修改用户信息  （1150～1169）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1150 | 修改用户信息成功 | Successful modification of user information |
| 1151 | 修改用户信息失败 | Failed to modify user information |
| 1152 | 修改用户参数信息错误 | Error modifying user parameter information |
| 1153 | 不存在该用户 | This user does not exist |

#### 删除用户信息  （1170～1189）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1170 | 删除用户信息成功 | Successful deletion of user information |
| 1171 | 删除用户信息失败 | Failed to delete user information |
| 1172 | 不存在该用户 | This user does not exist |

## Role  （错误码范围1210～1309）

#### 获取角色信息 （1210～1229）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1210 | 获取角色信息成功 | Acquiring Role Information Successfully |
| 1211 | 获取角色信息失败 | Failure to obtain role information |

#### 新增角色信息 （1230～1249）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1230 | 新增角色信息成功 | Success in Adding Role Information |
| 1231 | 新增角色信息失败 | Failure to add role information |
| 1232 | 新增角色参数错误 | Error adding role parameters |
| 1233 | 新增角色已存在 | Additional roles already exist |

#### 修改角色信息 （1250～1269）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1250 | 修改角色信息成功 | Successful modification of role information |
| 1251 | 修改角色信息失败 | Failed to modify role information |
| 1252 | 修改角色信息不存在 | Modifying role information does not exist |
| 1253 | 修改角色信息数据一致 | Modify role information data consistency |

#### 删除角色信息 （1270～1289）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1270 | 删除角色信息成功 | Successful deletion of role information |
| 1271 | 删除角色信息失败 | Failed to delete role information |
| 1272 | 角色不存在 | Character does not exist |
| 1273 | 删除权限不足 | Insufficient deletion privileges |


## Role_menu （错误码范围1310～1459）

#### 获取角色菜单 （1310～1339）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1310 | 获取角色菜单成功 | Get the Role Menu Successful |
| 1311 | 获取角色菜单失败 | Failed to get role menu |
| 1312 | 获取角色菜单参数错误 | Error obtaining role menu parameters |

#### 新增角色菜单 （1340～1369）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1340 | 新增角色菜单成功 | New Role Menu Successful |
| 1341 | 新增角色菜单失败 | Failed to add role menu |
| 1342 | 新增角色菜单参数错误 | Error adding role menu parameters |

#### 修改角色菜单 （1370～1399）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1370 | 修改角色菜单成功 | Successful modification of role menu |
| 1371 | 修改角色菜单失败 | Failed to modify role menu |
| 1372 | 修改角色菜单参数错误 | Error modifying role menu parameters |

#### 删除角色菜单 （1400～1429）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1400 | 删除角色菜单成功 | Successful deletion of role menu |
| 1401 | 删除角色菜单失败 | Failed to delete role menu |

## User_role (错误码范围1460～1609)

#### 获取用户角色 （1460～1489）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1460 | 获取用户角色成功 | Achieving User Role Success |
| 1461 | 获取用户角色失败 | Failure to acquire user roles |

#### 用户角色分配 （1490～1519）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1490 | 用户角色分配成功 | Successful user role assignment |
| 1491 | 用户角色分配失败 | User Role Assignment Failed |
| 1492 | 用户角色分配参数错误 | User role assignment parameter error |

#### 用户角色更新 （1520～1549）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1520 | 用户角色更新成功 | User Role Update Successful |
| 1521 | 用户角色更新失败 | User role update failed |
| 1522 | 用户角色参数错误 | User role parameter error |

#### 用户角色删除 （1550～1579）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1550 | 用户角色删除成功 | Successful deletion of user roles |
| 1551 | 用户角色删除失败 | User role deletion failed |
| 1552 | 用户角色参数错误 | User role parameter error |

## Menu （错误码范围1610～1709）

#### 获取菜单信息 （1610～1629）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1610 | 获取菜单信息成功 | Successful access to menu information |
| 1611 | 获取菜单信息失败 | Failed to get menu information |

#### 添加菜单信息 （1630～1649）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1630 | 添加菜单信息成功 | Successful addition of menu information |
| 1631 | 添加菜单信息失败 | Failed to add menu information |
| 1632 | is_hide参数值非法 | Illegal is_hide parameter value |
| 1633 | is_hide_children参数值非法 | Illegal is_hide_children parameter value |

#### 删除菜单信息 （1650～1669）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1650 | 删除菜单信息成功 | Successful deletion of menu information |
| 1651 | 删除菜单信息失败 | Failed to delete menu information |
| 1652 | 不存在相关菜单项 | No related menu items exist |
| 1653 | 当前菜单项存在子菜单 | Current menu items have submenus |

#### 更新菜单信息 （1670～1689）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1670 | 更新菜单信息成功 | Successful update of menu information |
| 1671 | 更新菜单信息失败 | Failed to update menu information |
| 1672 | is_hide参数值非法 | Illegal is_hide parameter value |
| 1673 | 菜单项不存在 | Menu item does not exist |

## system_config（错误码范围1710～1819）

####  更新系统Logo （1710～1719）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1710 | 更新系统Logo成功 | Logo Update System Successful |
| 1711 | 更新系统Logo失败 | Failure to update system Logo |
| 1712 | 未配置系统信息 | System information is not configured |

#### 初始化系统配置 （1720～1749）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1720 | 初始化系统配置成功 | Successful configuration of initialization system |
| 1721 | 初始化系统配置失败 | Initialization system configuration failed |
| 1722 | 初始化系统配置参数错误 | Initialization system configuration failed |

#### 获取系统配置 （1750～1779）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1750 | 获取系统配置成功 | Achieving System Configuration Success |
| 1751 | 获取系统配置失败 | Failure to obtain system configuration |
| 1752 | 未配置系统信息 | System information is not configured |

#### 更新系统配置 （1780～1809）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1780 | 更新系统配置成功 | Update System Configuration Successful |
| 1781 | 更新系统配置失败 | Failed to update system configuration |
| 1782 | 未配置系统信息 | System information is not configured |

## Logs （错误码范围1820～1959）

#### 获取事件日志 （1820～1839）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1820 | 获取事件日志成功 | Acquire Event Log Success |
| 1821 | 获取事件日志失败 | Failed to retrieve event log |

#### 删除事件日志 （1840～1859）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1840 | 删除事件日志成功 | Delete Event Log Successfully |
| 1841 | 删除事件日志失败 | Failed to delete event log |
| 1842 | 事件日志不存在 | No current log information exists |

#### 获取请求日志 （1860~1879）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1860 | 获取请求日志成功 | Get the request log successfully |
| 1861 | 获取请求日志失败 | Failed to retrieve request log |

#### 删除请求日志 （1880～1899）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1880 | 删除请求日志成功 | Delete request log successfully |
| 1881 | 删除请求日志失败 | Failed to delete request log |
| 1882 | 请求日志不存在 | No current log information exists |

#### 获取任务日志 （1900～1919）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1900 | 获取任务日志成功 | Acquire Task Log Success |
| 1901 | 获取任务日志失败 | Failed to obtain task log |

#### 删除任务日志 （1920～1939）

| code | 错误描述 | Error Sescription |
| ---- | ------- | ------------------ |
| 1920 | 删除任务日志成功 | Delete Task Log Successfully |
| 1921 | 删除任务日志失败 | Failed to delete task log |
| 1922 | 任务日志不存在 | No current log information exists |


## vCenter  instance（错误码范围: 3000～3999）

#### 虚拟机开机  （3000～3019）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3000 | 虚拟机开机成功 | Start VM Success   |
| 3001 | 虚拟机开机失败 | Start VM Failed   |

#### 虚拟机关机  （3020～3039）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3020 | 虚拟机关机成功 | Stop VM Success    |
| 3021 | 虚拟机关机失败 | Stop VM Failed    |

#### 暂停虚拟机  （3040～3059）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3040 | 虚拟机暂停成功 | Suspend VM Success   |
| 3041 | 虚拟机暂停失败 | Suspend VM Failed    |

#### 重启虚拟机  （3060~3079）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3060 | 虚拟机重启成功 | Restart VM Success   |
| 3061 | 虚拟机重启失败 | Restart VM Failed    |

#### 删除虚拟机  （3080～3099）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3080 | 虚拟机删除成功 | Delete VM Success   |
| 3081 | 虚拟机删除失败 | Delete VM Failed    |


#### 添加快照 （3150～3179）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3150 | 添加快照成功 | Added Snapshot Successfully |
| 3151 | 添加快照失败 | Failed To Add Snapshot |

#### 删除快照  （3180~3209）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3180 | 删除快照成功 | Successful deletion of snapshot |
| 3181 | 删除快照失败 | Failed to delete snapshot |
| 3182 | 未找到对应快照 | No corresponding snapshot was found |
| 3183 | 数据 | No corresponding snapshot was found |

#### 恢复快照  （3210～3239）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3210 | 恢复快照成功 | Successful snapshot recovery |
| 3211 | 恢复快照失败 | Failed to reply to snapshot |

#### 创建主机  （3290～3309）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3290 | 创建主机成功 | Successful Host Creation |
| 3291 | 创建主机失败 | Failed to create host |
| 3292 | 无对应DataCenter数据 | No corresponding DataCenter data |

#### 添加网卡信息  （3310～3329）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3310 | 添加网卡信息成功 | Successful Addition of Network Card Information |
| 3311 | 添加网卡信息失败 | Failed to add network card information |

#### 添加磁盘信息 （3330～3349）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3330 | 添加磁盘信息成功 | Successful addition of disk information |
| 3331 | 添加磁盘信息失败 | Failed to add disk information |
| 3332 | 传入磁盘信息格式不正确 | The disk information format is incorrect |
| 3333 | 输入磁盘类型 | Input disk type |
| 3334 | 输入磁盘大小 | Input disk size |

#### 添加镜像信息  （3350～3369）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3350 | 添加镜像信息成功 | Successful addition of mirror information |
| 3351 | 添加镜像信息失败 | Failed to add mirror information |
| 3352 | 无指定镜像信息 | No Specified Mirror Information |

#### 删除网卡信息  （3370～3389）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3370 | 删除网卡信息成功 | Successful deletion of network card information |
| 3371 | 删除网卡信息失败 | Failed to delete network card information |
| 3372 | 本地无对应网卡信息 | Local no corresponding network card information |

#### 删除磁盘信息  （3390～3409）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3390 | 删除磁盘信息成功 | Successful deletion of disk information |
| 3391 | 删除磁盘信息失败 | Failed to delete disk information |

#### 更新主机CPU信息 （3410～3429）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3410 | 更新主机CPU信息成功 | Successful updating of host CPU information |
| 3411 | 更新主机CPU信息失败 | Failed to update host CPU information |

#### 更新主机内存信息 （3430～3449）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3430 | 更新主机内存信息成功 | Successful update of host memory information |
| 3431 | 更新主机内存信息失败 | Failed to update host memory information |

#### 获取主机列表信息 （3550～3559）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3550 | 获取主机列表信息成功 | Successful acquisition of host list information |
| 3551 | 获取主机列表信息失败 | Failed to obtain host list information |

### 克隆主机信息  （3570～3599）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3570 | 克隆主机信息成功 | Cloning Host Information Successfully |
| 3571 | 克隆主机信息失败 | Failure to clone host information |
| 3572 | DS名称参数错误失败 | DataStore name parameter error failed |
| 3573 | 获取DS对象失败 | Failed to get DataStore object |
| 3574 | 本地查询DS失败 | Local Query DataStore Failed |

#### 冷迁移  （3600～3629）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3600 | 冷迁移成功 | Successful cold migration |
| 3601 | 冷迁移失败 | Failure of cold migration |
| 3602 | 查询ds或dc失败 | Query DS or DC failed |
| 3603 | 冷迁移后删除原数据失败 | Failure to delete original data after cold migration |

#### ip分配  （3630～3659）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3630 | ip分配成功 | Successful IP allocation |
| 3631 | ip分配失败 | IP allocation failure |
| 3632 | 机器还处于开机 | The machine is still on |
| 3633 | 捕获vmodl故障 | Caught vmodl fault |

#### 转换模板  （3660～3689）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3660 | 转换模板成功 | Conversion Template Successful |
| 3661 | 转换模板失败 | Transform template failed |
| 3662 | 无虚拟主机 | No Virtual Host |
| 3663 | Vm对象不存在 | Vm object does not exist |


#### 基础错误(3900~3999)

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3990 | 动作操作参数错误 | Error in operation parameters |
| 3991 | 更新参数错误 | Error in update parameters |
| 3992 | 更新成功 | Update Successful |
| 3993 | 获取本地虚拟机错误 | Get local VM Failed |