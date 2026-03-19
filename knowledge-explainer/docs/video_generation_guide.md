# 🎬 视频生成技术指南

## 📋 概述

Knowledge Explainer v4.0 使用 **Python + Pillow + FFmpeg** 纯本地方案生成教学视频，无需 Node.js、Chrome、Remotion 等复杂环境。

### 核心技术栈

| 组件 | 技术选型 | 版本要求 | 用途 |
|--|-|-|-|
| **图像处理** | Python Pillow | >= 8.0 | 绘制帧图像 |
| **中文字体** | Google Noto Sans CJK | - | 最美开源字体 |
| **视频编码** | FFmpeg | >= 4.0 | MP4 合成 |
| **运行环境** | Python 3 | >= 3.8 | 脚本执行 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# Python 包
pip install pillow

# FFmpeg (视频编码必需)
sudo apt install ffmpeg      # Ubuntu/Debian
sudo yum install ffmpeg      # CentOS/RHEL
brew install ffmpeg          # macOS
```

### 2. 运行示例

```bash
cd /home/wing/.openclaw/workspace/skills/knowledge-explainer/generators
python3 generate_video_v3_fixed.py
```

**输出**:
- `output/four_heroes_v3.mp4` - 最终视频（约 275KB）
- `output/frame_*.png` - 600 张预览帧（可任意查看场景）

---

## 📐 视频规格

```python
# 在 generate_video_v3_fixed.py 中配置

WIDTH = 1920       # 全高清宽度
HEIGHT = 1080      # 全高清高度
FPS = 30           # 帧率
TOTAL_FRAMES = 600 # 总帧数 = 20 秒 * 30fps

# 输出参数
CODEC = "libx264"  # H.264 编码（兼容性最佳）
PIX_FMT = "yuv420p" # 像素格式
CRF = 18           # 质量参数（越小越好，18=高质量）
```

**最终输出**:
- 分辨率：1920x1080 (全高清)
- 时长：20.00 秒
- 帧率：30fps
- 大小：~275KB（CRF=18）
- 格式：MP4 (H.264 + AAC 可选)

---

## 🎨 字体配置（核心亮点）

### Google Noto Sans CJK (思源黑体)

```python
# 加载最美中文字体
def load_chinese_fonts():
    try:
        # 首选：Noto Sans CJK Bold (粗体)
        font_title = ImageFont.truetype(
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 
            72  # 标题字体大小
        )
        
        # 正文：Noto Sans CJK Regular (常规)
        font_text = ImageFont.truetype(
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 
            40  # 正文字体大小
        )
        
        return {'title': font_title, 'text': font_text}, "Noto Sans CJK"
    except:
        # 备用字体（降级方案）
        ...
```

### 字体优势

| 特点 | 说明 |
|--|-|
| **专为屏幕优化** | x 坐标对齐，边缘锐利，小字号仍清晰 |
| **字形统一美观** | 笔画粗细均匀，视觉平衡感强 |
| **多字重支持** | Black, Bold, Regular, DemiLight, Light |
| **开源免费** | Google 开源字体库核心成员 |
| **多语言支持** | 简繁体中文 + 日文假名 + 韩文+Emoji |

### 替代方案（如果未安装思源黑体）

```python
# 备选 1: Noto Serif CJK (思源宋体) - 传统优雅风格
font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc", 40)

# 备选 2: AR PL UMing (明体)
font = ImageFont.truetype("/usr/share/fonts/truetype/arphic/uming.ttc", 40)

# 备选 3: AR PL UKai (楷体)
font = ImageFont.truetype("/usr/share/fonts/truetype/arphic/ukai.ttc", 40)
```

---

## 🎬 分场景结构设计

### 时间轴分配（20 秒）

```
总帧数：600 帧 @ 30fps = 20 秒

Scene 1 (0-90 帧):   标题开场 (0-3 秒)          progress: 0.00 - 0.15
Scene 2 (90-210 帧):  概念 1 详解 (3-7 秒)         progress: 0.15 - 0.35
Scene 3 (210-330 帧): 概念 2 详解 (7-11 秒)        progress: 0.35 - 0.55
Scene 4 (330-450 帧): 概念 3 详解 (11-15 秒)       progress: 0.55 - 0.75
Scene 5 (450-540 帧): 概念 4 详解 (15-18 秒)       progress: 0.75 - 0.90
Scene 6 (540-600 帧): 记忆口诀总结 (18-20 秒)      progress: 0.90 - 1.00
```

### 场景切换逻辑

```python
def create_frame(frame_num, total_frames=600):
    """根据帧号创建对应场景"""
    progress = frame_num / total_frames
    
    if progress < 0.15:
        return create_scene_title(progress)
    elif progress < 0.35:
        return create_concept1_scene(progress)
    elif progress < 0.55:
        return create_concept2_scene(progress)
    # ... 其他场景
    
