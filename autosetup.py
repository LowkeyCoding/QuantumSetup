import os
import requests
import subprocess
from colorama import Fore, Back, Style, just_fix_windows_console as colorama_init
import readchar
import sys
import argparse

colorama_init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def printr(text):
    print(text + Style.RESET_ALL)

def print_green(text):
    printr(Fore.GREEN + text)

def print_yellow(text):
    printr(Fore.YELLOW + text)

def print_red(text):
    printr(Fore.RED + text)

def is_posix_os():
    return os.name == 'posix'

def is_wayland():
    return os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland"

def get_project_name():
    return input("Enter your project name: ")

def fetch_backend_examples():
    try:
        url = "https://raw.githubusercontent.com/LowkeyCoding/QuantumSetup/refs/heads/master/examples.csv"
        response = requests.get(url)
        if response.status_code == 200:
            return list(map(str.strip, response.text.split(",")))
        return []
    except Exception as e:
        return None

def build_menu_structure():
    menu = []
    backends = ['AER', 'IBM', 'Azure', 'Braket']
    examples = fetch_backend_examples() or []
    for backend in backends:
        backend_entry = {
            'name': backend,
            'expanded': False,
            'children': [],
            'selected': False
        }
        for ex in examples:
            backend_entry['children'].append({
                'name': ex,
                'selected': False,
            })
        menu.append(backend_entry)
    return menu

def display_menu(menu, level=0, parent_indices=None):
    parent_indices = parent_indices or []
    for idx, item in enumerate(menu):
        current_indices = parent_indices + [idx + 1]
        prefix = "  " * level
        checkbox = "[X]" if item['selected'] else "[ ]"
        
        if item.get('children'):
            symbol = "▼" if item['expanded'] else "▶"
            line = f"{prefix}{'.'.join(map(str, current_indices))}. {symbol} {item['name']} {checkbox}"
            printr(line)
            if item['expanded']:
                display_menu(item['children'], level + 1, current_indices)
        else:
            line = f"{prefix}{'.'.join(map(str, current_indices))}.   {item['name']} {checkbox}"
            printr(line)

def get_node_by_indices(menu, indices):
    current_level = menu
    for i in indices[:-1]:
        current_node = current_level[i-1]
        current_level = current_node.get('children', [])
    return current_level[indices[-1]-1] if indices else None

class MenuNavigator:
    def __init__(self, menu, notebook):
        self.menu = menu
        self.path = []
        self.current_level = menu
        self.selected_idx = 0
        self.running = True
        self.max_width = 79  # Maximum width for menu items
        self.notebook = notebook

    def display(self):
        clear_screen()
        menu_string = "Navigate: ↑/↓  | Expand: → | Collapse: ← | Select: Space | Confirm: Enter | Exit: q"
        printr(Fore.YELLOW + menu_string)
        printr(Fore.YELLOW + "-"*len(menu_string))
        self._display_level(self.current_level, 0)
        
    def _display_level(self, items, level):
        for idx, item in enumerate(items):
            # Build prefix and symbols
            prefix = "  " * level
            checkbox = "[X]" if item['selected'] else "[ ]"
            symbol = ""
            
            if item.get('children'):
                symbol = "▼ " if item['expanded'] else "▶ "
            
            # Create left-aligned text part
            text_line = f"{prefix}{symbol}{item['name']}"
            
            # Calculate padding for checkbox alignment
            padding = self.max_width - len(text_line.expandtabs())
            if padding < 0:
                padding = 0
                
            # Full line with aligned checkbox
            full_line = f"{text_line}{' ' * padding} {checkbox}"
            
            # Highlight selected item
            if idx == self.selected_idx:
                printr(Back.WHITE + Fore.BLACK + full_line)
            else:
                printr(full_line)


    def handle_input(self):
        key = readchar.readkey()
        if key == readchar.key.UP:
            self.selected_idx = max(0, self.selected_idx - 1)
        elif key == readchar.key.DOWN:
            self.selected_idx = min(len(self.current_level)-1, self.selected_idx + 1)
        elif key == readchar.key.RIGHT:
            self.expand_item()
        elif key == readchar.key.LEFT:
            self.collapse_item()
        elif key == ' ':
            self.toggle_selection()
        elif key == readchar.key.ENTER:
            if not self.path:
                self.running = False
        elif key.lower() == 'q':
            clear_screen()
            sys.exit()

    def expand_item(self):
        item = self.current_level[self.selected_idx]
        if item.get('children'):
            item['expanded'] = True
            self.path.append((self.current_level, self.selected_idx))
            self.current_level = item['children']
            self.selected_idx = 0

    def collapse_item(self):
        if self.path:
            self.current_level, self.selected_idx = self.path.pop()
            self.current_level[self.selected_idx]['expanded'] = False

    def toggle_selection(self):
        item = self.current_level[self.selected_idx]
        if not item.get('children'):
            item['selected'] = not item['selected']
        else:
            new_state = not item['selected']
            item['selected'] = new_state
            for child in item['children']:
                child['selected'] = new_state

    def run(self):
        while self.running:
            self.display()
            self.handle_input()
        return self.get_selected()

    def get_selected(self):
        selected = []
        ext = ".ipynb" if self.notebook else ".py" 
        for backend in self.menu:
            for child in backend['children']:
                if child['selected']:
                    selected.append({
                        "backend": backend['name'],
                        "name": child['name'] + ext
                    })
        return selected


