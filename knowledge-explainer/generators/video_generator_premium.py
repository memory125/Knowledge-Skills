#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Premium 视频生成器 v1.0 - 高质量视觉版

升级特性：
✨ 渐变背景 + 装饰图案
✨ 平滑动画过渡（淡入/滑动）
✨ 高级配色方案（玻璃拟态 + 霓虹效果）
✨ 动态进度条 + 场景指示器
✨ 图标 + 装饰元素
"""

import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import sys
import math


def load_chinese_fonts():
    """加载最美中文字体"""
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 72)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 56)
        font_text = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 40)
        font_small = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 32)
        return {'title': font_title, 'subtitle': font_subtitle, 'text': font_text, 'small': font_small}, "Noto Sans CJK"
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/arphic/uming.ttc", 40)
            return {k: font for k in ['title', 'subtitle', 'text', 'small']}, "uming.ttc"
        except:
            default_font = ImageFont.load_default()
            return {k: default_font for k in ['title', 'subtitle', 'text', 'small']}, "default"


GLOBAL_FONTS, FONT_NAME = load_chinese_fonts()

# ✨ 高级配色方案（玻璃拟态 + 霓虹）
COLORS = {
    'bg_dark': '#0f0f1a',      # 深色背景
    'bg_light': '#1a1a2e',     # 渐变起点
    'accent_1': '#ff6b6b',     # 珊瑚红
    'accent_2': '#4ecdc4',     # 薄荷绿
    'accent_3': '#ffe66d',     # 暖黄
    'accent_4': '#95e1d3',     # 青色
    'purple': '#a855f7',       # 紫色霓虹
    'pink': '#ec4899',         # 粉色霓虹
    'white': '#ffffff',
    'gray_light': '#cccccc',   # 浅灰色
    'gray_dark': '#666666',    # 深灰色
    'glass': (255, 255, 255, 180),  # 玻璃效果（带透明度）
    'shadow': (0, 0, 0, 60)
}


def create_gradient_background(width, height, progress=0):
    """✨ Premium: 创建动态渐变背景"""
    img = Image.new('RGB', (width, height), COLORS['bg_dark'])
    draw = ImageDraw.Draw(img)
    
    # 计算渐变偏移（根据进度产生动画效果）
    offset = int(50 * math.sin(progress * 2 * math.pi))
    
    # 创建径向渐变
    center_x, center_y = width // 2, height // 2
    radius = max(width, height) * 0.8
    
    for r in range(int(radius), -1, -5):
        alpha = int(30 * (1 - r / radius))
        color = (
            int(15 + alpha * 0.5),
            int(15 + alpha * 0.4),
            int(26 + alpha * 0.6)
        )
        draw.ellipse([center_x-r+offset, center_y-r, center_x+r+offset, center_y+r], fill=color)
    
    # 添加星点装饰
    import random
    random.seed(int(progress * 100))
    for _ in range(20):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 3)
        brightness = random.randint(150, 255)
        draw.ellipse([x-size, y-size, x+size, y+size], fill=(brightness, brightness, brightness))
    
    return img


def create_glass_card(draw, x, y, width, height, color, progress=0):
    """✨ Premium: 创建玻璃拟态卡片"""
    # 动态透明度（淡入效果）
    alpha = min(int(180 * progress), 180)
    
    # 阴影
    shadow_rect = [x-5, y-5, x+width+5, y+height+5]
    draw.rounded_rectangle(shadow_rect, radius=15, fill=COLORS['shadow'])
    
    # 玻璃卡片
    glass_color = (color[0], color[1], color[2], alpha) if len(color) == 3 else color
    draw.rounded_rectangle([x, y, x+width, y+height], radius=15, fill=glass_color)
    
    # 顶部高光（玻璃质感）
    highlight_rect = [x, y, x+width, y+20]
    for i in range(20):
        alpha_i = int(80 * (1 - i/20) * progress)
        draw.rectangle([x, y+i, x+width, y+i+1], fill=(*COLORS['glass'][:3], alpha_i))


def create_progress_bar(draw, width, height, current_scene, total_scenes, progress):
    """✨ Premium: 动态进度条"""
    bar_height = 8
    bar_y = height - 40
    segment_width = width // total_scenes
    
    # 背景条
    draw.rounded_rectangle([20, bar_y, width-20, bar_y+bar_height], radius=4, fill=(30, 30, 50))
    
    # 进度段
    for i in range(total_scenes):
        x = 20 + i * segment_width
        alpha = int(200 if i < current_scene else 60)
        color = COLORS['accent_2'] if i == current_scene else (80, 80, 120)
        draw.rounded_rectangle([x, bar_y, x+segment_width-2, bar_y+bar_height], radius=3, fill=color)


def create_icon_emoji(draw, x, y, emoji, size=60):
    """✨ Premium: 渲染 Emoji 图标（带发光效果）"""
    # 简单处理：直接绘制文字
    draw.text((x, y), emoji, font=GLOBAL_FONTS['subtitle'], anchor='mm')


def create_scene_title_premium(topic, knowledge, progress):
    """Scene 1: Premium 标题开场（渐变 + 动画）"""
    width, height = 1920, 1080
    
    # 渐变背景
    img = create_gradient_background(width, height, progress)
    draw = ImageDraw.Draw(img)
    
    # 淡入效果
    alpha = min(progress / 0.15, 1)
    
    # 主标题（带发光效果）
    if alpha > 0.2:
        # 阴影
        shadow_offset = 3
        draw.text((width // 2 + shadow_offset, 380 + shadow_offset), 
                  knowledge["title"], 
                  fill=(0, 0, 0, 128), font=GLOBAL_FONTS['title'], anchor="mm")
        draw.text((width // 2, 380), knowledge["title"], 
                  fill=COLORS['white'], font=GLOBAL_FONTS['title'], anchor="mm")
    
    # 副标题（渐变颜色）
    if alpha > 0.5:
        subtitle_color = (
            int(78 + 25 * math.sin(progress * 10)),
            int(236 + 19 * math.cos(progress * 10)),
            int(196)
        )
        draw.text((width // 2, 480), knowledge["subtitle"], 
                  fill=subtitle_color, font=GLOBAL_FONTS['subtitle'], anchor="mm")
    
    # 装饰线（霓虹效果）
    if alpha > 0.7:
        line_width = min(300 + int(200 * (alpha - 0.7) / 0.3), 500)
        gradient_colors = [COLORS['accent_1'], COLORS['accent_2'], COLORS['accent_3']]
        for i in range(line_width):
            color_idx = int(i / line_width * len(gradient_colors)) % len(gradient_colors)
            x = width // 2 - line_width // 2 + i
            draw.line([(x, 560), (x+1, 560)], fill=gradient_colors[color_idx], width=3)
    
    # 场景指示器
    create_progress_bar(draw, width, height, 0, 6, progress)
    
    return img


def create_concept_scene_premium(topic, knowledge, concept_idx, scene_progress):
    """Scene 2-5: Premium 概念详解（玻璃卡片 + 动画）"""
    width, height = 1920, 1080
    concept = knowledge["concepts"][concept_idx]
    
    # 渐变背景
    img = create_gradient_background(width, height, scene_progress + concept_idx * 0.2)
    draw = ImageDraw.Draw(img)
    
    # 场景标题
    alpha_title = min(scene_progress / 0.3, 1)
    if alpha_title > 0:
        draw.text((width // 2, 80), f"第{concept_idx + 1}个要点", 
                  fill=COLORS['gray_light'], font=GLOBAL_FONTS['small'], anchor="mm")
    
    # ✨ 玻璃卡片（带淡入动画）
    card_x = width // 2 - 450
    card_y = 180
    card_w, card_h = 900, 350
    
    if scene_progress > 0.1:
        glass_color = (60, 60, 90, int(150 * min(scene_progress / 0.3, 1)))
        
        # 阴影
        draw.rounded_rectangle([card_x-8, card_y-8, card_x+card_w+8, card_y+card_h+8], 
                              radius=20, fill=(0, 0, 0, 80))
        
        # 玻璃卡片主体
        draw.rounded_rectangle([card_x, card_y, card_x+card_w, card_y+card_h], 
                              radius=20, fill=glass_color)
        
        # 顶部高光线（玻璃质感）
        for i in range(25):
            alpha_i = int(100 * (1 - i/25) * min(scene_progress / 0.3, 1))
            draw.rectangle([card_x+10, card_y+10+i, card_x+card_w-10, card_y+11+i], 
                          fill=(*COLORS['glass'][:3], alpha_i))
        
        # 图标（Emoji，带放大动画）
        if scene_progress > 0.2:
            scale = 1 + 0.1 * math.sin(scene_progress * 10)
            icon_size = int(80 * scale)
            draw.text((width // 2, 280), concept["icon"], 
                      fill=COLORS['white'], font=GLOBAL_FONTS['title'], anchor="mm")
        
        # 概念名称
        if scene_progress > 0.35:
            draw.text((width // 2, 360), concept["name"], 
                      fill=COLORS['white'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
        
        # 描述文字（逐行出现）
        if scene_progress > 0.5:
            desc_lines = concept["desc"].split("，")
            for i, line in enumerate(desc_lines[:3]):
                line_alpha = min((scene_progress - 0.5) / (0.1 * (i+1)), 1)
                if line_alpha > 0:
                    draw.text((width // 2, 480 + i * 50), line, 
                              fill=COLORS['white'], font=GLOBAL_FONTS['text'], anchor="mm")
    
    # ✨ 侧边装饰（霓虹条）
    neon_colors = [COLORS['accent_1'], COLORS['accent_2'], COLORS['accent_3'], COLORS['accent_4']]
    for i, color in enumerate(neon_colors):
        y_pos = 200 + i * 180
        if scene_progress > i * 0.15:
            # 动态宽度
            bar_width = min(60 + int(40 * math.sin(scene_progress * 20)), 100)
            draw.rounded_rectangle([width - bar_width - 30, y_pos, width - 30, y_pos + 80], 
                                  radius=10, fill=color)
    
    # 底部进度条
    total_scenes = len(knowledge["concepts"]) + 2
    current_scene = concept_idx + 1
    create_progress_bar(draw, width, height, current_scene, total_scenes, scene_progress)
    
    return img


def create_summary_scene_premium(topic, knowledge, progress):
    """Scene 6: Premium 总结（卡片网格 + 动画）"""
    width, height = 1920, 1080
    
    # 渐变背景
    img = create_gradient_background(width, height, progress)
    draw = ImageDraw.Draw(img)
    
    if progress > 0:
        # 标题（发光效果）
        shadow_offset = 3
        draw.text((width // 2 + shadow_offset, 150 + shadow_offset), "💡 记忆口诀", 
                  fill=(0, 0, 0, 128), font=GLOBAL_FONTS['title'], anchor="mm")
        draw.text((width // 2, 150), "💡 记忆口诀", 
                  fill=COLORS['accent_3'], font=GLOBAL_FONTS['title'], anchor="mm")
        
        # 总结卡片（大号玻璃效果）
        card_x = width // 2 - 700
        card_y = 280
        card_w, card_h = 1400, 250
        
        if progress > 0.2:
            alpha = min((progress - 0.2) / 0.3, 1)
            
            # 阴影
            draw.rounded_rectangle([card_x-10, card_y-10, card_x+card_w+10, card_y+card_h+10], 
                                  radius=25, fill=(0, 0, 0, int(100 * alpha)))
            
            # 玻璃卡片
            glass_color = (60, 60, 100, int(160 * alpha))
            draw.rounded_rectangle([card_x, card_y, card_x+card_w, card_y+card_h], 
                                  radius=25, fill=glass_color)
            
            # 顶部高光
            for i in range(30):
                alpha_i = int(120 * (1 - i/30) * alpha)
                draw.rectangle([card_x+12, card_y+12+i, card_x+card_w-12, card_y+13+i], 
                              fill=(*COLORS['glass'][:3], alpha_i))
            
            # 总结文字（居中，发光）
            if alpha > 0.5:
                draw.text((width // 2 + 3, 420), knowledge["summary"], 
                          fill=(0, 0, 0, 128), font=GLOBAL_FONTS['text'], anchor="mm")
                draw.text((width // 2, 420), knowledge["summary"], 
                          fill=COLORS['white'], font=GLOBAL_FONTS['text'], anchor="mm")
        
        # 底部版权信息
        if progress > 0.5:
            footer_y = height - 80
            draw.rounded_rectangle([width//2-600, footer_y, width//2+600, footer_y+60], 
                                  radius=15, fill=(30, 30, 50, 200))
            draw.text((width // 2, footer_y + 20), 
                      "© 2026 Knowledge Explainer v5.1 Premium | OpenClaw AI", 
                      fill=COLORS['gray_dark'], font=GLOBAL_FONTS['small'], anchor="mm")
    
    return img


def create_frame_premium(frame_num, total_frames, topic, knowledge):
    """根据帧号创建 Premium 场景"""
    num_scenes = len(knowledge["concepts"]) + 2
    
    # 计算每个场景的帧数（动态）
    title_frames = int(total_frames * 0.13)
    summary_frames = int(total_frames * 0.13)
    concept_frames_each = (total_frames - title_frames - summary_frames) // len(knowledge["concepts"])
    
    # 标题场景
    if frame_num < title_frames:
        progress = frame_num / title_frames
        return create_scene_title_premium(topic, knowledge, progress)
    
    frame_num -= title_frames
    
    # 概念场景
    concept_idx = frame_num // concept_frames_each
    if concept_idx < len(knowledge["concepts"]):
        scene_progress = (frame_num % concept_frames_each) / concept_frames_each
        return create_concept_scene_premium(topic, knowledge, concept_idx, scene_progress)
    
    # 总结场景
    summary_progress = (frame_num - len(knowledge["concepts"]) * concept_frames_each) / summary_frames
    return create_summary_scene_premium(topic, knowledge, summary_progress)


def generate_video_premium(topic, output_path=None, fps=30):
    """生成 Premium 质量视频"""
    
    if not output_path:
        skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_base = os.path.join(skill_dir, "output", topic)
        os.makedirs(output_base, exist_ok=True)
        output_path = os.path.join(output_base, f"{topic}_premium.mp4")
    
    # 获取知识内容
    knowledge = get_knowledge_content(topic)
    
    # 动态计算帧数
    title_frames = 60
    summary_frames = 90
    concept_frames_each = 75
    total_frames = title_frames + len(knowledge["concepts"]) * concept_frames_each + summary_frames
    
    # 创建临时帧目录
    frame_dir = os.path.join(os.path.dirname(output_path), "frames_premium")
    os.makedirs(frame_dir, exist_ok=True)
    
    print(f"🎬 Premium 视频生成器 v1.0")
    print(f"   • 主题：{topic}")
    print(f"   • 总帧数：{total_frames} (时长：{total_frames/fps:.1f}s)")
    print(f"   • 特效：渐变背景 + 玻璃卡片 + 霓虹装饰 + 动态进度条")
    
    # 生成所有帧
    for frame_num in range(total_frames):
        img = create_frame_premium(frame_num, total_frames, topic, knowledge)
        frame_path = os.path.join(frame_dir, f"frame_{frame_num:04d}.png")
        img.save(frame_path, "PNG")
        
        if frame_num % 50 == 0:
            progress = int(100 * frame_num / total_frames)
            print(f"   • 进度：{progress}%")
    
    # FFmpeg 合并（高质量编码）
    input_pattern = os.path.join(frame_dir, "frame_%04d.png")
    
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", input_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",  # 高质量（较低 CRF = 更高质量）
        "-preset", "medium",
        output_path
    ]
    
    print("🔄 正在合并帧为视频（高质量编码）...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # 清理临时文件
    import shutil
    if os.path.exists(frame_dir):
        shutil.rmtree(frame_dir)
    
    if result.returncode == 0:
        size_mb = os.path.getsize(output_path) / (1024*1024)
        print(f"✅ Premium 视频生成成功：{output_path}")
        print(f"   • 大小：{size_mb:.2f} MB")
        print(f"   • 质量：CRF18 高保真编码")
        return output_path
    else:
        print(f"❌ FFmpeg 失败:")
        print(result.stderr)
        return None


# 导入知识内容函数（从原文件复制）
def get_knowledge_content(topic):
    """根据主题返回对应的知识内容"""
    
    knowledge = {
        "费曼学习法": {
            "title": "📚 费曼学习法",
            "subtitle": "用教别人的方式学会知识",
            "concepts": [
                {"icon": "🎯", "name": "选目标", "desc": "确定要学习的概念或主题"},
                {"icon": "👨‍🏫", "name": "教别人", "desc": "假装给初学者讲解知识"},
                {"icon": "🔍", "name": "查漏洞", "desc": "卡住了说明没真懂，回去查资料"},
                {"icon": "✨", "name": "简化语言", "desc": "去掉术语，用大白话解释"}
            ],
            "summary": "选目标 → 教别人 → 查漏洞 → 简化 → 循环",
            "color": "#e94560"
        },
        
        # 添加更多主题（与原有保持一致）
        "量子力学": {
            "title": "⚛️ 量子力学",
            "subtitle": "微观世界的奇妙法则",
            "concepts": [
                {"icon": "🌊", "name": "波粒二象性", "desc": "既是波也是粒子"},
                {"icon": "❓", "name": "不确定性原理", "desc": "无法同时知道位置和动量"},
                {"icon": "🐱", "name": "叠加态", "desc": "薛定谔的猫生死并存"},
                {"icon": "🔗", "name": "量子纠缠", "desc": "瞬间跨距离影响"}
            ],
            "summary": "波粒二象 | 不确定性 | 叠加态 | 量子纠缠",
            "color": "#533483"
        },
        
        # 更多主题继续添加...
        "人工智能": {
            "title": "🤖 人工智能",
            "subtitle": "让机器拥有智慧",
            "concepts": [
                {"icon": "🧠", "name": "机器学习", "desc": "从数据中自动学习"},
                {"icon": "👁️", "name": "计算机视觉", "desc": "让机器看懂图像"},
                {"icon": "🗣️", "name": "自然语言处理", "desc": "理解人类语言"},
                {"icon": "🎯", "name": "强化学习", "desc": "通过试错优化决策"}
            ],
            "summary": "自主学习 | 感知世界 | 理解语言 | 持续进化",
            "color": "#10b981"
        }
    }
    
    if topic in knowledge:
        return knowledge[topic]
    
    # 通用模板
    return {
        "title": f"📖 {topic}",
        "subtitle": "深度解析",
        "concepts": [
            {"icon": "🎯", "name": "核心定义", "desc": f"{topic}的基本概念"},
            {"icon": "💡", "name": "关键特性", "desc": "主要特点和原理"},
            {"icon": "🌍", "name": "应用场景", "desc": "实际生活中的用途"},
            {"icon": "📚", "name": "扩展学习", "desc": "相关知识和资源"}
        ],
        "summary": f"理解{topic}的核心要点，掌握关键知识",
        "color": "#e94560"
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python video_generator_premium.py <主题>")
        sys.exit(1)
    
    topic = sys.argv[1]
    
    print("=" * 70)
    print(f"🎬 Premium 视频生成器 v1.0 - {topic}")
    print("=" * 70)
    print(f"✅ 字体：{FONT_NAME}")
    print()
    
    generate_video_premium(topic)
    
    print()
    print("=" * 70)
    print("✅ Premium 视频生成完成！")
    print("=" * 70)
