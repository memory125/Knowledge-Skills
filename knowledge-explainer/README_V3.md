# 📚 Knowledge Explainer v3.0 - 全功能知识解释系统

> **"把专家的知识，变成人人能懂的生动内容"** 🎨🎬🎤

**v3.0 核心升级：集成 Remotion 视频生成，实现文字→漫画→语音→视频的全方位知识呈现！**

---

## 🎯 **版本对比**

| 功能 | v1.0 | v2.0 | **v3.0** |
|------|-|-|-|
| 大白话解释 | ✅ | ✅ | ✅ |
| ASCII 图示 | ✅ | ✅ | ✅ |
| AI 漫画生成 | ❌ | ✅ | ✅ |
| 语音解说 | ❌ | ✅ | ✅ |
| 互动问答 | ❌ | ✅ | ✅ |
| 领域模板 | ❌ | ✅ | ✅ |
| 视频推荐 | ❌ | ✅ | ✅ |
| **自动视频生成** | ❌ | ❌ | **✅ Remotion** |

---

## 🚀 **v3.0 核心特性详解**

### 1️⃣ **智能知识解释（基础）**
```bash
./knowledge-explainer-v3 "区块链是什么"
```
输出：
- 💡 一句话总结（30 秒快速理解）
- 🎭 ASCII 漫画场景
- 💡 2-3 个生活化比喻
- 🔑 3-5 个核心要点
- 🔄 对比表格
- 🤔 常见问题预判

---

### 2️⃣ **AI 漫画生成（v2+）**
```bash
./knowledge-explainer-v3 "量子力学" --comic
```
**功能**：
- 自动调用 ComfyUI/Stable Diffusion
- 生成概念相关的卡通风格插图
- 支持多种风格：cartoon/comic/anime/infographic

**输出**：
```
✅ 漫画图片已生成: /tmp/knowledge-v3/comic_量子力学.png
```

---

### 3️⃣ **语音解说（v2+）**
```bash
./knowledge-explainer-v3 "人工智能原理" --audio
```
**功能**：
- Edge TTS（微软免费 TTS）生成中文语音
- 支持多种声音选择（女声/男声/儿童音）
- 可调节语速和音调

**输出**：
```
✅ 语音文件已生成: /tmp/knowledge-v3/explanation_20260309.mp3
⏱️ 时长：约 2-3 分钟
```

---

### 4️⃣ **互动问答（v2+）**
```bash
./knowledge-explainer-v3 interact "光合作用"
```
**功能**：
- 5 轮深度对话
- 根据上下文调整回答深度
- 循序渐进的引导式学习

**示例对话**：
```
🤖 进入互动问答模式
[第 1 轮] 你的问题：什么是光反应？
💡 首先让我们了解基础：就像植物在晒太阳...

[第 2 轮] 你的问题：那暗反应呢？
💡 进一步来说：这就像厨房里的加工环节...
```

---

### 5️⃣ **领域专用模板（v2+）**
```bash
./knowledge-explainer-v3 "癌症筛查" --domain medical
```
**支持领域**：
- 🏥 `medical` - 医学健康（带免责声明）
- ⚖️ `legal` - 法律常识（普法风格）
- 💻 `tech` - 科技产品（适度专业）
- 💰 `finance` - 投资理财（风险提示）
- 🔬 `science` - 科普知识（探索风格）

---

### 6️⃣ **视频推荐（v2+）**
```bash
./knowledge-explainer-v3 "黑洞是什么" --video
```
**功能**：
- 自动搜索 Bilibili/YouTube 相关科普视频
- 筛选适合初学者的内容
- 生成带链接的推荐列表

---

### 🎬 **7️⃣ Remotion 视频生成（v3.0 新特性）**
```bash
./knowledge-explainer-v3 "区块链原理" --video-generate -o block_chain.mp4
```

**核心功能**：
1. **自动生成 React 组件**: Python → TypeScript 代码转换
2. **智能内容提取**: 自动提取关键信息（总结、要点）
3. **动态视觉效果**:
   - 🎯 开场动画：概念标题淡入
   - 📊 要点展示：逐条出现，带淡入效果
   - 💡 总结场景：强调记忆点

**示例输出结构**：
```
Video Timeline (60 秒):
├── 0-3s:   开场黑屏 → Logo 动画
├── 3-10s:  "区块链是什么" 标题淡入
├── 10-20s: "大白话版解释" 副标题
├── 20-50s: 3 个核心要点逐条展示（每条 10 秒）
│   ├── 要点 1: "公开透明" + 动画效果
│   ├── 要点 2: "不可篡改" + 动画效果
│   └── 要点 3: "共同维护" + 动画效果
└── 50-60s: 💡 一句话总结（记忆点）
```

**输出文件**：
```
✅ 视频生成成功！
📁 /tmp/knowledge-videos/block_chain_video.mp4
🎬 时长：60 秒 | 分辨率：1280x720 | FPS: 30
```

---

## 💻 **系统要求**

### 基础环境（必需）
```bash
# Python 3.8+
python --version

# Ollama + 中文模型
ollama serve
ollama pull qwen2.5
```

### v3.0 完整环境（可选功能）
```bash
# Node.js 16+ (Remotion 需要)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# npm packages
npm install -g @remotion/cli

# Python dependencies
pip install --break-system-packages requests yt-dlp edge-tts
```

---

## 📖 **使用指南**

### 场景 1: 快速了解概念（基础模式）
```bash
./knowledge-explainer-v3 "什么是元宇宙"
```

