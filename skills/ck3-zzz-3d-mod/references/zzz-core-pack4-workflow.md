# 角色包内置 ZZZ Core／正式模型包制作与维护契约

## 基线、职责与证据

2026-10-10圣人光环交付快照：角色包1.3.0、内置Core来源0.6.2、正式Pack1–5 2.0.5／Pack6 1.0.1；25个私有画像组。数量和索引是交付快照，先核对settings、descriptor、manifest、安装收据与实际加载顺序。此文件名用于兼容已有技能链接，不表示默认维护旧Test目录。

| 职责 | 当前来源与输出 |
|---|---|
| 角色包与内置Core | `D:/CK3-mod/zzz_mod_project`，输出`zenless_zone_zero` |
| Core权威来源 | `core_integration/files`和`core_integration/manifest.json`；合并后的来源记录在`build_manifest.json` |
| 正式六包 | `D:/CK3-mod/miyabi_3d_mod_project/packs/`下的`pack1_angels`、`pack2_victoria`、`pack3_hsos6`、`pack4_spookshack`、`pack5_yunkui`、`pack6_cunning_hares` |
| 包配置 | 3D工程`sources/<包目录>/settings.json`，角色/外观按实际清单读取 |
| 测试线 | `D:/CK3-mod/zzz_core`与3D工程`packs/pack2_core_test`，Legacy0.6.1／测试包2.0.1 |

正式顺序为角色包前置 → 角色包 → 所需正式模型包。六包只依赖角色包，最低版本按各包当前descriptor/settings核对；Pack6交付要求角色包1.3.0，不因技能快照批量改旧包依赖。测试顺序为角色包 → Legacy → pack2-core-test，不与正式模型包混用；不自动切换用户启用状态。

Core管理共享GUI、相机、身份/包可用性、菜单、3D开关及诊断；Pack管理本人可见资源、隐藏head/torso、骨架、配对动画、Shader与道具。正式共享修改写入角色工程来源，不回写Legacy。旧内部`zzz_p1t_*`、`zzz_p3t_*`、`zzz_p4t_*`仍是正式包标识，不能因含t批量改名。Pack2、Pack5与Pack6使用各自当前前缀。

保持 source → manifest → 候选 → 运行输出及build_manifest闭合；来源哈希变化必须有对应差异和验证。包组合数量从当次配置计算，六包有64种子集（含角色包单独）；按本轮影响检查，静态闭包不是实机验收，光环的有界组合验证也不是全VFS重审。Legacy后加载不保证永远覆盖未来新增路径，按当前差异核对。

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

执行维护时从当前AGENTS及该层安装/恢复收据选择入口。最新角色包死亡入口为`scripts/repair_zzz_death_entry_115.py verify|restore|recover`；地图、接触、取景各用本轮入口。旧入口若遇后续合法变化应停止，不以全量恢复、放宽校验或刷新基线强行通过。

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

旧来源或收据名称不作为当前制作规则；以交付编号索引，未知路径先搜索当前工程，不凭技能快照创造文件。
