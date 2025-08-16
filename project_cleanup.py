#!/usr/bin/env python3
"""
Project Cleanup Script
Removes empty and problematic files that may cause integration issues
"""

import os
import sys
from pathlib import Path

def cleanup_project():
    """Clean up empty and problematic files"""
    
    project_root = Path("G:/c/OneDrive/Desktop/localai/local-agent")
    
    # List of empty/problematic files to remove
    empty_files_to_remove = [
        "fix_ollama_service.ps1",
        "gpt_oss_evaluator.py", 
        "GPT_OSS_INTEGRATION_SUITE.md",
        "run_gpt_oss_business_tests.py",
        "setup_ollama.bat",
        "test_gpt_oss_20b.ps1"
    ]
    
    # Files that should have minimal content
    files_to_check = [
        "agents/__init__.py"
    ]
    
    removed_count = 0
    errors = []
    
    print("🧹 Starting Project Cleanup...")
    print("=" * 50)
    
    # Remove completely empty files
    for filename in empty_files_to_remove:
        filepath = project_root / filename
        if filepath.exists():
            try:
                if filepath.stat().st_size == 0:
                    filepath.unlink()
                    print(f"✅ Removed empty file: {filename}")
                    removed_count += 1
                else:
                    print(f"⚠️  File not empty, keeping: {filename}")
            except Exception as e:
                errors.append(f"Failed to remove {filename}: {e}")
                print(f"❌ Error removing {filename}: {e}")
    
    # Check and fix __init__.py files
    for filename in files_to_check:
        filepath = project_root / filename
        if filepath.exists():
            try:
                content = filepath.read_text().strip()
                if not content:
                    # Add basic content to __init__.py
                    filepath.write_text('"""Agent module initialization"""')
                    print(f"✅ Fixed empty __init__.py: {filename}")
                else:
                    print(f"✅ __init__.py has content: {filename}")
            except Exception as e:
                errors.append(f"Failed to check {filename}: {e}")
                print(f"❌ Error checking {filename}: {e}")
    
    # Remove Python cache directories that might cause issues
    cache_dirs = list(project_root.rglob("__pycache__"))
    for cache_dir in cache_dirs:
        if cache_dir.name == "__pycache__" and "venv" not in str(cache_dir):
            try:
                import shutil
                shutil.rmtree(cache_dir)
                print(f"✅ Removed cache directory: {cache_dir.relative_to(project_root)}")
                removed_count += 1
            except Exception as e:
                errors.append(f"Failed to remove {cache_dir}: {e}")
                print(f"❌ Error removing cache {cache_dir}: {e}")
    
    # Check for .pyc files outside venv
    pyc_files = [f for f in project_root.rglob("*.pyc") if "venv" not in str(f)]
    for pyc_file in pyc_files:
        try:
            pyc_file.unlink()
            print(f"✅ Removed .pyc file: {pyc_file.relative_to(project_root)}")
            removed_count += 1
        except Exception as e:
            errors.append(f"Failed to remove {pyc_file}: {e}")
            print(f"❌ Error removing .pyc {pyc_file}: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Cleanup Summary:")
    print(f"   ✅ Files/directories removed: {removed_count}")
    print(f"   ❌ Errors encountered: {len(errors)}")
    
    if errors:
        print("\n🚨 Errors:")
        for error in errors:
            print(f"   - {error}")
    
    # Verify critical files exist
    print("\n🔍 Verifying Critical Files:")
    critical_files = [
        "unified_agent_api.py",
        "integration_checker.py", 
        "customer_request_agent.py",
        "requirements.txt",
        "agents/__init__.py",
        "agents/base_agent.py",
        "local-ai-service/ai_chat.html"
    ]
    
    for filename in critical_files:
        filepath = project_root / filename
        if filepath.exists() and filepath.stat().st_size > 0:
            print(f"   ✅ {filename}")
        else:
            print(f"   ❌ Missing or empty: {filename}")
    
    print("\n✅ Project cleanup completed!")
    
    return removed_count, errors

if __name__ == "__main__":
    removed, errors = cleanup_project()
    sys.exit(0 if len(errors) == 0 else 1)
