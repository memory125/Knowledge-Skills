#!/usr/bin/env python3
"""
Blender Video Generator - Core Script
生成 3D 教学视频的 Blender Python API 脚本

用法: blender --python generate_video.py -- topic=量子力学 quality=high duration=15
"""

import bpy
import sys
import math
import os
from datetime import datetime

# ===== 配置参数 =====
DEFAULT_CONFIG = {
    'topic': 'quantum_mechanics',
    'quality': 'medium',  # low, medium, high
    'resolution': (1920, 1080),
    'fps': 30,
    'duration': 15,  # 秒
    'render_engine': 'BLENDER_EEVEE',  # BLENDER_EEVEE(快) or CYCLES(慢但质量高)
    'output_path': './output'
}

def parse_args():
    """解析命令行参数"""
    config = DEFAULT_CONFIG.copy()
    
    for arg in sys.argv:
        if '=' in arg and not arg.startswith('--python'):
            key, value = arg.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            if key == 'topic':
                config['topic'] = value
            elif key == 'quality':
                config['quality'] = value.lower()
            elif key == 'duration':
                config['duration'] = int(float(value))
            elif key == 'render_engine':
                config['render_engine'] = value.upper()
    
    # 根据质量调整配置
    if config['quality'] == 'low':
        config['resolution'] = (640, 360)
        config['duration'] = min(config['duration'], 10)
    elif config['quality'] == 'high':
        config['resolution'] = (1920, 1080)
        config['render_engine'] = 'CYCLES'
    
    return config

def setup_scene(config):
    """初始化 3D 场景"""
    # 清空场景
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    scene = bpy.context.scene
    
    # 渲染设置
    # Blender 4.x 引擎名称映射
    engine_map = {'EEVEE': 'BLENDER_EEVEE', 'CYCLES': 'CYCLES'}
    scene.render.engine = engine_map.get(config['render_engine'], config['render_engine'])
    scene.render.resolution_x = config['resolution'][0]
    scene.render.resolution_y = config['resolution'][1]
    scene.render.fps = config['fps']
    scene.frame_start = 1
    scene.frame_end = config['duration'] * config['fps']
    
    # Cycles 渲染优化
    if config['render_engine'] == 'CYCLES':
        scene.cycles.samples = 128 if config['quality'] != 'high' else 512
        scene.cycles.use_denoising = True
    
    return scene

def add_lighting():
    """添加专业照明"""
    # 主光源
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(60), math.radians(45), 0)
    
    # 补光
    bpy.ops.object.light_add(type='AREA', location=(-5, -5, 5))
    fill = bpy.context.active_object
    fill.data.energy = 500.0
    fill.data.size = 5
    
    # 背光
    bpy.ops.object.light_add(type='POINT', location=(0, -10, 3))
    back = bpy.context.active_object
    back.data.energy = 200.0

