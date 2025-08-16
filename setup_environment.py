#!/usr/bin/env python3
"""
AI Agents Integration Lab - Environment Setup
Automated setup script for all dependencies
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and provide feedback"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error Output: {e.stderr}")
        return False

def setup_environment():
    """Setup the complete development environment"""
    
    print("🚀 AI Agents Integration Lab - Environment Setup")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    
    # Check if virtual environment exists
    venv_path = project_root / "venv"
    if not venv_path.exists():
        print("\n📦 Creating virtual environment...")
        if not run_command(f"{sys.executable} -m venv venv", "Virtual environment creation"):
            return False
    else:
        print("\n✅ Virtual environment already exists!")
    
    # Determine the correct python executable path
    if os.name == 'nt':  # Windows
        python_exe = project_root / "venv" / "Scripts" / "python.exe"
        pip_exe = project_root / "venv" / "Scripts" / "pip.exe"
    else:  # Linux/Mac
        python_exe = project_root / "venv" / "bin" / "python"
        pip_exe = project_root / "venv" / "bin" / "pip"
    
    # Upgrade pip
    if not run_command(f'"{pip_exe}" install --upgrade pip', "Pip upgrade"):
        return False
    
    # Install main requirements
    requirements_file = project_root / "requirements.txt"
    if requirements_file.exists():
        if not run_command(f'"{pip_exe}" install -r requirements.txt', "Main dependencies installation"):
            return False
    
    # Install local-ai-service requirements
    local_service_req = project_root / "local-ai-service" / "requirements.txt"
    if local_service_req.exists():
        if not run_command(f'"{pip_exe}" install -r "{local_service_req}"', "Local AI service dependencies"):
            return False
    
    # Install zero-cost marketplace requirements
    marketplace_req = project_root / "zero-cost-ai-marketplace" / "requirements.txt"
    if marketplace_req.exists():
        if not run_command(f'"{pip_exe}" install -r "{marketplace_req}"', "Zero-cost marketplace dependencies"):
            return False
    
    # Test imports
    print("\n🧪 Testing critical imports...")
    test_imports = [
        "fastapi", "uvicorn", "requests", "pandas", 
        "numpy", "httpx", "pytest", "psutil", "structlog"
    ]
    
    import_test_cmd = f'"{python_exe}" -c "import {", ".join(test_imports)}; print(\\"✅ All critical imports successful!\\")"'
    if not run_command(import_test_cmd, "Import testing"):
        return False
    
    print("\n🎉 Environment setup completed successfully!")
    print("\n📋 Next steps:")
    print(f"   1. Activate environment: {'venv\\Scripts\\activate' if os.name == 'nt' else 'source venv/bin/activate'}")
    print("   2. Run tests: python -m pytest")
    print("   3. Start services: python local-ai-service/start_api.py")
    
    return True

if __name__ == "__main__":
    success = setup_environment()
    sys.exit(0 if success else 1)
