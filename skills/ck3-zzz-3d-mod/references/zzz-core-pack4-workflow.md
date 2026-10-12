# 独立3D前置／正式模型Pack与角色包制作维护契约

## 基线、职责与证据

2026-10-11现装快照：**绝区零角色包1.4.0、绝区零3D模型独立前置包1.1.0（内置RUI 20可选兼容）、六个本地正式Pack全部1.0.0**，25个私有画像组。以正式配置、descriptor、清单、实际加载顺序与安装/恢复收据为准；数量不硬编码为未来上限。本页沿用旧文件名以保持技能链接，不表示默认维护Pack4Test或内置Core。

| 所属 | 功能归属 | 当前来源与输出 |
|---|---|---|
| 角色包 | 立绘与消隐、身份/职能特质、代理人和音擎调频、十连保底、余波/金币/首次自选、宝物、立绘换装、开局说明、双语、人物创建及可选3D回调 | `D:/CK3-mod/zzz_mod_project`，正式输出 `zenless_zone_zero`；沿用 `zzz_agents_local.mod`、工坊ID `3806658401` |
| 独立3D前置 | 独立右键选模型、阵营卡片与灰显、原外观备份/恢复、3D开关、理发店共享入口与动作筛选、姿势窗口、肖像分流、共享相机、场景适配、原版道具同步、死亡入口、Pack检测、兼容及debug诊断 | `D:/CK3-mod/zzz_split_test_project/mods/core`；沿用 `zzz_split_3d_core_test.mod`，名字虽含test但已转正，无工坊ID |
| 六个模型Pack | 本人可见模型、服装皮肤、隐藏head/torso、骨架、动画、表情眨眼、Shader、贴图、道具挂点及本包圣人光环注册 | `D:/CK3-mod/miyabi_3d_mod_project/packs/`；源配置为 `sources/<包目录>/settings.json` |
| 正式配置与冻结候选 | 配置随当前登记更新；转正候选/所有权保留Core1.0.0基线，后续RUI另有增量；源模式 `installed_snapshot` | 拆分工程 `formal_release/settings.json`、`formal_release/candidate`、`formal_release/installation.json`；名称更新另有 `formal_name_140` 收据 |
| RUI可选兼容增量 | 成人大肖像复用展示选择器，无RUI时保留原窗口入口，不改六包资源 | 拆分工程 `rui_compat.py`、`repair_rui_compat.py`、`test_rui_compat.py`及`rui_compat_110`收据；详见[RUI专项](rui-optional-compatibility.md) |
| 历史来源 | 算法、旧失败与增量证据，只读追溯 | 角色工程 `core_integration`、旧完整生成器、旧测试候选/收据、`D:/CK3-mod/zzz_core` Legacy与 `pack2_core_test`；不能覆写当前交付 |

六包目录依次为 `pack1_angels`、`pack2_victoria`、`pack3_hsos6`、`pack4_spookshack`、`pack5_yunkui`、`pack6_cunning_hares`；星见雅在Pack3。身份与外观索引从实际清单读取。旧内部 `zzz_p1t_*`、`zzz_p3t_*`、`zzz_p4t_*` 仍是正式标识，不能因含t或转正批量改名。

## 依赖与加载模式

| 模式 | 推荐加载顺序 | 模型接入 |
|---|---|---|
| 纯角色包 | 原三项前置 → 绝区零角色包 | 保留全部非3D玩法，不要求独立3D前置或Pack |
| 独立3D | 独立3D前置 → 所需正式Pack | 玩家右键任意在世人物，阵营与角色卡片选模型 |
| 联用 | 原三项前置 → 角色包 → 独立3D前置 → 所需Pack | 调频/自选人物创建后可选接入；直接选模型禁止 |

角色原三项依赖是 `二向箔核心库 / Anime Core Lib`、`婚舰通用库 / Hunjian Common Lib`、`女仆之国 / Maid Universalis`。二向箔是纸片人依赖之一，不是独立3D前置。独立3D前置无必需Mod依赖，六个本地正式Pack只声明独立前置，不依赖角色包，也不形成循环。旧工坊下载版的依赖/版本未改，不将本地迁移结论套给订阅版。

RUI是可选UI层，兼容内置于独立前置，不新增必需依赖或第三个兼容Mod。启用时建议RUI→独立前置→Pack；现行三种静态VFS情景（无RUI及两种RUI/Core顺序）已核对，游戏画面/即时刷新仍NOT_TESTED。作用于RUI基础大肖像类型，边界与无RUI闭包见[RUI专项](rui-optional-compatibility.md)。