def create_quantum_mechanics_scene(config):
    """创建量子力学主题场景"""
    print("Creating quantum mechanics visualization...")
    
    # 创建中心原子球体
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1, location=(0, 0, 0))
    core = bpy.context.active_object
    core.name = "Quantum_Core"
    
    # 核心材质（蓝色发光）
    mat_core = bpy.data.materials.new(name="Quantum_Core_Glow")
    mat_core.use_nodes = True
    nodes = mat_core.node_tree.nodes
    links = mat_core.node_tree.links
    nodes.clear()
    
    emit = nodes.new('ShaderNodeEmission')
    emit.inputs['Color'].default_value = (0.2, 0.6, 1.0, 1.0)
    emit.inputs['Strength'].default_value = 3.0
    
    output = nodes.new('ShaderNodeOutputMaterial')
    links.new(emit.outputs[0], output.inputs[0])
    
    core.data.materials.append(mat_core)
    
    # 创建轨道电子（简化版，不使用粒子系统）
    electron_count = 3 if config['quality'] == 'low' else 6
    
    for i in range(electron_count):
        angle = (i / electron_count) * 2 * math.pi
        radius = 2 + (i % 2) * 0.5
        
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15,
            location=(radius * math.cos(angle), radius * math.sin(angle), 0))
        electron = bpy.context.active_object
        electron.name = f"Electron_{i}"
        
        # 电子材质（绿色发光）
        mat_e = bpy.data.materials.new(name=f"Electron_Glow_{i}")
        mat_e.use_nodes = True
        nodes_e = mat_e.node_tree.nodes
        links_e = mat_e.node_tree.links
        nodes_e.clear()
        
        emit_e = nodes_e.new('ShaderNodeEmission')
        emit_e.inputs['Color'].default_value = (0.2, 1.0, 0.5, 1.0)
        emit_e.inputs['Strength'].default_value = 2.0
        
        output_e = nodes_e.new('ShaderNodeOutputMaterial')
        links_e.new(emit_e.outputs[0], output_e.inputs[0])
        
        electron.data.materials.append(mat_e)
        
        # 动画：电子旋转轨道运动
        electron.keyframe_insert(data_path='rotation_euler', frame=1)
        electron.rotation_euler.z = angle + math.radians(30)
        electron.keyframe_insert(data_path='rotation_euler', frame=config['duration'] * config['fps'])
    
    # 核心旋转动画
    core.keyframe_insert(data_path='rotation_euler', frame=1)
    core.rotation_euler.z = math.radians(45)
    core.rotation_euler.x = math.radians(20)
    core.keyframe_insert(data_path='rotation_euler', frame=config['duration'] * config['fps'])
    
    return core

def create_feynman_learning_scene(config):
    """创建费曼学习法场景"""
    print("Creating Feynman learning cycle visualization...")
    
    steps = ["选目标", "教别人", "查漏洞", "简化"]
    radius = 3
    
    for i, step in enumerate(steps):
        # 创建文本（3D）
        bpy.ops.object.text_add(location=(radius * math.cos(i * math.pi/2), 
                                          radius * math.sin(i * math.pi/2), 0))
        text_obj = bpy.context.active_object
        text_obj.data.body = step
        text_obj.scale = (1, 1, 1) * (2 if config['quality'] != 'low' else 1.5)
        
        # 转换为网格
        context = bpy.context
        obj = context.active_object
        depsgraph = bpy.context.evaluated_depsgraph_get()
        mesh_from_object = obj.to_mesh(depsgraph)
        
        new_obj = bpy.data.objects.new(f"Step_{i}_Mesh", mesh_from_object)
        context.collection.objects.link(new_obj)
        bpy.data.meshes.remove(mesh_from_object)
        context.collection.objects.unlink(obj)
        
        # 添加材质
        mat = bpy.data.materials.new(name=f"Step_{i}")
        mat.use_nodes = True
        colors = [(1, 0.8, 0.6), (0.6, 1, 0.8), (0.8, 0.6, 1), (1, 0.9, 0.6)]
        mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (*colors[i % len(colors)], 1)
        
        new_obj.data.materials.append(mat)
        
        # 动画：淡入
        new_obj.keyframe_insert(data_path='hide_viewport', frame=i * 15)
        new_obj.hide_viewport = False

