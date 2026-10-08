# 相机定义快照的生成与边界

先确认现装 绝区零绝区私有相机 的版本、有效相机来源及覆盖顺序，再用 `scripts/export_camera_catalogue.py <camera-file-or-directory> --output <report.json>` 导出到任务报告目录。不要导出到技能中替代维护规则。

导出器保存源 SHA-256、定义、节点和相机参数。ID 后缀族只用于检索，不代表真实用途；数量不等于事件数量、调用覆盖或实机通过。技能不再携带旧版本路径快照。

`runtime_status` 为 `NOT_TESTED`。GUI、人物位、条件、动作树、覆盖优先级、活动别名和引擎选择另行审计；工具不证明完整有效 VFS 或二进制节点归属。当前规范见[共用工作线](../../ck3-zzz-3d-mod/references/zzz-core-pack4-workflow.md)。
