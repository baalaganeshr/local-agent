#!/usr/bin/env python3
"""
OWL Bridge - Connects Integration Lab with Main OWL System
Allows integration lab to access OWL orchestration from main project
"""
import sys
import os
from pathlib import Path

def setup_owl_bridge():
    """Set up connection to main OWL system"""
    
    # Find the main Multi-ai-agents directory with OWL
    current_dir = Path(__file__).parent
    main_project_dir = current_dir / "Multi-ai-agents"
    
    if main_project_dir.exists():
        owl_path = main_project_dir / "owl"
        if owl_path.exists():
            # Add OWL to Python path
            sys.path.insert(0, str(owl_path))
            sys.path.insert(0, str(main_project_dir))
            
            try:
                # Test OWL import
                from owl_integration import OWLIntegration
                from agents.base_agent import BaseAgent
                
                print("✅ OWL Bridge: Successfully connected to main OWL system")
                return True
                
            except ImportError as e:
                print(f"⚠️ OWL Bridge: Import error - {e}")
                return False
        else:
            print("❌ OWL Bridge: OWL directory not found")
            return False
    else:
        print("❌ OWL Bridge: Main project directory not found")
        return False

def test_owl_connection():
    """Test OWL connection"""
    if setup_owl_bridge():
        try:
            from owl_integration import OWLIntegration
            integration = OWLIntegration()
            print(f"🦉 OWL Status: {'Available' if integration else 'Not Available'}")
            return True
        except Exception as e:
            print(f"❌ OWL Test Failed: {e}")
            return False
    return False

if __name__ == "__main__":
    print("🌉 Setting up OWL Bridge...")
    success = setup_owl_bridge()
    if success:
        test_owl_connection()
        print("🎉 OWL Bridge setup complete!")
    else:
        print("❌ OWL Bridge setup failed!")
