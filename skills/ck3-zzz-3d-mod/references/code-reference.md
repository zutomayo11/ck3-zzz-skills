# 五条核心链代码参考

本参考包供 Codex 在使用者自己的工程上复用算法。所有输入显式传入；模块导入不读取设置，不创建目录，不启动 Blender/游戏，不安装 Mod，也不访问网络。实际模型、贴图、动作、成品、备份和旧安装收据均不随包提供。

## 入口与职责

| 链 | 代码 | 当前提供的参考 |
|---|---|---|
| 转换 | [conversion.py](../scripts/zzz_reference/conversion.py) | 源索引核对、坐标变换、法线和镜像绕序；绑定矩阵使用同一坐标变换 |
| 动画 | [animation.py](../scripts/zzz_reference/animation.py) | xyzw 四元数、T/Q/S 同步、零缩放、符号连续、静态/动态通道及 PDX 动画树 |
| 重定向 | [retarget.py](../scripts/zzz_reference/retarget.py) | 父先子后世界矩阵、绑定朝向修正、单帧旋转迁移及原局部平移/比例保持 |
| 装配 | [assembly.py](../scripts/zzz_reference/assembly.py) | 显式材质、动画和状态的最小 `.asset` 文本生成与引用检查 |
| 验证 | [validation.py](../scripts/zzz_reference/validation.py) | 四槽蒙皮、父子索引、数值回读及用户指定来源顺序的文件引用解析 |

代码目录、示例和测试都位于本技能内部，安装整个技能即可保留相对关系。不要只复制本页或五个主模块中的一份；模块间直接依赖 `validation.py`。

按需读取：[输入契约](code-reference-inputs.md)、[制作接入流程](code-reference-workflow.md)、[验证范围](code-reference-validation.md)、[源码来源](code-reference-sources.md)。

角色玩法生成见[角色玩法参考边界](../../ck3-zzz-portrait-mod/references/role-code-reference.md)；独立前置的选模、回调与 UI 规则见[独立前置参考边界](standalone-core-reference.md)。五条资源链不负责创建人物、调频、修改身份或安装文件。

## 环境与命令

参考模块验证环境为 Python 3.12、NumPy 1.26.4；依赖文件限定 Python 3.10–3.12 的已知可安装组合。只运行本参考不需要 Pillow、PyYAML、Blender 或 PDX 导出库。实际工程按自己的工具链另行提供这些依赖，勿把系统 Python 的依赖安装误认为 Blender Python 已配置。

在仓库根目录运行：

```powershell
python -m pip install -r skills/ck3-zzz-3d-mod/requirements-reference.txt
python -B -m unittest discover -s skills/ck3-zzz-3d-mod/tests -p "test_*.py"
python -B skills/ck3-zzz-3d-mod/examples/reference_walkthrough.py
```

依赖已可用时不重复安装。示例仅打印数字和字符数，全部测试输入在 Python 代码内人工构造，运行不会生成模型/动画/贴图资源。示例中的 `demo.mesh` 等是字符串占位符，不代表仓库提供了这些文件。

从使用者工程调用时，将该技能 `scripts` 目录加入模块查找路径，再 `from zzz_reference import conversion, animation, retarget, assembly, validation`。具体路径由使用者的技能安装位置解析，不能沿用作者的盘符。

## 能力边界

这些是可测试的算法参考，不是完整人物包的一键制作器。源游戏提取器、Blender网格导出、面部/VAT着色、人物专属解剖校准、隐藏载体、道具动作、脚底/骑乘接触与实际 Mod 注册仍需使用者的目标工程适配。先确定目标角色与输入来源，再选函数；没有本人资源时明确报缺，不能用示例或其他角色替代。

技能中的版本和本机路径是历史证据索引。新任务以使用者当前配置、目录和交付状态为准；不因本参考入口可用就重跑历史全量构建或恢复。