def create_blockchain_scene(config):
    """创建区块链主题场景"""
    print("Creating blockchain visualization...")
    
    num_blocks = 3 if config['quality'] == 'low' else 5
    
    for i in range(num_blocks):
        # 创建区块立方体
        bpy.ops.mesh.primitive_cube_add(size=2, location=(i * 2.5, 0, 0))
        cube = bpy.context.active_object
        cube.name = f"Block_{i}"
        
        # 材质
        mat = bpy.data.materials.new(name=f"Block_Mat_{i}")
        mat.use_nodes = True
        hue = i / num_blocks
        mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (
            0.5 + 0.5 * math.cos(hue * 2 * math.pi),
            0.5 + 0.5 * math.sin(hue * 2 * math.pi),
            0.5, 1
        )
        cube.data.materials.append(mat)
        
        # 动画：连接动画
        cube.scale = (0.1, 0.1, 0.1)
        cube.keyframe_insert(data_path='scale', frame=1)
        cube.scale = (1, 1, 1)
        cube.keyframe_insert(data_path='scale', frame=(i + 1) * 20)
        
        # 创建连接箭头
        if i < num_blocks - 1:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1.5, 
                                               location=(i * 2.5 + 1.25, 0, 0))
            arrow = bpy.context.active_object
            arrow.name = f"Arrow_{i}"
            arrow.keyframe_insert(data_path='hide_viewport', frame=(i + 1) * 20)
            arrow.hide_viewport = False

def create_ai_neural_network_scene(config):
    """创建人工智能神经网络场景"""
    print("Creating neural network visualization...")
    
    layers = [3, 4, 4, 2] if config['quality'] != 'low' else [2, 3, 2]
    layer_spacing = 3
    
    for layer_idx, num_nodes in enumerate(layers):
        x_pos = (layer_idx - len(layers) / 2) * layer_spacing
        
        for node_idx in range(num_nodes):
            y_pos = (node_idx - num_nodes / 2) * 1.5
            
            # 创建节点球体
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(x_pos, y_pos, 0))
            sphere = bpy.context.active_object
            sphere.name = f"Layer_{layer_idx}_Node_{node_idx}"
            
            # 材质
            mat = bpy.data.materials.new(name=f"Node_Mat_{layer_idx}")
            mat.use_nodes = True
            mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (
                0.2 + 0.6 * (layer_idx / len(layers)),
                0.4 + 0.4 * (layer_idx / len(layers)),
                0.8, 1
            )
            sphere.data.materials.append(mat)
            
            # 动画：逐层出现
            start_frame = layer_idx * 25 + 1
            sphere.scale = (0, 0, 0)
            sphere.keyframe_insert(data_path='scale', frame=start_frame)
            sphere.scale = (1, 1, 1)
            sphere.keyframe_insert(data_path='scale', frame=start_frame + 15)

