# 🎬 Blender 3D 视频集成指南 - Knowledge Explainer v5.0

## 📊 版本升级概览

| 版本 | 2D 视频 | 3D 视频 | 智能选择 |
|-----|-:--:-:--:-:--:|
| v4.0 | ✅ Pillow | ❌ | ❌ |
| **v5.0** | ✅ Pillow | **✅ Blender** | **✅ 自动判断** |

---

## 🎯 核心能力对比

### 🎨 2D 视频引擎（保留）

**技术栈**: Python + Pillow + FFmpeg  
**生成时间**: ~15-30 秒  
**适用场景**:
- ✅ 定义类概念（什么是 X）
- ✅ 对比/分类（A vs B）
- ✅ 列表/步骤说明
- ✅ 简单流程图解

### 🌐 3D 视频引擎（新增）

**技术栈**: Blender Python API + FFmpeg  
**生成时间**: ~2-10 分钟（视质量而定）  
**适用场景**:
- ✅ **3D 结构**（分子、神经网络、建筑）
- ✅ **动态过程**（能量流动、信息传播）
- ✅ **抽象隐喻**（HSP 敏感度、情绪波动）
- ✅ **物理模拟**（碰撞、力场、流体力学）

---

## 🚀 智能选择逻辑

```python
def choose_video_engine(concept_type, complexity):
    """
    智能选择 2D 或 3D 视频引擎
    
    Args:
        concept_type: 概念类型（definition/structure/process/metaphor）
        complexity: 复杂度（1-5）
    
    Returns:
        '2d' or '3d'
    """
    # 需要空间关系或动态演示的概念 → 3D
    if concept_type in ['structure', 'process', 'metaphor']:
        return '3d'
    
    # 高复杂度概念（评分≥4）→ 3D
    if complexity >= 4:
        return '3d'
    
    # 默认使用 2D（快速）
    return '2d'

# 示例：
choose_video_engine('structure', 5) → '3d'  # 神经网络结构
choose_video_engine('definition', 2) → '2d'   # 什么是区块链
choose_video_engine('metaphor', 4) → '3d'    # HSP 敏感度隐喻
```

---

## 📚 支持的 3D 主题库

### 当前可用主题（5 个）

| 主题标识 | 中文名称 | 视觉元素 | 适用知识领域 |
|---------|-:--|-:--|--:--|
| `quantum_mechanics` | 量子力学 | 粒子云、概率波 | 物理/科学科普 |
| `neural_network` | 神经网络 | 层叠节点结构 | AI/机器学习 |
| `hsp` | 高敏感人群 | 情绪共振可视化 | 心理学/成长 |
| `blockchain` | 区块链 | 链式立方体连接 | 技术/金融 |
| `feynman_learning` | 费曼学习法 | 4 步骤循环文本 | 教育/学习方法 |

### 扩展新主题方法

```python
# 1. 在 blender-video-generator/scripts/generate_video.py 添加场景函数
def create_your_topic_scene(config):
    """创建你的主题场景"""
    # 实现你的 3D 可视化逻辑

# 2. 注册到主题处理器
topic_handlers = {
    'your-topic': create_your_topic_scene,
    'your_topic': create_your_topic_scene,
}

# 3. 在 references/topics.md 添加文档
```

---

## 🔧 快速使用指南

### 方式 1：命令行直接调用 Blender

```bash
cd /home/wing/.openclaw/workspace/skills/knowledge-explainer

# Step 1: 渲染 PNG 序列（~2-5 分钟）
blender --background \
  --python ../blender-video-generator/scripts/generate_video.py \
  -- topic=neural_network quality=medium duration=15

# Step 2: 合成 MP4（~10 秒）
python3 ../blender-video-generator/scripts/png_to_mp4.py \
  --input-dir ../blender-video-generator/output/neural_network_medium_* \
  --output output/ai_neural_network_explained.mp4
```

### 方式 2：集成到 Knowledge Explainer 工作流（推荐）

```bash
# 创建快捷脚本
cd /home/wing/.openclaw/workspace/skills/knowledge-explainer

cat > generate_3d_video.sh << 'EOF'
#!/bin/bash
TOPIC=$1
QUALITY=${2:-medium}
DURATION=${3:-15}

echo "生成 3D 视频：$TOPIC"
cd ../blender-video-generator

# 渲染
blender --background \
  --python scripts/generate_video.py \
  -- topic=$TOPIC quality=$QUALITY duration=$DURATION

# 合成 MP4
OUTPUT_DIR=$(ls -t output/*${TOPIC}_${QUALITY}_* | head -1)
python3 scripts/png_to_mp4.py \
  --input-dir $OUTPUT_DIR \
  --output ../../knowledge-explainer/output/${TOPIC}_3d.mp4

echo "✅ 视频已生成：output/${TOPIC}_3d.mp4"
EOF

chmod +x generate_3d_video.sh

# 使用示例
./generate_3d_video.sh neural_network high 20
```

