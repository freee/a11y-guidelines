#!/usr/bin/env python3
"""Test runner script for yaml2rst test suite."""
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    print(f"Exit code: {result.returncode}")
    return result.returncode == 0


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run yaml2rst test suite")
    parser.add_argument(
        '--type', 
        choices=['unit', 'integration', 'functional', 'performance', 'all'],
        default='all',
        help='Type of tests to run'
    )
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Run with coverage reporting'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Run with verbose output'
    )
    parser.add_argument(
        '--fast',
        action='store_true',
        help='Skip slow tests'
    )
    parser.add_argument(
        '--parallel',
        action='store_true',
        help='Run tests in parallel'
    )
    
    args = parser.parse_args()
    
    # Change to the script directory
    script_dir = Path(__file__).parent
    
    # Base pytest command
    pytest_cmd = ['python', '-m', 'pytest']
    
    # Add verbose flag
    if args.verbose:
        pytest_cmd.append('-v')
    else:
        pytest_cmd.append('-q')
    
    # Add coverage if requested
    if args.coverage:
        pytest_cmd.extend(['--cov=src/yaml2rst', '--cov-report=html', '--cov-report=term-missing'])
    
    # Add parallel execution if requested
    if args.parallel:
        pytest_cmd.extend(['-n', 'auto'])
    
    # Skip slow tests if requested
    if args.fast:
        pytest_cmd.extend(['-m', 'not slow'])
    
    # Determine which tests to run
    test_paths = []
    
    if args.type == 'all':
        test_paths = ['tests/']
    elif args.type == 'unit':
        test_paths = ['tests/unit/']
    elif args.type == 'integration':
        test_paths = ['tests/integration/']
    elif args.type == 'functional':
        test_paths = ['tests/functional/']
    elif args.type == 'performance':
        test_paths = ['tests/performance/']
    
    # Add test paths to command
    pytest_cmd.extend(test_paths)
    
    print("yaml2rst Test Suite Runner")
    print(f"Test type: {args.type}")
    print(f"Coverage: {args.coverage}")
    print(f"Verbose: {args.verbose}")
    print(f"Fast mode: {args.fast}")
    print(f"Parallel: {args.parallel}")
    
    # Run the tests
    success = run_command(pytest_cmd, f"Running {args.type} tests")
    
    if success:
        print("\n✅ All tests passed!")
        
        if args.coverage:
            print("\n📊 Coverage report generated in htmlcov/")
            
        # Run additional checks if all tests passed
        if args.type == 'all':
            print("\n🔍 Running additional quality checks...")
            
            # Check for test coverage
            if args.coverage:
                coverage_cmd = ['python', '-m', 'coverage', 'report', '--fail-under=85']
                coverage_success = run_command(coverage_cmd, "Checking coverage threshold")
                
                if not coverage_success:
                    print("❌ Coverage below threshold!")
                    return 1
            
            # Check for code style (if flake8 is available)
            try:
                flake8_cmd = ['python', '-m', 'flake8', 'src/', 'tests/']
                flake8_success = run_command(flake8_cmd, "Checking code style")
                
                if not flake8_success:
                    print("⚠️  Code style issues found (non-blocking)")
            except FileNotFoundError:
                print("ℹ️  flake8 not available, skipping style check")
        
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == '__main__':
    sys.exit(main())
