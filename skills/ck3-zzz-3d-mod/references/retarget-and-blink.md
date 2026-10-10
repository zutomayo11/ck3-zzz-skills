# CK3 身体动作与共享眨眼

当前绝区零工作线使用[内置 ZZZ Core／正式模型包 隐藏层契约](zzz-core-pack4-workflow.md)：head 保留独立取景和动态道具节点并按本人动作同步。下文旧导出与重定向算法仅按目标范围复用，不能删除当前所需节点或改动导入人物骨架。

## 历史算法参考：千夏动作对应

区分公开类别、实体状态与实际动画；下表是旧千夏方案的历史对应，不是当前正式模型包的 head 状态或普通情绪默认策略。当前制作优先遵循共用契约，菜单本人原生待机与实际 CK3 场景动作分离。

| 入口 | 千夏实际处理 | 维护位置 |
| --- | --- | --- |
| 普通 idle | 0.16.0起本人 `Galgame_Idle` 对话待机与同步原生面部；囚禁条件另外走原版 `misc_arrest` / `misc_dungeon` | `portrait_emotions.MENU_IDLE`、`angels_animation_profiles.py`、`sunna_actions/routes.py:native_idle_branch` |
| 主菜单/理发厅默认 | `frontend_center_idle/left/right` → 本包分支 → Galgame_Idle；24个 frontEnd_* 状态也映射本人原生对话；菜单head走独立 `zzz_menu_camera` | `menu_presentation.py`、`apply_menu_idle.py`、`menu_camera.py` |
| 原生独立待机 | `zzz_native_<原片段小写>` → `angels_summer_3d_*` → 内部 `angels_native_*` → 本人 `.anim` | `native_idle_menu.py`、`zzz_native_idles.txt` |
| 开心、伤心等普通情绪 | 本人 Galgame Start/Loop/End；按实际存在片段选择。千夏 Angry 缺身体片段时用本人都市待机 + 原生 Angry/Blink 组合，记录为 `MainCity_Angry_Adapted` | `portrait_emotions.py`、`angels_animation_profiles.py`、原生 animation/report |
| 间谍主管、宫廷坐姿、战斗等 CK3 动作 | 保留原版类别与随机状态、重定向本人身体动作；当前 head 按本人实际状态/重复序号同步，不统一固定 idle_entry | catalog 与当前隐藏层生成契约 |

该历史 catalog 有 477 个片段、503 个状态名、658 个状态块，均为当时快照。当前从真实来源解析状态和重复序号，不把片段数当菜单数。本人已有原生资源保持；实际场景动作保留 CK3 语义，不能因旧 protected_states 规则把全部事件改成原生情绪。

`bind_body_actions` 只移除 catalog 明确声明的旧重定向 ID，再补同名原版状态块；不能删除所有以角色前缀开头的 animation 声明，否则会连原生动作一起删掉。原生情绪类别已有肖像类型分支时优先保留。独立原生待机、情绪与 CK3 身体动作互不复制面部逐帧图集。

## 道具加载与挂接排查

动作能播放不代表原版道具已加载，也不代表挂点跟随正确骨架。分别检查两条链：

1. 加载链：原版 `animations_props` / `portrait_modifier_pack` 入口、私有 props gene、accessory、portrait modifier 到实际外观分支。私有 accessory 的 `portrait_group` 必须与本角色 gene 一致；modifier 显式指定的 accessory 名称必须存在于对应 gene/template，备用外观名称也要匹配。CK3 资源文本保持原有 UTF-8 BOM。缺失道具先看同次游戏日志中的加载错误，再核对最终 Pack 文件，不凭动画正常播放推断资源有效。
2. 定位链：当前正式模型包的 hidden head 动态左右手/地面节点按本人身体挂点计算完整 T/Q/S，状态与时间同步。检查实际 asset、accessory、旋转继承与最终世界变换；不强制沿用某个旧 inherit_rotation 值。静置同名节点竞争或错误载体应定向修正，不用固定偏移掩盖。

当前道具处理保留 hidden head 的左右手/地面动态节点及配套轨道，验证完整 T/Q/S、状态重复序号和实际 accessory 绑定。历史 `scripts/retarget_props.py` 的相机专用裁剪输出不是当前正式模型包收尾入口，不得重跑删除现用节点；具体实现按[共用规范](zzz-core-pack4-workflow.md)核对。

验证当前 head 动态节点归属、索引、绑定、状态/重复序号及真实道具引用，不能再断言 head 没有道具节点。回读最终人物、身体/隐藏动画及真实道具 mesh，覆盖酒杯、武器、骑乘和备用外观。历史 0.18.6/0.18.7 的去节点测试不适用于当前生成契约；其他来源缺资源单列，不伪造映射。

