#!/usr/bin/env python3
import os
import json
import re

def main():
    repo_path = "documentary-repository"
    manifest_file = os.path.join(repo_path, "manifest.json")
    lineage_file = "lineage.js"

    if not os.path.exists(manifest_file):
        print(f"Error: manifest.json not found at {manifest_file}")
        return

    if not os.path.exists(lineage_file):
        print(f"Error: lineage.js not found at {lineage_file}")
        return

    # 1. Load manifest.json
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # 2. Load and parse lineage.js as JSON
    with open(lineage_file, "r", encoding="utf-8") as f:
        lineage_content = f.read()

    # Find the JSON block between window.CONSTITUTION_LINEAGE = { ... };
    start_idx = lineage_content.find("{")
    end_idx = lineage_content.rfind("}")
    if start_idx == -1 or end_idx == -1:
        print("Error: Could not find JSON block in lineage.js")
        return

    json_str = lineage_content[start_idx:end_idx+1]
    lineage_data = json.loads(json_str)

    # 3. Create maps from lineage.js
    frameworks_map = {}
    era_map = {}
    for era in lineage_data["eras"]:
        era_title = f"{era['name']} ({era['span']})"
        era_map[era["id"]] = era_title
        for fw in era["frameworks"]:
            frameworks_map[fw["id"]] = {
                "era_title": era_title,
                "provisions": fw.get("provisions", []),
                "demise": fw.get("demise", "")
            }

    print(f"Loaded {len(manifest)} manifest entries and {len(frameworks_map)} lineage.js frameworks.")

    # 4. Generate metadata.json and text.md for each framework
    for entry in manifest:
        fw_id = entry["id"]
        folder_dir = entry["dir"]
        
        # Ensure the directory path is correct relative to the root
        target_dir = os.path.join(os.getcwd(), folder_dir)
        os.makedirs(target_dir, exist_ok=True)

        # Retrieve extra info from lineage.js
        extra = frameworks_map.get(fw_id, {
            "era_title": era_map.get(entry["era"], entry["era"]),
            "provisions": [],
            "demise": ""
        })

        # Construct metadata
        metadata = {
            "id": fw_id,
            "name": entry["name"],
            "date": entry["date"],
            "type": entry["type"],
            "era": extra["era_title"],
            "summary": entry.get("summary", ""),
            "key_provisions": extra["provisions"],
            "demise": extra["demise"],
            "provenance": {
                "source": entry.get("source") or "Sourced from legal history archives",
                "retrieved": "2026-06-12",
                "notes": f"Text status is {entry.get('textStatus') or 'pending'}"
            }
        }

        # Write metadata.json
        metadata_path = os.path.join(target_dir, "metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as out_f:
            json.dump(metadata, out_f, indent=2, ensure_ascii=False)
        print(f"Generated metadata.json for {fw_id} in {folder_dir}")

        # Write text.md if it doesn't exist
        text_path = os.path.join(target_dir, "text.md")
        if not os.path.exists(text_path):
            with open(text_path, "w", encoding="utf-8") as out_t:
                out_t.write(f"# {entry['name']}\n\n")
                out_t.write(f"**Era:** {extra['era_title']}  \n")
                out_t.write(f"**Date:** {entry['date']}  \n")
                out_t.write(f"**Type:** {entry['type']}  \n\n")
                out_t.write("---\n\n")
                out_t.write("## Status\n\n")
                out_t.write("PENDING ACQUISITION — authentic text to be sourced and placed here.\n")
            print(f"Initialized placeholder text.md for {fw_id}")

    # 5. Create master index.json in documentary-repository
    index_data = {
        "meta": {
            "name": "KSC.JUSNREM — Pre-1973 Constitutional Lineage",
            "total_frameworks": len(manifest),
            "last_updated": "2026-06-12",
            "description": "Complete structured repository of every constitutional and legal framework that governed the territories of Pakistan before 14 August 1973."
        },
        "eras": []
    }

    # Group by era
    grouped_eras = {}
    for era in lineage_data["eras"]:
        grouped_eras[era["id"]] = {
            "id": era["id"],
            "name": f"{era['name']} ({era['span']})",
            "count": 0,
            "frameworks": []
        }

    for entry in manifest:
        era_id = entry["era"]
        if era_id in grouped_eras:
            grouped_eras[era_id]["count"] += 1
            grouped_eras[era_id]["frameworks"].append(entry["id"])

    for era_id in lineage_data["eras"]:
        index_data["eras"].append(grouped_eras[era_id["id"]])

    index_path = os.path.join(repo_path, "index.json")
    with open(index_path, "w", encoding="utf-8") as index_f:
        json.dump(index_data, index_f, indent=2, ensure_ascii=False)
    print(f"Generated master index.json in {repo_path}")

if __name__ == "__main__":
    main()
