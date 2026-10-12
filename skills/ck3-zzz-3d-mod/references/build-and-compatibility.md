# 构建、兼容及交付

新Pack默认只构建新增角色；此前成品模型、动作、镜头、宫廷/王座与脚底基准保持。先按[新Pack生产规范](new-pack-production.md)做静态预检。下列rebuild/build_mod及旧集成命令仅展示历史算法和参数，不作为当前正式输出入口；明确要求全量范围也不能解除退役保护。未来更新使用当前来源的定向候选与独立收据，不运行旧命令覆盖成品。

## 工程入口

工程根为 `D:/CK3-mod/miyabi_3d_mod_project`。当前 ZZZ Core/Pack 路径、独立配置和定向入口见[共用工作规范](zzz-core-pack4-workflow.md)。下列主包/旧阵营算法仅用于明确维护对应历史方案，不是新包默认构建命令；Blender 路径由实际配置确认。

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

旧阵营方案曾使用四个 `packs/pack*` 包，其范围按对应配置核对。新包采用 独立3D前置／正式模型Pack，不能以旧 `build_faction_packs.py` 遍历全包收尾。仅对目标角色执行所需处理，受影响共享分支定向合入；独立性核对 Shader/贴图闭包、缺席依赖及实际加载来源，不能只看相机定义。

事件/活动按[调用点验证](portrait-routing-and-validation.md)处理：特殊事件保留原版调用，活动接入人物使用私有center，普通人物保留typed GetCamera，后续定向取景条件按现装源码核对。不恢复旧420别名，也不执行旧Recovery/finalize覆盖当前增量；保护未改相机及二进制资源。

本机 SteamModsPublisher 固定读取包根目录 `thumbnail.png`，要求小于1 MiB，descriptor 的 picture 或启动器本地缩略图不能替代上传文件。每包使用对应阵营 logo；thumbnail.png、旧路径 cover.png 与源 logo 保持一致，descriptor 指向 thumbnail.png。本地修复不会自动更新已发布条目的远端封面。

版本从目标包当前独立配置读取，同步 descriptor、本地登记和必要说明。独立3D前置／正式模型Pack 使用当前事务维护入口，保护存档、播放集、启动器数据库和其他包；历史登记/缩略图脚本不用于本轮默认安装。已有登记字段及工坊 ID 保持，不创建重复条目；仅技能更新不递增 Mod 版本。

当前包可用性默认由独立前置的 `common/scripted_triggers/00_zzz_core_interfaces.txt` 及Pack5/6接口提供，各Pack声明自身 `zzz_core_packN_available`。共享开关、菜单和同步由独立前置维护，缺席角色包采用安全默认；不恢复旧 `000_zzz_3d_optional_*` 或旧bridge覆盖。接口实改才检查受影响单包/组合，不为新增模型重复测试未变控制系统。

## 角色包、独立3D前置与模型Pack的边界

角色工程提供角色、身份特质、调频和 `zzz_skin`，独立工程 `D:/CK3-mod/zzz_split_test_project` 提供当前共享3D来源/输出及正式配置，模型工程提供各Pack资源。角色 `core_integration/files` 是历史输入，不回写或合回。读取角色清单、包独立配置与现装脚本的精确trait/皮肤索引，不凭中文名称猜标识；人物创建模板只放角色包。

现行总开关为 `zzz_split_3d_disabled`，由独立前置接入/恢复效果读取；旧 `zzz_3d_disabled` 不作为当前控制源。独立模式按保存模型和实际外观接入，联用读取角色包可选映射；关闭恢复原遗传外观但保留模型选择，开启重新接入，不重置身份、特质或皮肤变量、不复制调频人物。备份和接口边界见[共用规范](zzz-core-pack4-workflow.md#外观备份开关与理发店)。

`native_outfits.py`与`victoria_integration.py`是历史衣服/分支算法，不运行旧全量入口覆盖现装。原生列表、手选优先与特殊基因操作见[皮肤与装配](portrait-assembly-and-skins.md)；联用跟随角色包读取zzz_skin，独立人物缺变量时沿当前模型默认外观。

妄想天历史集成由 `angels_integration.py` 与 `angels_outfit_sources.py` 处理，可读取其本人外观与torso共享姿势算法，不把旧集成入口当现装写入步骤。联用角色包右键换肤仍调用 `zzz_skin_set_*`；独立使用理发店原生customization。自动outfit的 `normal_portrait_blocked_trigger = no` 与特殊衣服基因add规则保留；不靠切ethnicity强制刷新换肤，也不混同独立模型选择效果。

换装先区分联用按钮写zzz_skin与独立原生customization，再沿实际选项→权重/定制→gene/template→outfit/accessory→mesh/材质追踪。接口变化而多个皮肤指向同一副本仍不会换装，核对实际网格来源和成品哈希。天使3人10套是既有外观快照，不作后续固定数量；历史fallback说明不代表现在占位。

千夏重定向已并入主包。原独立千夏包和旧兼容补丁仅作回退，不与新主包同时启用；用户播放集由用户管理。千夏源资源、动作入口与眨眼的完整更新顺序见 [重定向与眨眼](retarget-and-blink.md)。

独立前置的 `gfx/portraits/portrait_animations/animations.txt` 有意提供共享类别适配，保留非目标内容。联用上游核心库更新后核对实际源码/VFS，不用陈旧副本覆盖其他角色。开启/关闭、模型选择和恢复入口在Core，Pack不复制控制决议；QA仅放显式隔离runtime。

公开原生待机菜单复用 `native_idle_menu.py` 算法，现行生效文本在独立前置来源/输出。每种片段仅注册一个 `zzz_native_*` 选项，按实际模型可见、整行过滤并忽略隐藏项。修改有效来源，不用历史菜单全量生成覆盖当前路由；详见[理发店动作](barbershop-native-idles.md)。

表情不能只检查骨架 asset：二向箔核心库在默认分类中为纸片人赋予高权重 `dead` 姿势。星见雅及所有3D角色都需有独立肖像类型分支，同时检查 default.hm_idle 对实际3D外观的排除条件；仅有专属分支、原生表情数据和 entity state 并不能保证选中它。共同语义分类在 `portrait_emotions.py`，最终回退隔离由 `court_animation_fallback.py` 处理。新增角色后检查从CK3类别到实际动画文件的完整路径，详见 [宫廷动作选择](court-animation-and-grounding.md)。

## 验证清单与问题定位

- 按新增/实改角色与模块选择相应导出验证器和 unittest，先确认范围；菜单文字、布局或局部材质修复不默认运行整个角色模型验证器。来源已变时原报告不能作为受影响部分的新验证。
- 本轮确有模型/动画生成时，仅回读其 `.mesh/.anim`：绑定矩阵、原权重、骨名顺序、帧率、TQS、同步和 DDS 行偏移。检查受影响 asset state 到声明及文件的完整引用，不为新包重查旧包所有二进制。
- 动作抽查可用 `scripts/preview_native_ck3_motion.py --clip MainCity_Stand_Idle02`（放在 Blender `--python` 后，参数前加 `--`）；Victoria 用 `render_victoria_previews.py`，先读取参数定义。星见雅预览读取报告骨数，不能恢复旧237硬编码。
- 游戏验证仅在任务需要且用户允许范围内做，使用隔离 runtime/测试存档；用户明确豁免就记“离线通过、未做本轮实机”。崩溃先看对应时间的 logs/crashes、版本及启用 Mod，区分加载前失败和动画播放失败。
- 修改后比较原网格哈希，若只改动作不应变化。版本每轮递增一次，保留 source→generated→validation 的报告引用。
