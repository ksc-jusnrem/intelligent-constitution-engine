#!/usr/bin/env python3
import os
import shutil

def update_index_paths(index_path):
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update script paths
    # <script src="data.js"></script> -> <script src="../data/constitution/data.js"></script>
    content = content.replace('<script src="data.js"></script>', '<script src="../data/constitution/data.js"></script>')
    # <script src="lineage.js"></script> -> <script src="../data/lineage.js"></script>
    content = content.replace('<script src="lineage.js"></script>', '<script src="../data/lineage.js"></script>')
    # <script src="statutes.js"></script> -> <script src="js/statutes.js"></script>
    content = content.replace('<script src="statutes.js"></script>', '<script src="js/statutes.js"></script>')
    # <script src="router.js"></script> -> <script src="js/router.js"></script>
    content = content.replace('<script src="router.js"></script>', '<script src="js/router.js"></script>')

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated script paths in {index_path}")

def main():
    print("Starting project refactoring and directory movement...")

    # Define source and destination mappings
    moves = [
        ("index.html", "src/index.html"),
        ("router.js", "src/js/router.js"),
        ("statutes.js", "src/js/statutes.js"),
        ("lineage.js", "data/lineage.js"),
        ("data.js", "data/constitution/data.js"),
        ("data.json", "data/constitution/data.json")
    ]

    for src, dst in moves:
        if os.path.exists(src):
            # Ensure destination directory exists
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            print(f"Copied {src} -> {dst}")
        else:
            print(f"Warning: Source file {src} not found, skipping copy.")

    # Update paths in the moved index.html
    moved_index = "src/index.html"
    if os.path.exists(moved_index):
        update_index_paths(moved_index)

    # Update vercel.json configuration to handle rewrites to the src/ directory
    vercel_path = "vercel.json"
    if os.path.exists(vercel_path):
        with open(vercel_path, "r", encoding="utf-8") as f:
            v_data = json.load(f) if 'json' in globals() else {}
            try:
                import json
                v_data = json.load(f)
            except Exception:
                # Manual parsing or fallback if json module fails
                v_data = None

        if v_data:
            # Inject rewrites
            v_data["rewrites"] = [
                { "source": "/(.*)", "destination": "/src/$1" }
            ]
            # Ensure static assets in data/ are accessible
            v_data["rewrites"].insert(0, { "source": "/data/(.*)", "destination": "/data/$1" })
            
            with open(vercel_path, "w", encoding="utf-8") as f:
                json.dump(v_data, f, indent=2)
            print("Updated vercel.json with src/ directory rewrites.")

    print("✅ Project refactoring step completed successfully!")

if __name__ == "__main__":
    main()
