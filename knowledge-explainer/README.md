# 📁 Knowledge Explainer v4.0 - 目录结构说明

## 📂 完整文件树

```
knowledge-explainer/
├── 📋 SKILL.md                    # Skill 定义文档（ClawHub 格式）
├── 📖 README.md                  # 本文件 - 使用说明
├── 🚀 explainer_v4.py            # v4.0 核心解释器代码
├── 🧪 explainer.py               # v1.0（保留供参考）
├── 🔧 explainer_v2.py            # v2.0（保留供参考）
│
├── 📁 generators/                # 视频生成器模块
│   └── generate_video_v3_fixed.py  # Python+Pillow+FFmpeg视频生成器⭐
│       • 分场景展示（6 个独立场景）
│       • Google 思源黑体字体（最美中文字体）
│       • 20 秒全高清视频输出
│
├── 📁 examples/                  # 示例和成果展示
│   ├── four_heroes_v3.mp4         # AI 四剑客教学视频（275KB, 20s）⭐
│   ├── ai_concepts_comparison.md  # 可视化对比图表
│   ├── ai_concepts_full.md        # 完整解析文档
│   ├── frame_0090.png             # Scene 1: 标题开场预览图
│   ├── frame_0240.png             # Scene 2: Agent 详解预览图
│   └── frame_0589.png             # Scene 6: 记忆口诀预览图
│
├── 📁 templates/                 # 输出模板（待扩展）
│   └── note_template.md           # Markdown 笔记模板
│
├── 📁 docs/                      # 技术文档（待扩展）
│   └── video_generation_guide.md  # 视频生成详细指南
│
└── 📁 references/                # 参考资料（待扩展）
    └── analysis_dimensions.md     # 分析维度说明
```

---

## 🎯 快速开始

### 1️⃣ 安装依赖

```bash
# Python 依赖（一次性安装）
pip install pillow

# FFmpeg（视频编码必需）
sudo apt install ffmpeg
```

### 2️⃣ 使用解释器

```bash
# 方式 A: 通过启动脚本（推荐）
cd /home/wing/.openclaw/workspace
./knowledge-explainer-v4 "什么是区块链" --depth 3 --visuals

# 方式 B: 直接运行 Python 脚本
cd /home/wing/.openclaw/workspace/skills/knowledge-explainer
python3 explainer_v4.py "量子力学" --depth 4 --analogies

# 方式 C: 生成教学视频 ✨
./knowledge-explainer-v4 "AI 四剑客" --all-features
```

### 3️⃣ 查看示例成果

```bash
# 播放 AI 四剑客教学视频（20 秒，分场景展示）
xdg-open examples/four_heroes_v3.mp4

# 查看场景预览图
xdg-open examples/frame_0090.png  # Scene 1 标题
xdg-open examples/frame_0240.png  # Scene 2 Agent
xdg-open examples/frame_0589.png  # Scene 6 总结

# 阅读四剑客完整解析
cat examples/ai_concepts_comparison.md | less
```

### 4️⃣ 生成自定义主题视频

```bash
cd generators

# 1. 复制脚本
cp generate_video_v3_fixed.py my_custom_video.py

# 2. 编辑脚本中的概念内容
nano my_custom_video.py
# 修改 create_agent_scene() → 改成你的概念 1
# 修改 create_skill_scene() → 改成你的概念 2
# ...

# 3. 生成视频
python3 my_custom_video.py

# 输出：output/your_topic.mp4
```

---

## 📊 版本对比

| 功能 | v1.0 | v2.0 | v3.0 | **v4.0** ⭐ |
|--|-|-|-|--|
| 大白话解释 | ✅ | ✅ | ✅ | ✅ |
| ASCII/Mermaid图表 | ❌ | ✅ | ✅ | ✅ |
| 生活类比 | ✅ | ✅ | ✅ | ✅ |
| **MP4 视频生成** | ❌ | ❌ | ❌ | **✅** |
| **最美字体（思源黑体）** | ❌ | ❌ | ❌ | **✅** 🎨 |
| **分场景深度讲解** | ❌ | ❌ | ❌ | **✅** 🎬 |
| **统一目录结构** | ❌ | ❌ | ❌ | **✅** 📁 |

---

## 🔧 技术架构

### 视频生成技术栈 ✨

