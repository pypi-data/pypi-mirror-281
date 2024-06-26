import os
import sys
import subprocess
import click

@click.command()
@click.option('--zip', 'zip_file', required=False, help='Specify the zip file to test.')
@click.option('--pass', 'password_list', required=False, help='Specify the file containing the list of passwords.')
@click.option('--unzip', is_flag=True, help='Automatically extract the zip file after finding the correct password.')
@click.option('--save', 'save_file', help='Save the found password to the specified file.')
@click.option('--silent', is_flag=True, help='Suppress output of password attempts, only display the found password.')
@click.option('--version', is_flag=True, help='Display version information and exit.')
@click.option('--help', 'help_flag', is_flag=True, help='Display help message and exit.')
def cli(zip_file, password_list, unzip, save_file, silent, version, help_flag):
    if not sys.platform.startswith('linux'):
        print("This tool only works on Linux.")
        sys.exit(1)

    script_path = os.path.join(os.path.dirname(__file__), 'ziplip.sh')

    command = ['bash', script_path]
    
    if zip_file:
        command.extend(['--zip', zip_file])
    if password_list:
        command.extend(['--pass', password_list])
    if unzip:
        command.append('--unzip')
    if save_file:
        command.extend(['--save', save_file])
    if silent:
        command.append('--silent')
    if version:
        command.append('--version')
    if help_flag:
        command.append('--help')

    subprocess.run(command)

if __name__ == "__main__":
    cli()
