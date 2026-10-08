# 角色包内置 绝区零绝区私有相机／正式模型包 制作与维护契约

## 基线、职责与证据

2026-10-08 当前基线为 **角色包 1.0.0（内置 绝区零绝区私有相机，来源版本 0.6.0）＋正式 Pack1／2／3／4 2.0.1**。版本、数量和索引是交付快照；先核对实际 settings、descriptor、安装收据与有效加载顺序。本文文件名沿用历史引用，Pack4Test 不再是默认运行目录或交付入口。

| 职责 | 当前来源与输出 |
| --- | --- |
| 角色玩法及内置 绝区零绝区私有相机 | `D:/CK3-mod/zzz_mod_project`；输出 `zenless_zone_zero`；版本来自 `settings.json` |
| 内置 绝区零绝区私有相机 权威来源 | 角色工程 `core_integration/files` 与 `core_integration/manifest.json`；由 `zzz_core_merge.py` 在 `build_mod.py` 末尾合并 |
| 正式模型资源 | `D:/CK3-mod/miyabi_3d_mod_project/packs/pack1_angels`、`pack2_victoria`、`pack3_hsos6`、`pack4_spookshack` |
| 模型包独立配置 | 3D 工程 `sources/<上述正式包目录名>/settings.json` |
| 现行维护入口与证据 | 3D 工程 `scripts/merge_zzz_core_role_100.py verify`；`reports/role_core_100/installation.json`、`verification.json`、`delivery.md` |

- 正式加载顺序：角色包原有前置 → 角色包 → 所需正式模型包。四个正式包只声明角色包为前置，不依赖独立 绝区零绝区私有相机。角色包现有二向箔、婚舰通用库、女仆之国前置保持；它们不等同于 绝区零绝区私有相机。
- 内置 绝区零绝区私有相机 负责相机、身份/包可用性分流、事件/活动覆盖、GUI、菜单、3D 开关同步和诊断；模型 Pack 负责本人模型、外观、隐藏 head/torso、配对动画、材质及道具。新增共享分支写入内置 绝区零绝区私有相机 来源和候选，不把 `D:/CK3-mod/zzz_core` 当正式编辑目标。
- `zzz core legacy` 0.6.0 位于 `D:/CK3-mod/zzz_core`，是保留的独立测试快照。测试组合为 **角色包 → zzz core legacy → pack2-core-test**，仍需角色包，由 legacy 覆盖同路径内置 绝区零绝区私有相机。测试包位于 3D 工程 `packs/pack2_core_test`，配置 `sources/pack2_core_test/settings.json`，版本 2.0.0、无工坊 ID；测试时停用四个正式模型包。交付时 legacy 和测试包留在库及当前播放集且停用；后续先读用户实际启用状态，不自动切换。
- legacy 与内置 绝区零绝区私有相机 本轮同源；任一来源后续变化都要重新检查最终 VFS 及 绝区零绝区私有相机 文件归属，不能保证旧快照永远完整覆盖新增功能。除明确维护测试线外，不同步改写 legacy，也不以它覆盖正式来源。
- 原 Pack1/3/4Test 已转为正式包；旧正式内容已被替换。旧 Test 目录、旧安装/恢复脚本只作历史取证，不重新登记或恢复。正式化保留 `zzz_p1t_*`、`zzz_p3t_*`、`zzz_p4t_*` 等私有标识；名称含 t 不代表仍是测试版，不能据此批量改名。Pack2 使用 `zzz_p2_*`。
- 当前四包共 16 人 28 外观（Pack1/3 合计 7 人 15 外观、Pack2 为 4 人 5 外观、Pack4 为 5 人 8 外观）；角色及外观从配置读取，不硬编码数量。
- 本轮合并的 17 种场景包括 16 种正式组合（含角色包单独加载）及 1 种独立 绝区零绝区私有相机 测试组合。模型资源哈希保持，离线 PASS 不表示游戏验收；此前站立/骑乘/载入的用户确认仅覆盖原报告案例，当前未观察入口仍为 `NOT_TESTED`。

