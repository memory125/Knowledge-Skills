# Knowledge Skills for OpenClaw

This repository contains OpenClaw agent skills for knowledge processing, explanation, and analysis.

## Skills Included

### 🎓 Knowledge Explainer (知识通俗解释器)
将复杂的概念、术语、问题用大白话 + 完美居中教学视频的方式可视化呈现。所有文字内容在彩色卡片背景上，居中对齐，视觉体验极致优化。支持智能判断：简单概念生成 HTML5 Canvas/WebGL 视频（Puppeteer），复杂结构/动态过程自动切换 3D Blender 动画。让任何人都能轻松理解。

**Features:**
- Visual knowledge explanation with centered text cards
- Auto-generate HTML5 Canvas/WebGL videos for simple concepts
- Switch to 3D Blender animation for complex structures
- Color-coded backgrounds for better visual hierarchy
- Support for dynamic processes and structural diagrams

### 📚 Ebook Analyzer (电子书智能分析工具)
电子书智能分析工具：上传 PDF/EPUB/MOBI/DOCX 等格式，自动生成多维度读书笔记（本书内容、一句话总结、逻辑结构图谱、要点汇总、金句提取、作者思想、现实意义、适合读者、书籍评分等）

**Features:**
- Multi-format support: PDF, EPUB, MOBI, DOCX
- Auto-generate comprehensive reading notes
- One-sentence summary
- Logical structure diagram
- Key points extraction
- Golden quotes extraction
- Author's core philosophy analysis
- Real-world relevance assessment
- Reader suitability recommendation
- Book rating system

## Installation

Copy the skill folders to your OpenClaw workspace:

```bash
cp -r knowledge-explainer ~/.openclaw/workspace/skills/
cp -r ebook-analyzer ~/.openclaw/workspace/skills/
```

## Usage

Ask your OpenClaw agent:
- "帮我解释一下量子力学"
- "用大白话讲清楚区块链"
- "分析这本电子书的核心内容"
- "生成这本书的读书笔记"

## License

MIT License

## Author

memory125
