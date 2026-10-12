# 绝区零 CK3 技能库

用于在 Codex 中制作、维护和诊断绝区零相关 Crusader Kings III Mod 的三份技能：三维角色、立绘与调频、肖像相机。

仓库提供技能说明、参考资料、五条3D核心链的代码参考和只读相机工具。技能中的工程位置、历史维护入口和版本记录是本机工作流程的快照；使用时以实际工程的设置、来源清单和当前维护规则为准。代码参考使用显式输入，不依赖作者的本机目录。

## 技能列表

| 技能 | 用途 | 入口 |
| --- | --- | --- |
| `ck3-zzz-3d-mod` | 三维角色、外观、原生动作、表情、道具、材质及模型包兼容 | [SKILL.md](skills/ck3-zzz-3d-mod/SKILL.md) |
| `ck3-zzz-portrait-mod` | 角色数据、透明立绘、身份与特性、音擎、调频、双语文本及角色包维护 | [SKILL.md](skills/ck3-zzz-portrait-mod/SKILL.md) |
| `ck3-portrait-camera` | 肖像入口、私有相机路由、隐藏定位载体、事件与活动取景的诊断和验证 | [SKILL.md](skills/ck3-portrait-camera/SKILL.md) |

三份技能存在同级目录之间的相对引用，请整套安装并保留原有文件夹名称。

## 3D 制作流程

![绝区零3D模型制作总览：六阶段及贯穿全过程的验证](skills/ck3-zzz-3d-mod/assets/production-workflow/overview.svg)

[详细流程与五条核心链](skills/ck3-zzz-3d-mod/references/production-workflow.md)说明输入、输出、原生动画与 CK3 重定向分支，以及模型 Pack、独立 3D 前置和角色包的职责。

[离线 HTML 浏览版本](skills/ck3-zzz-3d-mod/assets/production-workflow/production-workflow.html)下载后用浏览器打开，支持详细、浅色和深色视图。图示仅含文档文字和矢量形状，无实际游戏素材；参考模块不构成完整的一键人物制作器，图示验证也不代表游戏验收。

## 目录结构

```text
ck3-zzz-skills/
├── README.md
├── LICENSE
├── .gitignore
├── .gitattributes
├── source-manifest.json
└── skills/
    ├── ck3-zzz-3d-mod/           # 另含 scripts/zzz_reference、examples、tests、依赖声明
    ├── ck3-zzz-portrait-mod/     # SKILL.md、agents、references
    └── ck3-portrait-camera/      # 另含 scripts、assets、tests
```

- `SKILL.md`：技能的适用范围、工作流程和参考入口。
- `agents/openai.yaml`：Codex 展示信息。
- `references/`：按当前任务需要读取的详细规则。
- `scripts/`：3D技能的五条核心链参考模块；相机技能的两个只读分析工具。
- `examples/`：只使用人工数值、在内存中执行的参考示例。
- `assets/`：相机验证报告的 JSON 模板。
- `ck3-zzz-3d-mod/assets/production-workflow/`：三张纯文本 SVG 文档图与离线 HTML，随整个技能安装。
- `tests/`：工具测试、测试夹具和人工行为场景。

## 安装到 Codex

可以在 Codex 中提出以下请求：

```text
使用 $skill-installer，从 GitHub 仓库 zutomayo11/ck3-zzz-skills 的 main 分支
整套安装以下三个目录，并保留它们的同级目录关系：
skills/ck3-zzz-3d-mod
skills/ck3-zzz-portrait-mod
skills/ck3-portrait-camera
```

也可以克隆仓库后，将 `skills/` 下的三个完整目录复制到 `$CODEX_HOME/skills`，未设置 `CODEX_HOME` 时为 `~/.codex/skills`。例如 Windows 的默认位置为用户目录下的 `.codex/skills`。

遇到已经安装的同名技能时，先备份并比较现有内容，不直接覆盖。安装后按当前 Codex 的提示加载技能。

需要显式调用时，可以使用 `$ck3-zzz-3d-mod`、`$ck3-zzz-portrait-mod` 或 `$ck3-portrait-camera`，并说明实际工程位置、目标角色或出现问题的入口。

## 相机工具与验证

两个工具分别用于静态相机链检查和带来源哈希的相机定义快照导出：