## 0.15.0：扩展到其余七人

`scripts/retarget_characters.py` 从实际 manifest、skeleton 和工作 blend 定位南宫羽、爱芮、艾莲、丽娜、莱卡恩、可琳、星见雅，共14套外观。千夏3套仍沿用原路径。每人各477片段，新增3339个动画；原有原生片段及其同步脸部数值保持，宫廷根骨仅改别名。

可复现入口（主工程内执行，不启动游戏）：

```powershell
# 复用通过哈希和输入指纹检查的身体烘焙，重新提取眨眼并集成、回读验证
python -X utf8 scripts/build_character_retarget.py
# 身体来源或骨架改变时，用实际免费插件重新烘焙；支持逐片段断点复用
python -X utf8 scripts/build_character_retarget.py --rebake --workers 4
# 单角色动作预览，直接回读最终网格、动画与DDS
& 'E:/Blender/blender.exe' -b --factory-startup --threads 2 --python-exit-code 1 --python scripts/render_character_retarget.py -- --character ellen --label ck3_council_spymaster
```

身体烘焙直接调用归档的 `animation_retarget.core`，保留 MIT 许可及固定提交。缓存骨骼查找、预计算源局部姿势是性能优化，不替换插件变换计算；每片段首/中/尾帧对照真实 Blender 求值，全部成品回读。`--rig female_body / male_body` 必须与 catalog 的**片段源骨架声明**一致，不按文件夹 common_body 或目标性别猜测绑定。

每套独立绑定分别校准：艾莲有 Bip001 与 campus__Bip001 两条身体链，爱芮有人形 Bip001 与机械 Bip002；目前每条映射49个身体/手指关节，排除颈、头、面部。不能只重定向原皮再让校服或机器人停在静置姿势。其它装饰与头脸局部姿势取本人睁眼中性帧；保持所有非根位置、骨长、缩放及权重。源骨架报告、烘焙器、眨眼中性配置进入输入指纹，变动后不得绕过 stale-source 检查。

## 每皮肤补眨眼，而不复制整套面部动画

以千夏为例：从本人 `Galgame_Facial_Blink_Idle` 找到闭眼峰值，只取眼部键与中性帧的差值；从原皮/茶歇/萌系三个实际工作网格各提取33行眼睑渐变。新 CK3 身体动作的所有眨眼共享这些行，衣服宏选择自己的行偏移，嘴和眉毛不跟着重定向。原生动作继续采样原来的逐帧区间。

七人扩展由 `prepare_character_blinks.py` 提取。每个现有 DDS 保留所有原有效行，只复用末尾空白或增加64行对齐空间；不同拓扑原本需要独立图集的皮肤不强行合并。即使两套皮肤提取结果相似，也分别读取源网格并记录 SHA256。实际闭合节奏仍使用下文的 CK3 眼睑映射或有来源标注的自然调度。

**表情时钟不能跨骨架硬编码。** 从本人默认原生动画的时钟轨道拟合并验证 `local_translation = origin + atlas_row * axis`，对全段回归误差设界限。千夏接近局部X，维多利亚和星见雅可能接近局部Z；新增眨眼只更改该无权重时钟的平移向量，其旋转、缩放与其它所有骨骼通道不变。不要把新行号直接写入错误的轴，也不要整段 TQS 往返求值。

爱芮两套机械外观没有人形眼睑键。当前 `ZZZ_ROBOT_SCREEN_BLINK` 在本人私有 shader 中根据同一个时钟对原眼屏纹理做竖向压缩近似闭眼，未新增 sampler；原生区间保持原静态眼屏。必须标注为 authored screen closure，不称原游戏完整屏幕序列或面部重定向。它的两个屏幕材质槽保留私有路径，其余通过检查的身体、衣服、头发继续沿用宫廷选取入口。

## 回归证据与生成顺序

原生模型/动画生成 → 资源共用与裁空白 → 千夏集成 → 七人眨眼提取与集成 → 宫廷材质兼容检查 → apply_menu_idle.py（默认/前端路由及镜头校准）是主包资源集成流程。历史阵营流程曾由 build_faction_packs.py 完成最终镜头、道具、地面节点及待机回退隔离；当前正式模型包使用现行配置和定向候选，不重跑此旧全量链，再回读验证和登记；见 [最终宫廷收尾](court-animation-and-grounding.md)。`rebuild.py` 和 `build_angels.py` 已挂接前述主包流程；重建公共 animations.txt 的旧脚本后，要重新集成相关动作分支与最终 Pack 修复。

