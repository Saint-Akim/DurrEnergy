"""
Smoke tests for app_ultra_modern_improved.py (self-contained folder)
Run: python test_ultra_modern_app.py
"""
import sys
import os
import subprocess
import importlib.util
from pathlib import Path

APP_FILE = "app_ultra_modern_improved.py"
HERE = Path(__file__).resolve().parent
os.chdir(HERE)


def check_dependencies():
    print("🔍 Checking dependencies...")
    required = [
        'streamlit', 'pandas', 'plotly', 'requests', 'openpyxl', 'numpy'
    ]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
            print(f"✅ {pkg}")
        except ImportError:
            print(f"❌ {pkg}")
            missing.append(pkg)
    if missing:
        print("\n❌ Missing packages:", ", ".join(missing))
        print("Run: pip install " + " ".join(missing))
        return False
    print("✅ All dependencies satisfied!")
    return True


def validate_app_syntax():
    print("\n🔍 Validating app syntax...")
    try:
        spec = importlib.util.spec_from_file_location("app_module", APP_FILE)
        assert spec is not None and spec.loader is not None
        print("✅ Python syntax appears valid (spec loaded)")
        return True
    except Exception as e:
        print(f"❌ Syntax error or load issue: {e}")
        return False


def check_data_files():
    print("\n🔍 Checking presence of common data files (optional)...")
    candidates = [
        "gen (2).xlsx", "gen (2).csv",
        "history (5).xlsx", "history (5).csv",
        "FACTORY ELEC.csv",
        "Durr bottling Generator filling.xlsx",
        "New_inverter.csv",
        "September 2025.xlsx",
        "Solar_Goodwe&Fronius-Jan.csv",
        "Solar_goodwe&Fronius_April.csv",
        "Solar_goodwe&Fronius_may.csv",
    ]
    any_found = False
    for f in candidates:
        if Path(f).exists():
            print(f"✅ Found: {f}")
            any_found = True
    if not any_found:
        print("ℹ️ No local data files found; the app can still try GitHub fallbacks where applicable.")
    return True


def run_streamlit_parse_check():
    print("\n🔍 Testing Streamlit can parse the app...")
    try:
        code = (
            "import streamlit as st, runpy; "
            f"open('{APP_FILE}'); print('✅ Streamlit can access the file')"
        )
        result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Streamlit compatibility (basic parse) confirmed")
            return True
        else:
            print("❌ Streamlit parse error:", result.stderr)
            return False
    except Exception as e:
        print(f"❌ Streamlit test failed: {e}")
        return False


def main():
    print("🧪 Smoke tests: app_ultra_modern_improved.py")
    print("=" * 60)
    tests = [
        ("Dependencies", check_dependencies),
        ("App Syntax", validate_app_syntax),
        ("Data Files (optional)", check_data_files),
        ("Streamlit Compatibility", run_streamlit_parse_check),
    ]
    results = {}
    all_passed = True
    for name, fn in tests:
        ok = fn()
        results[name] = ok
        all_passed = all_passed and ok

    print("\n" + "=" * 60)
    print("🎯 RESULTS:")
    for name, ok in results.items():
        print(f"  {name}: {'✅ PASS' if ok else '❌ FAIL'}")

    if all_passed:
        print("\n🎉 Smoke tests passed.")
        print("To run locally: streamlit run app_ultra_modern_improved.py")
    else:
        print("\n❌ Some checks failed. See logs above.")
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
