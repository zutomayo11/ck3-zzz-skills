# 构建、兼容及交付

新 Pack 默认只构建新增角色；此前所有已完成包及其模型、动作、镜头、宫廷/王座与脚底基准保持。先按 [新 Pack 生产与 Token 节约](new-pack-production.md) 做一次静态预检，确认入口实际支持的目标筛选。以下全量/历史主包命令仅在明确需要该范围时使用，不能作为新包或小修复的默认流程。

## 工程入口

工程根为 `D:/CK3-mod/miyabi_3d_mod_project`。当前 绝区零绝区私有相机/Pack 路径、独立配置和定向入口见[共用工作规范](zzz-core-pack4-workflow.md)。下列主包/旧阵营算法仅用于明确维护对应历史方案，不是新包默认构建命令；Blender 路径由实际配置确认。

仅星见雅动作变化且 mesh/材质已经验证时：

```powershell
& 'E:/Blender/blender.exe' --background --factory-startup --python-exit-code 1 --python scripts/build_native_animation.py
python -X utf8 scripts/build_assets.py
python -X utf8 scripts/native_outfits.py
python -X utf8 scripts/validate_export.py
# 仅运行此次导出/动作修改实际影响的测试；不默认全项目 discover。
```

每条命令检查退出码，前步失败即停止依赖步骤。`build_native_animation.py` 必须在 Blender 内执行；普通系统 Python 没有 bpy。

完整重新生成用 `python -X utf8 rebuild.py --register`；仅维多利亚用 `python -X utf8 rebuild.py --victoria-only --register`。先看 `rebuild.py` 当前 stages，避免无关重建。兼容或角色包接口变化时需重新生成 `build_compatibility.py` 和 `victoria_integration.py`；后者生成最终 Victoria 分支，不能被后跑的旧桥覆盖。

`python -X utf8 build_mod.py --register` 是历史主包登记入口，对应 `miyabi_3d_local.mod`；当前阵营交付使用下面的 Pack 登记方法，不因新包恢复或更新旧主包。登记不等于启用播放集，也不自动上传。若已有启动器缓存且需要同步，只修改已核实的本地行，保留工坊条目及播放集；启动器正在运行时避免并发写缓存。

## 旧阵营方案的收尾与发布资料

旧阵营方案曾使用四个 `packs/pack*` 包，其范围按对应配置核对。新包采用 内置 绝区零绝区私有相机／正式模型包，不能以旧 `build_faction_packs.py` 遍历全包收尾。仅对目标角色执行所需处理，受影响共享分支定向合入；独立性核对 Shader/贴图闭包、缺席依赖及实际加载来源，不能只看相机定义。

事件/活动按[调用点验证](portrait-routing-and-validation.md)处理：目标人物通过事件叶分支或活动相机/动作别名直接调用私有相机，普通人物保留原调用。不要执行旧 Recovery/finalize 链撤销已正确分流；保护既有 绝区零绝区私有相机 相机与资源哈希，不重烘模型。

本机 SteamModsPublisher 固定读取包根目录 `thumbnail.png`，要求小于1 MiB，descriptor 的 picture 或启动器本地缩略图不能替代上传文件。每包使用对应阵营 logo；thumbnail.png、旧路径 cover.png 与源 logo 保持一致，descriptor 指向 thumbnail.png。本地修复不会自动更新已发布条目的远端封面。

版本从目标包当前独立配置读取，同步 descriptor、本地登记和必要说明。内置 绝区零绝区私有相机／正式模型包 使用当前事务维护入口，保护存档、播放集、启动器数据库和其他包；历史登记/缩略图脚本不用于本轮默认安装。已有登记字段及工坊 ID 保持，不创建重复条目；仅技能更新不递增 Mod 版本。

当前包可用性默认定义由角色包内置 绝区零绝区私有相机 的 `common/scripted_triggers/00_zzz_core_interfaces.txt` 提供，各正式包声明自身 `zzz_core_packN_available`。共享开关、菜单和同步由内置 绝区零绝区私有相机 维护，勿重新铺入旧 `000_zzz_3d_optional_*` 或独立 bridge 覆盖。只有接口实改时才检查受影响单包/组合；不因新增模型重复测试未变的旧控制系统。

## 角色包内置 绝区零绝区私有相机 与模型包的边界

角色工程 `D:/CK3-mod/zzz_mod_project` 提供角色、身份特质、召唤、zzz_skin 及内置 绝区零绝区私有相机；模型工程提供各正式包资源。绝区零绝区私有相机 来源为角色工程 core_integration/files，源 manifest 和最终输出必须一致。以角色包 build_manifest.json、包独立配置及生成代码读取精确 trait/皮肤 index，不凭中文名称猜标识。

