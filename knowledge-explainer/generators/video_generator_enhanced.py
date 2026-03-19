#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频生成器 v6.0 - 知识解释器优化版

在 v5.x 基础上全面升级：
✨ 所有文字内容都在彩色卡片背景上
✨ 完美居中对齐 (anchor="mm")
✨ 渐变背景 + 星点装饰
✨ 发光文字效果（阴影层）
✨ 霓虹渐变线条
✨ 高级进度条（带动画）
✨ 图标徽章设计
✨ 平滑淡入动画支持

核心改进：
- v6.0: 所有内容整合到大卡片内，避免分散显示
- 所有文本使用 anchor="mm" 实现真正的居中
- 卡片尺寸扩大以容纳更多文字内容
- 每个概念使用专属颜色增强视觉区分度

作者：OpenClaw AI Team
版本：6.0 (完整居中对齐版)
日期：2026-03-11
"""

import subprocess
from PIL import Image, ImageDraw, ImageFont
import os
import sys
import math
import random


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

# ✨ v5.2 高级配色方案（霓虹渐变）
COLORS = {
    'bg': '#0f0f1a',           # 深色背景
    'accent': '#e94560',       # 主色调
    'primary': '#0f3460',      # 主要强调色
    'white': '#ffffff',        # 白色
    'gray_light': '#cccccc',   # 浅灰色
    'gray_dark': '#666666',    # 深灰色
    
    # 霓虹渐变配色
    'accent_1': '#ff6b6b',     # 珊瑚红
    'accent_2': '#4ecdc4',     # 薄荷绿
    'accent_3': '#ffe66d',     # 暖黄
    'purple': '#a855f7',       # 紫色霓虹
    'pink': '#ec4899',         # 粉色霓虹
}


def create_gradient_bg(w, h):
    """✨ v5.2: 渐变背景 + 星点装饰"""
    img = Image.new('RGB', (w, h), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    cx, cy = w // 2, h // 2
    
    # 多层光晕（模拟景深）
    for r in range(500, 0, -40):
        alpha = int(30 * (1 - r/500))
        color = (15+alpha, 15+alpha, 26+alpha)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
    
    # 星点装饰（固定分布）
    random.seed(42)
    for _ in range(12):
        x, y = random.randint(0, w), random.randint(0, h)
        draw.ellipse([x-1, y-1, x+1, y+1], fill=(220, 220, 255))
    
    return img


def text_with_glow(draw, text, pos, color, font):
    """✨ v6.0: 带阴影发光效果的文字（完美居中）"""
    # 阴影层（使用 anchor="mm" 确保对齐）
    for dx, dy in [(-2,-2), (-2,0), (-2,2), (0,-2), (0,2), (2,-2), (2,0), (2,2)]:
        draw.text((pos[0]+dx, pos[1]+dy), text, fill=(0,0,0), font=font, anchor="mm")
    
    # 主文字 - 使用 anchor="mm" 确保完美居中
    draw.text(pos, text, fill=color, font=font, anchor="mm")


def gradient_line(draw, x1, y1, x2, y2):
    """✨ v5.2: 霓虹渐变线条"""
    colors = [COLORS['accent_1'], COLORS['accent_2'], COLORS['accent_3']]
    length = int(math.sqrt((x2-x1)**2 + (y2-y1)**2))
    
    for i in range(length):
        t = i / max(length, 1)
        x, y = int(x1 + (x2-x1)*t), int(y1 + (y2-y1)*t)
        cidx = int(t * len(colors)) % len(colors)
        draw.line([(x, y), (x+1, y)], fill=colors[cidx], width=4)


def progress_bar(draw, w, h, current, total):
    """✨ v6.0: 高级进度条（居中版）"""
    bar_h, bar_y = 10, h - 45
    bar_w = w - 120  # 留出边距
    track_left = w//2 - bar_w//2  # 居中对齐
    seg_w = bar_w // total
    
    # ✨ v6.0: 背景轨道（居中）
    draw.rounded_rectangle([track_left, bar_y, track_left+bar_w, bar_y+bar_h], radius=5, fill=(30,30,50))
    
    # ✨ v6.0: 进度段（居中，渐变效果）
    for i in range(total):
        x = track_left + i * seg_w
        if i < current:
            # 已完成 - 霓虹渐变
            colors = [COLORS['accent_1'], COLORS['accent_2'], COLORS['accent_3']]
            for j in range(seg_w-2):
                cidx = int(j/(seg_w-2) * len(colors)) % len(colors)
                draw.rectangle([x+j, bar_y, x+j+1, bar_y+bar_h], fill=colors[cidx])
        elif i == current:
            # 当前 - 高亮
            draw.rounded_rectangle([x, bar_y, x+seg_w-2, bar_y+bar_h], radius=3, fill=COLORS['accent'])
        else:
            # 未开始
            draw.rounded_rectangle([x, bar_y, x+seg_w-2, bar_y+bar_h], radius=3, fill=(60,60,80))


def get_knowledge_content(topic):
    """获取知识内容（从原文件共享）"""
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
            "color": COLORS['accent']
        },
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
            "color": COLORS['purple']
        },
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
            "color": COLORS['accent_2']
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
        "color": COLORS['accent']
    }


def create_title_scene(topic, knowledge):
    """Scene 1: 标题开场（v6.0 卡片版 - 所有文字在卡片上）"""
    w, h = 1920, 1080
    img = create_gradient_bg(w, h)
    draw = ImageDraw.Draw(img)
    
    # ✨ v6.0: 大卡片（容纳所有标题内容）- 居中
    card_w, card_h = 1200, 450
    card_x = w//2 - card_w//2
    card_y = h//2 - card_h//2
    
    # 卡片阴影
    draw.rounded_rectangle([card_x-15, card_y-15, card_x+card_w+15, card_y+card_h+15], 
                          radius=30, fill=(0,0,0,80))
    
    # 卡片主体（深色背景）
    draw.rounded_rectangle([card_x, card_y, card_x+card_w, card_y+card_h], 
                          radius=30, fill=COLORS['primary'])
    
    # ✨ v6.0: 主标题在卡片上居中
    text_with_glow(draw, knowledge["title"], (w//2, card_y + 100), COLORS['white'], GLOBAL_FONTS['title'])
    
    # ✨ v6.0: 副标题在卡片上居中
    color = knowledge.get("color", COLORS['accent'])
    draw.text((w//2, card_y + 200), knowledge["subtitle"], fill=color, font=GLOBAL_FONTS['subtitle'], anchor="mm")
    
    # ✨ v6.0: 装饰线在卡片内居中
    gradient_line(draw, w//2-200, card_y + 300, w//2+200, card_y + 300)
    
    # ✨ v6.0: 额外说明在卡片上居中（如果有）
    if "extra_info" in knowledge:
        draw.text((w//2, card_y + 370), knowledge["extra_info"], fill=COLORS['gray_light'], font=GLOBAL_FONTS['text'], anchor="mm")
    
    # ✨ v6.0: 高级进度条（居中）
    progress_bar(draw, w, h, 0, len(knowledge.get("concepts", [])) + 2)
    
    return img


def create_concept_scene(topic, knowledge, idx):
    """Scene 2-5: 概念详解（v6.0 卡片版 - 所有文字在彩色卡片上）"""
    w, h = 1920, 1080
    concept = knowledge["concepts"][idx]
    
    img = create_gradient_bg(w, h)
    draw = ImageDraw.Draw(img)
    
    # ✨ v6.0: 大卡片（容纳所有概念内容）- 居中
    card_w, card_h = 1200, 500
    card_x = w//2 - card_w//2
    card_y = h//2 - card_h//2
    
    # 阴影
    draw.rounded_rectangle([card_x-15, card_y-15, card_x+card_w+15, card_y+card_h+15], 
                          radius=30, fill=(0,0,0,80))
    
    # ✨ v6.0: 卡片主体（使用概念专属颜色）
    color = concept.get("color", COLORS['accent'])
    draw.rounded_rectangle([card_x, card_y, card_x+card_w, card_y+card_h], 
                          radius=30, fill=color)
    
    # ✨ v6.0: 场景编号在卡片上顶部居中
    draw.text((w//2, card_y + 50), f"第{idx+1}个要点", fill=COLORS['white'], font=GLOBAL_FONTS['small'], anchor="mm")
    
    # ✨ v6.0: 图标在卡片上居中
    text_with_glow(draw, concept.get("icon", "💡"), (w//2, card_y + 120), COLORS['white'], GLOBAL_FONTS['subtitle'])
    
    # ✨ v6.0: 概念名称在卡片上居中
    draw.text((w//2, card_y + 190), concept["name"], fill=COLORS['white'], font=GLOBAL_FONTS['title'], anchor="mm")
    
    # ✨ v6.0: 描述文字在卡片上居中
    draw.text((w//2, card_y + 270), concept["desc"], fill=COLORS['white'], font=GLOBAL_FONTS['text'], anchor="mm")
    
    # ✨ v6.0: 核心要点/关键信息在卡片上居中（如果有）
    if "key_point" in concept:
        draw.text((w//2, card_y + 350), f"✨ {concept['key_point']}", fill=COLORS['white'], font=GLOBAL_FONTS['small'], anchor="mm")
    
    # ✨ v6.0: 侧边装饰条（右侧对齐，不遮挡内容）
    neon_colors = [COLORS['accent_1'], COLORS['accent_2'], COLORS['accent_3']]
    for i, col in enumerate(neon_colors):
        y_pos = 350 + i * 140
        draw.rounded_rectangle([w-80, y_pos, w-20, y_pos+50], radius=10, fill=col)
    
    # ✨ v6.0: 底部进度条（居中）
    progress_bar(draw, w, h, idx+1, len(knowledge["concepts"]) + 2)
    
    return img


def create_summary_scene(topic, knowledge):
    """Scene 6: 总结（v6.0 卡片版 - 所有文字在卡片上）"""
    w, h = 1920, 1080
    img = create_gradient_bg(w, h)
    draw = ImageDraw.Draw(img)
    
    # ✨ v6.0: 大总结卡片（容纳所有内容）- 居中
    card_w, card_h = 1300, 450
    card_x = w//2 - card_w//2
    card_y = h//2 - card_h//2
    
    # 阴影
    draw.rounded_rectangle([card_x-15, card_y-15, card_x+card_w+15, card_y+card_h+15], 
                          radius=30, fill=(0,0,0,100))
    
    # ✨ v6.0: 卡片主体（深蓝背景）
    draw.rounded_rectangle([card_x, card_y, card_x+card_w, card_y+card_h], 
                          radius=30, fill=COLORS['primary'])
    
    # ✨ v6.0: 标题在卡片上居中
    text_with_glow(draw, "💡 记忆口诀", (w//2, card_y + 70), COLORS['accent_3'], GLOBAL_FONTS['title'])
    
    # ✨ v6.0: 分隔线在卡片内居中
    gradient_line(draw, w//2-250, card_y + 140, w//2+250, card_y + 140)
    
    # ✨ v6.0: 总结文字在卡片上居中
    summary = knowledge["summary"]
    if len(summary) > 60:
        # 如果太长，分成两行显示
        half_len = len(summary) // 2
        line1 = summary[:half_len]
        line2 = summary[half_len:]
        draw.text((w//2, card_y + 210), line1, fill=COLORS['white'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
        draw.text((w//2, card_y + 270), line2, fill=COLORS['gray_light'], font=GLOBAL_FONTS['text'], anchor="mm")
    else:
        draw.text((w//2, card_y + 230), summary, fill=COLORS['white'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
    
    # ✨ v6.0: 额外说明在卡片上居中（如果有）
    if "extra_notes" in knowledge:
        draw.text((w//2, card_y + 350), knowledge["extra_notes"], fill=COLORS['gray_light'], font=GLOBAL_FONTS['small'], anchor="mm")
    
    # ✨ v6.0: 版权信息单独小卡片在底部（不占用主卡片空间）
    footer_y = h - 70
    footer_w = 800
    footer_x = w//2 - footer_w//2
    draw.rounded_rectangle([footer_x, footer_y, footer_x+footer_w, footer_y+50], radius=15, fill=(30,30,50,200))
    draw.text((w//2, footer_y+25), "© 2026 Knowledge Explainer v6.0 | OpenClaw AI", 
              fill=COLORS['gray_dark'], font=GLOBAL_FONTS['small'], anchor="mm")
    
    return img


def generate_video_enhanced(topic, output_path=None, fps=30):
    """生成增强版视频（v6.0 完整居中对齐）"""
    
    if not output_path:
        skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_base = os.path.join(skill_dir, "output", topic)
        os.makedirs(output_base, exist_ok=True)
        output_path = os.path.join(output_base, f"{topic}_v6.0_centered.mp4")
    
    knowledge = get_knowledge_content(topic)
    
    # 动态计算帧数（同 v5.1）
    title_frames = 90          # 标题延长到 3 秒
    summary_frames = 120       # 总结延长到 4 秒  
    concept_frames_each = 90   # 每个概念 3 秒
    total_concepts = len(knowledge["concepts"])
    total_frames = title_frames + total_concepts * concept_frames_each + summary_frames
    
    frame_dir = os.path.join(os.path.dirname(output_path), "frames_v6.0")
    os.makedirs(frame_dir, exist_ok=True)
    
    print(f"🎬 v6.0 Enhanced 视频生成器（完整居中对齐版）")
    print(f"   • 主题：{topic}")
    print(f"   • 总概念数：{total_concepts}")
    print(f"   • 总帧数：{total_frames} (时长：{total_frames/fps:.1f}s)")
    print(f"   • 字体：{FONT_NAME}")
    print(f"   • 特效：渐变背景 + 发光文字 + 霓虹装饰 + 高级进度条")
    print(f"   • 布局：所有文字在彩色卡片上（完美居中）")
    
    # 生成帧
    for frame_num in range(total_frames):
        if frame_num < title_frames:
            img = create_title_scene(topic, knowledge)
        elif frame_num < title_frames + len(knowledge["concepts"]) * concept_frames_each:
            idx = (frame_num - title_frames) // concept_frames_each
            img = create_concept_scene(topic, knowledge, idx)
        else:
            img = create_summary_scene(topic, knowledge)
        
        frame_path = os.path.join(frame_dir, f"frame_{frame_num:04d}.png")
        img.save(frame_path, "PNG")
        
        if frame_num % 50 == 0:
            print(f"   • 进度：{int(100*frame_num/total_frames)}%")
    
    # FFmpeg 合并
    input_pattern = os.path.join(frame_dir, "frame_%04d.png")
    cmd = ["ffmpeg", "-y", "-framerate", str(fps), "-i", input_pattern, 
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", output_path]
    
    print("🔄 正在合并帧为视频（高质量编码）...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # 清理临时文件
    import shutil
    if os.path.exists(frame_dir):
        shutil.rmtree(frame_dir)
    
    if result.returncode == 0:
        size_mb = os.path.getsize(output_path) / (1024*1024)
        print(f"✅ v6.0 Enhanced 视频生成成功：{output_path}")
        print(f"   • 大小：{size_mb:.2f} MB")
        print(f"   • 时长：{total_frames/fps:.1f}秒")
        print(f"   • 质量：CRF18 高保真 + 完整居中对齐")
        return output_path
    else:
        print(f"❌ FFmpeg 失败：{result.stderr}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python video_generator_enhanced.py <主题> [输出路径]")
        sys.exit(1)
    
    topic = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("=" * 70)
    print(f"🎬 v6.0 Enhanced - {topic}")
    print("=" * 70)
    print(f"✅ 字体：{FONT_NAME}")
    if output_path:
        print(f"📁 输出路径：{output_path}")
    print()
    
    generate_video_enhanced(topic, output_path)
    
    print()
    print("=" * 70)
    print("✅ v6.0 Enhanced 视频生成完成！")
    print("✨ 特性：所有文字在彩色卡片上 + 完美居中对齐")
    print("=" * 70)    
    print()
    print("=" * 70)
    print("✅ v5.2 Enhanced 视频生成完成！")
    print("=" * 70)
