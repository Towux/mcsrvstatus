#!/usr/bin/env python3
"""Build and install script for mcsrvstatus library."""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description=""):
    """Execute command with output."""
    print(f"Running: {description or command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command execution error: {e}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False


def clean_build():
    """Clean build directories."""
    dirs_to_clean = ['build', 'dist', 'mcsrvstatus.egg-info']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removing directory: {dir_name}")
            shutil.rmtree(dir_name)
    
    # Remove __pycache__
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs[:]:
            if dir_name == '__pycache__':
                pycache_path = os.path.join(root, dir_name)
                print(f"Removing: {pycache_path}")
                shutil.rmtree(pycache_path)
                dirs.remove(dir_name)


def build_package():
    """Build package."""
    print("Building package...")
    
    # Build source distribution
    if not run_command("python setup.py sdist", "Creating source distribution"):
        return False
    
    # Build wheel package
    if not run_command("python setup.py bdist_wheel", "Creating wheel package"):
        return False
    
    return True


def install_package():
    """Install package in development mode."""
    print("Installing package in development mode...")
    return run_command("pip install -e .", "Installing in development mode")


def run_tests():
    """Run tests."""
    print("Running tests...")
    return run_command("python -m pytest tests/ -v", "Running tests")


def check_requirements():
    """Check installed dependencies."""
    print("Checking dependencies...")
    
    try:
        import requests
        print("✓ requests installed")
    except ImportError:
        print("✗ requests not installed")
        print("Installing requests...")
        if not run_command("pip install requests", "Installing requests"):
            return False
    
    try:
        import aiohttp
        print("✓ aiohttp installed")
    except ImportError:
        print("✗ aiohttp not installed")
        print("Installing aiohttp...")
        if not run_command("pip install aiohttp", "Installing aiohttp"):
            return False
    
    return True


def main():
    """Main function."""
    print("Building mcsrvstatus library")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('setup.py'):
        print("Error: setup.py file not found!")
        print("Make sure you are in the project root directory.")
        sys.exit(1)
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "clean":
            clean_build()
            return
        elif command == "build":
            clean_build()
            if check_requirements():
                build_package()
            return
        elif command == "install":
            if check_requirements():
                install_package()
            return
        elif command == "test":
            if check_requirements():
                run_tests()
            return
        elif command == "all":
            clean_build()
            if check_requirements():
                if build_package():
                    if install_package():
                        run_tests()
            return
        else:
            print(f"Unknown command: {command}")
            print("Available commands: clean, build, install, test, all")
            return
    
    # Default: full build
    clean_build()
    if check_requirements():
        if build_package():
            print("\\nBuild completed successfully!")
            print("\\nTo install run:")
            print("python build.py install")
            print("\\nTo run tests:")
            print("python build.py test")


if __name__ == "__main__":
    main()