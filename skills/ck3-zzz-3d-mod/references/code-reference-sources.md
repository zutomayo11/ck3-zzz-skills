# 软件源码来源与整理范围

本轮代码根据作者本机既有制作工程中的算法重新组织，未复制原工程完整入口。新增参考模块不依赖这些来源文件存在；下面的名字用于追溯，SHA256仅识别**软件源码**版本，不是素材清单或安装收据。

| 参考模块 | 原算法位置 | 整理方式 |
|---|---|---|
| `conversion.py` | `native_mesh_data.py:source_faces`；`import_native_json.py` 的单位/轴约定 | 保留索引对照，补截断/越界拒绝；坐标转换显式传入，不读取角色和Blender场景 |
| `animation.py` | `sunna_actions/format.py:qmatrix/decode/write_clip`；`build_victoria_animation.py:write_anim/sample_bones` | 独立为显式T/Q/S与PDX树，保留通道排列和四元数符号连续；不读取动画库、图集或Shader |
| `retarget.py` | `sunna_actions/format.py:rotation/worlds/solve/calibration`；`bake_character_retarget.py` | 保留世界矩阵和旋转求解；显式索引映射，不复制本人骨名、姿势目录或Blender第三方重定向核心 |
| `assembly.py` | `build_assets.py:make_asset` | 用显式名称和引用解释最小声明；不复制原版实体、私有Shader或完整人物模板 |
| `validation.py` | `validate_export.py:check_mesh_part`；`sunna_actions/format.py:write_clip` | 保留权重、回读检查；增加明确优先级的相对文件解析；不加载配置、游戏资源或旧收据 |

使用者仍需将原生提取接口、实际绑定/UV/材质、解剖校准、完整状态树、脸部/VAT及最终导出接入自己的工程。参考模块不声称移植了来源工程所有功能。

## 来源源码哈希

| 文件 | SHA256 |
|---|---|
| `native_mesh_data.py` | `a15c64ada75f52728cd27512db69c2304d7e3da3a30161e27c1e7ff00363ba7d` |
| `import_native_json.py` | `127c25ee57ef37911946ad65e323b388444fd64c1324d157c0d69492bd8b0677` |
| `build_victoria_animation.py` | `f9991a36f117b152f1158067cf10fc57ea2941d7342e9e2767e4227b18bc1f34` |
| `sunna_actions/format.py` | `e29fc84ad7438d4cef844d45042a3d47c88b134b0aada0125c8fe8f45c9ffd08` |
| `bake_character_retarget.py` | `a9dc698cf4de2bd74928cc8fd69efeb176fe623fa19b273152d02243a6fe97ba` |
| `build_assets.py` | `539c20017d7b6e68e4bb826c8c25ea32a216db721a252ef1fed27fe1b9d8e520` |
| `validate_export.py` | `9ae22739ac196b3024398db160c9995fde13f29d55c677c43017d0657e46f8f5` |

## 第三方边界

新增原创参考代码及文档沿用仓库MIT许可。这轮未分发 `io_pdx_mesh`、Blender重定向插件、AnimeStudio、ACL/RTM、运行时或编译器源码/二进制；外部工具遵循自己的许可。

PDX后端实际核对过 `read_meshfile`、`write_meshfile`、`write_animfile`，本机来源版本的 `license.txt` 为GPLv3。来源模块调用第三方工具不意味着该工具代码由本仓库MIT许可覆盖。依赖声明仅包含 NumPy版本；安装时由包管理器取得其原始许可包。

本轮用本机外部PDX后端对3帧、2个人工骨骼、含零缩放的临时动画做过二进制写入/回读，最大矩阵误差约 `4.45e-16`。临时动画未纳入交付，验证不覆盖真实人物或 CK3 游戏画面。
