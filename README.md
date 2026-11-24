# 视频制作知识库

记录从声音、素材到动画与成片的制作方法，以真实案例解释技术如何组合，并整理国风动漫等方向的选型思路。

## 从这里开始

| 想了解什么 | 阅读入口 |
| --- | --- |
| 一条视频从头到尾怎么制作 | [贾队长《慌啥子嘛，慢慢来》录音室版](example/jiaduizhang-recording-room/README.md) |
| 同一条声音如何做成国风代码动画 | [贾队长《慌啥子嘛》国风鼎香楼案例项目](example/guofeng-dingxiang-lou/README.md) |
| 各种工具分别解决什么问题 | [视频制作技术路线总览](docs/guides/video-production-overview.md) |
| 大模型出的人物图如何交给代码成片 | [生成图接入现有代码成片](docs/guides/video-production-overview.md#生成图接入现有代码成片) |
| Pillow 能做到什么，何时需要换方案 | [Pillow 与国风动漫](docs/guides/pillow-and-chinese-animation.md) |
| 二维角色演唱、四式身段，以及转身和打斗等连续动作 | [连续动作与打斗制作技术](docs/guides/character-motion-and-fighting.md) |
| 导出视频持续闪烁、黑块如何排查 | [国风鼎香楼闪烁修复记录](example/guofeng-dingxiang-lou/闪烁修复.md) |
| 记录一个新作品 | [制作案例模板](docs/templates/case-study.md) |

建议先读技术总览，再读实际案例，最后根据目标选择动作制作路线。

## 内容组织

```text
docs/
  guides/      原理、技术选型和制作方法
  templates/   新案例的记录模板
example/          案例项目：说明和该片的音频、静帧、成片放在一起
project_context/  维护约定、主题索引与会话记录
AGENTS.md         AI 协作约定
```

## 阅读约定

- 案例中的“实际使用”以留存脚本、参数与日志为依据。
- 技术指南中的推荐方案不代表已经在案例中实现。
- 参数与速度受硬件、软件版本和素材影响，历史数值不应当作通用保证。
- 案例放在 `example/<案例名>/`。说明写在该项目里，和音频、静帧、成片放在一起，并纳入版本库。
- 模型权重、第三方原始下载音源、字体和渲染缓存不放进仓库。案例项目里的歌曲相关音频是制作记录，不构成额外授权。

## 添加内容

新案例可复制[模板](docs/templates/case-study.md)，写清目标、输入、流程、实际参数、验证结果和限制，再更新本页入口。可复用的技术结论优先写入 `docs/guides/`，避免在多个案例中重复维护。

当前没有为第三方作品或模型授予额外使用权；使用相关资源时，请查阅各自来源与许可。
