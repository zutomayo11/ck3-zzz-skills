# 在自己的制作工程中接入

先读取[输入契约](code-reference-inputs.md)。这五条链处理一个明确目标的算法步骤；用户提供素材位置与输出位置后，由当前工程的定向入口调用。没有资产时只进行人工数值示例与代码检查。

整体阶段、原生动作与 CK3 重定向的分支，以及 Pack/Core/角色包职责见[3D 制作流程图](production-workflow.md)。

## 1. 转换

精确定位本人网格与版本，解析顶点、逆绑定、骨架、原索引和材质引用。调用 `source_faces` 对照转换器局部索引，再根据明确的单位/轴约定调用 `convert_geometry` 与 `change_basis`。保留原骨序、父子、蒙皮、UV、切线和所有其他通道。

参考函数不读 FBX 或操作 Blender场景。实际场景导入/导出由使用者已审核的 Blender 适配器执行；不要用骨骼显示 roll 替代源 Transform 绑定，也不要因为参考示例成功就跳过本人的几何回读。

## 2. 动画

读取本人原生动作的明确骨路径和 T/Q/S；索引顺序与最终骨架别名一致，面部曲线另行同步。用 `local_matrices`核对轨迹，`build_anim_tree`产生供外部 PDX 后端消费的树。

外部接口在本机代码中核对过的方法为 `write_animfile(path, tree)`、`read_meshfile(path)` 与 `write_meshfile(path, tree)`。仓库不复制该后端；调用者用自己的授权安装提供 `pdx_data` 对象。接口变化时先核对，不凭名称套其他库。

```python
from zzz_reference.animation import build_anim_tree, decode_anim_tree, local_matrices
from zzz_reference.validation import validate_roundtrip

# names/t/q/s/fps 来自调用者明确选择的目标；pdx_data 和 output_path 由工程提供。
tree = build_anim_tree(names, t, q, s, fps)
pdx_data.write_animfile(str(output_path), tree)
actual_tree = pdx_data.read_meshfile(str(output_path))
actual, actual_fps = decode_anim_tree(actual_tree)
if actual_fps != fps:
    raise ValueError("Binary FPS changed")
if [node.tag for node in actual_tree.find("info")] != list(names):
    raise ValueError("Binary bone order changed")
validate_roundtrip(local_matrices(t, q, s), actual)
```

这是有外部输入的接入片段，不是可以缺省变量运行的独立脚本。写入只作用于调用者指定的候选路径，先完成自己的防覆盖检查。本人 `Galgame_Idle`、特殊状态和原生动作分类从目标工程读取，不用通用示例代替缺失动作。

## 3. 重定向

使用 `worlds`核对源与目标绑定、显式建立映射并调用 `bind_corrections`。每帧用 `source_world_rotation @ correction` 得到 desired，再用 `solve`生成目标局部矩阵。解剖框架、脚踝/脚趾、机械腿、多骨链等目标规则由使用者工程补充。

结果必须与目标原骨序、原局部平移和尺度核对。根运动、源武器和 CK3 道具不同；相机取景、脚底定位与骑乘支撑面也是不同约束。本参考不包含自动补偿常量或已烘焙动作。

## 4. 装配

把实际已导出的网格、材质、Shader 和动作名称显式传给 `render_asset`，检查默认状态及引用。最小生成器用于解释 PDX 声明关系；正式角色接入须在其已有模板上保留实体阶段链、属性、变体、隐藏head/torso、画像组、基因、皮肤、道具和光环注册。

纯文本函数不验证材质视觉效果，也不包含任何原版或第三方 Shader 源码。需要的 Shader/Include 由使用者工程持有并按真实引用闭包检查。

## 5. 验证与交付

先检查本目标的拓扑、骨序、绑定、权重、T/Q/S、通道帧数与实际二进制回读；再解析真实材质、动画、Include 和状态闭包。显式列明受支持的包组合与当前有效文件来源。

交付前由目标工程做候选、范围白名单和受保护状态检查；这个参考包没有安装、启动器、数据库、存档、工坊或网络写入入口。游戏验证逐入口记录为用户反馈或 `NOT_TESTED`，不把数值回读当成游戏显示通过。

## 外部工具说明

- NumPy：本参考唯一运行依赖，版本与测试命令见[入口](code-reference.md)。
- Blender：仅实际场景适配/烘焙需要，使用者配置实际路径和版本；参考模块无需 `bpy`。
- PDX 后端：仅真实 `.mesh/.anim` 编码需要；本参考不分发 `io_pdx_mesh`。它的本机来源许可为 GPLv3，使用者保留原许可和自己的工具版本，不把它包含在本仓库 MIT 名下。
- 游戏资源提取器与 ACL：仅重新提取源数据时需要，五条核心链从使用者已解析的数据开始。AnimeStudio/ACL有特定变体（包含 HoYo 专用路径），不能默认任意标准 ACL库等价；这轮不分发其源码或二进制，使用者按自己的工具链获取与编译。

各工具的具体安装/下载由使用者选择。技能安装与运行本参考不自动安装工具、不抓取素材。
