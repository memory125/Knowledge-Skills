# 材质库 - Materials Reference

本文件包含所有预制材质的节点配置和使用方法。

## 🎨 核心材质配方

### 1. 霓虹发光材质 (Neon Glow)

**用途**: 科技感元素、高亮强调

```python
def create_neon_material(color=(1, 0, 0), strength=5.0):
    """创建霓虹自发光材质"""
    mat = bpy.data.materials.new(name=f"Neon_{color[0]:.2f}_{color[1]:.2f}_{color[2]:.2f}")
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # 自发光节点
    emit = nodes.new('ShaderNodeEmission')
    emit.inputs['Color'].default_value = (*color, 1.0)
    emit.inputs['Strength'].default_value = strength
    
    # 输出节点
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    links.new(emit.outputs['Emission'], input=output.inputs['Surface'])
    
    return mat
```

**颜色预设**:
- 🔴 红色警告：`(1, 0.2, 0.2)`
- 🟢 绿色成功：`(0.2, 1, 0.5)`
- 🔵 蓝色科技：`(0.3, 0.7, 1.0)`
- 🟡 黄色注意：`(1, 0.9, 0.2)`

---

### 2. 玻璃透明材质 (Glass Translucent)

**用途**: 高科技界面、透明效果

```python
def create_glass_material(roughness=0.1, transmission=1.0):
    """创建玻璃透明材质"""
    mat = bpy.data.materials.new(name="Glass_Transparent")
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # 原理 BSDF
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principelled.inputs['Base Color'].default_value = (0.95, 0.95, 1.0, 1.0)
    principelled.inputs['Metallic'].default_value = 0.0
    principelled.inputs['Roughness'].default_value = roughness
    principelled.inputs['Transmission'].default_value = transmission
    principelled.inputs['IOR'].default_value = 1.45
    
    # 输出节点
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    links.new(principelled.outputs['BSDF'], input=output.inputs['Surface'])
    
    return mat
```

---

### 3. 金属材质 (Metallic)

**用途**: 机械元素、工业风格

```python
def create_metal_material(color=(0.8, 0.8, 0.8), roughness=0.3):
    """创建金属材质"""
    mat = bpy.data.materials.new(name="Metal_Industrial")
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # 原理 BSDF
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principelled.inputs['Base Color'].default_value = (*color, 1.0)
    principelled.inputs['Metallic'].default_value = 1.0
    principelled.inputs['Roughness'].default_value = roughness
    
    # 输出节点
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    links.new(principelled.outputs['BSDF'], input=output.inputs['Surface'])
    
    return mat
```

**金属类型**:
- 🥈 银色：`(0.95, 0.95, 0.95), roughness=0.2`
- 🥇 金色：`(1.0, 0.85, 0.3), roughness=0.4`
- 🔩 钢铁：`(0.7, 0.7, 0.7), roughness=0.5`

---

### 4. 磨砂塑料材质 (Matte Plastic)

**用途**: 柔和背景、产品外壳

```python
def create_plastic_material(color=(0.5, 0.5, 0.5)):
    """创建磨砂塑料材质"""
    mat = bpy.data.materials.new(name="Plastic_Matte")
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # 原理 BSDF
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principelled.inputs['Base Color'].default_value = (*color, 1.0)
    principelled.inputs['Metallic'].default_value = 0.0
    principelled.inputs['Roughness'].default_value = 0.7
    principelled.inputs['Subsurface'].default_value = 0.1
    
    # 输出节点
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    links.new(principelled.outputs['BSDF'], input=output.inputs['Surface'])
    
    return mat
```

---

### 5. 程序化纹理材质 (Procedural Texture)

**用途**: 复杂表面、有机形状

```python
def create_procedural_material(scale=10, distortion=0.5):
    """创建噪波程序化纹理"""
    mat = bpy.data.materials.new(name="Procedural_Noise")
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    # 噪波纹理
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = scale
    noise.inputs['Distortion'].default_value = distortion
    
    # 颜色渐变
    color_ramp = nodes.new('ShaderNodeValToRGB')
    
    # 原理 BSDF
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    
    # 输出节点
    output = nodes.new('ShaderNodeOutputMaterial')
    
    # 连接节点
    links.new(noise.outputs['Fac'], input=color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], input=principled.inputs['Base Color'])
    links.new(principelled.outputs['BSDF'], input=output.inputs['Surface'])
    
    return mat
```

---

## 🎯 材质应用最佳实践

### 性能优化

| 渲染引擎 | 推荐材质 | 避免使用 |
|---------|---------|---------|
| **Eevee** | 简单 BSDF、自发光 | 复杂程序化纹理 |
| **Cycles** | 所有材质类型 | 过高的细分级别 |

### 颜色和谐原则

1. **主色调**: 选择 1-2 个核心颜色
2. **强调色**: 用于重点元素（对比度高）
3. **中性色**: 背景和次要元素

### 材质库快速调用

```python
# 在脚本中导入材质函数
from materials_library import (
    create_neon_material,
    create_glass_material,
    create_metal_material,
    create_plastic_material
)

# 快速创建
neon_blue = create_neon_material(color=(0.3, 0.7, 1.0))
metal_gold = create_metal_material(color=(1.0, 0.85, 0.3))
```

---

*所有材质都经过性能优化，适配 Eevee 和 Cycles 两种渲染引擎。*