```
generators/generate_video_v3_fixed.py
    ↓
├── Python Pillow          # 图像绘制（支持中文）
├── Google Noto Sans CJK   # 最美开源中文字体（思源黑体）
│   ├── Bold.ttc (72px)    # 标题粗体
│   └── Regular.ttc (40px) # 正文常规
└── FFmpeg H.264           # 视频编码（兼容性最佳）
```

### 分场景结构设计 🎬

```
总时长：20 秒 (600 帧 @ 30fps)

Scene 1 (0-3s):   标题开场              [0-90 帧]
Scene 2 (3-7s):   概念 1 详解             [90-210 帧]
Scene 3 (7-11s):  概念 2 详解             [210-330 帧]
Scene 4 (11-15s): 概念 3 详解             [330-450 帧]
Scene 5 (15-18s): 概念 4 详解             [450-540 帧]
Scene 6 (18-20s): 记忆口诀总结          [540-600 帧]
```

---

## 📝 输出示例

### Markdown 格式（默认）

```markdown
# 📚 区块链是什么？（大白话版）

> **"就像全班同学共同记账，没人能改别人的账"**

## 🎯 核心概念

用通俗易懂的语言解释...

## 🎭 生活化比喻

[ASCII/Mermaid可视化图表]

## 💡 记忆要点

1. **公开透明** - 所有人能看到所有交易
2. **不可篡改** - 一旦写入就改不了  
3. **共同维护** - 靠数学而不是人治
```

### MP4 视频格式 ✨

- **文件位置**: `examples/four_heroes_v3.mp4`
- **规格**: 1920x1080, H.264, 30fps, 20 秒，275KB
- **特点**: 
  - 6 个独立场景，逐个深入讲解
  - Google 思源黑体字体，视觉精美
  - 兼容性极佳（VLC/QuickTime/浏览器都支持）

---

## 🎁 核心成果

### ✅ 已实现功能

1. **知识通俗解释**
   - 专业术语 → 生活化语言
   - 自动判断难度等级
   - 多维度类比系统

2. **可视化图表生成**
   - ASCII 艺术图（无需 API）
   - Mermaid 流程图（代码转图）
   - 对比表格（清晰展示差异）

3. **MP4 教学视频** ✨
   - Python+Pillow+FFmpeg 纯本地方案
   - Google 思源黑体最美字体
   - 分场景独立展示结构
   - 20 秒深度讲解，信息密度适中

### 📂 示例成果（examples/目录）

- `four_heroes_v3.mp4` - AI 四剑客教学视频（275KB）
- `ai_concepts_comparison.md` - 可视化对比图（8.5KB）
- `ai_concepts_full.md` - 完整解析文档（2.9KB）
- `frame_*.png` - 场景预览图（可任意查看）

---

## 🚀 扩展开发

### 添加新概念到视频生成器

```python
# 在 generators/generate_video_v3_fixed.py 中添加新场景函数

def create_concept1_scene(progress):
    """新概念 1 详解"""
    width, height = 1920, 1080
    local_progress = (progress - 0.15) / 0.20
    
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    # 场景标题
    draw.text((width // 2, 80), "概念 1: XXX", fill=COLORS['color'], 
              font=GLOBAL_FONTS['title'], anchor="mm")
    
    # ... 添加具体内容
    
    return img

# 在 create_frame() 函数中添加新场景分支
elif progress < 0.35:
    return create_concept1_scene(progress)
```

### 自定义字体配置

```python
# generators/generate_video_v3_fixed.py - load_chinese_fonts()

# 已配置：Google Noto Sans CJK (思源黑体)
font_title = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 72)

# 可选其他字体（如果系统已安装）:
# - /usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc (思源宋体)
# - /usr/share/fonts/truetype/arphic/uming.ttc (明体)
# - /usr/share/fonts/truetype/arphic/ukai.ttc (楷体)
```

---

## 📞 反馈与支持

遇到问题？

- **解释不够通俗** → `--depth 1`（一句话级别）
- **需要更多类比** → `--analogies`（生活化比喻）
- **想要可视化** → `--visuals`（ASCII/Mermaid图表）
- **生成教学视频** → `--video`（MP4 分场景动画）✨

---

*让知识像漫画一样有趣，像聊天一样简单，像电影一样生动！* 🎨📚🎬✨

**版本**: 4.0  
**更新**: 2026-03-09  
**作者**: OpenClaw AI Team