不自动切换播放集或排序。当前转正曾按授权在其他播放集末尾追加Core；两种顺序有静态检查，但有效VFS和引擎覆盖需按实际启用组合核对。旧完整角色包、Legacy及旧Core测试版不与当前正式组合混用；旧完整包只保留一份校验ZIP，不另登记。

## 选模、联用与接口

独立选择窗口沿用角色包20个阵营、64张角色卡片；快照有25个模型，仅对应Pack实际加载时可选，其余灰显原因。儿童、外国人物和同模型多人允许，AI不自动使用；不依赖外交距离。窗口状态写玩家，外观写所选目标。取消只清窗口状态；目标死亡、Pack不可用或备份失败不得更改目标外观。

选择只写外观类型、模型选择变量与专用外观/姿势标记，不调用代理人创建、玩法初始化或调频效果，不改特质、属性、姓名、年龄、性别、文化、信仰、家族、头衔和财产。外观识别按实际ethnicity/模型状态，不要求独立使用者有身份trait。

| 接口/状态 | 契约 |
|---|---|
| `zzz_split_paper_loaded` | 由角色包声明已加载；缺席默认false，按当前加载脚本判断联用，不依赖存档残留模式标记 |
| `zzz_split_core_loaded` | 独立前置声明true；角色包缺席前置时安全默认false |
| `zzz_split_role_created` | 角色包在创建完成后调用；缺席Core时空效果，Core存在时按角色包身份映射和已加载Pack接入 |
| `zzz_core_packN_available` | 每个Pack声明自身可用；Core提供缺席默认，保持现有接口与私有资源名 |
| `zzz_core_active_identity` | 共享场景接入判定，结合实际模型与开关；不得重新限制成“必须有代理人身份” |
| `zzz_split_3d_disabled` | 当前存档持久3D总开关；旧 `zzz_3d_disabled` 只用于历史追溯，不作为现行控制变量 |
| `zzz_split_model` / `zzz_split_backup` | 目标保存模型选择和首次原外观备份载体引用；玩家窗口的 `zzz_split_target` 仅指向被操作目标 |

联用时在交互、窗口和执行效果三层阻止直接赋予模型；角色身份映射归角色包，Core只保留缺席安全默认及接入流程。调频限制、费用、特质和 `zzz_skin` 编号保持，无对应Pack继续显示立绘。21份Pack调频人物创建模板已删除，由角色包独占；后续构建不得重新放回Pack。Core的同路径空模板是历史兼容屏蔽，不是人物创建功能。

## 外观备份、开关与理发店

首次确认前创建专用无亲属、家族、雇主和头衔辅助人物，复制原外观类型及可遗传外观，再令其死亡；目标持久引用。A→B切换不覆盖首次备份。目标无有效位置、备份创建失败或备份缺失时停止并提示，不能随机造脸替代。

- 独立模式提供“恢复原外观”及“恢复全部测试外观”，处理所记录在世人物并清除模型选择；备份缺失者不改。辅助人物不成为亲属、廷臣或继承人。
- 关闭3D恢复原外观但保留模型选择，重新开启接回选择；联用按已获得人物与可用Pack接入。不直接编辑存档。
- 理发店服装/皮肤和动画资源由Pack提供，共享GUI及动作可见规则由Core维护。原生手选优先；联用“跟随角色包”读取 `zzz_skin`，独立使用保留缺变量时的默认外观，不给普通人物造身份或第二套皮肤变量。
- 姿势窗口和理发店按实际模型支持片段筛选。默认站姿为本人 `Galgame_Idle`，原版默认为CK3待机；保留原生名称、手选及特殊状态优先关系。
- 当前只实现原遗传外观备份/恢复流程，实际已故载体保存/读档可读性仍待测；不承诺DNA字符串逐字节一致、非遗传发型服装完整恢复或后代遗传不受影响。停用Core前先在游戏内恢复，删除Mod文件不能自动恢复存档外观。

## 原版道具与圣人光环归属

