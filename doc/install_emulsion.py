# INSTALLATION SCRIPT TO BE BUNDLED AS A SINGLE FILE USING pyinstaller
# Usage:
#    install_emulsion [VERSION [URL_SUFFIX]]
#        Install EMULSION for a specific platform. Default version is the one in the name of the script.
#        The URL_SUFFIX is an indication on where the documentation is located (e.g., 'devel' or '1.1')
#    instal_emulsion latest [URL_SUFFIX]
#        Install latest stable version available on pypi
#    python install_emulsion.py 1.2rc4 --build
#        Build the installation script from install_emulsion.py, for a specific version and for the
#        platform where it is run.

import os
import argparse
import subprocess
import platform
import yaml
from   pathlib    import Path
from   colorama   import Fore, Style

PYTHON_VERSION = '3.11'
DEFAULT_EMULSION_VERSION = '1.2rc4'
LATEST_URL = 'https://sourcesup.renater.fr/www/emulsion-public/'
HOME=Path.home()
OS_NAME = platform.system()
SCRIPT_NAME = Path(__file__)
ARCH = platform.uname().machine
ALIAS = 'MacOS' if OS_NAME == 'Darwin' else OS_NAME
MACHINE = f"{ALIAS}-{ARCH}"
SUFFIX = 'exe' if OS_NAME == 'Windows' else 'sh'
WGET = ['curl', '-O'] if OS_NAME == 'Darwin' else ['wget']
WGET_OUT = '--output-dir' if OS_NAME == 'Darwin' else '-P'

def subprocess_run(args):
    print(Style.BRIGHT, *args, Style.RESET_ALL)

def is_conda_installed(options):
    try:
        # execute command 'conda --version'
        result = subprocess.run(['conda', '--version'], **options)
        output = result.stdout.strip()  # retrieves command output as a string
        if 'conda' in output:
            return True  # Conda installed
    except FileNotFoundError:
        pass  # command 'conda' not found (Conda not installed) or not reachable (PATH issue?)
    return False  # Conda not available

def get_emulsion_version(conda_env, options):
    try:
        result = subprocess.run(['conda', 'run', '-n', conda_env, 'python', '-m', 'emulsion', '--version'], **options)
        return result.stdout.strip()
    except FileNotFoundError:
        pass
    return None

def is_graphviz_installed(options):
    try:
        # execute command 'dot -V'
        result = subprocess.run(['dot', '-V'], **options)
        output = result.stdout.strip()  # retrieves command output as a string
        if 'dot' in output:
            return True  # dot installed
    except FileNotFoundError:
        pass  # command 'dot' not found (graphviz not installed) or not reachable (PATH issue?)
    return False  # dot not available

def get_conda_env_list(options):
    result = subprocess.run(['conda', 'env', 'list'], **options)
    output = result.stdout.strip()
    env_lines = output.split('\n')[2:]  # Ignore the first two lines of output

    env_list = []
    for line in env_lines:
        parts = line.split()
        env_name = parts[0].strip()
        env_list.append((env_name))

    return env_list

def ask_for_existing_env(envlist):
    values = ', '.join(envlist)
    response = ''
    while response not in envlist:
        response = input('Choose an existing environment for EMULSION installation ({values}): ')
    return response

def ask_for_new_env(envlist):
    response = envlist[0]
    while response in envlist:
        response = input('Choose a new name for the EMULSION installation environment: ')
    return response

