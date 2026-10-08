# 原生资源到 CK3

新 Pack 复用本页流程，只提取、转换及导出新增角色和其皮肤；未改变的旧包原生资源、动画、绑定与已验证结论默认完整。制作边界和预检见 [新 Pack 生产与 Token 节约](new-pack-production.md)。仅动作菜单/UI问题直接读 [理发店原生动作与道具](barbershop-native-idles.md)，不重跑本页全链。

## 先核对来源

安装源默认 `D:/miHoYo Launcher/games/ZenlessZoneZero Game`，实际按本地设置和 inventory 定位。提取工程 `D:/CK3-mod/zzz_game_asset_probe` 的 `scripts`、`reports`、`export_*`、`native_motion_library` 是可复用资产流程，不重新下载外部模型替代已验证原版。

- 星见雅：`native_motion_library/manifest.json` 保存原名、BLK、PathID、帧数、采样率、原始 SHA256、decoded 文件夹及 NPZ。`scripts/extract_native_motion_batch.py` 读取已索引源块并调用 ACL 解码器；`package_native_motion_library.py` 解析骨路径和面部通道，逐项验证打包结果。已有片段先审计并复用，缺少时再重新提取。
- Victoria：`export_victoria_motion/all_source_animation_inventory.json` 与 `selected_sources.json` 选择源。依次使用 `scripts/extract_victoria_motion.py`、`package_victoria_motion.py`；输出 `export_victoria_motion/library/manifest.json`。新增角色要先扩充源选择与解析映射，不把别人的动作改名套入。
- 妄想天使：`export_angels_motion/library/manifest.json` 及 Summer、NangongYu、AriaIdol 本人 NPZ；主工程通过 `ZZZ_NATIVE_FAMILY=angels` 复用生成器。多根 Bone_Root/Root 层级由 `import_native_json.py` 导入。三角索引必须经 `native_mesh_data.source_faces` 对照原 index buffer，不能把子网格局部 FaceList 当全局索引。
- 所有网格沿 `selected_meshes.json` 中精确 PPtr 解析。相同名称和顶点数不能证明是同一版本网格。保留材质、纹理和骨架层级引用。
- 解码审计：字节长度、帧数、TQS/scalar 轨道数、有限值、单位四元数、绑定哈希全解析；NPZ 回读与原始 decoded 数组逐项一致。原 Animator 根运动和运行时显隐/物理没有自动移植；明示缺口。

## 模型和皮肤

正式工程 `scripts/convert_native_model.py`、`convert_victoria_models.py` 使用源逆绑定矩阵和原权重。骨轴取源 Transform 层级，不能取 FBX 显示骨 roll，否则源非均匀缩放可能变成无法编码的剪切。

星见雅原骨架231骨，银庭花信增加28个不同骨及6个辅助骨，当前导出265骨；所有消费端仍应读 skeleton/report，不把这个数量当永久常数。银庭花信源 FBX 存在场景偏移，使用骨架局部坐标对齐。艾莲校服有不同绑定，保留独立逆绑定与 `campus__` 别名，不能用原皮权重覆盖。

在动画模式中，完整可见模型在 body 中；head 输出隐藏几何作为镜头载体。星见雅两套服装由共享 torso 姿势的整身 accessory 驱动，服装基因 `mode = add`，不能 `replace`。镜头辅助骨无权重、挂原根骨；不要通过倾斜身体或改变原骨长修正俯视。

妄想天使脸与独立眉毛共同写入连续 VAT 区间，以 source_mesh_ranges 核对顶点拼接顺序；导入时默认形态键清零。衣服共有骨先核对静置变换，附加装饰骨保留本人绑定和原权重。爱芮构造体使用本人 Bip002 动作与独立图集，按片段相位适配，缺源回退本人待机；偶像嘴曲线组合须标明，眼屏静态帧不能冒称完整运行时表情。

## 动作及表情

星见雅配置为 `scripts/native_animation_profiles.py`，导出器 `build_native_animation.py`；Victoria 对应 `victoria_animation_profiles.py`、`build_victoria_animation.py`。星见雅源绑定器为提取工程 `scripts/preview_native_body_motion.py`；导出以 `work/miyabi_native_motion_<clip>.blend` 为来源，不依赖旧“armed”展示工程。

0.16.0 起，用户指定全部当前及未来角色的人物菜单默认使用本人 `Galgame_Idle`。公共常量为 `portrait_emotions.MENU_IDLE`，三个 profile 的无情绪默认映射使用该片段，Victoria/Angels 的资产生成器须用菜单默认，不能从 `animation.default_clip` 取菜单默认。后者仍记录都市烘焙/校准参考；菜单记录在 `menu_idle_clip`。保留都市与基础待机源片段及独立菜单、情绪分段、监禁条件、CK3事件/宫廷重定向。

当前 绝区零绝区私有相机 默认站姿维护复用 `scripts/zzz_core_pose_045.py` 的定向规则，按当前身份/皮肤及 head/torso 状态闭包验证；不运行旧全量 apply_menu_idle 收尾。本人 Galgame 待机用于菜单，原版默认仍可选，事件/活动实际动作保持。旧角色的原生导出算法可按目标范围复用。