CK3原版武器、杯子、马、战车等与绝区零源武器Shader显隐是不同链。当前Core兜底是独立路径 `gfx/portraits/portrait_modifiers/00_zzz_split_optional_props.txt` 的空定义（`usage = none`），真实DNA道具定义由各Pack的后续42文件提供。不得恢复Core里25份与Pack同路径的空props文件；仅调播放集顺序不能代替最终VFS及同名数据库定义的优先级核对。源与旧修复证据在拆分工程 `props_021`、`props_validation.py`，按[道具专项](mount-contact-and-framing.md)区分缺失、挂接、裁切与接触。

圣人光环注册独立存在六个Pack，条件为原版 `saint` 与 `rf_abrahamic`，复用原版光环实体、mesh、贴图和发光Shader，挂在实际head节点；Core负责原有显示路由，不提供光环装配注册或新封圣玩法，纸片人没有新绘制光环。详情见[光环专项](saint-halo.md)。

## 制作与维护顺序

圣人光环沿用[私有画像组装配规则](saint-halo.md)，注册由各Pack独立携带，原版资源只读复用；角色包/Core功能文件保持。新Pack或后续重建必须主动合入本包光环注册，不从旧全量来源覆盖现行交付。

冻结当前来源及保护清单 → 核对身份/画像/真实入口 → 定向修改调用或受影响资源 → 验证状态、索引和挂接 → 候选验证 → 事务安装。复用成熟算法但不运行依赖旧基线的历史全量构建；只生成新增或实改角色，保持既有数据。

## 相机调用结构

### 特殊事件与活动队列

相机兼容112撤除旧420个活动别名、130台事件/活动相机副本（含10台共用副本）及129台原版相机的5120条私有节点映射。特殊事件恢复原版相机、动作、选择条件、随机权重和顺序；必要的同路径注释屏蔽文件保留，防止旧内置设置再次生效。23台基础私有相机与普通GUI、菜单、载入调用保留。

活动进行中/结束各核对普通与接入人物分支：沿用实际`zzz_core_active_identity`和3D条件，接入人物调用`zzz_cam_camera_event_center`，普通人物保留原生typed `ActivityWindowCharacter.GetCamera`。原动作名与选择树保持，不包装getter为CString、不恢复逐别名站立/骑乘分流。

