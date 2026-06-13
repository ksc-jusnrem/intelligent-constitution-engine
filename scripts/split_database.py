#!/usr/bin/env python3
import os
import json

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    const_dir = os.path.join(base_dir, "data", "constitution")
    
    src_json_path = os.path.join(const_dir, "data.json")
    if not os.path.exists(src_json_path):
        print(f"Error: Source file {src_json_path} does not exist. Run extract_history.py first.")
        return
        
    with open(src_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # 1. Write data_full.json and data_full.js
    full_json_path = os.path.join(const_dir, "data_full.json")
    full_js_path = os.path.join(const_dir, "data_full.js")
    
    with open(full_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        
    with open(full_js_path, "w", encoding="utf-8") as f:
        f.write("/* Auto-generated full database. Do not edit manually. */\n")
        f.write("window.CONSTITUTION_DATA_FULL = ")
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    print(f"Wrote {full_json_path} and {full_js_path}")
    
    # 2. Generate individual article chunks (both .json and .js)
    articles_dir = os.path.join(const_dir, "articles")
    os.makedirs(articles_dir, exist_ok=True)
    
    for key, article in data["articles"].items():
        # js chunk
        art_js_path = os.path.join(articles_dir, f"{key}.js")
        with open(art_js_path, "w", encoding="utf-8") as f:
            f.write(f"/* Auto-generated chunk for {key}. */\n")
            f.write(f"if (window.CONSTITUTION_DATA && window.CONSTITUTION_DATA.articles['{key}']) {{\n")
            f.write(f"  window.CONSTITUTION_DATA.articles['{key}'].versions = ")
            json.dump(article["versions"], f, ensure_ascii=False, separators=(",", ":"))
            f.write(";\n}\n")
            
        # json chunk
        art_json_path = os.path.join(articles_dir, f"{key}.json")
        with open(art_json_path, "w", encoding="utf-8") as f:
            json.dump(article, f, ensure_ascii=False, separators=(",", ":"))
            
    print(f"Generated {len(data['articles'])} article chunks under {articles_dir}")
    
    # 3. Strip text from original data object to make a lightweight shell
    stripped_articles = {}
    for key, article in data["articles"].items():
        stripped_versions = []
        for ver in article["versions"]:
            # Keep only commit index, omit text
            stripped_versions.append({"commit": ver["commit"]})
        stripped_articles[key] = {
            "num": article["num"],
            "title": article["title"],
            "versions": stripped_versions
        }
        
    stripped_data = {
        "meta": data["meta"],
        "commits": data["commits"],
        "articles": stripped_articles
    }
    
    # Update meta to denote it's chunked
    stripped_data["meta"]["chunked"] = True
    
    # Overwrite data.json and data.js
    with open(src_json_path, "w", encoding="utf-8") as f:
        json.dump(stripped_data, f, ensure_ascii=False, separators=(",", ":"))
        
    src_js_path = os.path.join(const_dir, "data.js")
    with open(src_js_path, "w", encoding="utf-8") as f:
        f.write("/* Auto-generated shell database. Do not edit manually. */\n")
        f.write("window.CONSTITUTION_DATA = ")
        json.dump(stripped_data, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
        
    print(f"Overwrote stripped shell {src_json_path} and {src_js_path}")
    print("Database splitting complete!")

if __name__ == "__main__":
    main()
