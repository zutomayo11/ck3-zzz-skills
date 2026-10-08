# 生成、测试与本地登记

工作目录 `D:/CK3-mod/zzz_mod_project`。Python3.12与Pillow为当前可用环境，先验证实际解释器与依赖，不因技能文本安装另一套环境。

```powershell
python -X utf8 build_mod.py
python -X utf8 validate_mod.py
python -X utf8 -m unittest test_faction_opinions test_tuning_ui test_local_registration -v
```

逐条检查退出码，失败后停止依赖步骤。`validate_mod.py` 生成 `validation_report.json`；`build_manifest.json` 列出每个角色、身份、皮肤、纹理来源。检查报告时间与这次生成一致，旧runtime报告不能当成本版实测。相关规则测试是静态/模拟覆盖，不证明 CK3 GUI 渲染或所有API已通过实机。

上述为完整构建参考，不是每次局部修补的默认检查清单。纸片人、音擎和保底只选 [对应生成器及测试](paper-rendering-and-tuning.md)，检查实际启用包的VFS覆盖组合；不要为角色包更新重建3D包。短状态按任务读取 `ten_guarantee_status.json`、`paper_carrier_fix_status.json`、`startup_status.json` 或 `english_localization_status.json`，核对版本/时间；旧状态中的3D版本不代表当前设置。不回读全部历史构建日志，成功日志只留摘要，错误按相关片段逐步扩大。

版本唯一来源 `settings.json.version`；每次交付功能或修复更新一次，并同步 `zenless_zone_zero/descriptor.mod`、README 首页、已登记的 `zzz_agents_local.mod` 与本地缓存。保留历史说明和工坊条目 ID（当前3806658401，以现有descriptor为准），不在生成器硬编码另一份版本。

缓存更新必须等启动器安全关闭后备份，只改已核实的本地行，保留工坊条目、播放集及其他字段。运行中不并发写数据库；关闭被拒或无法确认进程身份时完成其余文件同步，记录缓存未同步及重启后核对事项，不冒称已退出或已同步。内容修复不授权改订阅/播放集或终止未知进程。

## 内置 绝区零绝区私有相机 与现行维护

角色包版本来自 settings.json；embedded_zzz_core.source_version=0.6.0 是导入来源版本，不是另一个正式发布包版本。`settings.json.core` 仍指二向箔参考库，不可改指 绝区零绝区私有相机。

权威源为 `core_integration/files` 与 manifest.json，`zzz_core_merge.py` 校验来源哈希和许可覆盖，`build_mod.py` 在角色包生成末尾合并。原生菜单先由 native_menu_merge.py 合并，绝区零绝区私有相机 再覆盖两份已登记菜单；核对最终 build_manifest.json 的有效来源。修改共享 绝区零绝区私有相机 需同步来源、声明的哈希及候选，不能只改输出或只刷新哈希绕过语义验证。

当前运行维护使用 `C:/Python312/python.exe -X utf8 -B D:/CK3-mod/miyabi_3d_mod_project/scripts/merge_zzz_core_role_100.py verify`，同入口 restore/recover 按本轮收据精确处理。上方完整 build_mod.py 命令仅为生成器参考；局部修复先做候选及必要验证，不直接覆盖现装成品。

四个正式模型包依赖角色包，不依赖独立 绝区零绝区私有相机。独立测试顺序是角色包 → zzz core legacy → pack2-core-test；仍加载角色包，由 legacy 提供同路径 绝区零绝区私有相机。详细基线、加载范围和恢复边界见[共用规范](../../ck3-zzz-3d-mod/references/zzz-core-pack4-workflow.md)，不默认切换播放集或改写 legacy。

## 开局初始化与说明（0.8起）

维护入口为 `startup.py`，不是3D初始化桥。`on_game_start_after_lobby` 追加私有开局动作：选中角色进入游戏后先执行 `zzz_role_init`、`zzz_role_refresh_living`，再显示调频/音擎说明。保留既有全局迁移标记和旧档决议兜底，不能为提示重置已有角色、余波、自选资格或冷却。