后续取景113是有限增量：指定五类活动骑乘请求和战车事件人物位使用受身份保护的定向相机；其他调用保持上述基础结构。当前源码与增量收据优先，不能把112基础结构误写成“所有动作永远只用center”。取景条件及构图目标见[地面道具与接触约束](mount-contact-and-framing.md#原版人物为主的取景)。

事件逐位追踪显式/默认相机、`triggered_animation`、`scripted_animation`、窗口默认和有效覆盖。`feast_default.2005`左位`disgust/camera_event_very_left`与中位`sick_stomach/camera_event_center_pointing_left`分别核查；侧身/背向先和原版剧情设计比较，不统一转正面。

### 有效来源与历史方案

解析最终VFS及实际人物作用域，记录GUI、slot、环境、动作类别、相机ID、画像、实体、节点及动画。未知嵌套结构、循环、覆盖冲突和未解析作用域阻止批量生成。无纹理位置单列，不以定义数量算渲染覆盖。

043的原相机/动作别名及逐事件副本方案已被112撤除，仅用于解释旧报告和回归失败，不是新制作步骤。历史直接探针成功只支持当时入口，不推导必须重新部署整套旧分流。原版/儿童/3D关闭与未接入人物维持原逻辑；私有名字不证明隔离。

## 隐藏骨架与原版兼容槽

按真实`portrait type → entity → pdxmesh → skeleton/animation → attachment`解码，不能用二进制字符串搜索、骨数或节点名判断引擎行为。`skin.bones=[4]`表示顶点影响槽数，不是总骨数。

| 载体 | 零基槽及用途 |
|---|---|
| torso | 2 `zzz_native_lumbar_compat`、75 `zzz_native_torso_compat`，无权重定位骨 |
| 隐藏head | 22原版头部兼容槽，保持已有动态定位、动画与小型head预加载 |
| 隐藏head基础布局示例 | 0根、1头部、2躯干、3/4左右手；22头部兼容，27/28肩部，29头骨；34地面代理、35腰部；其余占位保持 |

torso2/75分别复用本人隐藏lumbar/torso的定位变换并计入实际挂接链；采用独立名称保留原有身体骨。隐藏head的36槽基础布局和角色特殊扩展不是通用固定骨数，不能缩减或把所有角色截成36骨。

- 实际挂接为身体`ground_joint → zzz_cam_root`，按父级世界矩阵和隐藏根抵消计算。未来模型按真实祖先链处理，不假定所有辅助节点直接挂根；星见雅外层比例`0.889313653343`仅计一次。
- 状态配对键包含角色、状态名和重复序号occurrence；不能用唯一键字典覆盖同名随机变体。保留帧数/帧率、权重、entry/loop/exit、next_state和菜单闭包，缺匹配报错，不能固定回idle。
- 插骨/重排时同步原骨序映射、父索引、蒙皮索引、逆绑定、身体动画轨道和Shader表情/显隐时钟。时钟从实际发布骨架按骨名解析，不硬减固定偏移。
- 定向兼容算法为3D工程`scripts/zzz_native_camera_compat.py`，识别已适配资源并拒绝重复插骨。保留原骨名、父子关系、原T/Q/S、几何、权重、贴图和状态/道具契约。
- 小型隐藏head保留`streaming=Never`及有效几何，完整torso/附件不强制预加载。额外手部挂点按实际可见外观标签选择，不能只查zzz_skin。
- 插槽迁移的原通道应逐值相等；世界变换/定位误差不超过0.0002。接触修复另有允许平移白名单，不能把插槽迁移的“身体数据不变”约束误套为禁止已授权接触位移。

112快照包含55份mesh、14148份身体动画和33份Shader include，3766230帧回读；原骨世界误差0、定位最大约0.00000763。数值绑定该候选，不要求文档更新重复全量解码。

## 展示、死亡、取景与接触

展示、手选、静态头像、地图标记及115死亡入口集中在[展示与死亡](portrait-display-and-death.md)。`default`不是强制选择，GUI请求与实体状态不同；地图114只同步静态动作参数。死亡第一阶段已安装但游戏未测，死后换装变量错误仍待修。

RUI 20基础大肖像的固定`idle`已由前置1.1.0接入`zzz_core_display_animation`；复用两种默认与手选规则，原RUI死亡API及婴儿边界独立保留。不能把原版主面板的EvenIfDead死亡分支验收外推给RUI，见[RUI专项](rui-optional-compatibility.md)。

道具完整预期链、地面挂接、骑乘/战车定向取景及114支撑面求解集中在[接触与取景](mount-contact-and-framing.md)。取景调整不修相对接触，骨盆差不等于坐面差，地面附件代理的额外尺度不能重复使用。羊、乐器和衣裙等待确认项保留。

内阁使用`CouncilPositionType.GetPortraitAnimation`及原版文化/任务条件；手选会绕过部分自动选择。千夏东亚间谍姿态与艾莲匕首差异符合文化分支，“查找秘密”优先偷听，不能仅因姿态不同就重烘或强制欧洲站姿。证据见`reports/zzz_council_diagnostic_20261009/`。

## 保持的专项规则

### 载入

载入使用真实SaveGameItem/画像接口和已验证的专用自动分流，不虚构人物Custom接口。新增画像组先核对默认节点及human/anime回退；用户确认只支持其实际观察范围。不能将一个载入卡的离线图或游戏内成功扩展成全入口通过。

### 宫廷悬停与原版模型回归

016仅对需要兼容的身体/头发材质接入court_scene选择入口，脸、眼、眨眼和私有道具程序保持。失败015在同一MainCode放两份PDX_MAIN，造成X3000及原版模型异常；现行每个MainCode仅一个入口，在函数内部选着色分支。共享原版编译输出需用真实scache声明对照；离线编译不是游戏画面验收。

### 姿势菜单与命名

滚动列表内容使用原生scrollbox的`blockoverride "scrollbox_content"`。新默认站姿为本人Galgame，原版默认为已注册CK3待机；保留用户选择，其他原生名称/编号及可见条件见[理发店动作](barbershop-native-idles.md)。

新接口使用zzz命名，二进制名称修改须解析合法字段并独立验证数值/轨道，不盲替换浮点、DDS或第三方文件。旧存档标记迁移依已有`common/scripted_effects/zzz_namespace_046_legacy_save.txt`同步流程，不直接编辑存档或重置已有新变量。

### 诊断

诊断由Core提供，根widget用`visible="[InDebugMode]"`同时控制背景和文字，保持鼠标穿透与真实分支。开debug无标签时先查控件是否被删除；113活动诊断缺失是调用迁移后控件不在，不是InDebugMode失效。

区分GUI请求类别、Custom返回相机和引擎最终状态。活动标签随当前实际调用表达式；事件CAM可能只是被脚本覆盖前的GUIfallback。115主面板死亡标签跟随死亡组件，不能将旧常量待机标签当引擎跟踪。Pack不复制诊断GUI，不加入自动推进/定时器。

## 验证、安装与精确恢复

按改动层选择检查：路由验证逆变换、条件顺序和随机等价；骨架验证索引映射、实际挂接、状态重复序号与编码回读；取景与接触分别做几何及实机检查。没有二进制变化不重烘；仅更新技能不升Mod版本。

逐入口记录离线、规则模拟、用户实测和NOT_TESTED；保留USER_REPORTED_FAIL，不因静态PASS改写历史失败。包组合目标路径来源检查、资源闭包和逐组合游戏实测是不同证据；组合数随包范围变化，不固定复制历史32或64。

当前RUI 1.1.0增量唯一维护入口为 `C:/Python312/python.exe -X utf8 -B D:/CK3-mod/zzz_split_test_project/repair_rui_compat.py verify|restore|recover`，仅撤销该轮至前置1.0.0。其活动期间，旧`promote_formal_split.py verify`转发增量验证，旧全量restore/recover拒绝；精确回退后旧入口恢复原字节。先读`rui_compat_110/delivery.md`与收据，详见[RUI专项](rui-optional-compatibility.md)。

转正入口为 `C:/Python312/python.exe -X utf8 -B D:/CK3-mod/zzz_split_test_project/promote_formal_split.py verify|restore|recover`，但不得绕过上述活动增量保护运行旧全量恢复。当前已有转正候选和安装收据，不重复candidate/install；这些入口不是任意未来功能更新的通用重建器。未来修复读取当前正式输出/冻结来源及相关生成逻辑，做定向候选和独立收据。角色名称更新另有 `rename_formal_role.py` 与 `formal_name_140` 收据，不能只按转正旧哈希判断名称漂移。

`core_integration`、旧完整生成器、旧测试安装及各旧repair写入入口已退役/受保护。历史算法和报告可读，但不能运行旧全量构建或恢复覆盖现装。正式verify报告用户后续启动器/登记等外部变化时，应核对证据并保留差异，不能修改收据、放宽校验或刷新基线使其通过。

安装/恢复检查游戏与实际启动器关闭，冻结候选和保护清单，使用持久化journal备份与逐项回读；restore只撤销本轮，recover验证目标/方向/备份/已写内容后处理中断。保护存档、数据库、播放集、启用状态、工坊ID和Legacy/test；精确接纳授权的正式资源变化不能改写测试线运行文件。未执行正式恢复记NOT_RUN，不虚构恢复收据。不使用computer-use，不上传工坊。

## 按问题读取证据

以下相对`D:/CK3-mod/miyabi_3d_mod_project`，报告只支持其版本与范围：

| 编号/问题 | 报告与当前算法 |
|---|---|
| 111 展示与静态头像 | `reports/zzz_display_pose_111/`，`scripts/zzz_display_pose_111.py` |
| 112 原版相机兼容 | `reports/zzz_native_camera_112/`，`scripts/zzz_native_camera_compat.py` |
| 113 道具/死亡状态映射 | `reports/zzz_props_death_113/`；不代表GUI死亡入口已修 |
| 113 debug诊断 | `reports/zzz_debug_overlay_113/` |
| 113 定向取景 | `reports/zzz_ground_framing_113/`及`reports/zzz_ground_framing/` |
| 114 支撑接触 | `reports/zzz_mount_contact_114/`及`reports/zzz_mount_contact/` |
| 114 地图头像 | `reports/zzz_map_portrait_114/` |
| 115 死亡主面板第一阶段 | `reports/zzz_death_entry_115/`；前置分析`reports/zzz_death_entry_analysis_114/` |
| 内阁任务/文化 | `reports/zzz_council_diagnostic_20261009/` |
| 历史加载/宫廷/命名 | `reports/pack4_test_014/`、`zzz_core_load_044/`、`pack4_test_016/`、`zzz_namespace_046/` |
| 历史043分流 | `reports/zzz_core_camera_043/`；退役方案，只读取证 |

旧来源或收据名称不作为当前制作规则；先读拆分工程当前增量`rui_compat_110/delivery.md`，再按任务读`formal_release/delivery.md`、正式配置及安装收据，名称层读`formal_name_140/delivery.md`。表中111–115、光环和旧测试报告只用于理解保留算法及失败证据，不再作为当前默认写入入口。
