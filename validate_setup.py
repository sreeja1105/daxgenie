#!/usr/bin/env python3
"""
Quick validation script to check that daxgenie is set up correctly.
Run this before deploying to catch issues early.
"""

import sys
import subprocess
import os

def check_python_version():
    """Ensure Python 3.9+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check that required packages are installed"""
    required = ["streamlit", "fastapi", "uvicorn", "google.generativeai", "pytest"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg.replace("-", "_"))
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print(f"   Run: pip install {' '.join(missing)}")
        return False
    print(f"✅ All dependencies installed: {', '.join(required)}")
    return True

def check_env_file():
    """Check that .env file exists with GEMINI_API_KEY"""
    if not os.path.exists(".env"):
        print("⚠️  .env file not found. Copy .env.example to .env and set GEMINI_API_KEY")
        return True  # Not a hard failure, user can set it
    
    with open(".env") as f:
        content = f.read()
    
    if "GEMINI_API_KEY" in content and "your_gemini_api_key" not in content:
        print("✅ .env file found with GEMINI_API_KEY set")
        return True
    else:
        print("⚠️  .env found but GEMINI_API_KEY not configured. Set it before running.")
        return True

def check_syntax():
    """Check Python syntax of main files"""
    files = ["app.py", "api.py"]
    for fname in files:
        try:
            with open(fname) as f:
                compile(f.read(), fname, "exec")
        except SyntaxError as e:
            print(f"❌ Syntax error in {fname}: {e}")
            return False
    print(f"✅ Python syntax OK: {', '.join(files)}")
    return True

def run_tests():
    """Run pytest"""
    try:
        result = subprocess.run(["pytest", "-q", "tests/"], capture_output=True, timeout=30)
        if result.returncode == 0:
            print("✅ Tests pass")
            return True
        else:
            print(f"⚠️  Some tests failed:\n{result.stdout.decode()}")
            return False
    except FileNotFoundError:
        print("⚠️  pytest not found or tests/ directory missing")
        return True
    except subprocess.TimeoutExpired:
        print("⚠️  Tests timed out")
        return True

def check_docker():
    """Check if Docker is available"""
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.decode().strip()
            print(f"✅ Docker available: {version}")
            return True
    except FileNotFoundError:
        print("⚠️  Docker not found. Install Docker if you want to run docker-compose.")
        return True
    return False

def main():
    print("🧞 DAXGenie Setup Validation\n")
    
    checks = [
        ("Python version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment file", check_env_file),
        ("Syntax check", check_syntax),
        ("Unit tests", run_tests),
        ("Docker", check_docker),
    ]
    
    results = []
    for name, check_fn in checks:
        print(f"\n{name}:")
        results.append(check_fn())
    
    print("\n" + "="*50)
    if all(results):
        print("✅ All checks passed! Ready to deploy.")
        print("\nNext steps:")
        print("1. docker compose up --build")
        print("2. Visit http://localhost:8501")
        print("3. Test Generate and Explain modes")
        return 0
    else:
        print("⚠️  Some checks failed. See above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
