# RUI可选大肖像与姿势兼容

用于打开RUI后，主角色或同地点配偶的大肖像不跟随本人默认、原版默认和其他手选姿势。先查实际GUI动作参数，再判断相机或资源问题。归属与独立/联用模式见[共用规范](zzz-core-pack4-workflow.md)，通用权重及死亡路由见[展示与死亡](portrait-display-and-death.md)。

## 当前来源与范围

2026-10-11本机交付为前置1.1.0、角色包1.4.0、六Pack1.0.0；兼容内置于独立前置，不另建兼容Mod，不要求角色包或RUI必需依赖。当前来源如下，后续先核对实际descriptor、成品和收据，不能凭工坊ID假定未来版本内容相同。

| 用途 | 本机位置 |
|---|---|
| 正式运行根 | `D:/CK3-mod/zzz_split_test_project/mods/core` |
| 适配GUI | 运行根下`gui/00_000_zzz_rui_portraits.gui` |
| 生成、事务、测试 | 拆分工程`rui_compat.py`、`repair_rui_compat.py`、`test_rui_compat.py` |
| 交付与证据 | 拆分工程`rui_compat_110/delivery.md`、`installation.json`、`verify.json`、`gui_audit.json`、`pose_audit.json` |
| RUI 20.0只读源 | `D:/steam/steamapps/workshop/content/1158310/3239002020`，`gui/00_shared/RUI_Ch_portraits.gui`及`gui/00_views/RUI_Ch_main_character_view.gui` |

适用本机RUI:Character Unofficial 20.0的基础肖像类型，不包含AGOT、obfusCKate等扩展组合。六包模型、动画、Shader和相机资源保持。UI兼容改共享调用，不以重烘动画、插骨或调整相机替代入口修复。

`formal_release/candidate/core`仍是前置1.0.0转正冻结基线，当前RUI增量没有回写该历史候选。未来维护从现装运行目录与最新增量来源建立新候选，不能直接用转正候选覆盖1.1.0，或只更新版本号却遗漏适配GUI。

## 入口与两种默认

RUI类型`portrait_character_view`有成人全身/半身及婴儿全身/半身四个分支。成人原请求用`Character.GetAnimatedPortrait`，分别固定`camera_body/idle`与`camera_torso/idle`；主角和同地点配偶两处消费同一类型。固定`idle`绕过Core手选标志所作用的展示类别。

仅把两个成人请求的动作参数替换为`Character.Custom('zzz_core_display_animation')`，环境、相机、尺寸、遮罩、布局、监禁覆盖及API保持。选择器在活人、实际模型、对应Pack可用及3D开启时返回`zzz_core_menu_idle`，其他路径回退`idle`；按实际ethnicity/模型判断，不添加或要求代理人身份特质。

| 选择 | 当前手选标志 | 展示类别中的状态 |
|---|---|---|
| 本人Galgame默认 | `zzz_pose_native_idle` | `zzz_iface_menu_zzz_native_galgame_idle_torso` |
| CK3原版默认 | `zzz_pose_vanilla_idle` | `zzz_ck3_game_idle_entry` |
| 其他支持的手选 | 当前角色的`zzz_pose_*`集合 | 沿已有规则与状态，不新建第二套标志或动画菜单 |

核对Core的`common/customizable_localization/41_zzz_display_pose.txt`、双语`zzz_display_pose_l_*.yml`、`gfx/portraits/portrait_animations/animations.txt`中的真实类别、flag、权重、head/torso配对和女性画像别名。仅修改类别`default`或模拟器返回值，不能证明真实手选规则已接入。

## 无RUI闭包、顺序与分支

