"""
scripts/build_all.py
Single deterministic pipeline entrypoint for regenerating all GitHub profile data and SVGs.
Can be executed locally or inside GitHub Actions automation.
"""

import sys
import subprocess
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def run_step(step_name, script_name):
    print(f"\n==========================================")
    print(f">> RUNNING: {step_name} ({script_name})")
    print(f"==========================================")
    script_path = os.path.join(SCRIPT_DIR, script_name)
    result = subprocess.run([sys.executable, script_path], check=True)
    if result.returncode != 0:
        print(f"[!] Error: Step '{step_name}' failed with code {result.returncode}")
        sys.exit(result.returncode)


def main():
    print("[*] Starting Devanshu Singh profile art build pipeline...")
    run_step("Data Fetching", "fetch_data.py")
    run_step("Cyber HUD SVG Generation", "render_hud_svg.py")
    run_step("Contribution Matrix SVG Generation", "render_matrix_svg.py")
    run_step("Featured Project Matrix SVG Generation", "render_projects_svg.py")
    print("\n[+] All profile visuals regenerated successfully!")


if __name__ == "__main__":
    main()
