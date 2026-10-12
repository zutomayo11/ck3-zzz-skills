# 纸片人消隐、音擎与混合调频

只在相应问题出现时读取对应章节。工程为`D:/CK3-mod/zzz_mod_project`，生成器和测试位于工程根，不假定存在scripts或tests。当前版本/角色/音擎数量以设置和manifest为准，快照见[共用规范](../../ck3-zzz-3d-mod/references/zzz-core-pack4-workflow.md)。开局提示及双语维护见[构建与登记](build-and-registration.md)，不重复相机/展示规则。

## 纸片人前面的黑模型

复现至少区分：关闭3D且角色有模型、开启3D但角色无模型，以及原版human人物。纸片平面已显示不代表底下原版人体已消隐；不能通过修改3D骨架、镜头或全局资源加载来处理纸片人黑人体。

当前生成入口 `paper_carriers.py` 为anime组生成6个私有透明原版人体载体，完整复制原版pdxmesh/entity文本，仅替换私有名称与材质。原 `.mesh`、骨架、动画、挂点不改；角色包同路径覆盖 `common/portrait_types/anime_portrait_types.txt`，只替换8处head/torso引用，不影响human及私有3D画像组。数量属于本次记录，不硬编码为以后所有版本的固定总数。

材质使用原版 `gfx/FX/pdxmesh.shader` 的 `standard_alpha_blend`，DDS Alpha全0，禁深度写，阴影按Alpha剔除；不能遗留skin材质的 `texture index=3` 或专用defines。旧 `zzz_paper_hide_gene`、`zzz_paper_base_hide` 输出以空注释清退旧规则，不能仅停止生成而让已安装残留文件继续生效。

0.6.2–0.6.4基因/隐藏规则方案已被用户实测否定，不能因引用存在、数值为0或规则测试通过就宣称渲染修复。`test_paper_rendering.py` 验证实际启用包的VFS、全部材质面及原生实体/动画字段；0.6.5载体方案在当前记录中尚无独立实机验收。保留这一边界，不借后续3D镜头确认扩大结论。

## 代理人特性与音擎日志

复用本地JSON、`wengines.py` 与 `build_mod.py`，图标源为 `D:/CK3-mod/绝区零/特性logo`。代理人补对应职能特性，哲、铃除外；旧代理人用现有迁移入口补齐，身份ID和皮肤排序不变。职能特性与元素属性不要混为一套分类。

音擎作为日志宝物，通过混合调频或自选取得；每种音擎全局终身最多一件，销毁也不重造。稀有度映射宝物品质以本地JSON/manifest的已生成字段为准。必须装备在日志栏且拥有匹配特性才有收益，专属额外收益还需匹配代理人身份trait；仅持有、转赠或特性不符不授予属性。介绍保持音擎原介绍，另列CK3装备激活条件和效果，不以人物文案替代；无论是否装备都应显示条件。

首次自选及100余波自选区分代理人/音擎标签，代理人保持原界面，音擎按当前职能特性分类。结果中的音擎使用自己的DDS图片，独立图片控件，不生成假人物或占用角色肖像框；代理人仍用原肖像。

结果名称可用customizable_localization，图片不能依靠本地化返回路径。当前图片控件直接声明静态DDS路径，由结果kind、音擎ID标记控制显隐；重复或已销毁的音擎仍能显示抽取结果，不依赖活宝物scope。空结果窗口默认隐藏，读取结果变量前检查存在，避免进游戏即显示空十连框或 `trait_`。图片方案已有用户确认。

## 混合调频与十连保底（0.7）

- 代理人和音擎同池。普通每抽S 5%、A 15%、B 80%；重复S/A/B分别转40/10/1信号余波。代理人沿用同身份活人判重，音擎按终身创建标记判重。
- 每次十连至少一个A或S。前九抽普通池；若已出现A/S，第十抽仍普通池；否则第十抽S 5%、A 95%。代理人、音擎及重复的A/S均满足保底。
- `zzz_batch_high_rarity` 每批开始清空、结束移除，不把上一批保底状态带入下一批，不改变单抽。保留现有费用、冷却、首次自选与100余波自选规则，相关值以settings为准。
- 新玩法生成到独立 `common/scripted_effects/zzz_role_gameplay.txt`，由 `role_gameplay.py` 重写为 `zzz_role_` 函数。保底函数须列入其私有集合，GUI/decision/on_action调用同步重写；保留 `zzz_create_<agent>` 外观创建接口原样；创建完成后调用可选 `zzz_split_role_created`，Core缺席为空效果。现行Pack已移除21份创建模板，创建归角色包独占，禁止后续生成重新带回Pack。

相关检查按改动选择：`python -X utf8 -m unittest test_wengines`、`test_tuning_ui`、`test_ten_guarantee`、`test_paper_rendering`。使用实际启用包顺序的VFS覆盖组合；角色包单独输出正确不代表和3D包一起加载正确。规则模拟、静态引用与用户实机反馈分开记录，不为局部变化默认运行全部测试或重建3D资源。