修改内置 绝区零绝区私有相机 时保持 source → manifest → 合并后的候选 → 实际输出闭合；来源哈希变化需有对应差异及验证，不能只刷新摘要绕过检查。`native_menu_merge.py` 先合并原生菜单，内置 绝区零绝区私有相机 再按已审定的两份菜单覆盖规则接入，最终 `build_manifest.json` 应记录生效来源。复用算法不等于运行角色包或模型包历史全量构建。

## 制作顺序

冻结来源及保护清单 → 核对身份/画像组/动作契约 → 定向生成隐藏层 → 状态闭包及同步验证 → 绝区零绝区私有相机 接入 → 候选验证 → 事务安装。

只生成新增角色或实改数据。使用成熟提取、身体重定向、表情/眨眼、贴图处理算法，但不要运行依赖旧基线的全量构建或一次性安装入口。既有生成器仍可能保留历史名称；复用算法必须接上当前命名及后续补丁，不能直接拿首次构建产物替换现装成品。

## 相机调用结构

### 人物作用域与普通回退

沿用 `zzz_core_active_identity` 和当前实际画像/3D 开关条件。trait、节点名或目录名单独存在都不足以证明可接入；按最终角色作用域检查映射与资源契约。普通男女、儿童、其他包、关闭 3D 及不满足接入条件的分支保留原逻辑，不能由私有命名推断隔离成立。

### 活动：原调用点 → 隐藏别名 → 直接私有相机

1. 解析当前有效活动定义及嵌套动作树，记录原人物选择、条件、相机和动作。活动使用其原 `scope:character`，不从窗口左右位置猜作用域。
2. 对每个“原相机＋原动作”建立唯一、隐藏的动作入口别名。复制当前有效定义，保留身体/头部状态、权重、随机候选、道具与修正器，禁止加入理发店菜单或重建身体动画。
3. 原调用位置只有已接入人物选择对应别名。进行中、完成队列分别按别名直接传入已验证的私有相机名；别名传播、相机映射与调用位置必须闭合。
4. 普通人物和未适配路径仍使用原 `ActivityWindowCharacter.GetCamera`。它不是普通 CString；禁止包装成字符串后比较。也不能为“保留动态接口”撤回已成功的私有直接调用。

043 快照：23 种活动、909 个显式动作引用归并为 417 对组合，涉及 148 个动作；另外从原版 `NPortrait.DEFAULT_ANIMATION` 取得 3 个 idle 组合，最终为 **420 个别名**。同名动作存在多机位，不能按普通动作名统一路由。后续数量由当前源码重算；没有明确默认值时阻塞，不能猜 idle。

### 事件：人物位与有效覆盖

解析每个实际人物位的动作选择树，追踪显式相机、嵌套 `triggered_animation`/`scripted_animation`、窗口默认值和覆盖优先级。在已接入人物的对应叶分支直接指定私有相机；保留原条件顺序、随机变体及普通人物路径。原先没有原版覆盖且已正确使用私有 GUI 的调用保持。

`feast_default.2005` 的左位为 `disgust + camera_event_very_left`，中位为 `sick_stomach + camera_event_center_pointing_left`。只修左位会漏掉中位卢西娅；人物背向必须与该动作和原版镜头设计比较，不能一律旋转为正面。

043 清查快照为 8,082 个非调试事件、16,583 个人物位、20,455 行逐调用点记录，另列不产生肖像纹理的 41 个位置。每项区分已有私有调用、需要适配、无节点无需转换、不产生肖像和未解析；调试内容单列。未知结构、循环、覆盖冲突或遗漏作用域均阻止批量安装。

### 私有相机及有效来源

保留 绝区零绝区私有相机 原有相机数值和定位映射。新增副本完整保留距离、角度、偏移、FOV、裁剪和回退；只把需要适配的节点映射到已验证的隐藏 head 节点。043 的 128 种节点相机采用 125 个副本及 3 个等价复用，另 5 种无节点相机保持；这些是候选数量，不是已确认故障数量。

