# 本机证据索引

以[当前共用规范](../../ck3-zzz-3d-mod/references/zzz-core-pack4-workflow.md)中的版本和证据表为入口。工程根为 `D:/CK3-mod/miyabi_3d_mod_project`；报告绑定其原候选和版本，不以新名称改写旧结果。

读取角色工程 settings.json、core_integration/manifest.json、模型工程 sources/<正式包目录>/settings.json 及实际输出，确认当前来源。现行入口为 `scripts/merge_zzz_core_role_100.py verify`，证据在 `reports/role_core_100/`。旧 Test 验证器即使转发也不是首选入口，不重跑旧 build/install/restore。

活动/事件查看 `reports/zzz_core_camera_043/` 的逐调用点、别名、相机映射与阻塞清单；载入、宫廷、命名及诊断分别查看共用规范所列报告。当前成功证据只覆盖用户明确确认的对应站立、骑乘和载入案例；没有逐入口反馈的项目继续 `NOT_TESTED`。

技能不保存过期成品 JSON 或旧审计结果。需要新快照时对当前明确的来源执行只读工具，输出到任务报告目录，记录哈希、范围和未扫描依赖。外部参考、游戏安装目录及工坊只读，不复制资源到技能。
