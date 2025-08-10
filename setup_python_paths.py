#!/usr/bin/env python3
"""
Universal Python Path Setup
Fixes all import issues by setting up correct Python paths
"""
import sys
import os
from pathlib import Path

def setup_all_paths():
    """Setup all necessary Python paths"""
    
    current_dir = Path(__file__).parent
    
    # Add all component directories to Python path
    paths_to_add = [
        current_dir / "api-connectors",
        current_dir / "agent-adapters", 
        current_dir / "integration-tests",
        current_dir / "marketplace-api",
        current_dir / "external-agents",
        current_dir,  # Root integration lab directory
        current_dir / "Multi-ai-agents",  # Main project if exists
        current_dir / "Multi-ai-agents" / "owl"  # OWL framework if exists
    ]
    
    for path in paths_to_add:
        if path.exists():
            sys.path.insert(0, str(path))
            print(f"✅ Added to Python path: {path}")
    
    # Test imports
    print("\n🧪 Testing Critical Imports:")
    
    try:
        from agent_discovery_engine import AgentDiscoveryEngine
        print("✅ Import Success: AgentDiscoveryEngine")
    except ImportError as e:
        print(f"❌ Import Failed: AgentDiscoveryEngine - {e}")
    
    try:
        from marketplace_engine import MarketplaceEngine
        print("✅ Import Success: MarketplaceEngine") 
    except ImportError as e:
        print(f"❌ Import Failed: MarketplaceEngine - {e}")
    
    try:
        from comprehensive_integration_tests import IntegrationTestSuite
        print("✅ Import Success: IntegrationTestSuite")
    except ImportError as e:
        print(f"❌ Import Failed: IntegrationTestSuite - {e}")

if __name__ == "__main__":
    print("🔧 Setting up Python paths...")
    setup_all_paths()
    print("✅ Python path setup complete!")