def create_hsp_scene(config):
    """创建高敏感人群 (HSP) 场景 - 神经元敏感网络"""
    print("Creating HSP (Highly Sensitive Person) visualization...")
    
    # 1. 创建中心节点（大脑/自我）- 温暖金色球体
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0, 0, 0))
    center = bpy.context.active_object
    center.name = "HSP_Center"
    
    mat_center = bpy.data.materials.new(name="HSP_Center_Glow")
    mat_center.use_nodes = True
    nodes_c = mat_center.node_tree.nodes
    links_c = mat_center.node_tree.links
    nodes_c.clear()
    
    emit_c = nodes_c.new('ShaderNodeEmission')
    emit_c.inputs['Color'].default_value = (1.0, 0.75, 0.3, 1.0)  # 暖金色
    emit_c.inputs['Strength'].default_value = 4.0
    
    output_c = nodes_c.new('ShaderNodeOutputMaterial')
    links_c.new(emit_c.outputs[0], output_c.inputs[0])
    
    center.data.materials.append(mat_center)
    
    # 中心脉冲动画（模拟呼吸/感知）
    center.scale = (1, 1, 1)
    center.keyframe_insert(data_path='scale', frame=1)
    center.scale = (1.1, 1.1, 1.1)
    center.keyframe_insert(data_path='scale', frame=config['duration'] * config['fps'] // 4)
    center.scale = (1, 1, 1)
    center.keyframe_insert(data_path='scale', frame=config['duration'] * config['fps'] // 2)
    
    # 2. 创建感知射线（6 条向外辐射）
    num_rays = 6
    for i in range(num_rays):
        angle = (i / num_rays) * 2 * math.pi
        
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=3, location=(0, 0, 0))
        ray = bpy.context.active_object
        ray.name = f"Perception_Ray_{i}"
        
        # 旋转射线到正确角度
        ray.rotation_euler = (math.radians(45), 0, angle)
        ray.location = (0.5 * math.cos(angle), 0.5 * math.sin(angle), 0)
        
        # 淡紫色材质（宁静、直觉）
        mat_ray = bpy.data.materials.new(name=f"Ray_Mat_{i}")
        mat_ray.use_nodes = True
        nodes_r = mat_ray.node_tree.nodes
        links_r = mat_ray.node_tree.links
        nodes_r.clear()
        
        emit_r = nodes_r.new('ShaderNodeEmission')
        # 渐变紫色
        hue = i / num_rays
        emit_r.inputs['Color'].default_value = (0.5 + 0.3*math.cos(hue*2*math.pi), 
                                                  0.4, 
                                                  0.8 + 0.2*math.sin(hue*2*math.pi), 1.0)
        emit_r.inputs['Strength'].default_value = 1.5
        
        output_r = nodes_r.new('ShaderNodeOutputMaterial')
        links_r.new(emit_r.outputs[0], output_r.inputs[0])
        
        ray.data.materials.append(mat_ray)
        
        # 射线生长动画
        ray.scale = (0, 0, 0)
        ray.keyframe_insert(data_path='scale', frame=1 + i * 5)
        ray.scale = (1, 1, 1)
        ray.keyframe_insert(data_path='scale', frame=15 + i * 5)
    
    # 3. 创建环境刺激波（同心圆环）
    num_waves = 3
    for i in range(num_waves):
        radius = 2 + i * 1.5
        
        bpy.ops.mesh.primitive_torus_add(major_radius=radius, minor_radius=0.05, location=(0, 0, 0))
        wave = bpy.context.active_object
        wave.name = f"Stimulus_Wave_{i}"
        
        # 多彩柔和材质
        mat_wave = bpy.data.materials.new(name=f"Wave_Mat_{i}")
        mat_wave.use_nodes = True
        nodes_w = mat_wave.node_tree.nodes
        links_w = mat_wave.node_tree.links
        nodes_w.clear()
        
        emit_w = nodes_w.new('ShaderNodeEmission')
        colors = [(0.8, 0.3, 0.6), (0.3, 0.7, 0.8), (0.4, 0.9, 0.5)]  # 粉/蓝/绿
        emit_w.inputs['Color'].default_value = (*colors[i % len(colors)], 0.6)
        emit_w.inputs['Strength'].default_value = 1.0
        
        output_w = nodes_w.new('ShaderNodeOutputMaterial')
        links_w.new(emit_w.outputs[0], output_w.inputs[0])
        
        wave.data.materials.append(mat_wave)
        
        # 波浪扩散动画
        wave.scale = (0, 0, 0)
        wave.keyframe_insert(data_path='scale', frame=15 + i * 10)
        wave.scale = (1.2, 1.2, 1.2)
        wave.keyframe_insert(data_path='scale', frame=30 + i * 10)
        wave.scale = (1, 1, 1)
        # wave 保持可见作为环境背景元素
    
    # 4. 创建情绪回响圈（小型粒子点）
    particle_count = 20 if config['quality'] == 'low' else 50
    for i in range(particle_count):
        angle = math.radians(i * 360 / particle_count)
        radius = 1.5 + (i % 5) * 0.3
        
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, 
            location=(radius * math.cos(angle), radius * math.sin(angle), 0))
        particle = bpy.context.active_object
        particle.name = f"Emotion_Particle_{i}"
        
        # 渐隐的粉色/绿色材质
        mat_p = bpy.data.materials.new(name=f"Particle_Mat_{i}")
        mat_p.use_nodes = True
        nodes_p = mat_p.node_tree.nodes
        links_p = mat_p.node_tree.links
        nodes_p.clear()
        
        emit_p = nodes_p.new('ShaderNodeEmission')
        if i % 2 == 0:
            emit_p.inputs['Color'].default_value = (0.9, 0.6, 0.7, 1.0)  # 粉色
        else:
            emit_p.inputs['Color'].default_value = (0.4, 0.9, 0.5, 1.0)  # 绿色
        emit_p.inputs['Strength'].default_value = 0.8
        
        output_p = nodes_p.new('ShaderNodeOutputMaterial')
        links_p.new(emit_p.outputs[0], output_p.inputs[0])
        
        particle.data.materials.append(mat_p)
        
        # 粒子浮现动画
        particle.keyframe_insert(data_path='hide_viewport', frame=25 + i * 2)
        particle.hide_viewport = False
    
    print("✓ HSP 场景创建完成：中心节点 + 感知射线 + 环境刺激波 + 情绪回响圈")
    return center

