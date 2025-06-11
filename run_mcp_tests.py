import subprocess
import sys
import argparse

def run_tests_on_mcp(test_path=None, device_id=None, markers=None):
    """
    Run tests on MCP device farm
    
    Args:
        test_path: Path to specific test file or directory
        device_id: MCP device serial ID
        markers: pytest markers to filter tests
    """
    cmd = ["pytest", "-v"]
    
    # Add MCP flag
    cmd.append("--mcp")
    
    # Add device ID if specified
    if device_id:
        cmd.extend(["--device-id", device_id])
    
    # Add test markers if specified
    if markers:
        cmd.extend(["-m", markers])
    
    # Add test path if specified, otherwise run all tests
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append("tests/")
    
    # Run the tests
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with exit code {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tests on MCP device farm")
    parser.add_argument("--test-path", help="Path to specific test file or directory")
    parser.add_argument("--device-id", help="MCP device serial ID")
    parser.add_argument("--markers", help="pytest markers to filter tests")
    
    args = parser.parse_args()
    run_tests_on_mcp(args.test_path, args.device_id, args.markers) 