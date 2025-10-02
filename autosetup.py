import os
import requests
import subprocess
from colorama import Fore, Back, Style, just_fix_windows_console as colorama_init
import readchar
import sys
import argparse

VERSION = "2"
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

def fetch_simulator_data():
    try:
        url = "https://raw.githubusercontent.com/LowkeyCoding/QuantumSetup/refs/heads/master/backend_data.txt"
        response = requests.get(url)
        data_res = {}
        if response.status_code == 200:
            for line in response.text.splitlines():
                sim_name, data = line.split(":")
                data = data.strip()
                if sim_name == "Version" and data != VERSION:
                    print(f"Version mismatch in example data: expected v{VERSION} got v{data}")
                    print("Go to https://github.com/LowkeyCoding/QuantumSetup and update qproject")
                    exit()
                if sim_name != "Version":
                    sim, name = sim_name.split("|")
                    if sim not in data_res:
                        data_res[sim] = {}
                        data_res[sim]["default"] = {}
                        data_res[sim]["notebook"] = {}
                    if name.startswith("IPYNB"):
                        data_res[sim]["notebook"][name[6:]] = list(map(str.strip, data.split(",")))
                    elif name !="Version":
                        data_res[sim]["default"][name] = list(map(str.strip, data.split(",")))
            return data_res
        return None
    except Exception as e:
        #print(e)
        return None

def build_menu_structure(nb_mode):
    sim_menu = []
    backend_menus = {}
    sim_data = fetch_simulator_data()
    ft = "default"
    if nb_mode:
        ft = "notebook"
    if sim_data == None:
        print_red("No examples or notebook examples where found.")
        print_red("Go to https://github.com/LowkeyCoding/QuantumSetup for more information.")
    for sim in sim_data:
        backend_menus[sim] = []

        for backend in sim_data[sim][ft]:
            backend_entry = {
                'name': backend,
                'expanded': False,
                'children': [],
                'selected': False
            }
            for example in sim_data[sim][ft][backend]:
                backend_entry['children'].append({
                    'name': example,
                    'selected': False,
                })
            backend_menus[sim].append(backend_entry)
        sim_entry = {
            "name": sim,
            "expanded": False,
            "children": [],
            "selected": False
        }
        sim_menu.append(sim_entry)
    return (sim_menu, backend_menus)


class MenuNavigator:
    def __init__(self, menu, allow_multiple=True):
        self.menu = menu
        self.path = []
        self.current_level = menu
        self.selected_idx = 0
        self.running = True
        self.max_width = 79  # Maximum width for menu items
        self.allow_multiple = allow_multiple

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
            children = item.get('children')
            checkbox = "[X]" if (item['selected'] and not children) else "[ ]"
            symbol = ""
            if children:
                symbol = "▶ "
                if all(c.get('selected') for c in children):
                    checkbox = "[X]"
                elif any(c.get('selected') for c in children):
                    checkbox = "[*]"

                
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
        if not self.allow_multiple:
            for idx,item in enumerate(self.current_level):
                if  idx != self.selected_idx:
                    item['selected'] = False

    def run(self):
        while self.running:
            self.display()
            self.handle_input()
        return self.get_selected()

    def get_selected(self, menu = []):
        menu = menu if menu != [] else self.menu
        for idx,item in enumerate(menu):
            if "children" in item.keys() and len(item["children"]) > 0:
                menu[idx]["children"] = self.get_selected(menu=item["children"])
        # Backends themselves are not selected when only a child is selected
        selected = filter(lambda x : x["selected"] or ("children" in x.keys() and len(x["children"]) > 0), menu)
        return list(selected)

def hierarchical_menu(args):
    sim_menu,backend_menus = build_menu_structure(args.notebook)
    simulator = ""
    backends = []
    if args.simulator:
        simulator = args.simulator
    else:
        simulator_navigator = MenuNavigator(sim_menu, allow_multiple=False)
        simulator = simulator_navigator.run()
        if len(simulator):
            simulator = simulator[0]["name"]
        else:
            print_red("You have to select a simulator") 
            exit()
    if not args.no_examples:
        backend_navigator = MenuNavigator(backend_menus[simulator])
        backends = backend_navigator.run()
    return (simulator, backends)

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