`validate_character_retarget.py` 核对所有新动画骨序、fps、帧数、身体与眨眼差异、非映射骨姿势、非根平移/缩放、逐皮肤像素、原生文件除别名外的完整二进制树、同名随机状态块、事件类别默认分支。完整骨架/动作导出校验与 shader 安全测试仍需通过，不能把某个历史快照“所有文件不变”断言直接删掉而不补相应不变量。

报告：`character_retarget_integration.json`、`character_retarget_validation.json`、`<prefix>_native_and_retarget_routes.json`；身体源和逐片段插件对照在 `sources/character_retarget/<character>/clips/`，各皮肤眨眼来源在 `blink.json` / `outfit_blinks.npz`。预览来自最终成品的实际逆绑定、材质槽、动画及VAT，不是源blend摆姿，也不等于CK3实机。宫廷落座、鼠标悬停和事件触发仍由用户实测。

原版选取入口的声明保持原有单套星见雅结构，只更新它本来引用的星见雅 face include。0.14.2 多角色共享shader事故说明：HLSL条件宏不能隔离外层shader DSL的sampler定义，不能再把不同角色的顶层声明拼进 `court_scene.shader`。

## 已有工程与范围

主工程 `D:/CK3-mod/miyabi_3d_mod_project` 从 0.14.0 接入千夏动作。`settings.json.sunna_retarget.enabled` 控制集成；`sources/sunna_retarget/` 保存经哈希核验的身体烘焙、目录及眨眼形态数据，均在 Mod 输出目录之外。主包运行及重新集成不依赖独立千夏试验包。

原作者工程 `D:/CK3-mod/sunna_ck3_retarget_project` 保留供身体重新烘焙与回退。它的 0.4.0 成品只有间谍主管眨眼试验，不要让旧包/旧兼容补丁覆盖已合并的主包。不要自动修改用户播放集。当前千夏烘焙使用 MIT `igelbox/blender-retarget` 的实际 core/ops，提交 `9ab6889795903478d7bb4f0a0ff3ef056d3c86b7`；插件来源与逐片段数据在源目录报告中。源归档 authoring 文件供追溯，不是另一个可直接运行的完整工程。

身体重新烘焙时先在作者工程核对 `bake_retarget.py` 的路径、目标静置姿势、`mapping_rules.py` 和 catalog。按片段声明选择 female_body 或 male_body 源骨架，不能对全部 common_body 片段强套女体。执行真实插件，保留目标骨长/缩放/权重；颈、头、面部不做身体映射，头部自然继承胸部。导入新烘焙时更新主工程源文件及 SHA256，不能只替换成品动画。

## 接入原版事件和服装

- `scripts/sunna_actions/routes.py` 使用 `full_action_catalog.json` 中原版状态块，保留状态名、随机变体、起手/循环/收尾及 next_state；这样原版事件沿用原 animation 类别，无须新建每个动作的事件。
- 原生菜单与 CK3 场景动作分别维护。保留本人原生数据和当前显式映射，不用旧 protected_states 改写事件动作；公开原生菜单按真实片段注册，不为活动隐藏别名增加菜单。
- 各皮肤共享本人 torso 姿势；head 按角色/状态/重复序号配对真实身体 clip，不将全部动作统一到 idle_entry。身体、隐藏节点与表情时钟核对同一时间轴。
- 宫廷身体根、ground_joint、body_root 按本人现有来源和脚底契约保护；当前 head 挂接 ground_joint → zzz_cam_root，不能按旧原生根挂接重新布线。脚底另见[宫廷基准](court-animation-and-grounding.md)，不因相机修复重做旧人物支撑面。
- 合并共享 animations.txt 时保留其他角色分支及默认分支。VOTC 的 male-only 类别须补 default 和千夏分支；纸片人保留其 dead 静态规则。当前可选来源在 settings 的 votc_directory；启用 VOTC 时主包放在它之后。
- 验证原版同名状态的合法随机变体须逐项匹配 catalog，不能全局放开重复声明。QA 文件检测按 `_qa_` 等标识段匹配，避免把乐器 `qanun` 动作误认成 QA。

## 眨眼数据与方法

`scripts/sunna_actions/blink.py` 读取 CK3 已声明的 head 动画，按左右上眼睑局部 X 旋转提取闭合程度。仅在双眼轨道齐全、闭合幅度可辨且头/身体持续时间匹配时使用；按真实秒插值，保持身体帧数和 fps。当前归一化适用于已检查的 CK3 眼睑铰链，遇新骨架先检查旋转轴和静置方向。

没有可靠曲线则生成稳定种子的自然眨眼：间隔略有变化、闭眼快睁眼稍慢，片段两端睁眼。短于 1.2 秒的无源过渡不强行眨眼。死亡/睡眠/昏迷保持闭眼；绑定参考姿势静态睁眼。来源报告区分 ck3_eyelid_mapping、natural_schedule、closed_pose、static_open、short_transition_open。

