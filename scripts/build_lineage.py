#!/usr/bin/env python3
import os
import json
import re

ERA_BLURBS = {
    "era0": "Before the Crown governed directly, Parliament regulated the East India Company through a chain of statutes. Each tightened London's control and built the administrative skeleton later inherited by British India — and ultimately by Pakistan.",
    "era1": "After the uprising of 1857, the Crown assumed direct rule. Five great statutes then paced the slow widening of Indian participation in government — and the 1909 introduction of separate Muslim electorates set the constitutional trajectory that ended in Pakistan.",
    "era2": "Pakistan began life under an adapted colonial statute while its Constituent Assembly drafted a permanent constitution. The drafting took nine years, one dissolved assembly, and a courtroom battle whose doctrines haunt Pakistani law to this day.",
    "era3": "Pakistan's first indigenous constitution made it the world's first Islamic Republic — and lasted two and a half years. No general election was ever held under it.",
    "era4": "Ayub Khan gave the country a presidential constitution by decree — government 'suited to the genius of the people'. It lasted as long as he did.",
    "era5": "A provisional order, a framework for elections, a war that broke the federation in two, a judgment that outlawed usurpation, and an interim constitution — the road that ends where this engine's version-controlled history begins: 14 August 1973."
}

def main():
    repo_path = "documentary-repository"
    index_file = os.path.join(repo_path, "index.json")
    manifest_file = os.path.join(repo_path, "manifest.json")
    out_json = os.path.join("data", "lineage.json")
    out_js = os.path.join("data", "lineage.js")

    if not os.path.exists(index_file):
        print(f"Error: index.json not found at {index_file}")
        return

    # Load master index
    with open(index_file, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    # Load manifest to resolve IDs to folder paths
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    id_to_dir = {entry["id"]: entry["dir"] for entry in manifest}

    result = {
        "eras": []
    }

    for era in index_data["eras"]:
        era_id = era["id"]
        era_raw_name = era["name"]
        
        # Split name and span, e.g., "Company Rule — Precursor Statutes (1773–1853)"
        m = re.match(r"^(.*?)\s*\((.*?)\)$", era_raw_name)
        name = m.group(1) if m else era_raw_name
        span = m.group(2) if m else ""

        era_obj = {
            "id": era_id,
            "name": name,
            "span": span,
            "blurb": ERA_BLURBS.get(era_id, ""),
            "frameworks": []
        }

        for fw_id in era["frameworks"]:
            fw_dir = id_to_dir.get(fw_id)
            if not fw_dir:
                print(f"Warning: Could not find folder path for framework ID {fw_id}")
                continue

            metadata_path = os.path.join(fw_dir, "metadata.json")
            if not os.path.exists(metadata_path):
                print(f"Warning: metadata.json missing for {fw_id} at {metadata_path}")
                continue

            with open(metadata_path, "r", encoding="utf-8") as meta_f:
                meta = json.load(meta_f)

            # Reconstruct the compact version expected by the frontend
            fw_obj = {
                "id": meta["id"],
                "type": meta["type"],
                "date": meta["date"],
                "name": meta["name"],
                "summary": meta["summary"],
                "provisions": meta["key_provisions"],
                "demise": meta["demise"]
            }
            era_obj["frameworks"].append(fw_obj)

        result["eras"].append(era_obj)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(out_json), exist_ok=True)

    # Write lineage.json
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Wrote {out_json}")

    # Write lineage.js
    with open(out_js, "w", encoding="utf-8") as f:
        f.write("/* KSC.JUSNREM — Constitutional Intelligence Engine · constitution.codes\n")
        f.write("   Auto-generated from documentary-repository. Do not edit manually. */\n")
        f.write("window.CONSTITUTION_LINEAGE = ")
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print(f"Wrote {out_js}")

if __name__ == "__main__":
    main()
