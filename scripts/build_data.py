#!/usr/bin/env python3
import os
import sys
import subprocess

def main():
    print("====================================================")
    print("KSC.JUSNREM — Constitutional Intelligence Engine Build")
    print("====================================================")

    # 1. Run the Pre-1973 Lineage build
    print("\n--- Step 1: Building Constitutional Lineage ---")
    lineage_script = os.path.join("scripts", "build_lineage.py")
    if os.path.exists(lineage_script):
        result = subprocess.run([sys.executable, lineage_script], capture_output=True, encoding="utf-8")
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error building lineage:\n{result.stderr}")
            sys.exit(1)
    else:
        print("Error: build_lineage.py not found in scripts/.")
        sys.exit(1)

    # 2. Determine legalize-pk repository location
    print("--- Step 2: Locating legalize-pk data source ---")
    sibling_repo = os.path.abspath(os.path.join(os.getcwd(), "..", "legalize-pk"))
    temp_dir = os.environ.get("TEMP") or os.environ.get("TMP") or "C:\\Temp"
    temp_repo = os.path.join(temp_dir, "legalize-pk")

    repo_path = None
    if os.path.exists(os.path.join(sibling_repo, ".git")):
        print(f"Using sibling repository: {sibling_repo}")
        repo_path = sibling_repo
    elif os.path.exists(os.path.join(temp_repo, ".git")):
        print(f"Using cached temp repository: {temp_repo}")
        repo_path = temp_repo
    else:
        print(f"legalize-pk not found in sibling dir ({sibling_repo}) or temp ({temp_repo}).")
        print("Cloning upstream repository https://github.com/ksc-jusnrem/legalize-pk ...")
        try:
            os.makedirs(os.path.dirname(temp_repo), exist_ok=True)
            subprocess.run(["git", "clone", "https://github.com/ksc-jusnrem/legalize-pk.git", temp_repo], check=True)
            repo_path = temp_repo
            print("Successfully cloned legalize-pk.")
        except Exception as e:
            print(f"Error cloning legalize-pk repository: {e}")
            print("Please ensure Git is installed and you have network connectivity.")
            sys.exit(1)

    # 3. Run extract_history.py
    print("\n--- Step 3: Extracting 1973 Constitution Commit History ---")
    extract_script = os.path.join("scripts", "extract_history.py")
    if os.path.exists(extract_script):
        # We specify both arguments: REPO path and OUT path
        out_json = os.path.join("data", "constitution", "data.json")
        result = subprocess.run([sys.executable, extract_script, repo_path, out_json], capture_output=True, encoding="utf-8")
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error extracting history:\n{result.stderr}")
            sys.exit(1)
    else:
        print("Error: extract_history.py not found in scripts/.")
        sys.exit(1)

    # 4. Run split_database.py
    print("\n--- Step 4: Splitting database into chunks ---")
    split_script = os.path.join("scripts", "split_database.py")
    if os.path.exists(split_script):
        result = subprocess.run([sys.executable, split_script], capture_output=True, encoding="utf-8")
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error splitting database:\n{result.stderr}")
            sys.exit(1)
    else:
        print("Error: split_database.py not found in scripts/.")
        sys.exit(1)

    print("====================================================")
    print("BUILD COMPLETE: All data artifacts successfully generated!")
    print("====================================================")

if __name__ == "__main__":
    main()