def main(emulsion_version):
    subprocess_options = dict(capture_output=True, text=True)
    if OS_NAME == 'Windows':
        subprocess_options['shell'] = True
        # subprocess_options['executable'] = 'powershell.exe'
    else:
        # subprocess_options['executable'] = '/bin/bash'
        pass

    print(Style.BRIGHT + Fore.GREEN, '\n')
    print('-' * 42)
    print(f'Starting installation of EMULSION ({emulsion_version})')
    print('-' * 42, Style.RESET_ALL + Fore.RESET)

    new_conda_install = False
    print(Fore.YELLOW, 'Searching for Miniconda/Anaconda', Fore.RESET, end='... ')
    if is_conda_installed(subprocess_options):
        print(Fore.GREEN, 'INSTALLED', Fore.RESET)
    else:
        # Install Miniconda
        print(Fore.YELLOW, 'NOT FOUND', Fore.RESET)
        miniconda = f'Miniconda3-latest-{MACHINE}.{SUFFIX}'
        URL = f'https://repo.anaconda.com/miniconda/{miniconda}'

        download = True
        if Path(miniconda).exists():
            print(Fore.YELLOW, '\nMiniconda installer found in current directory', Fore.RESET)
            if input('Download new version ? (y/[N])') not in ('y', 'Y'):
                download = False

        if download:
            print(Fore.YELLOW, f'\nDownloading {URL}', Fore.RESET)
            subprocess.run(WGET + [URL])
            print(Fore.GREEN, 'DONE', Fore.RESET)

        print(Fore.YELLOW, f'\nInstalling {miniconda}', Fore.RESET)
        command = [] if OS_NAME == 'Windows' else ['bash']
        if OS_NAME == 'Windows':
            args = ['/InstallationType=JustMe', '/RegisterPython=0', '/S', '/AddToPath=1', f'/D={HOME}\\miniconda3']
        else:
            args = ['-p', f'{HOME}/miniconda3', '-b', '-f']
        subprocess.run(command + [miniconda] + args)

        # add conda to Path
        conda_path = HOME.joinpath('miniconda3', 'condabin')
        old_path = os.environ['PATH']
        path_sep = ';' if OS_NAME == 'Windows' else ':'
        os.environ['PATH'] = f'{conda_path}{path_sep}{old_path}'
        print(Fore.GREEN, '\nDONE', Fore.RESET)
        new_conda_install = True


    print(Fore.YELLOW, '\nInitializing conda...', Fore.RESET)
    shells = ['powershell'] if OS_NAME == 'Windows' else ['bash', 'zsh']
    for shell in shells:
        subprocess.run(['conda', 'init', shell])
    print(Fore.GREEN, '\nDONE', Fore.RESET)

    # Create or use a virtual environment
    conda_envs = get_conda_env_list(subprocess_options)
    env_name = conda_envs[0]
    create_env = True

    # if conda has just been installed, propose to use "base" environment rather than "emulsion<VERSION>"
    if new_conda_install and input(f'Do you want to install EMULSION in default conda environment ("{env_name}")? ([Y]/n): ') not in ('n', 'N'):
        create_env = False
    else:
        env_name = f'emulsion-{emulsion_version}'
        print(Fore.YELLOW, f'\nCurrent available conda environments:', Fore.RESET)
        print('\n'.join(conda_envs))

        # default env already exists
        if env_name in conda_envs:
            if input(f'\nDo you want to install EMULSION in existing environment "{env_name}"? ([Y]/n): ') not in ('n', 'N'):
                # use existing env
                create_env = False
            else:
                if len(conda_envs) > 1 and input('\nDo you want to install EMULSION in an existing conda environment? (y/[N]): ') in ('y', 'Y'):
                    # choose existing one
                    create_env = False
                    env_name = ask_for_existing_env(conda_envs)
                else:
                    # choose new name
                    env_name = ask_for_new_env(conda_envs)
        elif input('\nDo you want to install EMULSION in an existing conda environment? (y/[N]): ') in ('y', 'Y'):
            # choose existing env
            create_env = False
            env_name = ask_for_existing_env(conda_envs)

    if create_env:
        print(Fore.YELLOW, f'\nCreating new conda environment "{env_name}"', Fore.RESET)
        subprocess.run(['conda', 'create', '-y', '-n', env_name, f'python={PYTHON_VERSION}'])
        print(Style.BRIGHT, Fore.GREEN, 'DONE', Fore.RESET, Style.RESET_ALL)

    # Activate environment and install EMULSION
    print(Fore.YELLOW, f'\nActivating conda environment "{env_name}" and installing EMULSION {emulsion_version}', Fore.RESET)
    conda_prefix = f'conda run -n {env_name} '
    specific_version = '' if emulsion_version == 'latest' else f'=={emulsion_version}'
    pip_cmd = f'python -m pip install -U emulsion{specific_version}'
    subprocess.run(conda_prefix + pip_cmd, shell=True)
    print(Fore.GREEN, 'DONE', Fore.RESET)

    # print(Fore.YELLOW, f'\nInitializing EMULSION {emulsion_version}', Fore.RESET)
    # subprocess.run(conda_prefix + 'init_emulsion', shell=True)
    # print(Fore.GREEN, 'DONE', Fore.RESET)

    # Write info into .emulsionrc
    # retrieve $HOME and path to EMULSION repository
    print(Fore.YELLOW, 'Installing completion scripts', Fore.RESET)
    emulsion_rc = Path.home().join('.emulsionrc')
    emulsion_rc.mkdir(parents=True, exist_ok=True)
    compl_scripts = ['emulsion_powershell_completion.ps1'] if OS_NAME == 'Windows' else ['emulsion_bash_completion.sh', 'emulsion_zsh_completion.sh']
    for script in compl_scripts:
        subprocess.run(WGET + [WGET_OUT, str(emulsion_rc), f'{LATEST_URL}/{script}'])
    activate_dir = HOME.joinpath('miniconda3', 'envs', env_name, 'etc', 'conda', 'activate.d')
    activate_dir.mkdir(parents=True, exist_ok=True)
    init_script = activate_dir.joinpath('init_completion.bat' if OS_NAME == 'Windows' else 'init_completion.sh')
    subprocess.run(WGET + [WGET_OUT, str(activate_dir), f'{init_script}'])
    # make file executable
    os.chmod(init_script, 0o755)
    if emulsion_version == 'latest':
        emulsion_version = get_emulsion_version(env_name, subprocess_options)
    if emulsion_version is not None:
        print(Fore.GREEN, f'SUCCESSFULLY INSTALLED EMULSION version {emulsion_version}', Fore.RESET)
    else:
        print(Style.BRIGHT + Fore.RED, 'Warning: could not retrieve EMULSION version, check installation', Fore.RESET + Style.RESET_ALL)

    # update info on conda environment
    env_file = Path(emulsion_rc, 'environments.yaml')
    print(Fore.YELLOW, f'\nUpdating info on environment in file {env_file}', Fore.RESET)
    if env_file.exists():
        with open(env_file ,'r') as file:
            yaml_info = yaml.safe_load(file)
    else:
        yaml_info = {}
    yaml_info[env_name] = emulsion_version
    with open(env_file, 'w') as file:
        yaml.safe_dump(yaml_info, file)
    print(Fore.GREEN, 'DONE', Fore.RESET)

    print(Fore.YELLOW, '\nSearching for Graphviz', Fore.RESET, end='... ')
    if is_graphviz_installed(subprocess_options):
        print(Fore.GREEN, 'INSTALLED', Fore.RESET)
    else:
        # Install graphviz
        print(Fore.YELLOW, 'NOT FOUND', Fore.RESET)
        # Install conda package python-graphviz (executables e.g. dot command)
        print(Fore.YELLOW, "\nInstalling graphviz (conda package python-graphviz)", Fore.RESET)
        graphviz_installed = False
        try:
            subprocess.run(['conda', 'install', '-n', env_name, '-y', '-c', 'conda-forge', 'python-graphviz'], check=True)
            try:
                subprocess.run(['dot', '-c'], check=True)
                graphviz_installed = True
            except subprocess.CalledProcessError:
                print(Fore.RED, "An error occurred while trying to initialize graphviz ('dot -c' failed).\n", Fore.RESET)
        except subprocess.CalledProcessError:
            print(Fore.RED, "An error occurred while trying to install package python-graphviz via conda.\n", Fore.RESET)
        if not graphviz_installed:
            print(Fore.YELLOW, """Graphviz could not be installed automatically. 
            To get model diagrams, please consider manual installation on your system.
            \tSee https://graphviz.org/""", Fore.RESET)
        else:
            print(Fore.GREEN, 'DONE', Fore.RESET)


    if input('\nDo you want to download model examples and run a test? (y/[N]): ') in ('y', 'Y'):
        print(Fore.YELLOW, f'\nDownloading and extracting models.zip for EMULSION {emulsion_version}', Fore.RESET)
        subprocess.run(WGET + [f'{LATEST_URL}/models.zip'])
        subprocess.run(['unzip', '-o', '-q', 'models.zip'])
        print(Fore.GREEN, 'DONE', Fore.RESET)

        test_cmd = 'emulsion run --plot models/quickstart/quickstart.yaml -r 20 --silent --view-model'
        print(Fore.YELLOW, f'\nPlease wait, running following test:\n\t{test_cmd}', Fore.RESET)
        subprocess.run(conda_prefix + test_cmd, shell=True)
        print(Fore.GREEN, 'DONE', Fore.RESET)

    print(Style.BRIGHT + Fore.GREEN, '\n')
    print('-' * 42)
    print('EMULSION is now fully installed')
    print('-' * 42, Style.RESET_ALL)
    print(f'\tMore info: {LATEST_URL}', Fore.RESET)

    ### TO BE CONTINUED TO INSTALL STAND-ALONE EDITOR
    ### ...


