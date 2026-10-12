# 输入接口与单位契约

五条核心链使用普通 Python 容器和 NumPy 数组。调用者负责解析自己的源数据；本参考不包含角色清单、骨架数据、素材或生产配置。

## 转换

`source_faces(raw, converted)` 沿用已验证转换器的索引接口：

- `raw.m_VertexCount` 为顶点数，`raw.m_Indices` 为按子网格顺序连续拼接的整数索引数组。
- `raw.m_SubMeshes[]` 提供 `topology = "Triangles"`、`indexCount`、`firstVertex`。
- `converted.SubmeshList[].FaceList[].VertexIndices` 为相对 `firstVertex` 的局部索引，绕序与原始三角形逆序一致。
- 子网格数量、实际索引长度、局部到全局重建及顶点范围必须一致，函数不修复错误拓扑。若源采用字节偏移、稀疏段或其他 topology，调用者先精确解析并形成该连续布局；不要直接把任意 Unity 导出 JSON 传入。

`convert_geometry(positions, normals, faces, basis)`：输入分别为 `N×3`、`N×3`、`T×3` 和仿射 `4×4`；三角形为整数，顶点/法线为有限数值。`basis` 将源坐标映射到目标坐标，变换法线使用逆转置，并在负行列式时翻转绕序。返回新数组，不修改源数组。没有自动身高归一化。

`change_basis(matrices, basis)` 对 `…×4×4` 矩阵执行 `C M C^-1`。局部矩阵、世界矩阵和逆绑定矩阵必须使用同一 `C`。单位转换只表达一次；不要把外层统一尺度重复乘进衣服或隐藏载体。

UV、切线、材质分组、原始蒙皮与形态键由目标网格适配器保持。本参考几何函数不替代这些通道的完整导出。

## 动画

`local_matrices(t, q, s)` 与 `build_anim_tree(names, t, q, s, fps)` 使用：

| 字段 | 形状与约束 |
|---|---|
| `t` | `F×B×3` 局部平移，单位与目标绑定一致 |
| `q` | `F×B×4`，顺序 **x,y,z,w**，不能为零长度 |
| `s` | `F×B×3`，保留源尺度，允许零缩放和负缩放 |
| `names` | 长度 B，唯一 ASCII 骨骼别名；调用者保存原名/别名映射，不擅自改原骨架标识 |
| `fps` | 有限且大于零；F、B均大于零，不改变源时序 |

四元数只做归一化与相邻帧同半球选择；不做插帧、曲线重采样或改变动作时长。静态通道沿用第一帧，动态通道按 **帧→骨骼→分量** 展平。近似恒定的判定为绝对差 `1e-8`，动态回读仍需验证。

输出是供 PDX 后端消费的 `ElementTree`，属性值为 Python 列表，**不能用标准 XML 序列化把它当成动画文件**。`decode_anim_tree`面向本参考输出及对应后端回读：支持三分量尺度、全静态标量尺度；不承诺解析混合尺度宽度或任意游戏动作格式。

零缩放能从原 T/Q/S 直接编码；不能从奇异矩阵重新提取原旋转。面部曲线、眨眼和身体必须由目标工程提供同一真实时间轴，本参考不提供或合成本人面部数据。

## 重定向

`worlds(local, parents)`：`local` 为 `F×B×4×4`；`parents` 长度 B，根为 `-1`，其余父索引小于子索引。矩阵乘法为父世界矩阵乘子局部矩阵。

`bind_corrections(target_bind, source_bind, pairs)`：两组绑定世界矩阵；`pairs` 显式映射目标索引→源索引，输出目标索引→`(源索引, Rs^T Rt)`。它提供绑定朝向修正，没有自动猜测骨名或肢体方向。A/T姿势、脚踝/脚趾和特殊骨架的解剖修正必须另行提供或覆盖该修正矩阵。

`solve(rest_local, parents, desired)`：单帧目标参考局部矩阵及目标索引→所需世界旋转 `3×3`。保留参考局部平移和尺度，只迁移旋转；未映射骨骼保留原局部矩阵。映射骨的奇异/反射/剪切参考矩阵拒绝处理。面向普通刚体/统一尺度骨链，非均匀父尺度可能引入世界剪切，须在目标工程另行处理并验证。

输入应为仿射骨骼矩阵。此函数不迁移根运动、表情、源道具轨迹或接触位置；“保持骨长”不等于已满足脚底、王座或骑乘接触。

## 装配与验证

`render_asset(prefix, mesh_file, materials, animations, states, default_state, looping=...)` 返回字符串：

- `prefix` 为私有 ASCII 资源前缀；`mesh_file` 为使用者实际导出网格引用。
- `materials[]` 的 `index` 唯一且从0连续；提供 `diffuse`、`normal`、`properties`、`shader`、`shader_file`。不内置 Shader 或贴图。
- `animations` 为动画ID→文件引用，`states` 为状态名→动画ID；默认状态与全部动画必须已声明。
- 不提供 `looping` 时最小示例全部循环；实际进入/退出、死亡等状态需显式传入完整循环标志，且保留原实体阶段链、属性、随机变体和附件。该最小实体不能整体替换现行复杂实体。

`validate_skin` 检查 `N×4` 骨索引/权重，未使用槽为 `-1/0`，权重非负、和为1（绝对差 `1e-4`）。不自动删影响槽或重分配权重。

`validate_roundtrip` 要求相同形状和有限值，逐分量容差为 `max(absolute, abs(expected)*relative)`，默认 `3e-5/1.3e-7`。必须从真实输出重新读取 actual，不能传两份同源对象假装二进制验证。

`resolve_references` 按调用者给定的**最高优先级在前**的根目录找文件并返回来源。拒绝绝对路径、`..` 和跳到根外的链接。它检查已列出的文件引用，不解析 Include、数据库同名定义或整个 CK3 VFS；这些需用相机工具及工程专项审计补充。