def setup_camera():
    """设置相机位置"""
    scene = bpy.context.scene
    
    bpy.ops.object.camera_add(location=(0, -8, 5))
    camera = bpy.context.active_object
    scene.camera = camera  # 设置为活动渲染相机
    
    # 调整角度
    camera.rotation_euler = (math.radians(65), 0, 0)
    
    # 动画：缓慢移动（根据场景时长动态调整）
    scene.frame_end = scene.frame_end
    end_frame = min(scene.frame_end, 300)
    
    camera.keyframe_insert(data_path='location', frame=1)
    camera.location = (2, -8, 6)
    camera.keyframe_insert(data_path='location', frame=end_frame // 3)
    camera.location = (-2, -8, 6)
    camera.keyframe_insert(data_path='location', frame=(end_frame // 3) * 2)
    camera.location = (0, -8, 5)
    camera.keyframe_insert(data_path='location', frame=end_frame)
    
    return camera

def set_output_path(config):
    """设置输出路径"""
    os.makedirs(config['output_path'], exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(
        config['output_path'],
        f"{config['topic']}_{config['quality']}_{timestamp}"
    )
    
    # Blender 4.x 输出设置 - 使用 PNG 序列然后后期合成
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    output_dir = os.path.join(config['output_path'], f"{config['topic']}_{config['quality']}_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    bpy.context.scene.render.filepath = os.path.join(output_dir, "frame_####")
    
    return output_file
    
    return output_file

def main():
    """主函数"""
    print("=" * 50)
    print("Blender Video Generator")
    print("=" * 50)
    
    # 解析配置
    config = parse_args()
    print(f"配置：{config}")
    
    # 设置场景
    scene = setup_scene(config)
    
    # 添加照明
    add_lighting()
    
    # 根据主题创建场景
    topic_handlers = {
        '量子力学': create_quantum_mechanics_scene,
        'quantum_mechanics': create_quantum_mechanics_scene,
        '费曼学习法': create_feynman_learning_scene,
        'feynman': create_feynman_learning_scene,
        '区块链': create_blockchain_scene,
        'blockchain': create_blockchain_scene,
        '人工智能': create_ai_neural_network_scene,
        'ai': create_ai_neural_network_scene,
        'neural_network': create_ai_neural_network_scene,
        '高敏感人群': create_hsp_scene,
        'hsp': create_hsp_scene,
        'highly_sensitive_person': create_hsp_scene,
    }
    
    handler = topic_handlers.get(config['topic'])
    if handler:
        handler(config)
    else:
        print(f"警告：未找到主题 '{config['topic']}' 的处理函数，使用默认场景")
        create_quantum_mechanics_scene(config)  # 默认
    
    # 设置相机
    setup_camera()
    
    # 设置输出
    output_file = set_output_path(config)
    print(f"输出文件：{output_file}")
    
    # 渲染动画
    print("开始渲染...")
    bpy.ops.render.render(animation=True)
    print(f"渲染完成！输出：{output_file}")
    
    return 0

if __name__ == '__main__':
    main()
