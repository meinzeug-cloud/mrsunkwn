#!/usr/bin/env python3
"""
Mrs-Unkwn System Validation Test
Tests the code generation and issue management functionality
"""
import os
import sys
import subprocess
from pathlib import Path

def test_code_generation():
    """Test if the script generates substantial code"""
    print("🧪 Testing code generation...")
    
    # Count generated files
    backend_files = list(Path("backend/src").rglob("*.py"))
    frontend_files = list(Path("frontend/src").rglob("*.tsx")) + list(Path("frontend/src").rglob("*.ts"))
    
    print(f"📁 Backend files: {len(backend_files)}")
    print(f"📁 Frontend files: {len(frontend_files)}")
    
    # Check for Mrs-Unkwn specific components
    mrs_unkwn_files = []
    for file_path in backend_files + frontend_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if any(keyword in content for keyword in ['Mrs-Unkwn', 'Socratic', 'AntiCheat', 'ParentalControl']):
                    mrs_unkwn_files.append(file_path)
        except:
            pass
    
    print(f"🎯 Mrs-Unkwn specific files: {len(mrs_unkwn_files)}")
    
    # Count total lines of code
    total_lines = 0
    for file_path in backend_files + frontend_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                total_lines += len(f.readlines())
        except:
            pass
    
    print(f"📏 Total lines of code: {total_lines}")
    
    return {
        'backend_files': len(backend_files),
        'frontend_files': len(frontend_files),
        'mrs_unkwn_files': len(mrs_unkwn_files),
        'total_lines': total_lines
    }

def test_issue_tracking():
    """Test the issue tracking functionality"""
    print("🧪 Testing issue tracking...")
    
    issues_dir = Path("codex/data/issues")
    if not issues_dir.exists():
        print("❌ Issues directory not found")
        return False
    
    issue_files = list(issues_dir.glob("*.md"))
    summary_files = list(issues_dir.glob("*.json"))
    
    print(f"📋 Issue tracking files: {len(issue_files)}")
    print(f"📊 Summary files: {len(summary_files)}")
    
    # Check latest summary
    if summary_files:
        latest_summary = summary_files[-1]
        print(f"📄 Latest summary: {latest_summary.name}")
        try:
            import json
            with open(latest_summary, 'r') as f:
                summary_data = json.load(f)
                print(f"   - Total tasks: {summary_data.get('total_tasks', 0)}")
                print(f"   - Sprint number: {summary_data.get('sprint_number', 0)}")
        except:
            print("   - Could not read summary data")
    
    return len(issue_files) > 0 and len(summary_files) > 0

def test_roadmap_alignment():
    """Test if development follows roadmap"""
    print("🧪 Testing roadmap alignment...")
    
    roadmap_path = Path("roadmap.md")
    if not roadmap_path.exists():
        print("❌ Roadmap not found")
        return False
    
    with open(roadmap_path, 'r', encoding='utf-8') as f:
        roadmap_content = f.read()
    
    # Check if key Mrs-Unkwn features are mentioned
    key_features = [
        'AI Tutor',
        'Socratic Method',
        'Anti-Cheat',
        'Parental Controls',
        'Device Monitoring',
        'Learning Analytics',
        'Gamification'
    ]
    
    found_features = []
    for feature in key_features:
        if feature in roadmap_content:
            found_features.append(feature)
    
    print(f"🎯 Key features in roadmap: {len(found_features)}/{len(key_features)}")
    for feature in found_features:
        print(f"   ✅ {feature}")
    
    # Check if generated code implements these features
    implemented_features = []
    backend_dir = Path("backend/src")
    
    for feature in key_features:
        feature_files = []
        for file_path in backend_dir.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if feature.lower().replace(' ', '') in content.lower().replace(' ', '').replace('-', '').replace('_', ''):
                        feature_files.append(file_path)
            except:
                pass
        
        if feature_files:
            implemented_features.append(feature)
            print(f"   🏗️ {feature}: {len(feature_files)} files")
    
    return len(implemented_features) >= len(key_features) * 0.7  # At least 70% implemented

def test_script_execution():
    """Test if the start_agent.sh script can run"""
    print("🧪 Testing script execution...")
    
    script_path = Path("scripts/start_agent.sh")
    if not script_path.exists():
        print("❌ start_agent.sh not found")
        return False
    
    # Check if script is executable
    if not os.access(script_path, os.X_OK):
        print("⚠️ Script not executable, making it executable")
        os.chmod(script_path, 0o755)
    
    print("✅ Script exists and is executable")
    return True

def main():
    """Main test function"""
    print("🚀 Mrs-Unkwn System Validation")
    print("=" * 50)
    
    os.chdir(Path(__file__).parent)
    
    results = {}
    
    # Test 1: Code Generation
    code_stats = test_code_generation()
    results['code_generation'] = code_stats['total_lines'] > 20000  # At least 20K lines
    
    print()
    
    # Test 2: Issue Tracking
    results['issue_tracking'] = test_issue_tracking()
    
    print()
    
    # Test 3: Roadmap Alignment
    results['roadmap_alignment'] = test_roadmap_alignment()
    
    print()
    
    # Test 4: Script Execution
    results['script_execution'] = test_script_execution()
    
    print()
    print("📊 Test Results Summary:")
    print("=" * 30)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    overall_score = sum(results.values()) / len(results) * 100
    print(f"\n🎯 Overall Score: {overall_score:.1f}%")
    
    if overall_score >= 75:
        print("🏆 Mrs-Unkwn automation system is working well!")
        return 0
    elif overall_score >= 50:
        print("⚠️ Mrs-Unkwn automation system has some issues but is functional")
        return 1
    else:
        print("❌ Mrs-Unkwn automation system needs significant improvements")
        return 2

if __name__ == "__main__":
    sys.exit(main())