def hierarchical_menu(notebook):
    menu = build_menu_structure()
    navigator = MenuNavigator(menu, notebook)
    return navigator.run()

def create_project_directory(project_name):
    if not os.path.exists(project_name):
        os.makedirs(project_name)
    return project_name

def create_dotenv(project_dir):
    with open(os.path.join(project_dir, '.env'), 'w') as f:
        f.write("""
ibm_token=YOUR_IBM_TOKEN
ibm_crn=YOUR_IBM_CRN
azure_connection=YOUR_AZURE_CONNECTION_STRING
aws_access=YOUR_AWS_ACCESS_KEY
aws_secret=YOUR_AWS_SECRET_KEY
aws_region=YOUR_AWS_REGION
""".strip())

def download_pyproject(project_dir):
    url = "https://raw.githubusercontent.com/LowkeyCoding/QuantumSetup/refs/heads/master/pyproject.toml"
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(project_dir, 'pyproject.toml'), 'wb') as f:
            f.write(response.content)
        print("Downloaded pyproject.toml\n")
    else:
        print_red("Failed to download pyproject.toml\n")

def download_example(example, project_dir):
    url = f"https://raw.githubusercontent.com/LowkeyCoding/QuantumSetup/master/{example['backend'].lower()}/examples/{example['name']}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(project_dir, f"{example['backend'].lower()}_{example['name']}")
            with open(filename, 'wb') as f:
                f.write(response.content)
            print_green(f"  Downloaded {example['name']}")
        else:
            print_red(f"  Failed to download {example['name']}")
    except Exception as e:
        print_red(f"  Error downloading {example['name']}: {str(e)}")

def create_virtual_environment(project_dir):
    print("\nCreating virtual environment...")
    try:
        subprocess.run(["uv", "venv", "--directory", project_dir],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("Virtual environment created successfully.")
    except subprocess.CalledProcessError:
        print_red("Failed to create virtual environment.")

def guide_to_run_examples(examples, project_dir, notebook):
    print("\nTo activate the virtual environment:")
    print_green(f"  cd {os.path.join('./', project_dir)}")
    if is_posix_os():
        print_green(f"  source {os.path.join('.venv', 'bin', 'activate')}")
        if is_wayland():
            print_yellow("  When using Wayland: export QT_QPA_PLATFORM=xcb")
    else:
        print_green(f"  {os.path.join('.venv', 'Scripts', 'activate')}")
    if not notebook:
        print("\nRun examples with:")
        for ex in examples:
            print_green(f"  uv run {ex['backend'].lower()}_{ex['name']}.py")
    print("\nPress any key to exit...")
    input()

def main():
    parser = argparse.ArgumentParser(prog='qproject', usage='%(prog)s [options]', description='Qproject is a tool to crate a basic quantum development environment.')
    parser.add_argument('--notebook', action='store_true', help='Run in notebook mode')
    parser.add_argument('-n','--name', default="", help='Set the project name')
    args = parser.parse_args()
    clear_screen()
    print("Welcome to the Quantum Project Setup!")
    if args.notebook:
        print("Running in notebook mode\n")
    else:
        print("")
    project_name = "" 
    if args.name:
        project_name = args.name
    else:
        project_name = get_project_name()

    print("\x1b[?25l") # Hide cursor
    examples = hierarchical_menu(args.notebook)
    print("\x1b[?25h") # show cursor
    print("Creating project directory")
    project_dir = create_project_directory(project_name)
    print("Creating .env\n")
    create_dotenv(project_dir)
    print("Downloading pyproject.toml\n")
    download_pyproject(project_dir)
    print("Downloading Examples")
    for example in examples:
        download_example(example, project_dir)
    create_virtual_environment(project_dir)
    guide_to_run_examples(examples, project_dir, args.notebook)
    
if __name__ == "__main__":
    main()