#!/bin/bash
# @小哲 番茄小说下载器 - Termux 一键安装脚本
echo "🍅 番茄小说下载器 Termux 安装中..."
echo ""
echo "📦 更新包管理器..."
pkg update -y && pkg upgrade -y
echo ""
echo "📦 安装 Python 和依赖..."
pkg install python -y
pip install requests beautifulsoup4 tqdm gmssl
echo ""
echo "📂 复制文件..."
mkdir -p $PREFIX/opt/fanqie_downloader
cp fanqie_txt.py $PREFIX/opt/fanqie_downloader/
cp abogus.py $PREFIX/opt/fanqie_downloader/
echo ""
echo "🔗 创建快捷命令..."
cat > $PREFIX/bin/fanqie << 'EOF'
#!/bin/bash
cd $PREFIX/opt/fanqie_downloader && python3 fanqie_txt.py "$@"
EOF
chmod +x $PREFIX/bin/fanqie
echo ""
echo "✨ 安装完成！"
echo "使用方法:"
echo "  fanqie --book_id <id>     # 下载小说"
echo "  fanqie --search <关键词>   # 搜索"
echo "  fanqie --check <id>       # 查详情"
echo "  fanqie                     # 交互菜单"
