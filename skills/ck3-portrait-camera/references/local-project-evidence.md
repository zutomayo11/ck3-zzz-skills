# 本机证据索引

以[拆分共用规范](../../ck3-zzz-3d-mod/references/zzz-core-pack4-workflow.md)核对当前配置、清单、顺序与收据。正式入口/报告在 `D:/CK3-mod/zzz_split_test_project/formal_release`，名称层在 `formal_name_140`；模型算法与历史报告在 `D:/CK3-mod/miyabi_3d_mod_project`，不随新名称改写历史结果。

111展示默认/静态头像、112原版相机兼容、113道具/诊断/取景、114接触/地图、115死亡主面板是不同增量。分别读取reports/zzz_display_pose_111、zzz_native_camera_112、zzz_props_death_113、zzz_debug_overlay_113、zzz_ground_framing_113、zzz_mount_contact_114、zzz_map_portrait_114、zzz_death_entry_115。问题算法与限制在[展示/死亡](../../ck3-zzz-3d-mod/references/portrait-display-and-death.md)和[接触/取景](../../ck3-zzz-3d-mod/references/mount-contact-and-framing.md)。

当前回读/撤销/中断恢复使用拆分工程 `promote_formal_split.py verify|restore|recover`；115死亡及其他旧repair为历史增量，不用于转正后写入。新修复沿当前独立前置/Pack来源做定向候选和独立收据；旧校验因后续变化停止时不解除保护。043别名/副本只用于故障追溯。

离线逐帧、投影、规则模拟、用户截图和引擎实际状态分开记录。115死亡游戏NOT_TESTED，死后换装变量错误待修；接触/取景新增画面尚未验收，马入镜的用户反馈只支持相应案例。技能不保存游戏二进制、旧成品JSON、私人存档或粘贴对话全文；需要新快照时读取实际来源，输出任务报告并记录范围和SHA256。
