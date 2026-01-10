#!/usr/bin/env python3
import sys
import os
import mwclient

# ===== 路径配置 =====
CACHE_DIR = "./Cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

if len(sys.argv) < 2:
    print("missing")
    sys.exit(0)

title = sys.argv[1]
# 清理文件名中的非法字符
safe_filename = "".join([c for c in title if c.isalnum() or c in (' ', '_', '-')]).strip()
cache_path = os.path.join(CACHE_DIR, f"{safe_filename}.txt")

try:
    # 1. 连接到 Minecraft Wiki (中文)
    # 这里的 path='/' 是针对 minecraft.wiki 的标准配置
    site = mwclient.Site('zh.minecraft.wiki', path='/')

    # 2. 获取页面对象
    page = site.pages[title]

    # 3. 检查页面是否存在
    if not page.exists:
        print("missing")
        sys.exit(0)

    # 4. 处理重定向 (例如搜 "史蒂夫" 自动转到 "玩家")
    # mwclient 的 page 对象如果有重定向，直接调用 resolve_redirect() 即可拿到目标页
    if page.redirect:
        page = page.resolve_redirect()

    # 5. 获取完整的 WikiText 源码
    # page.text() 返回的是包含所有章节的完整内容
    content = page.text()

    if not content:
        print("missing")
    else:
        # === 写入本地缓存 ===
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            pass 
            
        # 输出给 stdout 供 AiChat.py 使用
        # 注意：这里输出的是原始 WikiText，AI 会自己提取信息
        print(content)

except Exception as e:
    # 调试时可打印 e 查看具体错误
    print("missing")