统一全局变量 `zzz_3d_disabled` 由内置 绝区零绝区私有相机 的身份/同步及开关效果读取；结合包可用性、本人身份、实际画像和既有禁用意图决定接入。检查现行 `zzz_core_identity.txt` 与 Pack2 旧标记迁移脚本，不能运行旧 build_compatibility 的全量控制生成覆盖它们。关闭/开启显示不重置身份、特质、皮肤变量或复制召唤人物。

`native_outfits.py` 管历史星见雅两套衣服；`victoria_integration.py` 管对应历史角色的服装、分支和兼容。当前内置 绝区零绝区私有相机／正式模型包工作线的原生列表、手动优先/恢复跟随及特殊基因操作见[皮肤与装配](portrait-assembly-and-skins.md)，不能运行这些旧全量入口覆盖当前包。默认原皮/对应皮肤按 `zzz_skin` 自动选择。

妄想天使用 `angels_integration.py` 与 `angels_outfit_sources.py`，保持维多利亚式 `zzz_skin → outfit → shared_pose_entity = torso`。右键切皮继续调用角色包原有 `zzz_skin_set_*`，不要在主包重复定义 scripted GUI 或靠切 ethnicity 刷新。自动 outfit 子 modifier 需 `normal_portrait_blocked_trigger = no`；否则被核心库普通肖像屏蔽规则挡住。衣服基因为 add，不能 replace。

换装故障先沿“按钮实际 GUI → zzz_skin 值 → modifier 权重 → outfit/accessory → 实际 mesh/材质”追踪。接口正常但每个皮肤指向同一原皮副本，仍不会换装；检查完整 Animator 精确网格来源和成品哈希，不能只修变量。当前天使 3 人 10 套真实外观的来源见 manifest，历史 fallback 说明不代表现在仍为占位。

千夏重定向已并入主包。原独立千夏包和旧兼容补丁仅作回退，不与新主包同时启用；用户播放集由用户管理。千夏源资源、动作入口与眨眼的完整更新顺序见 [重定向与眨眼](retarget-and-blink.md)。

核心库完整 `gfx/portraits/portrait_animations/animations.txt` 有意覆盖：只插入本包所需类型分支，其余内容保留。更新核心库或纸片人后重读原文件再生成，别用陈旧副本覆盖别的角色。正式包只放统一开关，QA 决议和事件留在 `work/runtime_qa` 或显式隔离 runtime 下。

公开原生待机菜单沿用 `native_idle_menu.py` 的算法，现行生效文本在角色包内置 绝区零绝区私有相机 来源及其合并输出。每种片段只注册一个 zzz_native_* 选项，保留逐角色可见规则、整行过滤和忽略隐藏项布局。修改相关规则须更新有效来源，不用历史菜单全量生成覆盖现行路由；详见[理发店原生动作与道具](barbershop-native-idles.md)。

表情不能只检查骨架 asset：二向箔核心库在默认分类中为纸片人赋予高权重 `dead` 姿势。星见雅及所有3D角色都需有独立肖像类型分支，同时检查 default.hm_idle 对实际3D外观的排除条件；仅有专属分支、原生表情数据和 entity state 并不能保证选中它。共同语义分类在 `portrait_emotions.py`，最终回退隔离由 `court_animation_fallback.py` 处理。新增角色后检查从CK3类别到实际动画文件的完整路径，详见 [宫廷动作选择](court-animation-and-grounding.md)。

## 验证清单与问题定位

- 按新增/实改角色与模块选择相应导出验证器和 unittest，先确认范围；菜单文字、布局或局部材质修复不默认运行整个角色模型验证器。来源已变时原报告不能作为受影响部分的新验证。
- 本轮确有模型/动画生成时，仅回读其 `.mesh/.anim`：绑定矩阵、原权重、骨名顺序、帧率、TQS、同步和 DDS 行偏移。检查受影响 asset state 到声明及文件的完整引用，不为新包重查旧包所有二进制。
- 动作抽查可用 `scripts/preview_native_ck3_motion.py --clip MainCity_Stand_Idle02`（放在 Blender `--python` 后，参数前加 `--`）；Victoria 用 `render_victoria_previews.py`，先读取参数定义。星见雅预览读取报告骨数，不能恢复旧237硬编码。
- 游戏验证仅在任务需要且用户允许范围内做，使用隔离 runtime/测试存档；用户明确豁免就记“离线通过、未做本轮实机”。崩溃先看对应时间的 logs/crashes、版本及启用 Mod，区分加载前失败和动画播放失败。
- 修改后比较原网格哈希，若只改动作不应变化。版本每轮递增一次，保留 source→generated→validation 的报告引用。
