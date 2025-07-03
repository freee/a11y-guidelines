#!/usr/bin/env python3
"""Test runner script for freee_a11y_gl tests."""

import subprocess
import sys


def run_tests():
    """Run all tests and provide a summary."""
    
    test_suites = [
        ("Core Utils Tests", "tests/core/test_utils.py"),
        ("Base Model Tests", "tests/models/test_base.py"),
        ("RelationshipManager Tests", "tests/managers/test_relationship_manager.py"),
        ("YAML Processor Tests", "tests/yaml_processor/test_process_yaml.py"),
    ]
    
    results = []
    
    for name, test_path in test_suites:
        print(f"\n{'='*60}")
        print(f"Running {name}")
        print('='*60)
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_path, "-v"],
                capture_output=True,
                text=True,
                cwd="/home/max/work/a11y-guidelines/tools/lib/freee_a11y_gl"
            )
            
            if result.returncode == 0:
                print(f"✅ {name}: PASSED")
                results.append((name, "PASSED", ""))
            else:
                print(f"❌ {name}: FAILED")
                results.append((name, "FAILED", result.stdout + result.stderr))
                
        except Exception as e:
            print(f"💥 {name}: ERROR - {e}")
            results.append((name, "ERROR", str(e)))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    passed = sum(1 for _, status, _ in results if status == "PASSED")
    failed = sum(1 for _, status, _ in results if status == "FAILED")
    errors = sum(1 for _, status, _ in results if status == "ERROR")
    
    for name, status, output in results:
        icon = "✅" if status == "PASSED" else "❌" if status == "FAILED" else "💥"
        print(f"{icon} {name}: {status}")
        if status != "PASSED" and output:
            print(f"   {output[:200]}...")
    
    print(f"\nTotal: {len(results)} test suites")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Errors: {errors}")
    
    return failed + errors == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)