def create_concept1_scene(progress):
    """概念 1 详解场景"""
    local_progress = (progress - 0.15) / 0.20  # 归一化到 0-1
    
    # 绘制场景内容
    img = Image.new('RGB', (WIDTH, HEIGHT), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    # 元素渐入效果
    if local_progress > 0:
        draw_text_with_animation(draw, "概念 1 标题", local_progress)
    if local_progress > 0.3:
        draw_text_with_animation(draw, "特点 1", local_progress - 0.3)
    # ...
    
    return img
```

---

## 🎨 动画效果实现

### 渐入动画（Fade In）

```python
def fade_in_text(draw, text, progress, x, y):
    """文字渐入效果"""
    alpha = min(progress / 0.1, 1.0)  # 0.1 秒内完成渐入
    
    if alpha > 0:
        # Pillow 不支持透明度，使用替代方案：
        # 1. 先画半透明背景（浅色）
        # 2. 再画文字（深色）
        opacity = int(255 * alpha)
        
        # 这里用简单方案：只在 progress > threshold 时显示
        if progress > 0.05:
            draw.text((x, y), text, fill='#ffffff', font=font, anchor="mm")
```

### 逐条显示（Staggered）

```python
features = ["✅ 特点 1", "✅ 特点 2", "✅ 特点 3"]
for i, feature in enumerate(features):
    # 每个特点延迟 0.2 秒显示
    delay = i * 0.2
    if local_progress > delay:
        draw.text((x, y + i * 65), feature, fill='#ffffff', font=font_text)
```

### 底部导航进度条

```python
# Scene 2 (概念 1)
nav_text = "概念 1 ▮ 概念 2 ◯ 概念 3 ◯ 概念 4"
draw.rectangle([0, height-80, width, height], fill=COLORS['skill'])
draw.text((width // 2, height - 40), nav_text, fill='#cccccc', font=font_small)
```

---

## 🛠️ 自定义主题视频

### Step 1: 复制脚本

```bash
cd /home/wing/.openclaw/workspace/skills/knowledge-explainer/generators
cp generate_video_v3_fixed.py my_custom_topic.py
```

### Step 2: 修改概念内容

编辑 `my_custom_topic.py`:

```python
# 找到场景函数，替换成你的概念

def create_agent_scene(progress):
    """Scene 2: 你的概念 1"""
    
    # 修改标题
    draw.text((width // 2, 80), "第 1 剑：你的概念", 
              fill=COLORS['agent'], font=GLOBAL_FONTS['title'])
    
    # 修改特点列表
    features = [
        "✅ 你的特点 1",
        "✅ 你的特点 2", 
        "✅ 你的特点 3"
    ]
```

### Step 3: 调整配色（可选）

```python
COLORS = {
    'bg': '#1a1a2e',           # 背景色
    'concept1': '#e94560',     # 概念 1 颜色（红）
    'concept2': '#0f3460',     # 概念 2 颜色（蓝）
    'concept3': '#16213e',     # 概念 3 颜色（深蓝）
    'concept4': '#533483',     # 概念 4 颜色（紫）
}
```

### Step 4: 生成视频

```bash
python3 my_custom_topic.py

# 输出：output/your_topic.mp4
```

---

## 🔧 常见问题

### Q1: 中文显示乱码？

**A**: 确保已加载支持中文的字体：

```python
# ✅ 正确
font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 40)

# ❌ 错误（默认字体不支持中文）
font = ImageFont.load_default()
```

### Q2: FFmpeg 未找到？

**A**: 安装 FFmpeg：

```bash
sudo apt install ffmpeg
```

### Q3: 视频文件过大？

**A**: 调整 CRF 参数（18→23，质量稍降）：

```python
cmd = [
    "ffmpeg", "-y", "-framerate", "30", "-i", input_pattern,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", 
    "-crf", "23",  # 18=高质量，23=适中，28=低质量
    output_mp4
]
```

### Q4: 如何添加音频？

**A**: 在 FFmpeg 命令中添加音频轨道：

```python
cmd = [
    "ffmpeg", "-y",
    "-framerate", "30", "-i", "frame_%04d.png",
    "-i", "background_music.mp3",  # 添加音频文件
    "-c:v", "libx264",
    "-c:a", "aac",                # 音频编码
    "-shortest",                 # 以较短的轨道为准
    output_mp4
]
```

---

## 📚 参考资料

- **Pillow 官方文档**: https://pillow.readthedocs.io/
- **FFmpeg 官方文档**: https://ffmpeg.org/documentation.html
- **Google Noto Fonts**: https://github.com/googlefonts/noto-cjk
- **H.264 编码参数**: https://trac.ffmpeg.org/wiki/Encode/H.264

---

*本指南基于 Knowledge Explainer v4.0 实际项目整理* 🎬✨
