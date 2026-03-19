#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用知识视频生成器 v1.0 - 动态主题支持
根据传入的主题自动生成对应的视频内容
"""

import subprocess
from PIL import Image, ImageDraw, ImageFont
import os
import sys


def load_chinese_fonts():
    """加载最美的中文字体 - Google Noto Sans/Serif CJK (思源系列)"""
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 72)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 56)
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

COLORS = {
    'bg': '#1a1a2e',
    'accent': '#e94560',
    'primary': '#0f3460',
    'secondary': '#16213e',
    'white': '#ffffff',
    'gray_light': '#cccccc',
    'gray_dark': '#666666'
}


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
        
        "区块链": {
            "title": "🔗 区块链技术",
            "subtitle": "去中心化的信任机制",
            "concepts": [
                {"icon": "📖", "name": "公共账本", "desc": "所有人都有副本"},
                {"icon": "🛡️", "name": "不可篡改", "desc": "数学规则防止作弊"},
                {"icon": "⛓️", "name": "区块链接", "desc": "哈希值形成链条"},
                {"icon": "🌐", "name": "去中心化", "desc": "无需信任中介"}
            ],
            "summary": "公开透明 | 不可篡改 | 共同维护 | 数学证明",
            "color": "#f7931a"
        },
        
        "机器学习": {
            "title": "🤖 机器学习",
            "subtitle": "让数据教会计算机",
            "concepts": [
                {"icon": "📚", "name": "监督学习", "desc": "用标注数据训练"},
                {"icon": "🔮", "name": "无监督学习", "desc": "自己发现模式"},
                {"icon": "🧠", "name": "深度学习", "desc": "多层神经网络"},
                {"icon": "🔄", "name": "持续优化", "desc": "不断调整参数"}
            ],
            "summary": "数据训练 | 自动学习 | 持续优化 | 智能决策",
            "color": "#10b981"
        },
        
        "相对论": {
            "title": "⏰ 相对论",
            "subtitle": "时空的革命性理解",
            "concepts": [
                {"icon": "📐", "name": "狭义相对论", "desc": "时空是相对的"},
                {"icon": "💨", "name": "光速极限", "desc": "无法超越光速"},
                {"icon": "⏱️", "name": "时间膨胀", "desc": "高速时钟变慢"},
                {"icon": "🌀", "name": "时空弯曲", "desc": "引力是几何效应"}
            ],
            "summary": "时空相对 | 光速极限 | 质能转换 | 引力弯曲",
            "color": "#3b82f6"
        },
        
        # 新增主题（v5.1 扩展）
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
        },
        
        "大模型 LLM": {
            "title": "📚 大语言模型 LLM",
            "subtitle": "AI 的通用大脑",
            "concepts": [
                {"icon": "📖", "name": "海量训练", "desc": "学习互联网所有知识"},
                {"icon": "🔄", "name": "预测下一个词", "desc": "概率生成文本"},
                {"icon": "🎭", "name": "Few-shot 学习", "desc": "少量示例就学会"},
                {"icon": "💬", "name": "对话能力", "desc": "像真人一样聊天"}
            ],
            "summary": "海量知识 | 概率预测 | 快速适应 | 自然对话",
            "color": "#8b5cf6"
        },
        
        "RAG 检索增强": {
            "title": "📖 RAG 检索增强",
            "subtitle": "AI 的精准知识外挂",
            "concepts": [
                {"icon": "🔍", "name": "先检索", "desc": "从知识库找答案"},
                {"icon": "🧠", "name": "再思考", "desc": "大模型组织语言"},
                {"icon": "✅", "name": "有依据", "desc": "回答可追溯来源"},
                {"icon": "🚫", "name": "少幻觉", "desc": "不胡说八道"}
            ],
            "summary": "检索优先 | 知识增强 | 有据可查 | 减少幻觉",
            "color": "#f59e0b"
        },
        
        "Agent 智能体": {
            "title": "🤖 Agent 智能体",
            "subtitle": "自主决策的 AI 助手",
            "concepts": [
                {"icon": "🎯", "name": "接受目标", "desc": "理解任务要求"},
                {"icon": "🧭", "name": "自动规划", "desc": "分解步骤执行"},
                {"icon": "🛠️", "name": "调用工具", "desc": "使用外部能力"},
                {"icon": "🔄", "name": "持续反馈", "desc": "根据结果调整"}
            ],
            "summary": "目标导向 | 自主规划 | 工具调用 | 循环优化",
            "color": "#ef4444"
        },
        
        "MCP 协议": {
            "title": "🔗 MCP 模型上下文协议",
            "subtitle": "AI 连接万物的 USB",
            "concepts": [
                {"icon": "🌉", "name": "统一标准", "desc": "通用连接协议"},
                {"icon": "📦", "name": "资源访问", "desc": "读取文件和数据"},
                {"icon": "⚡", "name": "工具调用", "desc": "执行外部操作"},
                {"icon": "🔌", "name": "即插即用", "desc": "轻松扩展能力"}
            ],
            "summary": "标准接口 | 资源共享 | 工具集成 | 快速扩展",
            "color": "#06b6d4"
        },
        
        "Prompt 提示词": {
            "title": "💡 Prompt 提示词工程",
            "subtitle": "与 AI 高效沟通的艺术",
            "concepts": [
                {"icon": "📝", "name": "清晰指令", "desc": "明确告诉 AI 做什么"},
                {"icon": "🎭", "name": "角色扮演", "desc": "设定专家身份"},
                {"icon": "📚", "name": "提供示例", "desc": "Few-shot 教学"},
                {"icon": "🔄", "name": "逐步优化", "desc": "迭代改进效果"}
            ],
            "summary": "指令清晰 | 角色设定 | 示例引导 | 持续优化",
            "color": "#ec4899"
        }
    }
    
    # 返回对应主题的知识，如果不存在则使用通用模板
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


def create_scene_title(topic, knowledge):
    """Scene 1: 标题开场（v5.1 优化版：渐变背景 + 装饰元素）"""
    width, height = 1920, 1080
    
    # ✨ v5.1 升级：渐变背景
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    # 绘制中心光晕效果
    for r in range(400, 0, -20):
        alpha = int(40 * (1 - r/400))
        color = (15 + alpha, 15 + alpha, 30 + alpha)
        draw.ellipse([width//2-r, height//2-r, width//2+r, height//2+r], fill=color)
    
    # ✨ v5.1 升级：带阴影的主标题
    shadow_offset = 4
    draw.text((width // 2 + shadow_offset, 350 + shadow_offset), knowledge["title"], 
              fill=(0, 0, 0), font=GLOBAL_FONTS['title'], anchor="mm")
    draw.text((width // 2, 350), knowledge["title"], 
              fill=COLORS['white'], font=GLOBAL_FONTS['title'], anchor="mm")
    
    # ✨ v5.1 升级：渐变色副标题
    subtitle_color = knowledge.get("color", COLORS['accent'])
    draw.text((width // 2, 480), knowledge["subtitle"], 
              fill=subtitle_color, font=GLOBAL_FONTS['subtitle'], anchor="mm")
    
    # ✨ v5.1 升级：霓虹装饰线（多色渐变）
    gradient_width = 600
    for i in range(gradient_width):
        x = width // 2 - gradient_width // 2 + i
        progress = i / gradient_width
        if progress < 0.33:
            color = COLORS['accent_1'] if 'accent_1' in COLORS else '#ff6b6b'
        elif progress < 0.66:
            color = COLORS['accent_2'] if 'accent_2' in COLORS else '#4ecdc4'
        else:
            color = COLORS['accent_3'] if 'accent_3' in COLORS else '#ffe66d'
        draw.line([(x, 560), (x+1, 560)], fill=color, width=4)
    
    return img


def create_concept_scene(topic, knowledge, concept_idx):
    """Scene 2-5: 概念详解 (每个 3-4 秒)"""
    width, height = 1920, 1080
    concept = knowledge["concepts"][concept_idx]
    
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    # 场景标题
    draw.text((width // 2, 80), f"第{concept_idx + 1}个要点", 
              fill=COLORS['gray_light'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
    
    # 主卡片
    card_x, card_y = width//2 - 400, 200
    draw.rounded_rectangle([card_x, card_y, card_x+800, card_y+300], 
                          radius=20, fill=knowledge["color"])
    
    # 图标和名称
    draw.text((width // 2, 280), concept["icon"], 
              fill=COLORS['white'], font=GLOBAL_FONTS['title'], anchor="mm")
    draw.text((width // 2, 360), concept["name"], 
              fill=COLORS['white'], font=GLOBAL_FONTS['subtitle'], anchor="mm")
    
    # 描述
    draw.text((width // 2, 550), concept["desc"], 
              fill=COLORS['white'], font=GLOBAL_FONTS['text'], anchor="mm")
    
    # 导航条
    nav_items = []
    for i in range(len(knowledge["concepts"])):
        if i == concept_idx:
            nav_items.append(f"{knowledge['concepts'][i]['icon']}")
        else:
            nav_items.append("○")
    
    draw.rectangle([0, height-80, width, height], fill=COLORS['primary'])
    nav_text = "  ".join(nav_items)
    draw.text((width // 2, height - 40), nav_text, 
              fill=COLORS['gray_light'], font=GLOBAL_FONTS['small'], anchor="mm")
    
    return img


def create_summary_scene(topic, knowledge):
    """Scene 6: 记忆口诀 (最后 2-3 秒)"""
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    # 标题
    draw.text((width // 2, 150), "💡 记忆口诀", 
              fill=knowledge["color"], font=GLOBAL_FONTS['title'], anchor="mm")
    
    # 总结卡片
    card_w = min(1400, len(knowledge["summary"]) * 30)
    card_h = 250
    card_x = (width - card_w) // 2
    
    draw.rounded_rectangle([card_x, 350, card_x+card_w, 350+card_h], 
                          radius=20, fill=knowledge["color"])
    
    # 总结文字（简化处理，实际应该分行）
    draw.text((width // 2, 480), knowledge["summary"], 
              fill=COLORS['white'], font=GLOBAL_FONTS['text'], anchor="mm")
    
    # 底部提示
    draw.rounded_rectangle([width//2-500, 750, width//2+500, 820], 
                          radius=15, fill=COLORS['primary'])
    draw.text((width // 2, 785), "© 2026 Knowledge Explainer v5.0 | OpenClaw AI", 
              fill=COLORS['gray_dark'], font=GLOBAL_FONTS['small'], anchor="mm")
    
    return img


def calculate_dynamic_frames(knowledge):
    """
    ✨ v5.1 优化：根据内容数量动态计算视频时长
    
    规则：
    - 每个概念 ≈ 2.5 秒（75 帧）
    - 标题开场 = 2 秒（60 帧）
    - 总结结尾 = 3 秒（90 帧）
    - 总时长 = 标题 + N×概念 + 总结
    
    Returns:
        总帧数，fps
    """
    num_concepts = len(knowledge["concepts"])
    
    # 动态计算：每个概念 75 帧（2.5 秒）
    frames_per_concept = 75
    title_frames = 60      # 2 秒
    summary_frames = 90    # 3 秒
    
    total_frames = title_frames + (num_concepts * frames_per_concept) + summary_frames
    fps = 30
    
    return total_frames, fps, {
        "title": title_frames,
        "concept_each": frames_per_concept,
        "summary": summary_frames
    }


def create_frame(frame_num, frame_config, topic, knowledge):
    """根据帧号创建对应场景（优化版：支持动态时长）"""
    
    scene_frames = frame_config
    
    if frame_num < scene_frames["title"]:
        return create_scene_title(topic, knowledge)
    
    frame_num -= scene_frames["title"]
    
    concept_idx = frame_num // scene_frames["concept_each"]
    if concept_idx < len(knowledge["concepts"]):
        return create_concept_scene(topic, knowledge, concept_idx)
    
    return create_summary_scene(topic, knowledge)


def generate_video(topic, output_path=None, custom_frames=None, fps=30):
    """生成完整的知识视频（v5.1：支持动态时长）"""
    
    if not output_path:
        skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_base = os.path.join(skill_dir, "output", topic)
        os.makedirs(output_base, exist_ok=True)
        output_path = os.path.join(output_base, f"{topic}_video.mp4")
    
    # 获取知识内容
    knowledge = get_knowledge_content(topic)
    
    # ✨ v5.1：动态计算帧数（根据概念数量）
    if custom_frames:
        total_frames = custom_frames
        frame_config = {
            "title": int(total_frames * 0.13),
            "concept_each": (total_frames - int(total_frames * 0.26)) // len(knowledge["concepts"]),
            "summary": int(total_frames * 0.13)
        }
    else:
        total_frames, fps, frame_config = calculate_dynamic_frames(knowledge)
    
    # 创建临时帧目录
    frame_dir = os.path.join(os.path.dirname(output_path), "frames_tmp")
    os.makedirs(frame_dir, exist_ok=True)
    
    # ✨ v5.1：输出动态时长信息
    print(f"🎬 开始生成视频：{topic}")
    print(f"   • 总帧数：{total_frames}")
    print(f"   • 时长：{total_frames/fps:.1f}秒 ({len(knowledge['concepts'])}个概念)")
    print(f"   • 场景：标题 ({frame_config['title']}帧) + {len(knowledge['concepts'])}×概念各 ({frame_config['concept_each']}帧) + 总结 ({frame_config['summary']}帧)")
    
    # 生成所有帧
    for frame_num in range(total_frames):
        img = create_frame(frame_num, frame_config, topic, knowledge)
        frame_path = os.path.join(frame_dir, f"frame_{frame_num:04d}.png")
        img.save(frame_path, "PNG")
        
        if frame_num % 50 == 0:
            progress = int(100 * frame_num / total_frames)
            print(f"   • 进度：{progress}%")
    
    # FFmpeg 合并帧为视频
    input_pattern = os.path.join(frame_dir, "frame_%04d.png")
    
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", input_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        output_path
    ]
    
    print("🔄 正在合并帧为视频...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # 清理临时帧文件
    import shutil
    if os.path.exists(frame_dir):
        shutil.rmtree(frame_dir)
    
    if result.returncode == 0:
        size_mb = os.path.getsize(output_path) / (1024*1024)
        print(f"✅ 视频生成成功：{output_path}")
        print(f"   • 大小：{size_mb:.2f} MB")
        return output_path
    else:
        print(f"❌ FFmpeg 失败:")
        print(result.stderr)
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python video_generator_dynamic.py <主题> [输出路径]")
        print("示例：python video_generator_dynamic.py 费曼学习法")
        sys.exit(1)
    
    topic = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("=" * 70)
    print(f"🎬 通用知识视频生成器 v1.0")
    print("=" * 70)
    print(f"✅ 字体：{FONT_NAME}")
    print()
    
    generate_video(topic, output_path)
    
    print()
    print("=" * 70)
    print("✅ 视频生成完成！")
    print("=" * 70)
