# 共享画像组、动态镜头与单入口隔离

新 Pack 优先读取[绝区零绝区私有相机 工作规范](../../ck3-zzz-3d-mod/references/zzz-core-pack4-workflow.md)。本页适用于既有包的共享映射维护，Test 沿用正式画像组，或头像/地图/事件小像需分别修复时读取。本页从 Pack3Test 0.1.0 与 Pack1Test 013/014 提炼规则；个例骨数、偏移和版本不作为通用配置。

## 公共 group lookup 不受私有 capability 完全隔离

先列出所有提供同一 portrait group / ethnicity / entity 的资源方案，以及它们是否互斥。GUI 的 character selector 可以检查 capability、本人 trait 和实际 ethnicity；原生相机内的 `position_node` / `look_at_node` group 映射仍可能对另一模型方案生效。只验证 Test selector 不足以证明正式包不受影响。

Pack3Test 与正式 Pack3 共用画像组。初期 `*_zzz_event_head_mid/camera_torso/lumbar` 事件叶节点与正式原解剖节点不同。最终 316 原生相机块 / 1,264 映射恢复原 default 节点名：`bn_h_head_mid`、`bn_h_skull`、`camera_torso_look_at`、`bn_sp_lumbar`；私有 selector 保持 Test 的能力/身份/ethnicity 三重条件。这里保持的是原查询语义，不能把事件节点仅因“也指向头部”当作等价解剖点。

校验公共映射时分别解码每个受影响模型的实际节点与动作，在进入、循环及代表动作首中末比较世界位置。正式 Pack3 原资源缺少 `bn_h_skull`，本轮保留原同名查找；缺节点的引擎 fallback 未实测，仍 NOT_TESTED。不要添加新节点、改公共 default 或按手工替代点渲染后宣称正式兼容已证明。

## 动态入口保留原调用链

活动/旅行不仅使用 event_center。逐项记录 GUI 控件、slot、environment、`ActivityWindowCharacter.GetCamera` 实际可能返回的相机、骑乘/阶段变体及其画像组映射。维护这些历史包时保留其已验证契约；新 绝区零绝区私有相机 路线按相机/动作别名直接调用私有相机，普通分支保留 GetCamera，环境与原调用点语义保持。

单个 event_center 的 Blender 图只能代表该相机的几何；不能证明完整活动返回集合、内阁职位或引擎随机动作正常。左右中事件相机也要各查实际资源，不能只对照中心镜头。缺退出片段不能拿 idle 冒充退出采样。

## 普通头像、地图圆标与事件小肖像分别校准

相同 shoulders 路由不代表相同 UI 裁剪、遮罩、镜像或纹理请求。定位“头像太大/地图偏位”先追每个控件的实际相机链，再按本人全部外观和特殊形态校准。

- **大小**：固定目标、方向及 FOV 时，沿视线调整 position 与 look_at 的距离；投影比例仅为近似，以真实遮罩图审确认。不改人物模型 scale。
- **位置**：若要平移构图并保持方向和距离，同步平移 position 与 look_at；先核对实际坐标轴、镜像和变换矩阵，不把图像的“上”直接写成世界 Y。
- **隔离**：地图与事件小肖像共享旧镜头但只地图有问题时，可以增加地图专用 selector/相机，沿用已验证 carrier/动画。原版及其他 Pack 的返回值逐语言保持等价，关闭 3D 的 ethnicity 回退保持。
- **骨序兼容**：Pack1Test 013 的 shoulders 27/28 是当时 donor 的兼容契约，既有其余隐藏骨序与轨道保留。别把编号推广到所有 head 骨架，也别因改地图构图重新烘焙正常动画。

Pack1Test 014 使用三人不同头像距离倍率，并给地图位置/目标同步平移，事件小像保持 013 路由。用户“差不多都可以了”只支持 USER_REPORTED_PARTIAL；014 新构图仍需同版本 CK3 实测。

## 采样与旧渲染复用

首帧、严格时间中点、头部位移极值、循环和末帧分别记录，不能把位移极值称为中点。该项目对一基帧号的严格中点定义为 `frame - 1 == frames // 2`；其他采样约定也须明确索引基数。使用真实候选 mesh/asset/anim/camera 和 UI 遮罩，图必须实际打开。

候选修正后复用旧图只适用于已证明的范围：

1. 保留旧图片、result、review 及它们的哈希与候选身份，不重写历史证据。
2. 验证受影响可见/隐藏模型与动画清单是否完全相同；不同就重新渲染受影响 case。
3. 用最终候选重解码每个旧 case 的相机、挂接、帧、位置/目标及其他成像参数，按明确单位/容差比较。位置相同但 FOV、遮罩或环境改变也不能称图像等价。
4. 单独生成 equivalence 收据，绑定旧/新候选、旧 result/图片、采样集合、最大误差与未覆盖范围。超出这些采样或改变引擎路由时，按变化重渲染或记为未测。

Pack3 原 570 图在 native mapping 修正前生成；最终模型清单相同，逐旧采样比较 position/target 最大变化 0.0000074671 cm，并单独保留 `render_equivalence.json`。另 130 张严格中点图直接来自最终候选。这证明有限离线采样几何，不证明 CK3 group lookup 或动态路由等价。

## 证据定位

- [Pack3 交付](D:/CK3-mod/miyabi_3d_mod_project/reports/pack3_test_010/delivery.md)、[映射修正](D:/CK3-mod/miyabi_3d_mod_project/reports/pack3_test_010/native_mapping_fix.json)、[渲染等价收据](D:/CK3-mod/miyabi_3d_mod_project/reports/pack3_test_010/render_equivalence.json)。
- [映射修正实现](D:/CK3-mod/miyabi_3d_mod_project/scripts/fix_pack3_test_native_mappings.py)、[等价验证实现](D:/CK3-mod/miyabi_3d_mod_project/scripts/verify_pack3_render_equivalence.py)：属于当次候选，后续先核对基线，不直接运行旧入口。
- [Pack1Test 014 交付](D:/CK3-mod/miyabi_3d_mod_project/reports/pack1_test_014/delivery.md)、[距离和平移证据](D:/CK3-mod/miyabi_3d_mod_project/reports/pack1_test_014/calibration_evidence.json)。

共享 Camera 会继续升级，历史报告仅证明其绑定版本。用当前 settings、登记与交付收据重新确定基线；不让旧完整 Camera 清单覆盖后续其他 Pack 更新。
