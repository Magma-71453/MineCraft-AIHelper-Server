#!/usr/bin/env python3
import sys
import os
import requests
import json

# ===== 路径配置 =====
CACHE_DIR = "./Cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

if len(sys.argv) < 2:
    print("missing")
    sys.exit(0)

title = sys.argv[1]
# 清理文件名中的非法字符（简单处理）
safe_filename = "".join([c for c in title if c.isalnum() or c in (' ', '_', '-')]).strip()
cache_path = os.path.join(CACHE_DIR, f"{safe_filename}.txt")

API = "https://minecraft.wiki/api.php"
params = {
    "action": "query",
    "prop": "extracts",
    "explaintext": 1,
    "exintro": 0,
    "format": "json",
    "titles": title,
    "redirects": 1  # 自动处理重定向
}

try:
    r = requests.get(API, params=params, timeout=10)
    data = r.json()

    pages = data.get("query", {}).get("pages", {})
    
    # 检查是否是无效页面 (-1)
    if "-1" in pages:
        print("missing")
        sys.exit(0)

    page = next(iter(pages.values()))
    extract = page.get("extract", "").strip()

    if not extract:
        print("missing")
    else:
        # 预处理文本：去除多余换行，方便单行存储和传输
        clean_text = extract.replace("\n", " ")
        
        # === 优化部分：写入本地缓存 ===
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(clean_text)
        except Exception:
            pass # 写入失败不影响输出
            
        # 输出给 stdout 供 AiChat.py 直接捕获使用
        print(clean_text)

except Exception:
    print("missing")
