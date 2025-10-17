#!/usr/bin/env python3
# Author: Juan Medina
# Email: jumedina@redhat.com

import subprocess
import sys
import re

def print_help():
    """Prints usage instructions for the script."""
    print("Jinja2 Expression Tester (JEX)")
    print("-" * 30)
    print("Usage: jex \"{{ YOUR_JINJA_EXPRESSION }}\" [options]")
    print("\nDescription:")
    print("Executes a Jinja2 expression using Ansible's templating engine (ansible localhost -m debug).")
    print("This is ideal for testing filters, lookups, and variable logic.")
    print("\nArguments:")
    print("  The expression must be enclosed in double quotes.")
    print("\nExamples:")
    print("  jex \"{{ [ 2, 4, 6, 8, 10 ] | reverse }}\"")
    print("  jex \"{{ lookup('env', 'USER') }}\"")
    print("  jex \"{{ non_existent_var | default('Default Value', true) }}\"")
    print("  jex \"{{ 'TestString' | regex_replace('S.*g', 'Word') }}\"")
    sys.exit(0)

def handle_error(e):
    """Parses the Ansible error output and provides specific dependency solutions."""
    stderr_output = e.stderr.decode('utf-8')
    dependency_match = re.search(r"No module named '(\w+)'", stderr_output)
    passlib_match = re.search(r"Unable to encrypt nor hash, passlib must be installed", stderr_output)
    
    print("\n" + "="*50)
    print("EXECUTION FAILED: DEPENDENCY OR TEMPLATING ERROR")
    print("="*50)

    if dependency_match or passlib_match:
        if passlib_match:
            missing_package = 'passlib'
        else:
            missing_package = dependency_match.group(1)
        print(f"ERROR: The executed Ansible filter requires the Python library '{missing_package}'.")
        print("Ansible filters often rely on external Python packages not included in 'ansible-core'.")
        print("\nACTION REQUIRED: Install the missing package via pip.")
        print(f"  --> Suggested command: pip install {missing_package}")        
    else:
        print("A generic Ansible error occurred. Review the full output for details.")
        
    print("\n--- Full Error Trace ---")
    print(f"{stderr_output.strip()}")
    print("\n--- Recommended Dependencies for Ansible Filters ---")
    print("Install these to test most common filters (e.g., hashing, XML, YAML):")
    print("  pip install passlib jmespath xmltodict jmespath python-dateutil requests")
    sys.exit(1)

def main():
    """Main function to parse arguments and execute the Ansible command."""
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print_help()
    jinja_expression = sys.argv[1]
    extra_args = sys.argv[2:]
    ansible_cmd = [
        'ansible',
        'localhost',
        '-i', '/dev/null',
        '-m', 'debug',
        '-a', f'msg="{jinja_expression}"'
    ]
    ansible_cmd.extend(extra_args)
    print(f"--- Running command: {' '.join(ansible_cmd)}")
    try:
        process = subprocess.run(ansible_cmd, capture_output=True, check=True)
        sys.stdout.buffer.write(process.stdout)
    except subprocess.CalledProcessError as e:
        handle_error(e)
    except FileNotFoundError:
        print("\nError: 'ansible' command not found. Ensure Ansible is installed and in your PATH.")
        sys.exit(1)

if __name__ == "__main__":
    main()