### 场景 2: 深度学习和可视化（推荐）
```bash
# 文本 + 漫画
./knowledge-explainer-v3 "量子纠缠" --comic -o quantum.md

# 文本 + 语音（可边听边看）
./knowledge-explainer-v3 "光合作用" --audio

# 全功能开启
./knowledge-explainer-v3 "人工智能原理" --all-features -o ai_full.md
```

### 场景 3: 生成教学视频（v3.0 核心）
```bash
# 单概念视频
./knowledge-explainer-v3 "区块链" --video-generate -o block_chain.mp4

# 指定输出路径
./knowledge-explainer-v3 "黑洞原理" --video-generate \
    --output-dir ./videos/ \
    -o black_hole_60s.mp4
```

### 场景 4: 互动学习模式
```bash
./knowledge-explainer-v3 interact "机器学习基础"
# 然后进行多轮问答
```

### 场景 5: 专业领域解释
```bash
# 医学健康
./knowledge-explainer-v3 "疫苗接种原理" --domain medical

# 法律常识
./knowledge-explainer-v3 "合同违约怎么办" --domain legal

# 投资理财
./knowledge-explainer-v3 "基金和股票区别" --domain finance
```

---

## 🎨 **Remotion 视频生成详细**

### 自动生成流程
```
用户输入概念
    ↓
AI 生成文字解释（包含总结、要点）
    ↓
Python 提取关键信息
    ↓
自动生成 Remotion React 组件 (.tsx)
    ↓
调用 Remotion CLI 渲染视频
    ↓
输出 MP4/GIF/WebM
```

### 自定义视频参数
```bash
./knowledge-explainer-v3 "概念" --video-generate \
    --duration 90 \        # 时长（秒）
    --fps 60 \            # 帧率
    --resolution 1920x1080 \
    --theme dark          # 主题：light/dark/custom
```

### 视频模板示例
```tsx
// Remotion 组件结构
<KnowledgeVideo>
  <IntroScene />          // 开场动画（10 秒）
  <KeyPointsScene />      // 要点展示（40 秒）
  <SummaryScene />        // 总结记忆点（10 秒）
</KnowledgeVideo>
```

---

## 📊 **输出示例预览**

### 文字解释输出（Markdown）
```markdown
# 📚 区块链（大白话版 v3.0）

> 💡 **一句话总结**: 全班同学共同记账，没人能改别人的账

## 🎭 漫画场景
[A] === [B] === [C]
全网同步，无人能改！ ✅

## 💡 生活化类比
就像公共账本...

## 🔑 核心要点
1. **公开透明** - 所有人能看到
2. **不可篡改** - 数学保证
3. **共同维护** - 去中心化

...

## 🎬 生成内容
✅ 漫画图片：comic_区块链.png
🎵 语音文件：explanation.mp3  
📹 教学视频：blockchain_video.mp4 (60s)
```

### Remotion 视频输出
- **格式**: MP4 (H.264)
- **时长**: 默认 60 秒（可定制）
- **分辨率**: 1280x720 / 1920x1080
- **内容结构**: 开场→要点→总结
- **特效**: 淡入淡出、缩放、文字动画

---

## 🎯 **典型应用场景**

| 用户群体 | 推荐模式 | 输出形式 |
|--|-|--|--|
| **学生备考** | `--domain science` | 文字 + 语音（可复听） |
| **内容创作者** | `--all-features` | 全格式素材包 |
| **知识博主** | `--video-generate` | 60 秒短视频 |
| **培训师** | `--interactive` | 互动式学习材料 |
| **家长辅导孩子** | `--comic --audio` | 视觉 + 听觉双重呈现 |

---

## 🔧 **技术架构**

```
knowledge-explainer/
├── explainer.py           # v1.0 基础版
├── explainer_v2.py        # v2.0 全功能版（漫画/语音/互动）
├── video_generator.py     # v3.0 Remotion 视频生成 ⭐
├── SKILL.md              # 技能说明
├── README.md             # 基础文档
├── README_V3.md          # v3.0 完整版文档（当前）
├── config.example.json   # 配置示例
├── templates/            # 输出模板
└── output/               # 生成文件存放
```

---

## 📞 **常见问题**

### Q1: Remotion 视频生成失败？
```bash
# 检查 Node.js 版本
node --version  # 需要 v16+

# 重新初始化项目
rm -rf /tmp/knowledge-videos/remotion-project
./knowledge-explainer-v3 "概念" --video-generate
```

### Q2: 漫画生成不工作？
需要配置 AI 绘图服务：
```bash
export COMFYUI_API_KEY="your-key"
# 或运行本地 Stable Diffusion
./stable-diffusion-webui --api
```

### Q3: 语音生成无声？
```bash
# 安装依赖
pip install --break-system-packages edge-tts

# 测试
edge-tts --text "你好" --voice zh-CN-XiaoxiaoNeural --write-media test.mp3
```

---

## 🚀 **下一步计划**

- [ ] **多语言支持**: 英语/日语等版本
- [ ] **批量处理**: 一次生成多个概念的系列视频
- [ ] **自动字幕**: 视频自动添加中英文字幕
- [ ] **互动测验**: 根据内容自动生成选择题
- [ ] **知识图谱可视化**: D3.js 交互式概念图

---

## 🎉 **总结**

Knowledge Explainer v3.0 是一个**全方位的知识通俗化系统**，能够将任何复杂概念转化为：
- ✅ 通俗易懂的文字解释
- ✅ 生动的漫画插图
- ✅ 自然流畅的语音解说
- ✅ 60 秒教学短视频
- ✅ 互动式学习体验

**现在就开始体验知识可视化的力量！** 🎨🎬📚

```bash
./knowledge-explainer-v3 "输入任何你想理解的复杂概念" --all-features
```

---

*让知识像电影一样精彩，像聊天一样简单！* ✨