---

## 🎯 知识类型 → 视频引擎映射表

| 知识类型 | 推荐引擎 | 原因 | 示例主题 |
|---------|-:--|--:--|-:--|
| **定义类**（什么是 X） | 2D | 静态信息，文字 + 简单图示 | 区块链定义 |
| **对比类**（A vs B） | 2D | 表格/流程图为主 | Python vs Java |
| **分类类**（X 的类型） | 2D | 列表展示即可 | 机器学习三大类型 |
| **结构类**（X 的组成） | **3D** ⭐ | 空间关系重要 | 神经网络架构 |
| **流程类**（X 如何工作） | **3D** ⭐ | 需要时间维度演示 | 能量流动过程 |
| **隐喻类**（抽象概念具象化） | **3D** ⭐ | 视觉隐喻强大 | HSP 敏感度可视化 |
| **物理类**（自然现象） | **3D** ⭐ | 物理模拟准确 | 量子力学概率云 |

---

## 💡 最佳实践

### 1. **先 2D 后 3D 策略**

```bash
# 首次解释概念 → 用 2D 快速验证
python3 explainer.py "神经网络" --depth 3 --video=2d

# 用户需要深入理解 → 升级到 3D
./generate_3d_video.sh neural_network medium 15
```

### 2. **质量分级使用**

| 场景 | 推荐质量 | 预估时间 |
|-----|-:--|--:--|-
| 快速原型验证 | low (640x360) | ~2-3 分钟 |
| 演示/分享 | medium (1280x720) | ~5-8 分钟 |
| 高质量交付 | high (1920x1080) | ~10-15 分钟 |

### 3. **主题复用策略**

```bash
# 同一主题可生成多个变体
./generate_3d_video.sh hsp low 10   # 快速版
./generate_3d_video.sh hsp high 20  # 高质量版
./generate_3d_video.sh hsp medium 15 --custom-colors  # 定制版
```

---

## 🔧 故障排查

### 问题 1: Blender 未安装
```bash
# 解决方案
sudo apt update && sudo apt install blender
blender --version  # 验证安装（需 3.x+）
```

### 问题 2: 渲染黑屏
- ✅ 检查光源：`add_lighting()` 函数已调用
- ✅ 检查相机：`scene.camera = camera` 已设置
- ✅ 检查场景物体是否可见

### 问题 3: 文件过小（<100KB）
```bash
# 原因：CRF 过高导致压缩过度
# 解决方案：降低 CRF 值（18-23 推荐）
python3 scripts/png_to_mp4.py --crf 18 ...
```

### 问题 4: 内存不足
```bash
# 减少粒子数量或几何体复杂度
# 编辑 generate_video.py 中的参数
particle_count = 50 if config['quality'] == 'low' else 200
```

---

## 📊 性能对比数据

| 指标 | 2D (Pillow) | 3D (Blender low) | 3D (Blender high) |
|-----|-:--|-:--:-:--:|
| **生成时间** | ~15-30 秒 | ~2-5 分钟 | ~10-15 分钟 |
| **文件质量** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **文件大小** | ~200-500KB | ~5-10MB | ~15-30MB |
| **适用场景** | 简单概念 | 中等复杂度 | 专业级交付 |

---

## 🎬 实际案例演示

### 案例：解释"高敏感人群 (HSP)"

```bash
# Step 1: AI 生成文字解释 + 2D 图示
python3 explainer.py "什么是高敏感人群" --depth 4

# Step 2: 生成 3D 可视化视频（展示情绪共振）
./generate_3d_video.sh hsp medium 15

# Step 3: 输出整合
# - Markdown 解释文档
# - ASCII/Mermaid图表  
# - 3D MP4 视频 (output/hsp_3d.mp4)
```

**预期效果**:
- 📝 **文字**: HSP 定义、特征、正面意义
- 🎨 **2D 图**: HSP vs 普通人对比表
- 🌐 **3D 视频**: 金色中心节点（自我）+ 紫色感知射线 + 彩色情绪波纹

---

## 📞 扩展支持

### 添加自定义主题

联系开发者或参考：
- `blender-video-generator/references/hsp_topic.md` - 完整主题设计示例
- `blender-video-generator/scripts/generate_video.py` - 场景函数模板

### 贡献新主题

1. Fork 仓库
2. 在 `scripts/` 添加新场景函数
3. 在 `references/` 添加主题文档
4. 提交 PR

---

*Knowledge Explainer v5.0：从 2D 到 3D，让知识可视化达到全新维度！* 🎨🌐✨