站立、骑乘复用已成功的私有相机。历史 ID 中包含某个角色名不等于只能服务该角色，须用共同资源契约证明复用。保留原剧情侧面、背身、跪地、倒吊及骑乘构图，不统一成 event_center。

绝区零绝区私有相机 提供按有效文件覆盖顺序生成的条件覆盖，记录原文件哈希；不编辑游戏安装目录。未知同名覆盖不能静默接受。定义数、GUI 参数与最终引擎相机是三种证据，不能互相替代。

## 隐藏骨架：五骨参考与 36 骨实现

| 项目 | 五骨参考载体 | 正式 Pack4（继承 Test 隐藏层） |
|---|---|---|
| 基础节点 | 根、头部取景、躯干取景、左右手道具 | 前五项保留对应功能和顺序，采用本地 `zzz` 名称 |
| 额外节点 | 无 | 头部、肩部、地面、腰部兼容节点及固定索引的占位节点 |
| 绑定姿态 | 参考资源的五节点为单位矩阵 | 部分节点包含位置偏移，不可强行归零 |
| 动画 | 动画驱动定位节点 | 从本人身体动作重新计算隐藏节点，保持状态与时间同步 |

五骨是参考结构，36 槽基础布局是当前正式模型包的数据契约，均不是所有 CK3 模型必须采用的骨数。没有证据证明应把 36 骨缩减成五骨。不要用二进制字符串搜索判断骨架，也不要把 `skin.bones = [4]` 的顶点影响槽数当骨数。

以下为 Pack4 基础布局的零基索引示例（其他包使用各自前缀）：0 `zzz_cam_root`；1 `zzz_cam_head`；2 `zzz_cam_torso`；3/4 `zzz_cam_prop_l/r`；5–33 保留占位布局，其中 22 `bn_h_head_mid`、29 `bn_h_skull`、27/28 `zzz_p4t_shoulders_position/target`；34 `zzz_cam_prop_ground`；35 `zzz_cam_lumbar`。维护时从实际 mesh 解码验证，不因节点看似未用而压缩索引。艾莲校服、爱芮机械外观所需的额外手部节点追加在基础布局之后，按实际可见外观标签选择；不能只按 zzz_skin 值选择，也不能把所有角色截为固定 36 骨。

- 跟踪 `portrait type → entity → pdxmesh → skeleton/animation → attachment` 的实际有效资源；记录索引、父级、逆绑定矩阵及所属 head/torso，拒绝重复节点归属造成的错误取点。
- 当前隐藏 head 是根加子节点的布局，挂接 `ground_joint → zzz_cam_root`，根变换在生成中消去。未来角色仍按实际祖先链计算，不能因为此布局而假定任何骨架都直接挂根。
- 状态配对键为角色、状态名、重复序号 occurrence。同名随机状态不能放进唯一键字典后覆盖。保留 clip、帧数/帧率、权重、entry/loop/exit、next_state 与菜单可达闭包；缺本人动作应构建失败，不能固定回 idle。
- 原理上比较 `body_parent_world @ inverse(aux_root_world) @ aux_node_world` 的最终挂接结果；编码已经消去 root 时不得重复消去。镜头锚点按原策略跟随，道具节点继承本人对应挂点完整平移/旋转/缩放和时间轴；地面、马、战车等单独验证。
- 身体的 `ground_joint` 和隐藏 `zzz_cam_prop_ground` 用途不同，不能直接互换。绑定偏移不等于运行时错误，先检查最终世界变换。可见资源的外层尺度仅使用一次，各皮肤共享姿势须核对实际骨序和绑定。
- 小型隐藏 head 的 pdxmesh 设置 `streaming = Never`；完整 torso 与可见附件保持既有策略，禁止全局强制预加载。隐藏几何仍须有效三角形、UV、包围盒与权重索引。
- 只改路由、命名或预加载时保护可见 mesh、导入骨架、身体动作、表情、眨眼、贴图及材质。隐藏数据未变且哈希相同可引用旧逐帧证据，标明原轮次；不得刷新旧收据冒充重新验证。