历史 0.16.1 的 frontend 类别、24 个状态和第121帧校准属于当时八人主包，不能强制复制到新 绝区零绝区私有相机 包。新增人物先枚举实际入口/状态和本人片段，再按当前隐藏层重算；不覆盖其他用途的节点或动画，也不通过自动居中掩盖相机问题。

菜单校准复用本人对话动作和真实眼位资料；当前隐藏 head/torso 挂接及动态节点按[内置 绝区零绝区私有相机／正式模型包 契约](zzz-core-pack4-workflow.md#隐藏骨架五骨参考与-36-骨实现)制作，不再裁成去道具的相机专用副本。保留原始身体/面部轨道、尺度及皮肤蒙皮；菜单片段路由不改事件实际动作。既有旧包的挂接实现只按该包收据维护。

星见雅原生独立待机包括 `Idle`、`Idle_AFK`、`MainCity_Stand_Idle`、`MainCity_Stand_Idle02`；按精确原名匹配，不能臆造 `Stand_Idle01`。各自保留同步脸部曲线和原武器轨迹，删除的只是旧 `miyabi_native_armed_idle` 特殊入口。

莱卡恩对话待机的离线细线问题曾来自预览器：蒙皮前归零怀表顶点会被不同骨变换重新拉开。`render_sunna_retarget.py` 现在在最终蒙皮后用 `preview_geometry.collapse_hidden_props` 将已标记道具三角形合并为零面积；这是对应游戏 shader 蒙皮后隐藏的预览修正，不是身体动画修正。`Lycaon_Weapon` 是机械腿，保持可见；不可用宽泛 Weapon 过滤隐藏它。取景只按身体、脸和机械腿包围范围，避免远处道具把人物缩小；不把离线图作为实机验证。

Victoria 对话情绪用本人 Galgame Start/Loop/End；艾莲、可琳有 Excited，另两人回退本人 Happy。CK3 进入/循环/退出按实际存在状态映射，不编造引擎会自动调用的状态。独立待机另注册选择入口；不擅自将所有长动作随机混进普通人物肖像。

情绪期间 Victoria 隐藏可分离武器和人偶，判断由 `hides_props/is_expression_prop` 管理；`Lycaon_Weapon` 是机械腿，不能按名字包含 Weapon 就删除。新增角色按源蒙皮归属确认道具和身体。不要因“不要单独持刀动作”就删掉所有原生动作武器。

妄想天使某些都市待机缺少原运行时显示控制，会把道具留在地面；通过按源蒙皮分类的 prop 标记和表情帧区间隐藏可分离道具，保留身体与机械部件。原生零缩放轨道用局部 TQS 代数转换，不能求逆奇异世界矩阵。面部与身体须采样同一真实时间轴。

脸部40条形态键通过顶点动画 DDS 同步输送：UV1 保留眼层 R/G，UV2 保存脸部顶点索引，无权重时钟骨驱动帧号。图集单 mip、高度按总帧数64行对齐，shader 高度/时钟索引从报告生成。重建后更新内容散列 include，令入口 shader 感知布局变化。时钟局部变换直接消去父矩阵，避免大图集行号在世界矩阵往返中放大 float32 误差。

## 材质易错点

- 眼球灰膜：先核对 Eye_E 原 RGBA 和顶点颜色层，分离基础眼、眼睑阴影、反光层；不要整体重涂眼球或丢弃 LUT alpha。
- 爱芮偶像眼层与星见雅/维多利亚不同：G0/G1 虹膜/瞳孔，G2 反光，G3 眼睑阴影，G4 装饰，透明层使用源预乘混合。不能沿用别人的分层编号；眼神异常先分清材质层和动画曲线问题。
- 阴影闪烁：本工程 toon 已禁用全身 SSAO，脸部光照平缓；先查实际 shader 分支和层重叠，勿归咎原始脸型。不要用 HDR 过曝截图作亮度基准。
- 袜子：只在 Body1 的 Map1_A 对应区域使用 Eff_Matcap_Socks，不把材质处理施加整个身体。
- shader 纹理槽要同时考虑 Ref 隐式15/16和显式声明，新增 sampler 前核对完整布局。
- 原模型数据用程序导出或 Blender 检查，不能以 AI 生成图片冒充提取模型或验证画面。

## 历史主菜单缓存经验

历史 0.16.3 曾否定“只刷新 last_save 就能修复主菜单”的推断，并在对应八人主包中分离兼容 dead 与真正死亡类别。当前载入使用共用规范的自动私有相机方案，不运行旧菜单生成器或改写存档。维护旧方案时才按其收据追查类别→实体→动画，不能把历史待机别名推广成所有新包要求。

历史二进制存档状态哈希和修改工具仅用于当时缓存调查，不是当前维护入口。本工作线可只读核对元数据与最终 asset，但不迁移或盲替换用户存档；载入没有人物读取接口时按现有专用节点映射处理。

不通过反复刷新存档猜测选择器，不把实体状态与 CK3 动作类别混为一谈。现有死亡/睡眠状态保持；菜单、载入、事件分别验证，不由离线解析或某张成功截图外推全入口。
