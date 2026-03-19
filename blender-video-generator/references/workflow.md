# Blender Video Generator - 工作流指南

## 🚀 快速开始

### 1. 环境检查

```bash
# 验证 Blender 安装
blender --version

# 运行基础测试
blender --background --python scripts/test_render.py
```

### 2. 生成视频

```bash
# 基本用法（量子力学主题）
blender --background \
  --python scripts/generate_video.py \
  -- topic=量子力学 \
     quality=medium \
     duration=15

# 高质量渲染（需要 GPU）
blender --background \
  --python scripts/generate_video.py \
  -- topic=人工智能 \
     quality=high \
     render_engine=CYCLES \
     duration=20
```

### 3. 查看输出

```bash
# 生成的视频在 output/ 目录
ls -lh output/

# 播放视频（Linux）
vlc output/*.mp4
```

---

## 📋 完整工作流

### 阶段 1: 规划 (2-5 分钟)

**任务**: 确定视频参数

```python
# 主题选择（见 references/topics.md）
topic = "费曼学习法"  # 或 "量子力学"/"区块链"/"人工智能"

# 质量等级
quality = "medium"  # low(快)/medium(平衡)/high(慢但质量好)

# 时长（秒）
duration = 15  # 推荐 10-30 秒，过长会显著增加渲染时间
```

**决策点**:
- ⚡ **快速验证**: quality=low, duration=10 (渲染~1 分钟)
- 📊 **展示用途**: quality=medium, duration=15 (渲染~2-3 分钟)
- 🎬 **高质量输出**: quality=high, duration=20+ (渲染~5-10 分钟，需 GPU)

---

### 阶段 2: 执行生成 (1-10 分钟)

**运行命令**:

```bash
cd /home/wing/.openclaw/workspace/skills/blender-video-generator

blender --background \
  --python scripts/generate_video.py \
  -- topic=<主题> \
     quality=<质量等级> \
     duration=<时长>
```

**输出格式**:
```
output/<topic>_<quality>_YYYYMMDD_HHMMSS.mp4
```

---

### 阶段 3: 验证输出 (1 分钟)

```bash
# 检查文件大小（预估）
ls -lh output/

# 低质量：~2-5MB
# 中等质量：~5-10MB
# 高质量：~10-20MB

# 查看视频信息
ffprobe -v error -show_format -show_streams output/<video_name>.mp4
```

---

## 🎛️ 参数详解

### topic（主题）

| 值 | 中文 | 视觉效果 |
|-----|-----|---------|
| `量子力学` / `quantum_mechanics` | 量子力学 | 粒子云、概率波 |
| `费曼学习法` / `feynman` | 费曼学习法 | 4 步骤循环文本 |
| `区块链` / `blockchain` | 区块链 | 链式立方体连接 |
| `人工智能` / `ai` / `neural_network` | AI 神经网络 | 多层节点网络 |

**扩展**: 编辑 `scripts/generate_video.py` 添加新主题（见 references/topics.md）

---

### quality（质量等级）

| 等级 | 分辨率 | 渲染引擎 | 时间预估 |
|-----|------|---------|---------|
| `low` | 640x360 | Eevee | ~1-2 分钟 |
| `medium` (默认) | 1280x720 | Eevee | ~2-4 分钟 |
| `high` | 1920x1080 | Cycles | ~5-10 分钟 |

**注意**: 
- `high` 质量需要 GPU 加速（CUDA/OptiX）
- Cycles 渲染比 Eevee 慢 5-10 倍但效果更好

---

### duration（时长）

| 值（秒） | 帧数 (30fps) | 适用场景 |
|---------|------------|---------|
| 10-15 | 300-450 | 短视频、快速演示 |
| 15-20 | 450-600 | 教学视频、详细解释 |
| 20-30 | 600-900 | 完整课程片段 |

**建议**: 首次测试用 10-15 秒，验证动画逻辑后再延长

---

### render_engine（渲染引擎）

