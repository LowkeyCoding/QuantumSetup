import os
import requests
import subprocess
from colorama import just_fix_windows_console, Fore, Style

just_fix_windows_console()

def green(string):
    return Fore.GREEN+string+Style.RESET_ALL

def yellow(string):
    return Fore.YELLOW+string+Style.RESET_ALL

def red(string):
    return Fore.RED+string+Style.RESET_ALL

def is_posix_os():
    # Check if the current OS is posix-like (Linux, macOS, etc.)
    return os.name == 'posix'

def is_wayland():
    return os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland"

def get_project_name():
    project_name = input("Enter your project name: ")
    return project_name

def select_examples():
    examples = {
        'AER': False,
        'IBM': False,
        'Azure': False,
        'Braket': False
    }

    for ex in examples:
        response = input(f"Do you want to include {ex}? (y/n): ").strip().lower()
        if response == 'y':
            examples[ex] = True
    
    return [ex for ex, included in examples.items() if included]

def create_project_directory(project_name):
    # Create project directory
    if not os.path.exists(project_name):
        os.makedirs(project_name)
    return project_name

def create_dotenv(project_dir):
    dotenv_content = """
ibm_token=YOUR_IBM_TOKEN
azure_connection=YOUR_AZURE_CONNECTION_STRING
aws_access=YOUR_AWS_ACCESS_KEY
aws_secret=YOUR_AWS_SECRET_KEY
aws_region=YOUR_AWS_REGION
    """
    
    with open(os.path.join(project_dir, '.env'), 'w') as f:
        f.write(dotenv_content.strip())

def download_pyproject(project_dir):
    url = "https://raw.githubusercontent.com/LowkeyCoding/QuantumSetup/refs/heads/master/pyproject.toml"
    response = requests.get(url)

    if response.status_code == 200:
        with open(os.path.join(project_dir, 'pyproject.toml'), 'wb') as f:
            f.write(response.content)
        print("Successfully downloaded pyproject.toml.")
    else:
        print(red("Failed to download pyproject.toml."))

def download_example(name, project_dir):
    # Convert exendency name to lowercase for the URL
    url = f"https://raw.githubusercontent.com/LowkeyCoding/QuantumSetup/master/{name.lower()}/sample.py"
    response = requests.get(url)

    if response.status_code == 200:
        with open(os.path.join(project_dir, f"{name.lower()}_sample.py"), 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded {name.lower()}_sample.py.")
    else:
        print(f"Failed to download sample for {name}.")

def create_virtual_environment(project_dir):
    print("\nCreating a virtual environment...")
    try:
        subprocess.run(["uv", "venv", "--directory", project_dir],
            check=True,
            stdout=subprocess.DEVNULL,  # Suppress standard output
            stderr=subprocess.DEVNULL   # Suppress standard error
        )
        print("Virtual environment created successfully.")
    except subprocess.CalledProcessError:
        print(red("Failed to create the virtual environment. Make sure 'uv' is installed and available."))

def guide_to_run_examples(examples, project_dir):

    # Highlight the environment activation command
    print("\nTo activate the virtual environment, run:")
    print(green(f"\tcd {os.path.join("./",project_dir)}"))
    if is_posix_os():
        print(green(f"\tsource {os.path.join('.venv', 'bin', 'activate')}"))
        if is_wayland():
            print(yellow("\tWhen using wayland you may need to run: export QT_QPA_PLATFORM=xcb"))
    else:
        print(green(f"\t{os.path.join('.venv', 'Scripts', 'activate')}\n"))
    print("\nThen to run the examples, use the following commands:")
    for ex in examples:
        sample_name = f"{ex.lower()}_sample.py"
        print(green(f"\tuv run {sample_name}"))

def create_project():
    print("Welcome to the Python Project Setup!")
    project_name = get_project_name()
    
    # Create project directory
    project_dir = create_project_directory(project_name)
    
    examples = select_examples()

    print(f"\nProject: {project_name}")
    print("Selected examples:")
    if examples:
        for ex in examples:
            print(f"- {ex}")
    else:
        print("No Examples selected.")
    
    # Create .env file with specific keys
    create_dotenv(project_dir)
    print("\nCreated .env")
    
    # Download the pyproject.toml file
    download_pyproject(project_dir)

    # Download sample.py for each selected exendency
    for ex in examples:
        download_example(ex, project_dir)

    # Create the virtual environment
    create_virtual_environment(project_dir)

    # Guide user on how to run examples
    guide_to_run_examples(examples, project_dir)

if __name__ == "__main__":
    create_project()