## 专项入口与故障处理

### 原生皮肤列表与空模型

读[原生皮肤与装配排查](portrait-assembly-and-skins.md)。Pack4Test017只有自动外观和跟随，018才补五人八外观原生列表；不要把跟随项当成完整换肤菜单。特殊外观基因用add；Pack1/3的031 replace为已知失败用例，032撤销。对截图剪影先查实际装配与材质阻断，不先改相机；未获得游戏确认不能宣称人物已恢复。

### 取景异常

固定同一角色、外观、动作和入口，先区分纹理未生成与纹理生成后拍错。查最终 VFS、实际人物作用域、动作/别名、相机覆盖、节点加载及归属，再查绑定和动态变换，最后才考虑参数校准。不同时改相机、骨架、动作和加载策略。

私有直接调用成功而源头分流后再现错误，优先检查别名传播和最终覆盖，保留已成功调用；不要重试已否定的普通 getter 路径。日志中节点无效可支持加载/归属假设，不能独自证明具体骨索引机制。

### 载入预览自动取景

本机 `SaveGameItem` 导出接口没有可用的 Character/画像组读取方法；不得虚构 Character.Custom 调用。绝区零绝区私有相机 的 `zzz_p4c044_camera_save_load` 保留原 camera_body 参数，专用定义中 `human`、`anime` 显式使用原 `camera_torso_look_at`，default 使用 `zzz_cam_torso`。

这是针对当前画像组集合的自动节点分流，不是全球 default 修改，也不是所有第三方组都兼容。新增/重复/变化画像组阻止直接沿用，必须重新核对节点契约与普通人物回退。无按钮、无姓名匹配、无存档改写。用户已确认对应载入案例成功；主菜单、游戏内及多人复用预览的其余角色、皮肤、儿童与 3D 关闭场景按证据逐项列出。

### 宫廷悬停与原版模型回归

先区分动作、地面锚点、材质选择入口和鼠标命中。016 对八外观的 31 个兼容身体/头发材质接入 court_scene 选择入口；脸、眼睛、眉毛、覆盖层和私有道具程序保持。不是把全部材质替换成公共 Shader。

失败 015 在条件分支中写两份 `PDX_MAIN`，CK3 只展开首个，造成 X3000 及原版模型异常。016 每个 MainCode 仅保留一个入口，函数内部选择原版或卡通路径。共享声明、Include、Effect 和其他阶段需保护；不要依赖宏隔离多套入口或拼接采样器声明。

实际 scache 声明配合 `d3dcompiler_47` 复现旧错并编译新候选；16 组原版 DX11 输出逐字节等价、3 组卡通编译通过。这不替代其他后端、悬停/描边、左右键及游戏画面验收。共享 Shader 回归应先核对原版人物，再测绝区零身体、脸、眨眼和道具。

### 姿势菜单

滚动列表使用原生 scrollbox 的 `blockoverride "scrollbox_content"`，不能直接把 vbox 放外面。旧待机显示“原版默认站姿”，新“默认站姿”使用本人 Galgame 对话待机；保留用户已选姿势。当前状态为 `zzz_iface_menu_zzz_native_galgame_idle_torso`，原版状态为 `zzz_ck3_game_idle_entry`；以实际 head/torso 定义核对闭包。菜单变化不重写事件、活动和宫廷实际动作类别。

### 命名与诊断

新相机、Custom、GUI、触发器、回调和隐藏节点使用 `zzz`。迁移先查调用/定义/有效覆盖与外部引用；二进制只改解析出的对象名称，保持长度或按合法格式重编码，并独立验证数值、骨序、绑定和轨道。不能盲替换 DDS、浮点字节或第三方文件。

旧存档兼容由 绝区零绝区私有相机 既有启动/同步流程中的[迁移脚本](D:/CK3-mod/zzz_mod_project/core_integration/files/common/scripted_effects/zzz_namespace_046_legacy_save.txt)负责，只读/移除旧标记，不覆盖已有新变量；无需在技能内抄录退役标识，不直接编辑存档。