1. 适配文件只定义RUI所用`portrait_character_view`，不覆盖原版`portrait_character_view_main`或其他窗口。扫描当前游戏/Core及支持组合，确认无RUI的原窗口没有消费新增类型；模板、纹理及数据函数都由游戏/Core解析，不留下RUI专用符号或新增必需依赖。
2. 本机RUI 20四个空/隐藏扩展钩子`RUI_Ch_OBFS_template_21`、`RUI_Ch_AGOT_type_12`、`RUI_Ch_OBFS_type_09/10`从适配类型移除。先核对真实定义；这只支持当前基础RUI，不表示可以删掉其他版本或已启用扩展的有功能钩子。
3. 全身/半身依据已有`VariableSystem.Exists('RUI_Ch_portrait_torso')`。普通婴儿的坐姿条件为年龄小于1且`StringIsEmpty(Character.Custom('zzz_cam_is_zzz'))`；普通婴儿保留原`frontend_right_idle`/`idle`请求，已经独立选为ZZZ模型的婴儿走模型展示入口。四个分支互斥完整。
4. RUI死亡仍用原`Character.GetAnimatedPortrait`及展示选择器的`idle`回退；此轮不增加`EvenIfDead`入口。原版主面板的死亡修复、死后换装变量问题及RUI死亡表现分别记录，不能互相代替验收。
5. 推荐RUI→独立前置→Pack，不自动改变播放集或顺序。先组装同路径覆盖后的VFS，再按当前GUI定义选择规则核对不同路径同名类型的获选来源。现行适配路径早于RUI源路径，三种静态情景仅此类型来源变化；真实引擎加载与画面仍需实测。

化简RUI专用条件时，直接保留原生`And`/`Not`分支及`Character.IsImprisoned`。此实现不使用未经原版确认的`True`/`False`数据常量；Python模拟器接受某个值不构成CK3语法证据。未知函数、上游结构变化或无法解析的依赖应停止候选生成并定位来源，而非把未知值默认成false继续安装。

## 验证与证据层次

- 无RUI及两种RUI/Core顺序分别核对定义与消费入口、原生引用闭包、其他类型获选来源保持；不能只比较文件名或只在源目录检查。
- 两种默认及该角色全部支持手选读取实际规则；分别覆盖模型/普通人物、Pack缺席、3D开关、活人/死亡、婴儿、主角/配偶、全身/半身。普通人物真实选择器探针不得附加ZZZ身份。
- 对六包、角色包与未改Core运行文件保留完整哈希和元数据基线。此类GUI改动不触发模型或动画重烘。
- 候选、安装和回退使用真实临时ZIP事务与SQLite演练，检查未知文件、候选变更、重复安装、中断及等大小等时间戳的资源修改。SQLite连接须显式关闭：`with sqlite3.connect(...)`只负责提交/回滚，不保证关闭，Windows原子替换前用`contextlib.closing`等可靠释放方式。
- 本轮73项相关回归、14项专项复核、25组/8,150条手选/208选择器状态及三种VFS静态情景通过；这些数字只描述该交付，不是未来模型数量或游戏覆盖目标。GUI画面、即时刷新及实际加载顺序仍NOT_TESTED；游戏验收需分别切换两个默认和其他手选，检查主角/配偶、全身/半身及无RUI回归。

## 维护与精确回退

本机已安装后只使用下列动作，不重跑candidate/install，也不把这个已冻结增量入口当作未来任意功能重建器：

```powershell
C:/Python312/python.exe -X utf8 -B D:/CK3-mod/zzz_split_test_project/repair_rui_compat.py verify
C:/Python312/python.exe -X utf8 -B D:/CK3-mod/zzz_split_test_project/repair_rui_compat.py restore
C:/Python312/python.exe -X utf8 -B D:/CK3-mod/zzz_split_test_project/repair_rui_compat.py recover
```

修改前按当前授权范围冻结独立候选与保护清单；安装/回退/恢复前关闭游戏和实际启动器。`restore`只撤销本轮9个目标，删新增GUI、恢复前置1.0.0及登记/SQLite/维护文件原字节；六包、角色包、存档和播放集不回滚。`recover`在任何写入前对受保护包做完整哈希核对，仅比大小/mtime会漏过同尺寸同时间戳改动；外部变化拒绝继续。

本轮收据目录内`core_100_preimages.zip`、`transaction_spec.json`、`protection.json`及`installation.json`共同限定目标、备份和状态。初次真实安装→精确回退的取证在`rui_compat_110_initial_retired`，它是退役证据，不可再次安装。最终候选已重新审查和安装，不把初次回退演练描述为最终版本游戏通过。

活动增量期间，旧`promote_formal_split.py verify`转发本轮验证，旧全量restore/recover拒绝；精确回退后旧维护文件恢复原字节。用户后续启动器/登记/存档变化保留并记录，不改旧收据或放宽校验来消除差异；未来获授权更新可建立新的当前保护基线与独立收据。

仅更新本技能不执行这些模组命令、不修改模组或用户状态、不递增Mod版本；代码、模型、贴图、SQLite备份及存档不复制进技能目录。
