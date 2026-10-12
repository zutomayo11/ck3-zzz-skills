# 圣人光环装配与维护

用于圣人／封圣人物在ZZZ三维肖像中缺光环、位置或裁剪异常，以及新增Pack复用。当前规则是模型包的装配兼容；二维立绘没有新增绘制光环。

## 原版链与缺口

`saint → 特质肖像修饰 → 光环特殊基因 → 附件 → head节点 → 原版发光Shader`。封圣流程会添加`saint`，无需再造封圣变量或更改人物信仰。

| 层 | 实际规则／资源 |
|---|---|
| 触发 | `traits = { saint }`，`trigger = { faith.religion = { is_in_family = rf_abrahamic } }` |
| 原版修饰 | 游戏`gfx/portraits/trait_portrait_modifiers/00_trait_modifiers.txt`的`saint`，只向`dna_modifiers.human`装配 |
| 原版基因 | `common/genes/08_genes_special_visual_traits.txt`的`character_halo`／`christianity_religion_halo` |
| 附件／实体 | `gfx/portraits/accessories/props.txt`的`pam_christianity_religion_halo`；实体`pam_christianity_religion_halo_entity` |
| 挂点 | `bn_h_head_mid`；当前六包实际引用的隐藏head均保留该节点，零基第22槽 |
| 渲染 | `gfx/models/portraits/attachments/halo/pam_christianity_religion_halo.asset`，`mesh_vfx_head_halo`，`gfx/FX/pdxmesh.shader`／`pdxmesh_vfx.fxh` |

光环是朝向相机的3D发光附件，原版Shader将其沿视线移到头后。原版规则不会自动适配私有画像组。人物主面板的“Saint version”GUI分支只是取图入口，不会替私有画像组补附件；不要把死亡入口维护当作光环修复。

## 私有画像组接入

1. 从当前成品`common/portrait_types`解析每个真实`group/type → head entity → pdxmesh → file`。合法解码该mesh的骨架，核对挂点唯一性、父链和实际动作下的变换；不搜索未被引用的备用mesh后就宣称兼容。第22槽是本项目现行兼容契约的快照，不能凭槽号或骨名推断画面位置。
2. 为本包每个画像组注册私有光环特殊基因和男女模板映射；保持一角色一基因文件，与现有来源结构一致。光环特殊基因不写入人物持久DNA。
3. 私有附件显式设本人的`portrait_group`，`node = "bn_h_head_mid"`，引用原版光环实体。特质肖像修饰只向本包画像组以`mode = add`装配私有基因，保留上述原版宗教条件。不覆盖原版`saint`组，不读取`zzz_skin`等活人变量，不改变换装/手选优先级。
4. 注册由各包独立携带，缺席包不留下其未知画像组声明。共用原版mesh、贴图和Shader；角色原mesh、骨序、权重、比例、动画、表情、眨眼及正常相机保持。

当前命名为`<角色前缀>_saint_halo`与`<角色前缀>_saint_halo_accessory`。运行文件是`common/genes/43_<前缀>_saint_halo.txt`、`gfx/portraits/accessories/43_zzz_saint_halo_packN.txt`及`gfx/portraits/trait_portrait_modifiers/43_zzz_saint_halo_packN.txt`。前缀从实际实体读取，保留旧`zzz_p1t`／`zzz_p3t`／`zzz_p4t`内部标识。

## 生成来源与新增包

工程为`D:/CK3-mod/miyabi_3d_mod_project`。可复用源码是`scripts/zzz_saint_halo.py`的`catalog(pack_root)`与`overlay(pack, groups)`；现有冻结覆盖在`sources/zzz_saint_halo/overlay/<包目录>/`，索引`manifest.json`。各包`sources/<包目录>/settings.json`记录`saint_halo_adapter`与`saint_halo_source`。

**生成器的`PACKS`、包编号及25人断言，以及配套测试的64组合范围固定于六包交付，不直接支持Pack7。** 新包先明确本包目录、编号、真实画像组与模板，再在新包的独立定向构建入口复用/参数化上述函数，合入其候选、清单与测试；不能重跑现有`generate()`、已冻结六包candidate/install，或重烘旧包以添加注册。后续重建已适配包也要显式合入该覆盖；settings记录来源不等于旧构建器会自动消费它。

## 界面与验证边界

人物主面板（含圣人／牧民）、左下角HUD、生活方式、内阁、普通小头像、地图小头像和载入卡沿用既有肖像装配。先查触发/注册/挂接，再查相机、遮罩和裁剪；不把缺失附件修成逐界面2D叠图，不把静态`GetPortrait`改为持续动画，也不虚构载入`SaveGameItem`的人物Custom接口。

验证新包男女模板能解析到实际附件、原版实体和有效挂点；对比圣人/非圣人、亚伯拉罕/其他宗教，并确认没有活人变量读取。按当次包范围核对注册名称唯一性、缺席包回退及引用闭包；保护未改资源和用户状态。现行25组/50类型、37份注册、7项测试及64子集只支持六包本轮的有界注册链验证，不是全游戏VFS重审或实机通过。

各入口仍需分别实测不同体型、换装、动作、活人/已故圣人、重启/读档的大小、位置和裁剪。未观察画面为`NOT_TESTED`；保留既有死后换装限制。不能因挂点存在或离线规则通过就称光环在所有界面正常。

## 当前归属与历史证据

现行六个本地Pack均1.0.0，仍保留本包光环注册；独立前置提供共享显示入口，光环资源来自CK3原版，角色包不提供新封圣或二维光环。当前路径、版本与维护入口见[共用规范](zzz-core-pack4-workflow.md)。

以下是转正前的2026-10-10历史安装快照：角色包1.3.0不变，Pack1–5 2.0.5／Pack6 1.0.1。原模型/动画/DDS/Shader/相机/GUI均无本轮写入。详见工程`reports/zzz_saint_halo/delivery.md`、`payload.json`、`installation.json`、`verification.json`与`review.json`；实际画面均`NOT_TESTED`。

下列是历史光环轮次入口，保留用于核对旧证据，不对当前转正包执行写入/恢复；历史verify也可能因后续授权变化拒绝，不解除保护。

```text
C:/Python312/python.exe -X utf8 -B D:/CK3-mod/miyabi_3d_mod_project/scripts/repair_zzz_saint_halo.py verify
```

历史同入口`restore`／`recover`仅针对当时光环轮次；关闭游戏与实际启动器，外部变化停止。restore精确回到Pack1–5 2.0.4／Pack6 1.0.0，保留角色包1.3.0与此前修复；实际成品restore尚未执行。已安装后不再执行candidate/install，不使用旧全量恢复覆盖后续状态。

当前测试为工程`tests/test_zzz_saint_halo.py`与`test_zzz_saint_halo_maintenance.py`。Pack6旧首次登记测试在本轮安装前因已登记而报错，见`pack6_regression_tests.log`；不为通过该历史用例撤销登记或修改数据库。
