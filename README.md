# 绝区零 CK3 技能库

用于在 Codex 中制作、维护和诊断绝区零相关 Crusader Kings III Mod 的三份技能：三维角色、立绘与调频、肖像相机。

本次发布保留已经在作者本机使用的技能说明、参考资料及工具。技能中的工程位置、历史维护入口和版本记录是本机工作流程的快照；使用时以实际工程的设置、来源清单和当前维护规则为准。

## 技能列表

| 技能 | 用途 | 入口 |
| --- | --- | --- |
| `ck3-zzz-3d-mod` | 三维角色、外观、原生动作、表情、道具、材质及模型包兼容 | [SKILL.md](skills/ck3-zzz-3d-mod/SKILL.md) |
| `ck3-zzz-portrait-mod` | 角色数据、透明立绘、身份与特性、音擎、调频、双语文本及角色包维护 | [SKILL.md](skills/ck3-zzz-portrait-mod/SKILL.md) |
| `ck3-portrait-camera` | 肖像入口、私有相机路由、隐藏定位载体、事件与活动取景的诊断和验证 | [SKILL.md](skills/ck3-portrait-camera/SKILL.md) |

三份技能存在同级目录之间的相对引用，请整套安装并保留原有文件夹名称。

## 目录结构

```text
ck3-zzz-skills/
├── README.md
├── LICENSE
├── .gitignore
├── .gitattributes
├── source-manifest.json
└── skills/
    ├── ck3-zzz-3d-mod/           # SKILL.md、agents、references
    ├── ck3-zzz-portrait-mod/     # SKILL.md、agents、references
    └── ck3-portrait-camera/      # 另含 scripts、assets、tests
```

- `SKILL.md`：技能的适用范围、工作流程和参考入口。
- `agents/openai.yaml`：Codex 展示信息。
- `references/`：按当前任务需要读取的详细规则。
- `scripts/`：相机技能自带的两个只读分析工具。
- `assets/`：相机验证报告的 JSON 模板。
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

## 来源与后续维护

[source-manifest.json](source-manifest.json) 记录本次复制时间、技能名称、每个技能文件的相对路径、字节数和 SHA256。技能文件按原始字节保存，`.gitattributes` 禁止 Git 自动转换这些文件的换行符。

后续同步时，先检查本机技能的新变化，只更新这三个目录的相关文件和来源清单，再验证引用及现有测试后提交。技能更新不自动改变 Mod 版本，也不执行工程构建、游戏启动或工坊发布。

## 许可

仓库内的原创技能说明、参考资料、脚本、模板和测试采用 [MIT 许可](LICENSE)，署名为 `2026 zutomayo11`。

游戏模型、贴图、提取资源、完整 Mod 工程、私人存档及工程备份不包含在发布内容中。MIT 许可不授予这些外部资源或第三方游戏、名称、商标的权利；相关资源遵循其各自的权利与使用条件。
