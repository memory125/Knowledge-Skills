# Knowledge Skills for OpenClaw

This repository contains OpenClaw agent skills for knowledge processing, explanation, analysis, and 3D visualization.

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

### 🎬 Blender Video Generator (专业级 3D 教学视频生成)
专业级 3D 教学视频生成技能。使用 Blender Python API 创建 3D 动画视频，支持量子力学、费曼学习法、区块链、AI 神经网络等主题。包含完整工作流：场景搭建、材质配置、关键帧动画、渲染输出。

**Features:**
- Professional 3D educational video generation
- Blender Python API integration
- Complete workflow: scene setup, material configuration, keyframe animation, rendering
- Supports quantum mechanics, Feynman learning method, blockchain, AI neural networks themes
- Both Eevee (fast) and Cycles (high quality) render engines
- Ideal for 3D concept demonstration, physics simulation, cinema-grade visualization

## Installation

Copy the skill folders to your OpenClaw workspace:

```bash
cp -r knowledge-explainer ~/.openclaw/workspace/skills/
cp -r ebook-analyzer ~/.openclaw/workspace/skills/
cp -r blender-video-generator ~/.openclaw/workspace/skills/
```

## Usage

Ask your OpenClaw agent:

**Knowledge Explainer:**
- "帮我解释一下量子力学"
- "用大白话讲清楚区块链"
- "生成神经网络的教学视频"

**Ebook Analyzer:**
- "分析这本电子书的核心内容"
- "生成这本书的读书笔记"
- "提取这本书的金句"

**Blender Video Generator:**
- "生成量子力学的 3D 演示视频"
- "用 Blender 创建费曼学习法的动画"
- "制作区块链概念的 3D 教学视频"

## Quick Start

### Knowledge Explainer
```bash
cd ~/.openclaw/workspace/skills/knowledge-explainer
python3 explainer.py
```

### Ebook Analyzer
```bash
cd ~/.openclaw/workspace/skills/ebook-analyzer
python3 analyzer.py your-book.pdf
```

### Blender Video Generator
```bash
cd ~/.openclaw/workspace/skills/blender-video-generator
python3 scripts/generate_video.py --topic "quantum_mechanics"
```

## Project Structure

```
Knowledge-Skills/
├── knowledge-explainer/          # 知识通俗解释器
│   ├── explainer.py              # 主程序
│   ├── generators/               # 视频生成器
│   ├── templates/                # HTML 模板
│   └── references/               # 参考资料
├── ebook-analyzer/               # 电子书分析工具
│   ├── analyzer.py               # 主程序
│   ├── templates/                # 笔记模板
│   └── references/               # 分析维度
├── blender-video-generator/      # 3D 视频生成器
│   ├── scripts/                  # Blender 脚本
│   ├── references/               # 主题库、材质库
│   └── workflow.md               # 工作流程
└── README.md                     # 本文件
```

## License

MIT License

## Author

memory125

## Links

- Chinese Classics Skills: https://github.com/memory125/Chinese-Classics-Skills
- OpenClaw Docs: https://docs.openclaw.ai
- ClawHub: https://clawhub.com
