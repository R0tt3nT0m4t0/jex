#!/usr/bin/env python3
# Author: Juan Medina
# Email: jumedina@redhat.com

import subprocess
import sys

def print_help():
    """Prints usage instructions for the script."""
    print("Jinja2 Expression Tester (JEX)")
    print("-" * 30)
    print("Usage: jex.py \"{{ YOUR_JINJA_EXPRESSION }}\" [options]")
    print("\nDescription:")
    print("Executes a Jinja2 expression using Ansible's templating engine (ansible localhost -m debug).")
    print("This is ideal for testing filters, lookups, and variable logic.")
    print("\nArguments:")
    print("  The expression must be enclosed in double quotes.")
    print("\nExamples:")
    print("  jex.py \"{{ [ 2, 4, 6, 8, 10 ] | reverse }}\"")
    print("  jex.py \"{{ lookup('env', 'USER') }}\"")
    print("  jex.py \"{{ non_existent_var | default('Default Value', true) }}\"")
    print("  jex.py \"{{ 'TestString' | regex_replace('S.*g', 'Word') }}\"")
    sys.exit(0)

def main():
    """Main function to parse arguments and execute the Ansible command."""
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print_help()

    # The Jinja expression is the first argument
    jinja_expression = sys.argv[1]

    # Optional extra arguments to pass to ansible (e.g., -e for variables)
    extra_args = sys.argv[2:]

    # Construct the base Ansible command
    # We use 'msg' and wrap the argument in double quotes for safety
    ansible_cmd = [
        'ansible',
        'localhost',
        '-i', '/dev/null',
        '-m', 'debug',
        '-a', f'msg="{jinja_expression}"'
    ]

    # Add any extra arguments passed after the expression
    ansible_cmd.extend(extra_args)

    print(f"--- Running command: {' '.join(ansible_cmd)}")

    try:
        # Execute the command and stream output
        process = subprocess.run(ansible_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nError executing Ansible command: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\nError: 'ansible' command not found. Ensure Ansible is installed and in your PATH.")
        sys.exit(1)

if __name__ == "__main__":
    main()
  
