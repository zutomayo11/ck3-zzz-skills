# 路由与相机族

## 对象分层

记录时必须把下列对象放在不同字段：GUI 路由键；Custom/本地化返回值；相机定义；`position_node`/`look_at_node`；portrait group/type/ethnicity；environment、animation、slot；相机辅助节点；道具挂点。

## 入口清单

至少分别审计：frontend 主肖像；人物面板/配偶/小头像；地图左下角 HUD；内阁、战争、战斗、生活方式；普通事件、大事件、scheme、duel、上下排与 VFX；活动主布局、参与者和结束队列、锦标赛；载入存档卡；书签；大厅/游戏内切换；理发店；宫廷三维场景。二维肖像纹理和宫廷三维场景不能互相外推。`SaveGameItem`、`BookmarkCharacter`、`ActivityWindowCharacter.GetCamera` 等接口要按实际调用者核对，不用普通 `Character` 假设替代。

## 相机族原则

`body`、`head`、`shoulders`、`torso`、`event_center`、`combat_window`、活动动态 getter 只有在源码映射和验证证据都支持时才能复用。事件原本要求侧身、背向、跪姿或对视时不能一律改正面。活动保留原相机/动作选择语义：目标角色按隐藏别名直接调用私有相机，普通人物保留 `GetCamera`；GUI 接入数量不能代替事件脚本、`triggered_animation`、活动定义中的 `camera =` 审计。

静态调用清单建议字段：`entrypoint`, `gui_file`, `widget`, `display_scope`, `slot`, `api_kind`, `environment`, `animation`, `source_camera`, `route_key`, `condition`, `expected_camera_id`, `definition_file`, `position_node`, `look_at_node`, `entity`, `skin`, `status`, `evidence`。动态和静态推导分别保存；“预期返回”不是“实际使用”。

## 覆盖检查

比较原版 GUI、当前 绝区零绝区私有相机 GUI、目标 Pack 的同名文件和加载顺序；解析完整嵌套块，不用“匹配到第一个右括号”的正则代替块解析。相同相机名、文件存在或旧接口前缀不是删除/改名依据。生成器展开的共享模板要保留角色局部参数。
