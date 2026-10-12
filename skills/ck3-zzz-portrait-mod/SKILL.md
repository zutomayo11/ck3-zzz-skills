---
name: ck3-zzz-portrait-mod
description: 制作维护 CK3 绝区零角色包的立绘、消隐、身份特质、调频自选、音擎宝物、换装、开局说明、双语与本地登记；涉及拆分后的可选3D接入时配合 ck3-zzz-3d-mod，镜头问题配合 ck3-portrait-camera。
---

# 绝区零 CK3 角色包

代码参考的职责与后续提取范围见[角色玩法参考边界](references/role-code-reference.md)，3D资源算法见[五条核心链](../ck3-zzz-3d-mod/references/code-reference.md)。本轮只提供3D核心算法及玩法/前置分工说明，未移植完整角色生成器。下方版本与本机路径为历史快照，执行时核对用户当前工程，不将旧入口当成通用构建器。

默认中文沟通。素材档案与生成工程分开维护，先定位数据再改对应生成逻辑，不把整个生成目录当手工源码。

当前正式角色包为 **绝区零角色包1.4.0**，保留非3D玩法，共享3D功能已移入独立前置。职责、两种模型接入方式、版本与维护约束集中在[拆分架构共用规范](../ck3-zzz-3d-mod/references/zzz-core-pack4-workflow.md)。版本属于2026-10-11现装快照，后续以实际配置、成品和收据为准；未观察的游戏表现仍为 `NOT_TESTED`。

## 工作入口

- 素材与角色设计：`D:/CK3-mod/绝区零`。
- 角色工程：`D:/CK3-mod/zzz_mod_project`；先读 `AGENTS.md` 和 `settings.json`。
- 正式运行输出：`zenless_zone_zero`，沿用 `zzz_agents_local.mod` 和工坊ID `3806658401`。旧完整角色包只保留校验ZIP，不恢复登记或加入播放集。
- 拆分配置与正式维护：`D:/CK3-mod/zzz_split_test_project/formal_release/settings.json` 与 `promote_formal_split.py`。旧完整 `build_mod.py` 等写入入口已退役，不能为局部玩法修复重跑覆盖转正成品。

新增角色、皮肤、宝物或核对姓名时读[数据与兼容规则](references/content-and-compatibility.md)；开局提示、双语、构建和登记问题读[构建与登记](references/build-and-registration.md)对应节。角色原三项依赖是二向箔核心库、婚舰通用库、女仆之国；二向箔与独立3D前置不同。纯角色包不需要3D前置或模型Pack。

纸片人黑模型、代理人特性、音擎、混合调频与十连保底读[纸片人消隐与调频](references/paper-rendering-and-tuning.md)。仅加载当前问题所需部分，数量和字段从现装清单与当次源数据读取。

## 可选3D接入与职责

角色包独占代理人创建、身份和 `zzz_skin` 映射。创建完成后调用 `zzz_split_role_created`；无前置时是安全空效果，有前置与对应Pack时接入模型。没有对应Pack继续立绘，不改变调频限制、费用、自选机会、冷却或皮肤编号。

共享相机、展示姿势、小头像/地图、理发店动作、3D开关和外观恢复属于独立前置；人物模型、动画及挂点属于Pack。联用时普通人物直接选模型在交互、窗口和执行效果三层禁止。不要为联动修改人物特质或把3D模板放回Pack。

展示与死亡读[展示待机、静态头像与死亡](../ck3-zzz-3d-mod/references/portrait-display-and-death.md)，道具/取景/接触读[专项约束](../ck3-zzz-3d-mod/references/mount-contact-and-framing.md)。按实际职责定位独立工程与Pack，不通过角色数据或存档修改掩盖资源/调用错误；历史 `core_integration` 不再是现行共享3D来源。

## 执行方式

1. 从当前设置、短状态和清单定位目标；源JSON、玩法生成器和历史 `build_mod.py.load_data` 可供读取算法，不意味着允许旧全量输出。路径失效先搜索现有工程。
2. 明确实改文件，保持角色ID、皮肤排序、旧档迁移和可选回调。新修复基于当前正式输出做定向候选与独立收据，不重复运行已有转正的candidate/install。
3. 运行最小相关测试与静态验证，检查透明DDS、双语、GUI、作用域及真实启用组合；规则模拟不等于CK3显示验收。角色玩法变化不触发模型资源重建。
4. Mod功能升次版本、修复升补丁，每轮仅递增一次，并同步对应配置、descriptor、登记和说明；仅技能更新不升Mod版本。缓存写入需要游戏及实际启动器关闭，并保留工坊ID和非目标用户状态。
5. 正式回读/撤销/中断恢复遵循[共用维护约束](../ck3-zzz-3d-mod/references/zzz-core-pack4-workflow.md#验证安装与精确恢复)；外部变化停止，不刷新基线绕过保护。用户仅授权制作/修复，不自动发布、改订阅或切换播放集。

续接复用最近短状态和必要取证，不反复读完整历史。用户已要求不使用computer-use，缺游戏证据就标明待用户实测，不另建UI helper绕过限制。技能目录只保存流程与参考，不复制角色图片、游戏资源或私人存档。
