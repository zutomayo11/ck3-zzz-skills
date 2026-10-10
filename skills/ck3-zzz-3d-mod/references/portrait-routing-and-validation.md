# 事件、活动与队列路由验证

当前调用以[共用规范](zzz-core-pack4-workflow.md#相机调用结构)为准。特殊事件保留原版调用；活动接入人物私有center、普通人物typed GetCamera，后续定向骑乘/战车相机为有限例外。旧420别名/逐事件副本方案已退役，不重跑历史Recovery或构建来撤回现行修复。

## 调用点清查

从最终VFS解析事件/活动ID、人物位和实际作用域、动作树、默认/显式相机及覆盖优先级。无camera字段仍追窗口默认和嵌套触发；不产生肖像位置单列，未知结构与循环阻止批量安装。

活动保留原scope:character和动作请求，进行中/结束的普通与接入分支分别核对。只有当前源码明确的取景条件才选择定向相机，不按普通动作名猜全部事件机位。特殊事件还原须比较原版条件、顺序、权重和动作列表；必要注释屏蔽文件保持。

## 诊断与验证

同角色、同外观、同动作、同入口对照，记录GUI API、类别、相机参数、实际画像/实体/节点、分辨率和挂接。多图角色不同不能直接归因于骨名或相机。feast_default.2005左位disgust/very_left与中位sick_stomach/center_pointing_left分别比较原版设计。

静态检查包括原版动作树等价、逆变换移除定向分支恢复原文、普通typed getter保持、相机参数白名单和节点归属；只改文本路由时保护二进制，不重烘。

debug标签根widget用[InDebugMode]控制背景和文字，保持鼠标穿透。无标签先查控件是否存在和是否满足原分支；区分调用请求、Custom返回与引擎最终选择，事件GUI CAM可能被camera覆盖。当前诊断及主面板死亡标签分别参考113/115收据，不把旧常量当实际状态。

活动必须观察真实ActivityWindow进行中/结束队列，普通事件加宴会背景不能替代。队列无人物、缓存未更新或截图遮挡不算通过。游戏未观察项保持NOT_TESTED，不使用computer-use或新增UI helper。

当前证据为工程reports/zzz_native_camera_112、zzz_ground_framing_113、zzz_debug_overlay_113；043逐调用点资料用于历史追溯。头像/死亡另读[展示入口](portrait-display-and-death.md)，道具/取景/接触另读[接触参考](mount-contact-and-framing.md)。
