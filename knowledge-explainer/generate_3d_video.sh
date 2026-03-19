#!/bin/bash
# Knowledge Explainer v5.0 - 3D 视频生成器
# 智能调用 Blender 生成 3D 教学视频

set -e

# ===== 配置 =====
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BLENDER_DIR="${SKILL_DIR}/../blender-video-generator"
OUTPUT_DIR="${SKILL_DIR}/output"

# ===== 参数解析 =====
TOPIC=""
QUALITY="medium"    # low/medium/high
DURATION=15         # 秒
CRF=23              # 视频质量（18-23，越低越好）

while [[ $# -gt 0 ]]; do
    case $1 in
        --topic)
            TOPIC="$2"
            shift 2
            ;;
        --quality|-q)
            QUALITY="$2"
            shift 2
            ;;
        --duration|-d)
            DURATION="$2"
            shift 2
            ;;
        --crf)
            CRF="$2"
            shift 2
            ;;
        -h|--help)
            echo "用法：$0 [选项]..."
            echo ""
            echo "选项:"
            echo "  --topic TOPIC     主题名称（必需）: neural_network, hsp, quantum_mechanics, blockchain, feynman"
            echo "  --quality QUAL    质量等级 (默认：medium): low | medium | high"
            echo "  --duration SEC    视频时长秒数 (默认：15)"
            echo "  --crf VALUE       FFmpeg CRF 值 (默认：23, 范围 18-28)"
            echo ""
            echo "示例:"
            echo "  $0 --topic neural_network --quality high"
            echo "  $0 --topic hsp -q medium -d 20"
            exit 0
            ;;
        *)
            # 如果第一个参数不带--，认为是 topic
            if [ -z "$TOPIC" ]; then
                TOPIC="$1"
            fi
            shift
            ;;
    esac
done

# ===== 验证输入 =====
if [ -z "$TOPIC" ]; then
    echo "❌ 错误：缺少主题名称 (--topic)"
    echo "可用主题：neural_network, hsp, quantum_mechanics, blockchain, feynman_learning"
    exit 1
fi

if [ ! -d "$BLENDER_DIR" ]; then
    echo "❌ 错误：Blender Video Generator 技能未找到"
    echo "请确保 blender-video-generator 在同级目录中"
    exit 1
fi

# ===== 执行流程 =====
echo "=========================================="
echo "🎬 Knowledge Explainer v5.0 - 3D 视频生成"
echo "=========================================="
echo ""
echo "📋 配置:"
echo "  主题：$TOPIC"
echo "  质量：$QUALITY"
echo "  时长：${DURATION}秒"
echo "  CRF: $CRF"
echo ""

# Step 1: 渲染 PNG 序列
echo "⏳ [1/2] 正在渲染 3D 场景（约 2-10 分钟）..."
cd "$BLENDER_DIR"

blender --background \
  --python scripts/generate_video.py \
  -- topic="$TOPIC" \
     quality="$QUALITY" \
     duration="$DURATION" \
  2>&1 | tail -20

# Step 2: 查找输出目录
cd "$BLENDER_DIR"

echo "📂 Searching in: $(pwd)/output/"

# 精确匹配文件夹（排除 PNG 文件）
OUTPUT_FOLDER=$(find output -maxdepth 1 -type d -name "*${TOPIC}_${QUALITY}_*" 2>/dev/null | sort -r | head -1)

if [ -z "$OUTPUT_FOLDER" ]; then
    echo "❌ 未找到输出文件夹，尝试手动查找..."
    ls -la output/
    exit 1
fi

echo "✅ Found folder: $OUTPUT_FOLDER"

if [ -z "$OUTPUT_FOLDER" ] || [ ! -d "$OUTPUT_FOLDER" ]; then
    echo "❌ 错误：未找到渲染输出文件夹"
    echo "请检查 blender-video-generator/output/ 目录"
    exit 1
fi

echo ""
echo "✅ PNG 序列已生成：$OUTPUT_FOLDER"
ls -lh "$OUTPUT_FOLDER" | head -3
echo "... $(ls "$OUTPUT_FOLDER"/*.png | wc -l) 帧 PNG"

# Step 3: 合成 MP4
echo ""
echo "⏳ [2/2] 正在合成 MP4 视频（约 10-30 秒）..."
mkdir -p "$OUTPUT_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${OUTPUT_DIR}/${TOPIC}_${QUALITY}_${TIMESTAMP}.mp4"

python3 scripts/png_to_mp4.py \
  --input-dir "$OUTPUT_FOLDER" \
  --output "$OUTPUT_FILE" \
  --fps 30 \
  --crf "$CRF"

# Step 4: 结果汇总
echo ""
echo "=========================================="
echo "✅ 3D 视频生成完成！"
echo "=========================================="
echo ""
echo "📁 输出文件:"
ls -lh "$OUTPUT_FILE" | awk '{print "  " $9 " (" $5 ")"}'
echo ""
echo "🎬 立即播放:"
echo "  xdg-open \"$OUTPUT_FILE\""
echo ""
echo "💡 提示：视频也保存在 PNG 序列目录中，可用于后期调整"
echo ""