| 引擎 | 优点 | 缺点 | 推荐场景 |
|-----|-----|-----|---------|
| `EEVEE` (默认) | 快速实时 | 光影效果有限 | 测试、快速产出 |
| `CYCLES` | 电影级质量 | 渲染慢 | 最终输出 |

**启用 GPU 加速**:
1. Blender → 编辑 → 偏好设置 → 系统
2. 启用 CUDA/OptiX/OpenCL
3. 选择你的 GPU

---

## 🔧 自定义配置

### 修改颜色方案

编辑 `scripts/generate_video.py` 中的材质函数：

```python
# 找到颜色定义部分
colors = [(1, 0.8, 0.6), (0.6, 1, 0.8), ...]

# 修改为自定义配色
custom_colors = [
    (0.2, 0.5, 1.0),  # 深蓝
    (1.0, 0.8, 0.2),  # 橙色
    (0.3, 0.8, 0.5),  # 绿色
]
```

### 添加新主题

1. **创建场景函数**（见 references/topics.md）
2. **注册到 handler 字典**：
```python
topic_handlers = {
    '你的主题': create_your_topic_scene,
}
```
3. **测试运行**:
```bash
blender --background --python scripts/generate_video.py \
  -- topic=你的主题 quality=low duration=10
```

### 调整动画速度

```python
# 在场景函数中修改关键帧间隔
cube.keyframe_insert(data_path='scale', frame=start_frame)
cube.scale = (1, 1, 1)
cube.keyframe_insert(data_path='scale', frame=start_frame + 15)  # 改这里的数字

# 更慢：增加间隔（如 20）
# 更快：减少间隔（如 10）
```

---

## 🐛 故障排查

### 问题 1: 渲染黑屏

**原因**: 缺少光源或相机角度错误

**解决**:
```bash
# 检查日志中的警告信息
# 在脚本中添加 add_lighting() 函数调用
```

### 问题 2: 渲染极慢

**原因**: 采样数过高或几何体过复杂

**解决**:
```python
# 降低 Cycles 采样数
scene.cycles.samples = 128  # 原值可能是 512

# 或使用 Eevee 引擎
config['render_engine'] = 'EEVEE'
```

### 问题 3: 内存不足

**原因**: 粒子系统过大或场景复杂度过高

**解决**:
```python
# 减少粒子数量
particle_count = 100 if config['quality'] == 'low' else 200  # 原值可能更高

# 降低几何体细分级别
bpy.ops.mesh.primitive_icosphere_add(subdivisions=1)  # 原值可能是 3
```

### 问题 4: 输出文件损坏

**原因**: 渲染中断或编码器问题

**解决**:
```bash
# 重新运行（Blender 会覆盖同名文件）
blender --background --python scripts/generate_video.py \
  -- topic=量子力学 quality=low duration=10

# 检查 ffmpeg 安装
ffmpeg -version
```

---

## 📈 性能优化技巧

### 1. 分步渲染测试

```bash
# Step 1: 低分辨率验证动画逻辑
quality=low resolution=320x240 duration=10

# Step 2: 中分辨率验证视觉效果
quality=medium duration=15

# Step 3: 高分辨率最终输出
quality=high duration=20
```

### 2. 缓存中间结果

```python
# 修改脚本，渲染为序列帧而非直接视频
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(animation=True)

# 后期使用 ffmpeg 合成
ffmpeg -i frame_%04d.png -c:v libx264 output.mp4
```

### 3. GPU 渲染加速

```bash
# 在 Blender 中设置：
# Edit → Preferences → System → 启用 CUDA/OptiX
```

---

## 📚 参考资源

- **主题扩展**: `references/topics.md`
- **材质配置**: `references/materials.md`
- **Blender 官方文档**: https://docs.blender.org/api/current/
- **Eevee vs Cycles**: https://docs.blender.org/manual/en/latest/render/

---

*工作流持续优化中，欢迎贡献最佳实践。*
