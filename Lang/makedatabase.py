import json

with open("lang/zh_CN.json", "r", encoding="utf-8") as f:
    zh = json.load(f)

with open("lang/en_US.json", "r", encoding="utf-8") as f:
    en = json.load(f)

result = {}

def infer_type(key: str):
    if key.startswith("block.minecraft."):
        return "block"
    if key.startswith("item.minecraft."):
        return "item"
    if key.startswith("entity.minecraft."):
        return "entity"
    return "other"

for key, zh_name in zh.items():
    if key not in en:
        continue

    en_name = en[key]
    type_ = infer_type(key)

    # 只收集“有意义的实体”
    if type_ == "other":
        continue

    result[zh_name] = {
        "en": en_name,
        "id": key,
        "type": type_,
        "aliases": []
    }

with open("mc_zh_en_db.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"已生成 {len(result)} 条 Minecraft 实体映射")