诊断仅由 绝区零绝区私有相机 提供。每个诊断面板根 widget 使用 `visible = "[InDebugMode]"`，同时隐藏背景与文字，保持鼠标穿透和原分支。当前为六份 GUI 的 56 面板；正常模式不得显示，Pack 不复制诊断 GUI。活动标签应能展示别名与直接 CALL；事件标签中的 CAM 仅是 GUI 参数，不能冒充脚本最终镜头。

## 验证与安装

先做定义/引用/作用域和逆变换检查，再验证受影响状态、骨架、逐帧坐标和图像。负例至少覆盖多机位同动作、错误作用域、遗漏位置、条件/随机丢失、重复/循环引用、缺相机、别名错机位及 getter 字符串转换。骨架验证增加缺状态、错误归属、重复消 root、道具丢 T/Q/S 与错误预加载。

逐入口记录静态、离线、用户实测和未测结果；真实网格预览不能代替 CK3 分流和最终取点。没有身体/隐藏二进制变化时不重烘模型。仅文档修改不重建 Mod，不升 Mod 版本。

游戏和实际 Paradox 启动器关闭后才事务安装；备份目标和保护清单，记录写入 journal，完整回读 绝区零绝区私有相机/Pack及元数据。失败只回退本次写入，外部变更保留并报告，不能恢复用户播放集或启动器数据库来强行通过。不要按泛称 Launcher 误停其他服务。不使用 computer-use，不上传工坊。

当前统一回读为 `C:/Python312/python.exe -X utf8 -B D:/CK3-mod/miyabi_3d_mod_project/scripts/merge_zzz_core_role_100.py verify`。同入口支持 restore/recover；本轮精确恢复目标为角色包 0.11.0、绝区零绝区私有相机 0.6.0、四正式包 2.0.0，并撤销本轮新增测试包及登记，不回到历史 Test 包或 Pack2 1.10.0。以 installation/restoration 收据为准，外部修改冲突时停止，不覆盖后续改动。旧 verify 可能转发现行入口，旧 build/install/restore 不可用于覆盖当前成品。

## 按问题读取证据

以下均相对工程根，报告属于对应版本，不代表本次全新验收：

| 问题 | 实现与证据入口 |
|---|---|
| 当前内置 绝区零绝区私有相机 与正式包 | `scripts/merge_zzz_core_role_100.py`、`reports/role_core_100/`；以当前收据核对，build/install 已为本轮一次性入口 |
| 正式化及 Pack2 迁入来源 | `reports/formal_packs_200/`、`reports/zzz_pack2_1110/`；历史来源与逐帧/Shader 证据，不重跑旧安装 |
| 初始隐藏层与同步 | `scripts/build_pack4_test_010.py`、`reports/pack4_test_010/`；只读算法，不重跑旧构建 |
| head 加载 | `scripts/repair_pack4_test_014.py`、`reports/pack4_test_014/delivery.md` |
| 全量事件/活动 | `scripts/zzz_core_camera_043.py`、`scripts/audit_zzz_core_camera_043.py`；`reports/zzz_core_camera_043/` 中 call_sites、aliases、camera_map、semantic_validation、inactive_slots、blockers |
| 载入 | `scripts/repair_zzz_core_load_044.py`、`reports/zzz_core_load_044/delivery.md`；报告早期未测状态与后续用户对应确认分别记录 |
| 宫廷 | `scripts/pack4_court_016.py`、`reports/pack4_test_016/delivery.md` 与编译 verification |
| 菜单 | `scripts/zzz_core_pose_045.py`、`reports/zzz_core_pose_045/delivery.md` |
| 命名 | `scripts/zzz_namespace_046.py`、`reports/zzz_namespace_046/delivery.md` 与 binary_equivalence |
| 诊断 | `scripts/zzz_core_diagnostics_047.py`、`reports/zzz_core_diagnostics_047/delivery.md` |
