# 📚 Ebook Analyzer v2.0 - 37 维深度分析系统

## 🎯 版本更新 (v1.0 → v2.0)

| 特性 | v1.0 | v2.0 |
|------|-------|-|
| **分析维度** | 9 个 | 37 个（全面升级） |
| **预设模式** | 无 | 8 种场景模式 |
| **自定义维度** | 不支持 | 支持灵活组合 |
| **超时时间** | 5 分钟 | 10 分钟（深度分析） |
| **词频分析** | 不支持 | 支持关键词云 |

---

## 🚀 快速开始

### 列出所有预设模式
```bash
./ebook-analyzer analyze book.pdf --list-modes
```

### 列出所有 37 个维度
```bash
./ebook-analyzer analyze book.pdf --list-dimensions
```

---

## 📊 8 种预设分析模式

| 模式名 | 维度数 | 适用场景 | 命令示例 |
|--------|-------|---------|---------|
| `quick` | 4 维 | 快速筛选，决定是否深入阅读 | `--mode quick` |
| `core` | 9 维 | 经典九维基础分析 | `--mode core` |
| `deep` | 20 维 | **推荐**深度精读 | `--mode deep` |
| `academic` | 17 维 | 学术研究、批判性分析 | `--mode academic` |
| `skill` | 9 维 | 技能提升、方法提取 | `--mode skill` |
| `literature` | 8 维 | 小说/文学欣赏 | `--mode literature` |
| `discussion` | 8 维 | 读书会、读书分享准备 | `--mode discussion` |
| `all` | 37 维 | 完整分析（仅推荐长书） | `--mode all` |

---

## 💡 使用指南

### 方法 1：预设模式（推荐）

```bash
# 快速筛选 - 5 分钟搞定
./ebook-analyzer analyze book.pdf --mode quick

# 深度阅读 - 20 维全面分析（最常用）
./ebook-analyzer analyze book.epub --mode deep

# 学术研究 - 批判性思维导向
./ebook-analyzer analyze thesis.pdf --mode academic

# 技能提升 - 提取方法 + 行动清单
./ebook-analyzer analyze skills.docx --mode skill

# 文学欣赏 - 分析写作技巧
./ebook-analyzer analyze novel.epub --mode literature

# 读书会准备 - 讨论问题 + 共鸣记录
./ebook-analyzer analyze book.pdf --mode discussion
```

### 方法 2：自定义维度组合

```bash
# 维度编号说明：1-37（见下文完整列表）

# 示例 1：只要核心九维中的部分内容
./ebook-analyzer analyze book.pdf --dimensions "1,2,5,7,9"

# 示例 2：组合不同类别的维度
./ebook-analyzer analyze book.epub --dimensions "1-3,19,25,33"

# 示例 3：混合范围 + 单个
./ebook-analyzer analyze book.docx --dimensions "1-5,14,20,25,37"
```

### 方法 3：导出文件

```bash
# Markdown 格式（默认）
./ebook-analyzer analyze book.pdf --mode deep -o notes.md

# JSON 格式（需要自行解析输出）
./ebook-analyzer analyze book.epub --mode skill -o analysis.json
```

---

## 📋 37 维完整索引

### 🎯 核心九维 (1-9)
| 编号 | 维度 | 图标 |
|------|-------|-|
| 1 | 内容概述 | 📖 |
| 2 | 一句话总结 | 💡 |
| 3 | 结构图谱 | 🗺️ |
| 4 | 本书要点 | 🔑 |
| 5 | 金句汇总 | ✨ |
| 6 | 作者思想 | 🎯 |
| 7 | 现实意义 | 🌍 |
| 8 | 适合读者 | 👥 |
| 9 | 书籍评分 | ⭐ |

### 📐 文本结构层 (10-12)
| 编号 | 维度 | 图标 |
|------|-------|-|
| 10 | 写作手法分析 | ✍️ |
| 11 | 章节脉络图 | 📚 |
| 12 | 关键词云 | ☁️ |

### 💭 思想内容层 (13-17)
| 编号 | 维度 | 图标 |
|------|-------|-|
| 13 | 核心问题清单 | ❓ |
| 14 | 概念词典 | 📖 |
| 15 | 论证逻辑链 | 🔗 |
| 16 | 人物弧光分析 | 👤 |
| 17 | 冲突类型分析 | ⚔️ |

### 🧠 知识体系层 (18-20)
| 编号 | 维度 | 图标 |
|------|-------|-|
| 18 | 知识图谱 | 🌐 |
| 19 | 方法论清单 | 🛠️ |
| 20 | 案例库 | 📋 |

### ⚖️ 批判性思维层 (21-24)
| 编号 | 维度 | 图标 |
|------|-------|-|
| 21 | 潜在偏见识别 | ⚖️ |
| 22 | 逻辑漏洞检测 | 🔍 |
| 23 | 反方观点 | ↔️ |
| 24 | 争议点整理 | 🎭 |

### 🚀 学习应用层 (25-28)
| 编号 | 维度 | 图标 |
|------|-------|-|
| 25 | 行动清单 | ✅ |
| 26 | 习惯养成计划 | 📅 |
| 27 | 讨论问题集 | 💬 |
| 28 | 复习要点 | 📝 |

### 🔗 跨文本分析层 (29-31)
| 编号 | 维度 | 图标 |
|------|-------|-|
| 29 | 同类书对比 | 🔀 |
| 30 | 思想渊源追溯 | 🌳 |
| 31 | 后续影响评估 | 📢 |

