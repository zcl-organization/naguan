# 错误码定义


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

#### 冷迁移  （3600～3629）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3600 | 冷迁移成功 | Successful cold migration |
| 3601 | 冷迁移失败 | Failure of cold migration |

#### ip分配  （3630～3659）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3630 | ip分配成功 | Successful IP allocation |
| 3631 | ip分配失败 | IP allocation failure |

#### 转换模板  （3660～3689）

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3660 | 转换模板成功 | Conversion Template Successful |
| 3661 | 转换模板失败 | Transform template failed |

#### 基础错误(3900~3999)

| code | 错误描述 | Error Description |
| ---- | -------- | ----------------- |
| 3990 | 动作操作参数错误 | Error in operation parameters |