def download_pyproject(project_dir, simulator):
    url = ""
    if simulator != "Qiskit":
        url = f"https://raw.githubusercontent.com/LowkeyCoding/QuantumSetup/refs/heads/master/{simulator.lower()}/pyproject.toml"
    else:
        url = "https://raw.githubusercontent.com/LowkeyCoding/QuantumSetup/refs/heads/master/pyproject.toml"
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(project_dir, 'pyproject.toml'), 'wb') as f:
            f.write(response.content)
        print("Downloaded pyproject.toml\n")
    else:
        print_red("Failed to download pyproject.toml\n")

def download_readme(simulator, project_dir):
    if simulator != "Qiskit":
        url = f"https://raw.githubusercontent.com/LowkeyCoding/QuantumSetup/master/{simulator.lower()}/README.md"
    else:
        url = f"https://raw.githubusercontent.com/LowkeyCoding/QuantumSetup/master/Q_README.md"
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(project_dir, 'README.md'), 'wb') as f:
            f.write(response.content)
        print("Downloaded README.md\n")
    else:
        print_red("Failed to download README.md\n")

def download_example(example,backend, simulator, project_dir, nb):
    url = ""
    ext = ".ipynb" if nb else ".py"

    if simulator != "Qiskit":
        url = f"https://raw.githubusercontent.com/LowkeyCoding/QuantumSetup/master/{simulator.lower()}/{backend.lower()}/{example['name']}"
    else:
        url = f"https://raw.githubusercontent.com/LowkeyCoding/QuantumSetup/master/{backend.lower()}/examples/{example['name']}"
    url += ext
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(project_dir, f"{backend.lower()}_{example['name']}{ext}")
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

def guide_to_run_examples(examples, simulator, project_dir, notebook):
    ext = ".ipynb" if notebook else ".py"
    print("\nTo activate the virtual environment:")
    print_green(f"  cd {os.path.join('./', project_dir)}")
    if is_posix_os():
        print_green(f"  source {os.path.join('.venv', 'bin', 'activate')}")
        if is_wayland():
            print_yellow("  When using Wayland: export QT_QPA_PLATFORM=xcb")
    else:
        print_green(f"  {os.path.join('.venv', 'Scripts', 'activate')}")
    if simulator == "Pennylane":
        print("\nWhen using Pennylane there are 4 options for backend cpu, gpu, tensor or qiskit")
        print("To chose use --extra followed by the backend you want to use")
    if not notebook:
        print("\nRun examples with:")
        for backend in examples:
            for example in backend["children"]:
                file = f"{backend["name"].lower()}_{example['name']}{ext}"
                if simulator == "Qiskit":
                    print_green(f"  uv run {file}")
                elif simulator == "Pennylane":
                    if backend["name"] == "IBM":
                        print_green(f"  uv run --extra qiskit {file}")
                    else:
                        print_green(f"  uv run --extra cpu {file}")
                else:
                    print_yellow(f"No instructions for {simulator} how did we get here?")
    print("\nPress any key to exit...")
    input()

def main():
    parser = argparse.ArgumentParser(prog='qproject', usage='%(prog)s [options]', description='Qproject is a tool to crate a basic quantum development environment.')
    parser.add_argument('--notebook', action='store_true', help='Run in notebook mode')
    parser.add_argument('-n','--name', default="", help='Set the project name')
    parser.add_argument('-s', '--simulator', choices=['Pennylane', 'Qiskit'], help='Set the simulator: ')
    parser.add_argument('-x','--no-examples', action='store_true', help='Removes the examples prompt')
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
    simulator, examples = hierarchical_menu(args)
    print("\x1b[?25h") # show cursor
    print("Creating project directory")
    project_dir = create_project_directory(project_name)
    print("Creating .env\n")
    create_dotenv(project_dir)
    print("Downloading pyproject.toml\n")
    download_pyproject(project_dir, simulator)
    print("Downloading README.md\n")
    download_readme(simulator, project_dir)
    print("Downloading Examples")
    for backend in examples:
        for example in backend["children"]:
            download_example(example, backend["name"],simulator, project_dir, args.notebook)
    create_virtual_environment(project_dir)
    guide_to_run_examples(examples, simulator, project_dir, args.notebook)
    
if __name__ == "__main__":
    main()