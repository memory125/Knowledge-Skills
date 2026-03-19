---
name: "blender-video-generator"
description: "专业级 3D 教学视频生成技能。使用 Blender Python API 创建 3D 动画视频，支持量子力学、费曼学习法、区块链、AI 神经网络等主题。包含完整工作流：场景搭建、材质配置、关键帧动画、渲染输出。适用场景：3D 概念演示、物理过程模拟、电影级可视化需求。不适用于简单 2D 图表或快速原型验证。需要 Blender 3.x+ 环境，支持 Eevee（快）和 Cycles（高质量）两种渲染引擎。"
---

# 🎬 Blender Video Generator - 专业级 3D 视频生成

> **从概念到视觉：用代码驱动电影级教学视频** ✨🎥

## 🚀 快速开始

### 基本用法

```bash
cd /home/wing/.openclaw/workspace/skills/blender-video-generator

# 快速测试环境
blender --background --python scripts/test_render.py

# 生成 3D 教学视频（10-20 分钟）
blender --background \
  --python scripts/generate_video.py \
  -- topic=量子力学 quality=medium duration=15
```

### 支持主题（v1.0）

| 主题 | 视觉效果 | 渲染时间 |
|-----|-------|---------|
| **量子力学** | 粒子云、概率波 | ~2-3 分钟 |
| **费曼学习法** | 4 步骤循环动画 | ~2 分钟 |
| **区块链** | 链式立方体连接 | ~2.5 分钟 |
| **人工智能** | 神经网络层叠 | ~3-4 分钟 |

---

## 📂 技能结构

```
blender-video-generator/
├── SKILL.md              # 本文件（导航与触发指引）
├── scripts/
│   ├── generate_video.py # 核心生成脚本（支持命令行参数）
│   └── test_render.py    # 环境测试脚本
└── references/
    ├── workflow.md       # 完整工作流指南（含故障排查）
    ├── topics.md         # 主题库与扩展指南
    └── materials.md      # 材质库配方
```

---

## 🎯 使用指引

### 场景选择

**适用于：**
- ✅ 3D 概念演示（分子结构、建筑可视化）
- ✅ 物理过程模拟（流体力学、碰撞动画）
- ✅ 电影级视觉质量要求
- ✅ 需要真实光影效果的内容

**不适用：**
- ❌ 简单 2D 图表展示
- ❌ 快速原型验证（建议使用视频帧技能替代）
- ❌ 低配置设备环境

---

## 📖 参考资料

### 完整文档
- **工作流指南**: `references/workflow.md` - 详细步骤、参数说明、性能优化
- **主题库**: `references/topics.md` - 所有支持主题的详细说明与扩展方法
- **材质配方**: `references/materials.md` - PBR 材质系统配置与最佳实践

### 快速导航

**需要做什么？**
1. **生成视频** → 查看 `references/workflow.md` "快速开始"
2. **自定义主题** → 查看 `references/topics.md` "添加新主题"
3. **调整视觉效果** → 查看 `references/materials.md` 材质配方
4. **解决渲染问题** → 查看 `references/workflow.md` "故障排查"

---

## ⚡ 关键配置

### 质量等级对比

| 等级 | 分辨率 | 引擎 | 时间 | 场景 |
|-----|------|-----|-|---|
| `low` | 640x360 | Eevee | ~1-2 分钟 | 快速测试 |
| `medium` | 1280x720 | Eevee | ~2-4 分钟 | 演示输出 |
| `high` | 1920x1080 | Cycles | ~5-10 分钟 | 高质量交付 |

### 渲染引擎选择

**Eevee**: 实时渲染，快速但光影效果有限
- 适合：测试验证、快速产出

**Cycles**: 光线追踪，电影级质量但速度慢
- 适合：最终输出、高质量演示

---

## 🔧 核心参数

```bash
# topic（主题）: 量子力学 | 费曼学习法 | 区块链 | 人工智能
# quality（质量）: low | medium | high
# duration（时长）: 10-30 秒（秒为单位）
# render_engine（引擎）: EEEVEE | CYCLES

blender --background \
  --python scripts/generate_video.py \
  -- topic=费曼学习法 \
     quality=high \
     duration=20 \
     render_engine=CYCLES
```

---

## 💡 最佳实践

1. **低质量先行** - 先用 `quality=low` + `duration=10` 验证动画逻辑
2. **GPU 加速** - 在 Blender 偏好设置中启用 CUDA/OptiX（提升 5-10 倍速度）
3. **分步渲染** - 先序列帧后合成，便于局部重渲染
4. **缓存场景** - 保存 `.blend` 文件避免重复搭建

---

## 📚 外部资源

- [Blender Python API](https://docs.blender.org/api/current/)
- [Eevee vs Cycles 对比](https://docs.blender.org/manual/en/latest/render/)
- [3D 动画基础教程](https://www.blender.org/support/tutorials/)

---

*代码驱动视觉，让知识从平面走向立体。* 🎬🚀
