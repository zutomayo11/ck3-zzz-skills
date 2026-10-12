---
name: ck3-portrait-camera
description: CK3 3D角色肖像相机、隐藏定位节点、RUI大肖像姿势不同步及事件、活动、载入取景的诊断与回归；绝区零按独立3D前置／正式模型Pack契约定位来源，模型提取与完整动作制作由对应技能处理。
---

# CK3 肖像相机与 ZZZ Core 适配

把相机工作分为入口调用、资源挂接和构图证据。先保护正常入口，在隔离候选中做有证据的最小修改；静态、离线图像与游戏验收分别记录。

## 当前工作线

绝区零项目先读[独立3D前置／正式模型Pack工作规范](../ck3-zzz-3d-mod/references/zzz-core-pack4-workflow.md)。2026-10-11现装快照为角色包1.4.0、独立前置1.1.0（内置RUI 20可选兼容）及六个本地正式Pack均1.0.0；25个私有画像组。共享GUI与相机运行来源是 `D:/CK3-mod/zzz_split_test_project/mods/core`，正式转正配置与冻结候选在该工程 `formal_release`，RUI增量收据在 `rui_compat_110`。角色工程 `core_integration` 和 `D:/CK3-mod/zzz_core` 只作历史来源，不回写。具体接口、模式与维护边界按共用规范；实际成品和收据优先。

- 独立3D前置管理相机、分流、事件/活动覆盖和诊断；Pack 管理隐藏载体及动画。角色作用域、画像组和资源契约均满足后才进入私有路径。
- 特殊事件保持原版调用与动作树；活动两队列接入人物使用私有center，普通人物保留typed `GetCamera`。指定骑乘/战车定向取景作为当前有限例外，按源码审计，不恢复旧420别名。
- 隐藏head保留基础占位、角色扩展、动态节点和预加载；torso零基2/75与head22兼容定位槽按实际祖先挂接计算。骨数/骨名不证明引擎取点；按本人状态及重复序号验证头身同步，不重复插骨或全局预加载torso。
- 使用 `zzz` 命名，保护既有 ZZZ Core数值/定位、可见模型、原骨序、蒙皮、身体动作、表情、眨眼与道具。只修单入口不连带校准正常入口。

## 按问题读取

- RUI主角/配偶全身或半身大肖像不跟随默认/手选姿势：[RUI可选肖像兼容](../ck3-zzz-3d-mod/references/rui-optional-compatibility.md)。先查固定`idle`是否绕过展示选择器，保持相机和六包资源；无RUI及两种顺序需独立核对，不因肖像变大就校准骨架或改相机。
- 默认姿势、小头像、地图标记和死亡入口：[展示待机与死亡](../ck3-zzz-3d-mod/references/portrait-display-and-death.md)。静态API与动作选择分开核查，死亡第一阶段尚待实机。
- 马/车缺失、取景裁切与人物悬空：[道具与接触约束](../ck3-zzz-3d-mod/references/mount-contact-and-framing.md)。缺失、裁切和接触错位分别取证。
- 圣人／封圣人物光环缺失或被裁切：[圣人光环装配与维护](../ck3-zzz-3d-mod/references/saint-halo.md)。先核对`saint`／宗教条件与私有画像组装配，再核对实际头部挂点、相机和遮罩；现行六包没有为光环修改GUI或相机。

## 工作流程

1. 核对最终 VFS 和来源，分别记录 GUI、角色作用域、slot、环境、动作/别名、脚本覆盖、相机、group/type、entity、节点与动画。
2. 逐入口列清单：面板/配偶/头像、HUD/地图、内阁/战争/生活方式、事件及特殊窗口、活动进行中/结束、载入、书签/切人、理发店与宫廷。不用一个事件或菜单镜头代表全部。
3. 区分纹理未生成、调用错误、资源未加载、节点归属、动画变换、相机参数与 UI 裁剪。先查最直接证据，不在失败路径上同时修改多个层次。
4. 冻结正常基线、改动白名单和保护哈希。共享 GUI/相机/节点改变时扩大受影响回归；新私有名字不自动证明普通人物隔离。
5. 验证引用、动作树语义、节点归属及同步，再检查实际候选构图。游戏入口未观察即 `NOT_TESTED`；用户确认仅覆盖其实际反馈范围。

## 保护与验收

原版男女/儿童、其他角色和 3D 关闭路径保持。世界坐标相等不证明引擎选中相同节点；节点同名、日志无错、定义数量和 Blender 手工选点均不是运行时证据。现行调用以最新交付为准，历史成功探针不能作为继续保留已撤旧别名的依据。

单入口合入冻结完整 GUI→路由→相机→节点/动画链；版本回退核对完整基线、增量与较新残留，不能混用版本。按当前事务入口安装，仅回退本轮写入；不修改存档、播放集、工坊，不使用 computer-use。

图像记录候选哈希、角色/外观、入口、真实动作/帧、相机与载体、分辨率和裁剪。Blender 读取实际成品资源，首帧/严格中点/极值/循环各有用途，不能自动居中代替成品相机。只做文本/路由小改时不默认重烘模型；变更影响什么就验证什么。

## 按需参考与只读工具

- [路由与入口清单](references/routing-and-camera-families.md)
- [隐藏载体与校准](references/carrier-and-calibration.md)
- [Blender 与运行时证据](references/blender-and-runtime-validation.md)
- [失败案例及单入口合入](references/regression-and-failure-cases.md)
- [本机证据索引](references/local-project-evidence.md)
- [ZZZ Core 与 Pack 归属](references/standalone-camera-ownership.md)
- [共享画像组与采样隔离](references/shared-groups-and-entry-isolation.md)
- [相机快照导出边界](references/project-camera-catalogue.md)

`scripts/audit_camera_chain.py` 只索引文本定义、Custom、预期返回与动态接口引用；不解析完整事件动作树、活动别名传播或二进制同步，未扫描的依赖不能断言缺失。`scripts/export_camera_catalogue.py` 只导出带来源哈希的定义快照；不携带旧成品快照冒充现装版本。报告模板为 `assets/camera_validation_report.template.json`。相关行为场景是人工决策检查材料，自动结构检查不证明代理行为或游戏成功。
