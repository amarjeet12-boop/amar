
import argparse
import subprocess
import sys
from pathlib import Path

def scan_with_safety(requirements_file=None):
    """
    Run Safety to scan for vulnerabilities.
    
    Args:
        requirements_file (str, optional): Path to requirements.txt file.
    
    Returns:
        bool: True if scan completes successfully, False otherwise.
    """
    try:
        cmd = ['safety', 'check']
        if requirements_file:
            cmd.extend(['--file', requirements_file])
        
        # Run the safety command
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if result.stdout:
            print("Vulnerabilities found:")
            print(result.stdout)
            return False  # Vulnerabilities detected
        else:
            print("No known vulnerabilities found in the scanned packages.")
            return True  # Clean scan
        
    except subprocess.CalledProcessError as e:
        print(f"Error running Safety: {e}")
        if e.stderr:
            print(e.stderr)
        return False
    except FileNotFoundError:
        print("Error: 'safety' command not found. Install it with: pip install safety")
        return False

def main():
    parser = argparse.ArgumentParser(description="Scan Python dependencies for vulnerabilities.")
    parser.add_argument('--file', type=str, help="Path to requirements.txt file (optional; scans installed packages by default)")
    args = parser.parse_args()
    
    requirements_file = args.file if args.file else None
    if requirements_file and not Path(requirements_file).exists():
        print(f"Error: File '{requirements_file}' not found.")
        sys.exit(1)
    
    print("Starting vulnerability scan...")
    has_vulns = scan_with_safety(requirements_file)
    
    if has_vulns:
        print("\nScan complete: No critical issues found. Keep your dependencies updated!")
    else:
        print("\nScan complete: Review and update vulnerable packages immediately.")
        sys.exit(1)  # Exit with error code if vulnerabilities are found

if __name__ == "__main__":
    main()
