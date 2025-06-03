#!/usr/bin/env python3
"""
Setup script for Chess Engine Battle Program

This script:
1. Installs required Python dependencies
2. Installs Stockfish chess engine
3. Detects Stockfish installation path
4. Updates chess_e1_vs_e2.py with the correct Stockfish path
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path


def run_command(cmd, check=True, capture_output=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd, shell=True, check=check, capture_output=capture_output, text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        if check:
            print(f"Error running command: {cmd}")
            print(f"Error: {e}")
            return None
        return e


def install_python_dependencies():
    """Install required Python packages."""
    print("Installing Python dependencies...")
    result = run_command(f"{sys.executable} -m pip install python-chess")
    if result and result.returncode == 0:
        print("✓ python-chess installed successfully")
        return True
    else:
        print("✗ Failed to install python-chess")
        return False


def install_stockfish():
    """Install Stockfish chess engine based on the operating system."""
    print("Installing Stockfish...")
    
    # Check if Stockfish is already installed
    if shutil.which("stockfish"):
        print("✓ Stockfish is already installed")
        return True
    
    system = platform.system().lower()
    
    if system == "linux":
        # Try different package managers
        # First try apt (Ubuntu/Debian)
        result = run_command("which apt-get", check=False)
        if result and result.returncode == 0:
            print("Using apt package manager...")
            print("Note: This may require sudo privileges. If prompted, please enter your password.")
            result = run_command("apt-get update && apt-get install -y stockfish", check=False)
            if result and result.returncode == 0:
                print("✓ Stockfish installed via apt")
                return True
            else:
                print("Note: Installation may have failed due to missing sudo privileges")
                print("Trying alternative installation methods...")
        
        # Try yum (RedHat/CentOS)
        result = run_command("which yum", check=False)
        if result and result.returncode == 0:
            print("Using yum package manager...")
            result = run_command("yum install -y stockfish", check=False)
            if result and result.returncode == 0:
                print("✓ Stockfish installed via yum")
                return True
        
        # Try dnf (Fedora)
        result = run_command("which dnf", check=False)
        if result and result.returncode == 0:
            print("Using dnf package manager...")
            result = run_command("dnf install -y stockfish", check=False)
            if result and result.returncode == 0:
                print("✓ Stockfish installed via dnf")
                return True
                
    elif system == "darwin":  # macOS
        # Try Homebrew
        result = run_command("which brew", check=False)
        if result and result.returncode == 0:
            print("Using Homebrew...")
            result = run_command("brew install stockfish", check=False)
            if result and result.returncode == 0:
                print("✓ Stockfish installed via Homebrew")
                return True
    
    print("✗ Could not install Stockfish automatically")
    print("Please install Stockfish manually using one of these commands:")
    print("  Ubuntu/Debian: sudo apt-get install stockfish")
    print("  Red Hat/CentOS: sudo yum install stockfish")
    print("  Fedora: sudo dnf install stockfish")
    print("  macOS: brew install stockfish")
    print("Then run this setup script again.")
    return False


def detect_stockfish_path():
    """Detect the path to the Stockfish binary."""
    print("Detecting Stockfish path...")
    
    # First try using 'which' command
    result = run_command("which stockfish", check=False)
    if result and result.returncode == 0 and result.stdout.strip():
        path = result.stdout.strip()
        print(f"✓ Found Stockfish at: {path}")
        return path
    
    # Try common installation paths
    common_paths = [
        "/usr/bin/stockfish",
        "/usr/local/bin/stockfish",
        "/opt/homebrew/bin/stockfish",  # macOS Homebrew
        "/home/linuxbrew/.linuxbrew/bin/stockfish",  # Linux Homebrew
        "/usr/games/stockfish",  # Some Debian/Ubuntu installations
    ]
    
    for path in common_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            print(f"✓ Found Stockfish at: {path}")
            return path
    
    print("✗ Could not detect Stockfish path")
    return None


def update_chess_script(stockfish_path):
    """Update chess_e1_vs_e2.py with the detected Stockfish path."""
    script_path = Path("chess_e1_vs_e2.py")
    
    if not script_path.exists():
        print("✗ chess_e1_vs_e2.py not found")
        return False
    
    print("Updating chess_e1_vs_e2.py with Stockfish path...")
    
    # Read the current file
    with open(script_path, 'r') as f:
        content = f.read()
    
    # Find and replace the Stockfish path line
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith("sf") and "=" in line:
            # Replace the hardcoded path with the detected one
            lines[i] = f"sf    = '{stockfish_path}'"
            print(f"✓ Updated Stockfish path to: {stockfish_path}")
            break
    else:
        print("✗ Could not find Stockfish path line in chess_e1_vs_e2.py")
        return False
    
    # Write the updated content back
    with open(script_path, 'w') as f:
        f.write('\n'.join(lines))
    
    return True


def main():
    """Main setup function."""
    print("=" * 50)
    print("Chess Engine Battle Program Setup")
    print("=" * 50)
    
    success = True
    
    # Install Python dependencies
    if not install_python_dependencies():
        success = False
    
    # Install Stockfish
    if not install_stockfish():
        success = False
    
    # Detect Stockfish path
    stockfish_path = detect_stockfish_path()
    if not stockfish_path:
        success = False
    
    # Update the chess script
    if stockfish_path and not update_chess_script(stockfish_path):
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✓ Setup completed successfully!")
        print("\nYou can now run the chess program with:")
        print("python3 chess_e1_vs_e2.py")
    else:
        print("✗ Setup completed with errors")
        print("Please check the error messages above and resolve them manually")
    print("=" * 50)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())