同一玩家人物以角色flag `zzz_role_intro_seen` 控制只提示一次；说明页不消耗首次免费自选、金币、余波或冷却。背景源为 `assets/startup/background.jpg`，复用现有生成。只改角色包，3D接口、模型和动作保持。

相关检查为 `python -X utf8 -m unittest test_startup -v`，覆盖初始化先后、重复调用、共享登记、进度保留及实际启用包VFS组合。`startup_status.json` / `startup_build_report.json` 是证据入口；开局弹窗、实机显示和卡顿改善未取得新反馈时仍记待实测，不能由规则测试推断性能改善。

## 完整双语与英文生成（0.9起）

英文由 `english_localization.py` 和 `localization_sources/english/` 生成；成品主文件为 `localization/english/zzz_role_text_l_english.yml`，不只手改成品。简体中文与英文完整键集合一致，输出必须有UTF-8 BOM及正确语言头。覆盖姓名、家族、皮肤、各视角记忆、音擎原介绍/激活条件、调频和联动界面，保留动态表达式、图标、格式标记与数值。

新增/修改中文先复核对应英文，再更新 `localization_sources/english/source_index.json` 的中文catalog SHA256；哈希守卫失败表示源文变化，不能只改摘要绕过翻译检查。新本地化同步双语；语言任务只改角色包，不修改3D工程或借语言生成改变玩法/身份/皮肤顺序。

相关检查为 `python -X utf8 -m unittest test_english_localization -v`，检查完整键、动态标记及有效3D覆盖组合中的英文资源；按实改模块补其他测试。`english_localization_status.json` / `english_localization_report.json` 记录构建证据；静态/模拟通过与实际切换游戏语言显示分开记录，不把旧版本测试计作本轮新测试。

## 本地/工坊同名冲突

CK3 会按名称去重，本地条目即使在播放集中禁用仍可能挡住同名工坊条目。不要以反复改名或给正式上传目录添加“开发版”后缀解决，也不要删工坊文件。

在游戏和启动器已关闭、任务确需切换模式时：

- 本地开发登记：`python -X utf8 register_local_mod.py --local`。
- 准备用户授权的上传：`python -X utf8 register_local_mod.py --publish`。这只登记，不是上传；之后仍需用户明确的发布授权。
- 使用工坊订阅版：`python -X utf8 register_local_mod.py --workshop`。不带参数也默认此模式，会把本地注册移到 backups，不能当普通“登记命令”误运行。

`--local`/`--publish` 都指向正式 `zenless_zone_zero`，旧 `zenless_zone_zero_local` 不再作运行或上传目录。模式切换保留正式输出、存档、订阅内容和播放集；不用直接 SQL 改用户勾选。

`switch_mod_mode.ps1` 及 D:/CK3-mod 下已有快捷 cmd 可用于人工切换；运行前检查当前状态，不凭旧消息断定应切哪种模式。用户只要求内容修复时，不额外切到工坊模式。

## 发现异常时

1. 核对实际启用的是本地还是工坊输出、descriptor 版本、三个前置顺序以及日志挂载路径。
2. 查看对应本轮启动 `logs/error.log` 和崩溃目录，区分未挂载、同名去重、GUI缺引用、脚本错误与旧档数据丢失。
3. 只有在未加载 Mod 时保存已丢失自定义特质的旧档，才讨论数据缺失；不能保证重新加载自动恢复。
4. 按问题运行最小相关规则测试，修生成器或源数据后再生成。检查 UTF-8 BOM、本地化键、descriptor 末尾换行，避免 path 与 remote_file_id 粘连。
5. 不修改工坊下载内容排错。若需要隔离实测，使用单独测试存档与用户目录；用户豁免实机时交付清楚标注静态验证结果。
