# 原生理发店皮肤与人物模型消失

适用于角色包内置 绝区零绝区私有相机／正式模型包工作线的外观列表、换肤不生效、人物剪影和理发店空模型。动作名称与原生武器隐藏另见 [动作与道具](barbershop-native-idles.md)。只检查本次受影响的人物和入口，不重建未变的模型或动画。

## 原生皮肤注册：自动装配与手动列表是两条链

当前四个正式包均按原生列表与“跟随角色包”契约维护；逐角色配置及最终装配优先。以下是历史来源：Pack4Test 0.1.7 有自动外观装配和“跟随角色包”，但没有可手选皮肤注册；不能因参照它便宣称理发店已列出皮肤。旧正式 Pack4 的原生 `add_accessory_modifiers` 是列表参考；Pack1/3Test 0.3.2、Pack4Test 0.1.8 按此结构接入。版本只是证据索引，先读现装文件。

在人物已有的 customization 分组中保留空跟随选项，并逐模板增加条目。下面是结构示例，实际名称取当前包配置：

```text
custom_zzz_p4t_alice_clothes = {
 portrait_group = zzz_p4t_alice_g
 usage = customization
 interface_position = 2
 zzz_p4t_alice_clothes_follow = { dna_modifiers = { } }
 add_accessory_modifiers = { gene = zzz_p4t_alice_outfit template = zzz_p4t_alice_base }
 add_accessory_modifiers = { gene = zzz_p4t_alice_outfit template = zzz_p4t_alice_swimwear }
}
```

- 追踪画像类型、每人物独立 customization_rules、gene group 与颜色/服装容器，确保界面分组属于被操作人物。只有 gene/template 定义不会自动形成菜单列表。
- 每个选项使用本人特殊基因及现有模板。按角色包实际 `zzz_skin` 索引映射，不按文件排序或显示名称猜编号。只有基础皮肤的人物也保留基础选项和跟随。
- 中英皮肤名沿用角色包 `zzz_skin_set_<trait>_<index>_label`。补模板裸键、`PORTRAIT_MODIFIER_<custom-group>_<template>`、分组及跟随项本地化；YML 用 UTF-8 BOM，检查键唯一。
- 自动分支继续根据 `zzz_skin` 互斥选中一个外观；保留缺变量、默认值及未知值回退。原生手选作为 customization 覆盖，选择跟随后恢复自动读取。**不新增第二套手动变量，不承诺两个入口双向同步，不为列表修复新建 绝区零绝区私有相机 GUI。**
- 角色包按钮仍写 `var:zzz_skin_target` 指向的人物；不要误写玩家 ROOT，也不要复制 DNA、切 ethnicity 强制刷新或改角色包接口。旧解析器可能丢掉键中的冒号，作用域验证须能拒绝无目标作用域的 setter。
- 对形态影响挂点的角色，以实际可见附件的私有 `set_tags` 和道具分支 `required_tags` 选节点。爱芮手选形态可能与 `zzz_skin` 不同，普通与 alternate 入口都需按相同实际标签分流，名称及 绝区零绝区私有相机 调用保持。四外观、两套入口、所有存储皮肤值交叉检查，不能只测自动换肤。

## 特殊基因的操作限制

先读取实际 gene 定义类别。当前外观在 `special_genes/accessory_genes` 下，自动装配使用 `mode = add`。引擎的 `modify`、`modify_multiply`、`replace` 只适用于 regular genes；**不能为避免推测中的叠加而把特殊外观基因改成 replace**。自动权重互斥与基因操作合法性必须分别验证。

Pack1/3Test 0.3.1 的 replace 是已知失败用例：出现人物剪影、理发店无模型。0.3.2 恢复 add；这证明应撤销错误操作，不代表其他空模型都由此引起。旧验证器曾要求 replace 才通过，必须撤除这种镜像实现的断言；负例按真实基因类别拒绝非法操作，不能禁止 regular genes 的合法用法。

## 模型消失：按阻断链取证

先冻结对应版本、启用顺序、人物/外观/入口、截图及当次 error.log。日志会被下一次启动覆盖；若原日志已丢失，明确标为此前观察，不能拿不同播放集的新日志冒充原始证据。

1. 确认实际启用的 Test 包、本人身份、3D 开关与私有 ethnicity，区分包未加载、身份未接入和渲染失败。不要为排查改存档。
2. 从 `portrait type → head/torso entity` 及 `customization rule → 实际基因类别/操作 → template → accessory → entity → pdxmesh → 材质/Shader/include/贴图` 两条链交汇检查；覆盖每套皮肤，而不是只证明变量或权重变化。
3. 缺 customization 注册时按角色拆独立规则文件，并核对 gene group/颜色容器；不要认为多组写在一个文件就都会被引擎识别。先用最新日志证实，不一律重写所有注册。
4. Shader include 按实际 `gfx/FX` 根解析；逐可见材质检查 Effect、编译和贴图闭包。不能用相对于 Shader 文件目录的“文件存在”检查掩盖真实缺引用。
5. 只有材质与装配通过后仍有取景/道具节点错误，才沿当前隐藏 head 的加载、节点归属和挂接检查。小型 head 的 `streaming = Never` 不是可见模型统一预加载方案；不同时更改相机参数、骨架、动作和材质来碰运气。

直接把 mesh 加进 Blender 的预览绕过了画像注册、基因与附件选择，不能证明游戏人物会出现。报告明确区分资源预览、装配静态检查、游戏画面。先让用户在同存档/同组合确认原失败人物恢复，再扩大皮肤、表情/眨眼、道具和其他场景验收；未观察均为 `NOT_TESTED`。

## 定向验证与恢复

- 负例覆盖特殊基因非法操作、漏列表项、重复/串人物选项、断模板或实体、错本地化、错操作人物、跟随回退以及形态挂点错误。
- 菜单文本修改优先检查完整装配和自动分支保持；未变 mesh/anim/DDS/Shader 用哈希证明保持，不重新烘焙或重复宣称逐帧/编译实测。
- 从最终候选验证受支持组合和共享注册冲突；安装前检查游戏及实际启动器关闭，逐文件 journal 与回读。保护当前用户状态，不套用旧播放集快照。
- 区分精确撤销本轮和可用模型恢复。若安装前版本已知失败，默认故障恢复不能回到它；提供保留 add 的模型恢复候选，并清楚标明恢复操作是否实际执行。

本机实现与证据：工程 `scripts/zzz_pack13_032.py`、`scripts/repair_zzz_pack13_032.py`、`scripts/repair_pack4_test_018.py`；对应 `reports/zzz_pack13_032/`、`reports/pack4_test_018/`。只使用当前维护入口，历史生成器只读；这些离线报告不自动构成用户实测通过。
