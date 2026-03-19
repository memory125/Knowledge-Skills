# 📚 Ebook Analyzer - 电子书智能分析工具

完全本地化的电子书分析工具，无需任何外部 API，使用本地 Ollama 模型进行深度内容分析和总结。

## ✨ 核心特性

- **🔒 完全本地化**: 所有内容处理在本地完成，保护隐私
- **📖 多格式支持**: PDF, EPUB, DOCX, PPTX 等常见格式
- **🎯 九维分析**: 本书内容、一句话总结、逻辑结构、要点、金句、作者思想、现实意义、适合读者、书籍评分
- **🤖 AI 驱动**: 利用本地 Ollama 模型智能分析
- **⚡ 快速生成**: 自动生成结构化读书笔记

## 📋 系统要求

### 必需
- **Python 3.8+**
- **Ollama** (已安装并运行 `ollama serve`)
- **推荐模型**: qwen2.5, llama3.1, 或任何中文能力强的本地模型

### 可选依赖（根据格式）
```bash
# PDF 支持
pip install pdfplumber

# Word 文档支持  
pip install python-docx

# PPT 演示文稿支持
pip install python-pptx

# EPUB 电子书支持
pip install ebooklib

# 一次性安装所有
pip install pdfplumber python-docx python-pptx ebooklib
```

## 🚀 快速开始

### 1. 确保 Ollama 已运行
```bash
# 启动 Ollama 服务
ollama serve

# 拉取推荐模型（首次）
ollama pull qwen2.5
```

### 2. 安装依赖库
```bash
cd /home/wing/.openclaw/workspace/skills/ebook-analyzer
pip install pdfplumber python-docx python-pptx ebooklib
```

### 3. 运行分析
```bash
# 基本用法
python analyzer.py analyze /path/to/your/book.pdf

# 指定模型
python analyzer.py analyze book.epub --model llama3.1

# 导出到文件
python analyzer.py analyze book.docx --output notes.md

# JSON 格式输出
python analyzer.py analyze book.pdf --format json -o analysis.json
```

## 📖 使用示例

### 示例 1: 分析 PDF 书籍
```bash
python analyzer.py analyze "/home/wing/Books/深度工作.pdf"
```

### 示例 2: 分析 EPUB 电子书
```bash
python analyzer.py analyze "./books/atomic-habits.epub" --model qwen2.5 -o ./atomic-habits-notes.md
```

### 示例 3: 分析 Word 文档
```bash
python analyzer.py analyze "document.docx"
```

## 📊 输出样例

分析报告包含以下九个维度：

```markdown
# 《深度工作》读书笔记

## 📖 本书内容
卡尔·纽波特的《深度工作》探讨了在碎片化时代如何培养专注力的重要性...

## 💡 一句话总结
掌握深度工作能力是信息时代的稀缺技能，能带来巨大竞争优势。

## 🗺️ 逻辑结构图谱
深度工作概念 → 四种哲学 → 实施策略 → 消除浅薄 → 培养习惯

## 🔑 本书要点
1. 深度工作的定义：在无干扰状态下进行职业活动
2. 深度工作假设：这种能力能带来高价值产出
...

## ✨ 金句汇总
> "在分心的世界中，专注力就是超能力" - 第 2 章
> "浅薄的工作越多，深度工作的能力就越弱" - 第 3 章
...

## 🎯 作者思想
卡尔·纽波特认为现代社会的结构性问题导致注意力分散...

## 🌍 现实意义
对知识工作者、学生、创作者都有重要的实践指导价值...

## 👥 适合读者
- 知识工作者和程序员
- 需要长时间专注的学生和研究者
- 希望提升工作效率的职场人士
...

## ⭐ 书籍评分
| 维度 | 评分 | 备注 |
|------|------|------|
| 内容深度 | ⭐⭐⭐⭐⭐ (5/5) | 理论基础扎实，案例丰富 |
| 可读性 | ⭐⭐⭐⭐ (4/5) | 逻辑清晰，语言简洁 |
| 启发性 | ⭐⭐⭐⭐⭐ (5/5) | 提供了具体的行动指南 |
```

## ⚙️ 高级选项

### 选择分析模型
```bash
# 查看已安装的模型
ollama list

# 使用特定模型
python analyzer.py analyze book.pdf --model llama3.1
python analyzer.py analyze book.epub --model mistral
```

### 自定义输出格式
```bash
# Markdown 格式（默认）
python analyzer.py analyze book.pdf --format markdown

# JSON 格式（便于后续处理）
python analyzer.py analyze book.pdf --format json -o analysis.json
```

## 🔧 故障排除

### 问题：无法提取 PDF 内容
**解决**: 安装 pdfplumber
```bash
pip install pdfplumber
```

### 问题：Ollama 未找到
**解决**: 确保 Ollama 服务已运行
```bash
ollama serve  # 在后台运行
```

### 问题：分析超时
**解决**: 
- 书籍过长时，可以分段处理
- 选择更快的模型（如 qwen2.5:7b）
- 增加超时时间（修改代码中的 timeout 参数）

### 问题：中文乱码
**解决**: 确保使用支持中文的模型
```bash
ollama pull qwen2.5  # 推荐
# 或
ollama pull llama3.1
```

## 📝 分析维度说明

工具会自动从以下九个维度进行分析：

| 维度 | 内容 | 字数建议 |
|------|------|---------|
| 本书内容 | 全书概述和结构 | 300-500 字 |
| 一句话总结 | 精炼核心 | ≤50 字 |
| 逻辑结构图谱 | 概念/人物关系 | 可视化 |
| 本书要点 | 核心观点提取 | 5-10 点 |
| 金句汇总 | 名言警句摘录 | 5-8 句 |
| 作者思想 | 深度分析 | 200-300 字 |
| 现实意义 | 实用价值 | 具体可行 |
| 适合读者 | 目标人群 | 画像描述 |
| 书籍评分 | 多维度评价 | 5 星制 |

## 🤝 贡献与反馈

欢迎提出改进建议和 Issue！

## 📄 License

MIT License

---

*让每一本书都成为你的知识资产*