def build(emulsion_version):
    suffix = '' if OS_NAME == 'Darwin' else f'.{SUFFIX}'
    additional_options = []
    if OS_NAME == 'Windows':
        additional_options.append('--uac-admin')
    if OS_NAME == 'Darwin':
        additional_options += ['--target-architecture', ARCH]
    exec_name = f'install_emulsion-{emulsion_version}-{MACHINE}{suffix}'
    print(Fore.YELLOW, f'Building {exec_name}...', Fore.RESET)
    distpath = SCRIPT_NAME.parent.joinpath('dist')
    try:
        subprocess.run(['pyinstaller'] + additional_options + ['-n', exec_name, '--onefile', '--clean', SCRIPT_NAME], check=True, shell=(OS_NAME == 'Windows'))
    except subprocess.CalledProcessError:
        print(Style.BRIGHT + Fore.RED, 'Build process failed. Try manually instead', Style.RESET_ALL + Fore.RESET)
    print(Fore.GREEN, f'Success. Installation script available: dist/{exec_name}', Fore.RESET)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script for EMULSION installation (or to build installer)')
    parser.add_argument('version', nargs='?', default=DEFAULT_EMULSION_VERSION, help=f'Version number (default: {DEFAULT_EMULSION_VERSION})')
    parser.add_argument('url_suffix', nargs='?', default=None, help=f'Subdirs for default URL (default: None)')
    parser.add_argument('--build', action='store_true', help='Build platform-specific install script from generic python script')
    args = parser.parse_args()
    version = args.version
    if args.url_suffix is not None:
        LATEST_URL += f'/{args.url_suffix}'
    if args.build:
        if SCRIPT_NAME.name == 'install_emulsion.py':
            build(version)
        else:
            print(Style.BRIGHT + Fore.RED, f'Option --build can be used only with script "install_emulsion.py" (not with "{SCRIPT_NAME.name}")', Style.RESET_ALL + Fore.RESET)
    else:
        main(version)