# 宫廷动作与地面基准

工程路径、版本与权限沿用 SKILL.md。此页适用于宫廷动作未播放、朝向或站立高度异常；道具问题另见 [挂接排查](retarget-and-blink.md#道具加载与挂接排查)。

范围规则：制作新 Pack 仅为新增角色建立或校准宫廷/王座路由、ground_joint 与实际脚底支撑面。此前完整包的脚底基准、辅助骨、动画和验证结论直接沿用；没有当前异常证据，不重新测量旧角色或遍历旧包重建。以下历史全链校验用于对应角色发生变化或明确完整重建的任务，不能当作每次新包的默认检查。

## 先区分三个问题

| 症状 | 首先检查 |
|---|---|
| 只播放本人 Galgame_Idle | 实际肖像类型、类别分支、default.hm_idle 条件及实体 dead 映射 |
| 已交谈但朝向或姿势不对 | 当次场景分配的动画类别、实际 asset 引用、成品骨盆朝向与原版源动作 |
| 已播放场景动作但脚部沉地 | 场景用的锚点、实际蒙皮脚底、每角色及各外观的支撑面 |

用户明确选择沿用原版随机场景，不按职位强制姿势或站位。原版 `gfx/court_scene/character_roles/00_default_roles.txt` 可给内阁成员分配交谈等随机角色；位置来自 scene_settings。不能仅凭“军事总管未拿剑”判定绑定错。静态截图不能证明是否播放动画，必要时先问清实际动态表现。读取日志或存档前核对其时间和启用包；旧 last_save 不代表截图中的当前场景，二进制存档不能用 Get-Content 当文本读。

## 本人待机覆盖场景动作（1.0.3）

本包3D角色仍保留纸片人身份。共享 animations.txt 的 `default.hm_idle` 原本只检查 `waifu_portrait_trigger = yes`，权重增加32767并请求 head/torso 的 dead。实体 dead 为旧菜单兼容映射到本人 Galgame_Idle，因此需要同时检查默认回退，不能只验证专属动画分支和文件存在。

`scripts/court_animation_fallback.py` 给 hm_idle 增加 `NOT = { zzz_3d_animated_portrait_trigger = yes }`，按实际本包3D ethnicity 排除回退。不要全局改 waifu_portrait_trigger、角色身份、真正死亡类别或旧菜单兼容状态。

现行正式包以角色包内置 绝区零绝区私有相机 的包可用性、身份和实际画像分流为准，不重新安装下列旧桥。历史旧桥曾由各包共享 `common/scripted_triggers/000_zzz_court_animation_defaults.txt`，对缺失的包默认返回 false；各包后加载的 `zzz_court_animation_pack*.txt` 仅引用本包存在的 ethnicity。共享接口实改时保持共享文件字节一致，并检查受影响启用组合、关闭3D后的纸片人及其他角色；数量从当前包清单推导，不固定三包七组合。接口未变不重复检查旧组合。`tests/test_court_animation_fallback.py` 还检查幂等和原规则保留。

1.0.3 的离线测试证明存在并排除了上述条件冲突；随后截图可见莱卡恩采用了交谈姿势，但未取得运行时跟踪证明所有宫廷类别的具体继承路径。不要把截图或条件求值扩大为全场景实测结论。

## 分离原生根与场景锚点（1.0.2）

原生根常在骨盆高度，不能直接作为站立 ground_joint。`scripts/court_grounding.py` 保留原根为 `zzz_native_root`，在骨序末尾追加无权重 ground_joint；body_root 继续供王座定位。这一节仅解释旧身体地面基准，不能据此重接当前隐藏 head。当前正式模型包按实际挂接使用 ground_joint → zzz_cam_root，保留独立动态地面道具节点，见[当前契约](zzz-core-pack4-workflow.md)。

normalize 去掉辅助节点并恢复旧别名，必须精确还原原网格、骨序、权重和动画轨道。`reports/court_grounding.json` 保存输入/输出哈希，base_hash 只在实际输出匹配审计记录时追溯旧数据；不能跳过身体、表情、镜头或道具校验。辅助节点不是新增蒙皮骨，不能给它权重或更改原骨编号。

## 零点不等于脚底（1.0.4）

1.0.2 把辅助节点固定在世界零点，旧测试只检查该节点为零，仍漏掉莱卡恩约20cm的脚部穿地。源转换 `convert_victoria_models.py` 计算归零边界时排除了含 Weapon 的对象，但 Lycaon_Weapon 实为机械腿。成品绑定脚底 Y 约 -19.270859cm，交谈时约 -19.8cm。这是按网格测出的本次数据，**不要把该数字硬编码为所有角色或未来外观的补偿**。

当前 `character_floor` 从每套实际导出网格里脚/趾权重合计超过0.5的顶点测量绑定脚底，计入机械脚。同角色各外观共享 torso 姿势，采用所有外观最低脚底与零点中的较低值作为支撑面；原先高于零点的离地设计保留。新角色若没有可识别的脚部权重，应报错并检查实际骨架，不能静默返回零或套别人的高度。

mesh 辅助骨的逆绑定对应该支撑面；动画辅助轨道为 `inverse(native_root) × support_plane`，使其世界位置稳定在测得的 ground_y。只改辅助节点，保留原身高、比例、骨长、身体/表情轨道、王座 body_root、镜头和道具。不要通过统一缩放、拉腿、逐帧强压脚底或固定前后偏移掩盖问题。

验证要蒙皮实际脚部顶点，再减去实际场景锚点的世界高度；不要只测静置顶点、骨盆或节点是否为零。分别覆盖角色、外观、交谈随机变体、内阁、王座；身体数据不变和站位正确是两类证据。预览用统一世界比例及地面，不能逐人自动缩放取景。

## 历史算法与局部验证入口

维护采用旧流水线的包时，按其收据核对 `scripts/build_faction_packs.py` 的阶段顺序；新 绝区零绝区私有相机 工作线按共用规范定向生成，只向这些阶段交给受影响包/角色：必要时先还原目标已有辅助节点，再完成资源集成、菜单镜头、道具和材质处理，最后运行 court_grounding 和 court_animation_fallback。不能为制作新包调用遍历旧包的全量 build，也不还原或重施未改旧包的地面节点。后续原生重导出不能视为最终发布包。court_grounding 先临时生成并回读当前目标的全部受影响资源，再替换成品；只备份将实际变更的文件及相关报告。

相关验证在正式工程内执行，以下是可选验证集合；只选择当前异常或新增角色涉及的模块，并确认实际目标筛选。没有二进制变化不跑全包 `--binary-check`；既有测试固定检查未改旧人时不为通过它而重建旧数据。不必为技能文档更新重建 Mod：

```powershell
python -X utf8 -m unittest tests.test_court_foot_floor tests.test_court_grounding tests.test_court_animation_fallback tests.test_retarget_props tests.test_pack_menu_camera tests.test_menu_presentation tests.test_pack_retarget tests.test_court_body_selection tests.test_pack_workshop_cover -v
python -X utf8 scripts/pack_retarget.py --binary-check
```

1.0.4 实例：33项测试、8人3816个片段及17套外观通过。实际脚底覆盖646个外观/动作组合，每段九个时点，最大下探约0.564cm；这不是所有动作的全帧或游戏实测。4128个资源的原始数据可逆还原，其中2095个文件仅辅助节点变化。来源为工程 `reports/court_character_floor_1_0_4.md`、`court_support_1_0_4_all_variants.json` 和 `court_grounding.json`；数量应以当次报告为准。

`work/preview_feet_1_0_4.py`、`work/check_court_support_1_0_4.py` 是本轮诊断示例。带版本号的发布/审计脚本依赖当时版本和备份，不要直接套到下一版。1.0.4 尚待用户冷启动游戏复测；技能更新请求本身不等于实机通过。
