# MoviePilot UI Design References

本文件是 `moviepilot-ui-design` 的低频参考资料。常规 UI 任务优先读取 `SKILL.md`，只有需要吸收外部 UI 知识、复盘 UI 大学习、处理复杂图表/动效/候选技能时再看这里。

## Distillation Sources

本地 UI 能力曾吸收以下资料的可复用部分：

- Impeccable
- Taste Skill
- Designer Skills
- UI Design Brain
- UI UX Pro Max
- Anthropic frontend-design
- Vercel web design guidelines
- Better Icons
- Motion AI Kit
- 115 STRM helper UI study
- Vibe UI candidates: Figma implementation, UX research, visualization critique, theme discipline, data visualization, artifact layout

只保留方法，不复制品牌皮肤、安装噪声或外部运行依赖。

## Reference Distillation

当用户给 UI 参考或说“UI 大学习”：

1. 提取可复用结构，不提取品牌皮肤。
2. 保留信息架构、组件节奏、密度、状态模型、图标语义和交互模式。
3. 丢弃品牌资产、凭据、无关业务逻辑、营销效果和外部安装噪声。
4. 先转成 MoviePilot 安全规则，再实现。

## Vibe UI Candidate Handling

- **Figma implementation**：把 Figma 链接/截图当设计证据，提取布局、间距、字体、token、组件意图；不把 Figma MCP 作为硬依赖。
- **UX research**：使用轻量操作者旅程，如 novice admin、media curator、site maintainer、cautious operator；不制造厚重 persona 文档。
- **Visualization critique**：仪表盘与图表必须表达状态、趋势、风险和下一动作；先查标签、图例、比例、对比、颜色含义和空/错状态。
- **Theme discipline**：保留 MoviePilot 官方主题变量和语义色；外部配色只是参考。
- **Artifact layout**：报告、卡片、表格、向导页优先优化层级与扫读性。
- **Interactive polish**：交互图表、动画、生成图、演示效果只在提高操作安全或清晰度时使用。

默认落点是 `moviepilot-ui-design`，不要再拆出一堆泛 UI 技能。候选能力只可作为小规则、清单或实现模式进入本技能。

## Extended Component Notes

- Charts / visualizations：只有当表格不能更快解释状态、趋势、风险或比较时才使用；必须提供单位、轴标签和文本 fallback。
- Motion：tab/window/expansion/dialog 过渡通常足够；异步动作先有 loading/result feedback，再考虑装饰动画。
- High-risk actions：靠隔离、预览、确认和备份降低风险，不靠酷炫动效。
- Icons：语义一致比数量重要；不要给每个 label 都塞图标。
- Tables：用于可比较记录和历史；保留筛选、状态、结果、时间、路径等关键列。

## Extended Review Checklist

- 布局在窄屏是否可用？
- 图表是否有误导性比例或缺失单位？
- 操作按钮是否按任务和风险分组？
- 高级设置是否不会压过推荐路径？
- 风险文案是否明确列出数据、路径、站点、插件或任务范围？
- 失败状态是否告诉用户下一步能做什么？
- 插件配置字段是否保留兼容，不因 UI 重构丢键？
- 若改动作入口，是否检查插件命令/能力注册？