- [audit_camera_chain.py](skills/ck3-portrait-camera/scripts/audit_camera_chain.py)
- [export_camera_catalogue.py](skills/ck3-portrait-camera/scripts/export_camera_catalogue.py)

在仓库根目录查看工具参数、运行现有测试：

```powershell
python -B skills/ck3-portrait-camera/scripts/audit_camera_chain.py --help
python -B skills/ck3-portrait-camera/scripts/export_camera_catalogue.py --help
python -B -m unittest discover -s skills/ck3-portrait-camera/tests -p "test_*.py"
```

测试中的 `fixtures/broken` 是刻意包含错误的自建测试样例。`behavior_scenarios.json` 用于人工检查技能决策，不属于自动测试通过的证明。

静态扫描、离线图像验证和实际 CK3 运行验收分别记录。自动测试通过不代表人物取景、模型显示或动画已经在游戏中验收；未观察的游戏表现继续标记为 `NOT_TESTED`。

## 五条核心链代码参考

从[代码参考入口](skills/ck3-zzz-3d-mod/references/code-reference.md)读取环境、输入契约、接入流程和验证边界。代码与说明随整个3D技能安装，不额外依赖仓库根目录。

| 链 | 功能 |
|---|---|
| 转换 | 原始/局部索引核对、坐标/绑定变换、法线及镜像绕序 |
| 动画 | 原 T/Q/S、四元数连续、静态/动态通道及 PDX 动画树 |
| 重定向 | 骨架世界矩阵、绑定修正和保留原局部平移/尺度的旋转迁移 |
| 装配 | 显式材质、动作及状态的最小资产声明 |
| 验证 | 蒙皮、父子顺序、回读误差和指定来源的文件引用 |

```powershell
python -m pip install -r skills/ck3-zzz-3d-mod/requirements-reference.txt
python -B -m unittest discover -s skills/ck3-zzz-3d-mod/tests -p "test_*.py"
python -B skills/ck3-zzz-3d-mod/examples/reference_walkthrough.py
python -B -m unittest discover -s tests -p "test_*.py"
python -B tools/check_repository.py
```

示例只打印摘要，不生成资源。输入全部在代码内人工构造；仓库不提供实际游戏网格、贴图、动画数据、成品、备份或旧安装收据。二进制PDX后端及实际Blender/游戏适配由使用者提供，参考代码不执行安装或发布。

[角色玩法](skills/ck3-zzz-portrait-mod/references/role-code-reference.md)和[独立前置规则](skills/ck3-zzz-3d-mod/references/standalone-core-reference.md)独立说明职责与后续代码提取点；本轮没有移植其完整生成器或历史维护器。资源算法测试不代表这两个模块的玩法/UI已经通过。

## 来源与后续维护

[source-manifest.json](source-manifest.json) 记录仓库技能快照时间、名称、每个技能文件的相对路径、字节数和 SHA256。基础技能来自作者本机，新增代码与文档在仓库维护；具体算法追溯见[软件源码来源](skills/ck3-zzz-3d-mod/references/code-reference-sources.md)。`.gitattributes` 禁止 Git 自动转换技能文件的换行符。

后续同步时，先比较本机与仓库的变化，保留仓库新增的参考模块；不要用整个本机目录覆盖仓库扩展。更新相关文件和来源清单，验证引用及测试后提交。技能更新不自动改变 Mod 版本，也不执行工程构建、游戏启动或工坊发布。

修改完成后用 `python -B tools/check_repository.py --update-manifest` 更新技能文件清单，再用无参数命令回读。检查器仅对白名单中的四份 SVG/HTML 文档图例外放行，拒绝其脚本、嵌入图片与非本地资源引用；其他资源/二进制类型及新增生产数据/安装收据JSON仍拒绝。检查全部Python语法、相对文件链接及技能文件哈希；游戏资产的真实性和使用许可仍需使用者按自己的来源确认。根目录 `tools/` 与 `tests/` 是仓库维护工具，安装技能时不需要复制它们。

## 许可

仓库内的原创技能说明、参考资料、脚本、模板和测试采用 [MIT 许可](LICENSE)，署名为 `2026 zutomayo11`。

游戏模型、贴图、提取资源、完整 Mod 工程、私人存档及工程备份不包含在发布内容中。MIT 许可不授予这些外部资源或第三方游戏、名称、商标的权利；相关资源遵循其各自的权利与使用条件。