千夏使用本人 `Galgame_Facial_Blink_Idle` 权重与现有中性基准，但每套服装从自己的工作网格形态键分别提取 33 行闭合渐变；嘴、眉毛、眼球骨旋转不动。`prepare_sunna_blinks.py` 输出 `sources/sunna_retarget/outfit_blinks.npz` 和逐皮肤来源报告。三套数据共用一张 DDS 的不同区域，动作时钟保持相同范围，通过 asset 的 SUNNA_BLINK_TEABREAK / SUNNA_BLINK_CUTENESS 宏选择行偏移。不要只改报告偏移，忘记实际 shader/asset。

本轮图集从 6336×7232 增至 6336×7296（64行对齐），只增加 1,622,016 字节，原有效 7,184 行保持；不复制完整183MB图集。原皮/茶歇/萌系分别独立提取，即使肉眼相近也不能未经比较就认定数据相同。`blink_ramp.npz` 保留初版来源元数据；`atlas_preservation.json` 约束原有效像素，重建时仅允许 DDS 头的高度更新及原空白区扩展。原生图集改变后重新提取审核，不能绕过哈希保护。

同一皮肤的所有动作共享该皮肤的 ramp，仅更改无权重 `*_face_clock` 骨平移 X；动态时钟当前按源 fps 存储，恒定时钟只保留参考值。不要承诺引擎支持未经验证的稀疏关键帧。PDX 写出器不支持空属性数组，零动态平移时应移除 samples.t，而非写入空列表；用二进制回读测试覆盖静态姿势。

更改动画时只改该字段，避免整段 TQS → 矩阵 → TQS 往返误差。shader 扩展时钟 clamp，新增 ramp 区间继续隐藏分离道具，生成内容散列 include 并更新 atlas 报告。原生时钟仍指向原行，不受影响。

## 构建和验证

在主工程执行：

```powershell
& 'E:/Blender/blender.exe' -b --factory-startup --threads 2 --python-exit-code 1 --python scripts/prepare_sunna_blinks.py
python -X utf8 scripts/integrate_sunna_retarget.py
python -X utf8 scripts/validate_sunna_retarget.py
$env:ZZZ_NATIVE_FAMILY='angels'
python -X utf8 scripts/validate_victoria_export.py
python -X utf8 -m unittest discover -s tests -v
python -X utf8 build_mod.py --register
```

每步检查退出码。天使完整/复用构建通过 `scripts/build_angels.py` 在资源优化后重新集成；直接运行会重写共享入口的旧脚本后，也要重跑千夏集成。测试集会读取导出验证报告，先完成验证再跑依赖该报告的测试，不能并发读取未完成报告。

`reports/sunna_retarget_integration.json` 记录源头部、方法、闭合曲线、哈希与体积；`sunna_retarget_validation.json` 比较所有身体/颈头/其它面部通道，检查三套服装、原生动画、图集及无关资源保留。验证源快照在工程备份中，别从分发包删除资源来满足检查。

预览用 `render_sunna_retarget.py` 回读成品 mesh/anim/DDS。每套服装的 material_index 必须来自其实际 slots，不能重新枚举成0..n再查全局材质表，否则茶歇等服装会采到原皮的错误贴图，看起来像脸部翻转。各服装须用成品自己的逆绑定矩阵和独立眨眼行；不能据错误预览改变模型权重或绑定。预览不等于 CK3 实机。

## 旧菜单缓存与死亡状态分离（0.16.3历史案例）

本节解释历史八人主包的实体映射，不能直接套到当前全部角色。当前20人死亡类别与115主面板API/类别分流见[展示与死亡](portrait-display-and-death.md#真正死亡与旧菜单兼容)；资源存在或手选死亡成功不证明实际已故人物GUI正确。各人旧dead映射不完全相同，不全局重绑。

原版事件animation = dead请求的是肖像类别。仅本包8人该类别的head/torso映射到zzz_death_pose；新状态保留catalog死亡片段、闭眼和阶段参数，next_state指向自身。实体dead保留为旧纸片人/存档菜单姿势兼容入口，改接本人Galgame_Idle与head_menu_camera。验证器须对zzz_death_pose核对原catalog，同时对dead核对菜单片段，不能简单跳过死亡验证。其余原生、重定向状态与所有动画二进制保留。直接请求实体dead的外部调用也会走待机；原版死亡类别仍走真正死亡片段。

宫廷角色只有本人待机时，还需检查共享 default.hm_idle 是否仍以纸片人身份命中上述实体 dead；实际3D外观的排除条件由 court_animation_fallback.py 生成，见 [宫廷动作选择](court-animation-and-grounding.md)。
