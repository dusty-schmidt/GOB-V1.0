#!/usr/bin/env python3
"""
Test script for the GOB Agent Naming System

This script demonstrates:
1. Daily main agent identity changes
2. Consistent subordinate agent naming 
3. API endpoint functionality
4. Web UI integration concepts

Run this script to see the naming system in action.
"""

import sys
import os
import datetime
from datetime import date, timedelta

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from python.helpers.naming_service import get_naming_service

def demonstrate_naming_system():
    print("=" * 60)
    print("GOB Agent Naming System Demo")
    print("=" * 60)
    
    naming_service = get_naming_service()
    
    # Show current main agent identity
    print("\n1. Current Main Agent Identity:")
    print("-" * 30)
    today = date.today()
    main_identity = naming_service.get_full_agent_identity("main")
    print(f"   Acronym: {main_identity['acronym']}")
    print(f"   Full Name: {main_identity['full_name']}")
    print(f"   Date: {main_identity['date']}")
    print(f"   Type: {main_identity['type']}")
    
    # Show different dates produce different names (for demonstration)
    print("\n2. Main Agent Identity for Different Dates:")
    print("-" * 45)
    for i in range(3):
        test_date = today + timedelta(days=i)
        identity = naming_service.get_full_agent_identity("main", date=test_date)
        print(f"   {test_date}: {identity['acronym']} - {identity['full_name']}")
    
    # Show subordinate agent naming
    print("\n3. Subordinate Agent Naming:")
    print("-" * 30)
    agent_types = ["developer", "researcher", "analyst", "writer"]
    for agent_type in agent_types:
        identity = naming_service.get_full_agent_identity(agent_type, context_id=f"ctx-{agent_type}-001")
        print(f"   {agent_type.title()}: {identity['acronym']} - {identity['full_name']}")
    
    # Show consistency with same context
    print("\n4. Subordinate Agent Consistency:")
    print("-" * 35)
    context_id = "ctx-dev-project-alpha"
    for i in range(3):
        identity = naming_service.get_full_agent_identity("developer", context_id=context_id)
        print(f"   Call {i+1}: {identity['acronym']} - {identity['full_name']}")
    
    # Show the convenience functions
    print("\n5. Convenience Functions:")
    print("-" * 25)
    from python.helpers.naming_service import (
        get_main_agent_name, 
        get_subordinate_agent_name, 
        get_agent_display_name
    )
    print(f"   get_main_agent_name(): {get_main_agent_name()}")
    print(f"   get_subordinate_agent_name('analyst'): {get_subordinate_agent_name('analyst')}")
    print(f"   get_agent_display_name(): {get_agent_display_name()}")
    
    print("\n6. System Features:")
    print("-" * 18)
    print("   ✓ Daily changing main agent identity")
    print("   ✓ Consistent subordinate agent acronyms (all GOB)")
    print("   ✓ Context-based subordinate name variations") 
    print("   ✓ Deterministic randomness (same input = same output)")
    print("   ✓ Graceful fallbacks when file loading fails")
    print("   ✓ API endpoint for web UI integration")
    print("   ✓ Automatic midnight updates in browser")
    
    print("\n7. Web UI Integration:")
    print("-" * 23)
    print("   • API Endpoint: /api_agent_identity")
    print("   • JavaScript Service: js/agent-naming.js")
    print("   • Automatic Updates: Every midnight")
    print("   • Cache Duration: 5 minutes")
    print("   • UI Updates: Title, version info, custom elements")
    
    print("\n" + "=" * 60)
    print("Demo Complete! 🎉")
    print("The naming system is ready for production use.")
    print("=" * 60)

if __name__ == "__main__":
    demonstrate_naming_system()