### 🌱 个人成长层 (32-34)
| 编号 | 维度 | 图标 |
|------|-------|-|
| 32 | 共鸣记录 | ❤️ |
| 33 | 认知升级点 | 🧠 |
| 34 | 引用创作素材库 | ✏️ |

### 🎓 元认知层 (35-37)
| 编号 | 维度 | 图标 |
|------|-------|-|
| 35 | 阅读反思日志 | 📔 |
| 36 | 知识体系定位 | 🗺️ |
| 37 | 未解答的问题 | ❔ |

---

## 🎨 输出样例（深度模式）

```markdown
# 《原子习惯》深度阅读分析

> 作者：詹姆斯·克利尔  
> 分析日期：2026-03-08  
> 分析维度：20 维

---

## 📖 内容概述

《原子习惯》是一本关于行为改变的实操指南...
（500 字详细概述）

---

## 💡 一句话总结

通过微小改变积累巨大成果，4% 的改进带来惊人复利效应。

---

## 🗺️ 结构图谱

```
身份认同 → 四大法则 → 系统优化 → 持续改进
    ↓          ↓           ↓          ↓
是谁       怎么做      如何坚持    如何迭代
```

---

## 🔑 本书要点

1. **复利效应**: 每天进步 1%，一年后成长 37 倍
2. **系统优于目标**: 关注过程而非结果
3. **身份改变**: 从"我想做什么"到"我是谁"
4. **环境设计**: 让好习惯显而易见...
（共 5-10 个要点）

---

## ✨ 金句汇总

> "你不会达到自己的野心高度，你会跌落到你的系统水平。" - 第 2 章

> "习惯是复利的魔法，微小改变带来巨大成果。" - 第 1 章

（共 5-8 句）

---

## 🛠️ 方法论清单

### 方法 1: 两分钟规则
**步骤:**
1. 将新习惯缩减到 2 分钟内可完成
2. 例如："读完一本书" → "读一页书"
3. 建立惯性后再逐步扩展

**关键注意点:**
- 重点是开始，不是完成
- 降低门槛才能养成习惯

（共提取多个方法论）

---

## ✅ 行动清单

本周可执行:
☐ 识别一个想要改变的习惯
☐ 使用"两分钟规则"重新定义它
☐ 设计环境提示（如把书放在床头）
☐ 建立追踪系统

---

... (其他 17 个维度)

---

## ⭐ 书籍评分

| 维度 | 评分 | 理由 |
|------|------|------|
| 内容深度 | 5/5 | 理论基础扎实，案例丰富 |
| 可读性 | 4/5 | 语言简洁，结构清晰 |
| 启发性 | 5/5 | 提供了大量可操作的方法 |

综合评价：⭐⭐⭐⭐⭐ (强烈推荐)
```

---

## ⚙️ 高级技巧

### 技巧 1：多模式组合使用
```bash
# 先用 quick 快速筛选
./ebook-analyzer analyze book.pdf --mode quick

# 决定深入后，用 deep 完整分析
./ebook-analyzer analyze book.pdf --mode deep -o full_analysis.md
```

### 技巧 2：针对特定需求定制
```bash
# 写论文需要：核心内容 + 论证逻辑 + 批判性分析
./ebook-analyzer analyze source.pdf --dimensions "1-3,6,13-15,21-24,29-30"

# 想学技能：方法论 + 行动清单 + 复习要点
./ebook-analyzer analyze skills.epub --dimensions "1,2,19,20,25,28"
```

### 技巧 3：长书分段分析
```bash
# 如果书籍超过 500 页，考虑分章节处理
# 先提取文本预览结构
./ebook-analyzer extract long-book.pdf

# 根据章节手动分割后分别分析
```

---

## 🎯 推荐工作流

### 场景 A：买书前的决策
```bash
# 只看 core+8，快速判断是否值得深入阅读
./ebook-analyzer analyze book.pdf --dimensions "1,2,4,8"
```

### 场景 B：精读一本好书
```bash
# 第一天：基础理解（模式 quick + deep）
./ebook-analyzer analyze book.pdf --mode quick
./ebook-analyzer analyze book.pdf --mode deep -o day1.md

# 第三天：应用转化（技能提升维度）
./ebook-analyzer analyze book.pdf --dimensions "19,20,25,26" -o actions.md

# 第七天：深化思考（批判性维度）
./ebook-analyzer analyze book.pdf --dimensions "6,13-15,21-24,37" -o reflection.md
```

### 场景 C：学术研究
```bash
# 学术模式 + 文献对比
./ebook-analyzer analyze thesis.pdf --mode academic -o research_analysis.md
```

---

## 🐛 故障排除

| 问题 | 原因 | 解决 |
|------|------|-------|
| Ollama 未找到 | 服务未运行 | `ollama serve` |
| 分析超时 | 维度太多/书太长 | 减少维度或分段处理 |
| 模型未下载 | 指定模型不存在 | `ollama pull qwen2.5` |
| PDF 无法提取 | 加密/扫描版 | 使用 OCR 工具预处理 |

---

## 📞 获取帮助

```bash
# 查看所有参数
./ebook-analyzer --help

# 查看预设模式
./ebook-analyzer analyze book.pdf --list-modes

# 查看所有维度
./ebook-analyzer analyze book.pdf --list-dimensions
```

---

*让每一本书都成为你的知识资产 - v2.0 深度阅读系统*
