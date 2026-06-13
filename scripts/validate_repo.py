#!/usr/bin/env python3
import os
import json

def validate_framework(fw_id, fw_dir):
    errors = []
    warnings = []

    # 1. Check folder existence
    if not os.path.exists(fw_dir):
        errors.append(f"Folder does not exist: {fw_dir}")
        return errors, warnings

    # 2. Check metadata.json
    metadata_path = os.path.join(fw_dir, "metadata.json")
    if not os.path.exists(metadata_path):
        errors.append(f"Missing metadata.json at {metadata_path}")
    else:
        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            
            # Check required fields
            req_fields = ["id", "name", "date", "type", "era", "summary", "key_provisions", "demise", "provenance"]
            for field in req_fields:
                if field not in meta:
                    errors.append(f"metadata.json missing field: '{field}'")
                elif field in ["key_provisions"] and not isinstance(meta[field], list):
                    errors.append(f"metadata.json field '{field}' must be a list")
                elif field in ["provenance"] and not isinstance(meta[field], dict):
                    errors.append(f"metadata.json field '{field}' must be an object")

            if meta.get("id") != fw_id:
                errors.append(f"metadata.json ID mismatch: expected '{fw_id}', got '{meta.get('id')}'")
        except json.JSONDecodeError as e:
            errors.append(f"metadata.json contains invalid JSON: {e}")

    # 3. Check README.md
    readme_path = os.path.join(fw_dir, "README.md")
    if not os.path.exists(readme_path):
        errors.append(f"Missing README.md at {readme_path}")
    elif os.path.getsize(readme_path) == 0:
        warnings.append(f"README.md is empty at {readme_path}")

    # 4. Check text.md
    text_path = os.path.join(fw_dir, "text.md")
    if not os.path.exists(text_path):
        errors.append(f"Missing text.md at {text_path}")
    else:
        with open(text_path, "r", encoding="utf-8") as f:
            content = f.read()
        if "PENDING ACQUISITION" in content:
            warnings.append(f"text.md is a placeholder (PENDING ACQUISITION) at {text_path}")
        elif len(content.strip()) < 50:
            warnings.append(f"text.md is unusually short at {text_path}")

    return errors, warnings

def main():
    repo_path = "documentary-repository"
    manifest_file = os.path.join(repo_path, "manifest.json")
    
    if not os.path.exists(manifest_file):
        print(f"Error: manifest.json not found at {manifest_file}")
        return

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    total_errors = 0
    total_warnings = 0

    print("====================================================")
    print("KSC.JUSNREM — Documentary Repository Validation")
    print("====================================================")

    for entry in manifest:
        fw_id = entry["id"]
        fw_dir = entry["dir"]
        
        errors, warnings = validate_framework(fw_id, fw_dir)
        
        if errors or warnings:
            print(f"\n[!] Framework: {fw_id} ({entry['name']})")
            for err in errors:
                print(f"    - ERROR: {err}")
                total_errors += 1
            for warn in warnings:
                print(f"    - WARNING: {warn}")
                total_warnings += 1

    print("\n====================================================")
    print(f"Validation finished: {total_errors} error(s), {total_warnings} warning(s).")
    if total_errors > 0:
        print("[FAIL] Validation FAILED. Please resolve errors before committing.")
        sys.exit(1)
    else:
        print("[OK] Validation PASSED. Documentary repository is clean!")
        sys.exit(0)

if __name__ == "__main__":
    import sys
    main()
