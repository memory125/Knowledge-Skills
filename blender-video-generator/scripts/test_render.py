#!/usr/bin/env python3
"""
快速测试渲染脚本
用于验证 Blender 环境和基本功能是否正常
"""

import bpy
import sys

def quick_test():
    """快速测试场景"""
    print("启动 Blender 环境测试...")
    
    # 清空场景
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # 添加测试立方体
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    cube = bpy.context.active_object
    
    # 添加材质
    mat = bpy.data.materials.new(name="Test_Material")
    mat.use_nodes = True
    mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (1, 0.5, 0.2, 1)
    cube.data.materials.append(mat)
    
    # 添加光源
    bpy.ops.object.light_add(type='SUN', location=(3, 3, 5))
    
    # 设置相机
    bpy.ops.object.camera_add(location=(0, -5, 2))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.0, 0, 0)
    
    # 渲染设置
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 640
    scene.render.resolution_y = 360
    scene.frame_start = 1
    scene.frame_end = 30
    
    # 动画测试
    cube.keyframe_insert(data_path='rotation_euler', frame=1)
    cube.rotation_euler.z = 3.14
    cube.keyframe_insert(data_path='rotation_euler', frame=30)
    
    print("✓ 场景创建完成")
    print(f"✓ 渲染引擎：{scene.render.engine}")
    print(f"✓ 分辨率：{scene.render.resolution_x}x{scene.render.resolution_y}")
    print(f"✓ 帧数：{scene.frame_end}")
    
    return True

if __name__ == '__main__':
    if quick_test():
        print("\n✅ Blender 环境测试通过！")
        sys.exit(0)
    else:
        print("\n❌ 测试失败")
        sys.exit(1)
