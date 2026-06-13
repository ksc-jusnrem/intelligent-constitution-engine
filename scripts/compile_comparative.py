#!/usr/bin/env python3
import os
import re
import json

def clean_country_name(name):
    # e.g., "Antigua_and_Barbuda" -> "Antigua and Barbuda"
    # "Cote_DIvoire" -> "Côte d'Ivoire" (or similar cleanups)
    cleaned = name.replace("_", " ")
    if "DIvoire" in cleaned:
        cleaned = "Cote d'Ivoire"
    return cleaned

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    repo_dir = os.path.join(base_dir, "documentary-repository")
    out_dir = os.path.join(base_dir, "data")
    
    if not os.path.exists(repo_dir):
        print(f"Error: documentary-repository folder not found at {repo_dir}")
        return
        
    constitutions = []
    # Regex to match [Country]_[Year].pdf or [Country]_[Year]D.pdf (Drafts)
    pattern = re.compile(r"^([A-Za-z_]+)_(\d{4})([D]?)\.pdf$")
    
    for filename in sorted(os.listdir(repo_dir)):
        match = pattern.match(filename)
        if match:
            country_raw = match.group(1)
            year = int(match.group(2))
            is_draft = match.group(3) == "D"
            
            country_name = clean_country_name(country_raw)
            label = f"{country_name} ({year})" + (" (Draft)" if is_draft else "")
            
            constitutions.append({
                "id": filename.replace(".pdf", "").lower(),
                "country": country_name,
                "year": year,
                "draft": is_draft,
                "file": filename,
                "label": label
            })
            
    # Write comparative.json
    out_json_path = os.path.join(out_dir, "comparative.json")
    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(constitutions, f, ensure_ascii=False, separators=(",", ":"))
        
    # Write comparative.js
    out_js_path = os.path.join(out_dir, "comparative.js")
    with open(out_js_path, "w", encoding="utf-8") as f:
        f.write("/* Auto-generated comparative index. Do not edit manually. */\n")
        f.write("window.COMPARATIVE_DATA = ")
        json.dump(constitutions, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
        
    print(f"Compiled comparative index: {len(constitutions)} global constitutions indexed.")
    print(f"Wrote {out_json_path} and {out_js_path}")

if __name__ == "__main__":
    main()
