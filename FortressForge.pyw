import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import os
import subprocess
import webbrowser
import json

# Function to run the server
def run_server():
    server_exe = entry_exe.get()
    host_name = entry_name.get()
    map_name = entry_map.get()
    max_players = entry_max_players.get()
    port = entry_port.get()
    password = entry_password.get()
    token = entry_token.get()
    rcon_password = entry_rcon_password.get()
    command_line_options = entry_options.get()

    if not os.path.isfile(server_exe):
        messagebox.showerror("File Not Found", f"The file '{server_exe}' does not exist.")
        return

    command = f'"{server_exe}" -game tf -console -secure -port {port} +maxplayers {max_players} +map {map_name} +hostname "{host_name}"'
    if password:
        command += f" +sv_password \"{password}\""
    if token:
        command += f" +sv_setsteamaccount \"{token}\""
    if command_line_options:
        command += f" {command_line_options}"
    if rcon_password:
        command += f" +rcon_password \"{rcon_password}\""

    subprocess.run(command, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

# Function to browse for the executable
def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
    if filename:
        entry_exe.delete(0, tk.END)
        entry_exe.insert(0, filename)
    check_mandatory_fields()

# Function to save the configuration
def save_configuration():
    config = {
        "server_exe": entry_exe.get(),
        "host_name": entry_name.get(),
        "map_name": entry_map.get(),
        "max_players": entry_max_players.get(),
        "port": entry_port.get(),
        "password": entry_password.get(),
        "token": entry_token.get(),
        "rcon_password": entry_rcon_password.get(),
        "command_line_options": entry_options.get()
    }
    with open("server_config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)
    messagebox.showinfo("Save", "Configuration succesfully saved in server_config.json.")

# Function to load the configuration
def load_configuration():
    if os.path.isfile("server_config.json"):
        with open("server_config.json", "r") as config_file:
            config = json.load(config_file)
            entry_exe.insert(0, config.get("server_exe", ""))
            entry_name.insert(0, config.get("host_name", ""))
            entry_map.insert(0, config.get("map_name", ""))
            entry_max_players.insert(0, config.get("max_players", ""))
            entry_port.insert(0, config.get("port", ""))
            entry_password.insert(0, config.get("password", ""))
            entry_token.insert(0, config.get("token", ""))
            entry_rcon_password.insert(0, config.get("rcon_password", ""))
            entry_options.insert(0, config.get("command_line_options", ""))

# Function to validate that only numbers are entered
def validate_number(P):
    return P.isdigit() or P == ""

# Function to validate the range of max players
def validate_max_players(P):
    return P.isdigit() and 1 <= int(P) <= 100 or P == ""

# Function to validate the range of max portnumber
def validate_max_portnumber(P):
    return P.isdigit() and 1 <= int(P) <= 65535 or P == ""

def open_token_url(event):
    webbrowser.open_new("https://steamcommunity.com/dev/managegameservers")

def open_command_line_options_url(event):
    webbrowser.open_new("https://developer.valvesoftware.com/wiki/Command_line_options")

# Function to check if mandatory fields are filled
def check_mandatory_fields(*args):
    if entry_name.get() and entry_port.get() and entry_max_players.get() and entry_map.get():
        run_button.state(["!disabled"])
    else:
        run_button.state(["disabled"])

def toggle_password_visibility():
    entry_password.config(show='' if password_var.get() else '*')

def toggle_token_visibility():
    entry_token.config(show='' if token_var.get() else '*')

def toggle_rcon_visibility():
    entry_rcon_password.config(show='' if rcon_var.get() else '*')

# Initialize the GUI window with a modern theme
root = tk.Tk()
root.title("FortressForge v1.1.2")
root.minsize(650, 400)

# Menu bar
menubar = tk.Menu(root)

# Define menu items and their corresponding functions in a dictionary
menu_items = {
    "SteamCMD": lambda: webbrowser.open_new("https://developer.valvesoftware.com/wiki/SteamCMD"),
    "UPnP Portmapper": lambda: webbrowser.open_new("https://github.com/kaklakariada/portmapper/releases/"),
    "KVManager": lambda: webbrowser.open_new("https://forums.alliedmods.net/showthread.php?t=81160"),
    "SourceMod": lambda: webbrowser.open_new("https://www.sourcemod.net/downloads.php?branch=stable"),
    "MetaMod:Source": lambda: webbrowser.open_new("https://www.sourcemm.net/downloads.php?branch=master&all=1")
}

# Create downloads menu using the dictionary
downloadsmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Downloads", menu=downloadsmenu)
for label, function in menu_items.items():
    downloadsmenu.add_command(label=label, command=function)

# Define menu items and their corresponding functions in a dictionary for Help menu
help_menu_items = {
    "Open Steam Guide": lambda: webbrowser.open_new("https://steamcommunity.com/sharedfiles/filedetails/?id=3256322927"),
    "Open GitHub Repository": lambda: webbrowser.open_new("https://github.com/EierkuchenHD/FortressForge")
}

# Create help menu using the dictionary
helpmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
for label, function in help_menu_items.items():
    helpmenu.add_command(label=label, command=function)

root.config(menu=menubar)

# Input validation for numerical fields
vcmd_max_players = (root.register(validate_max_players), '%P')
vcmd_max_portnumber = (root.register(validate_max_portnumber), '%P')

# GUI elements
ttk.Label(root, text="Path to srcds_win64.exe OR srcds.exe*", font=("Segoe UI", 9)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_exe = ttk.Entry(root, width=50)
entry_exe.grid(row=0, column=1, padx=10, pady=5)
entry_exe.bind("<KeyRelease>", check_mandatory_fields)
browse_button = ttk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=0, column=2, padx=10, pady=5)

ttk.Label(root, text="Host Name*", font=("Segoe UI", 9)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_name = ttk.Entry(root, width=50)
entry_name.grid(row=1, column=1, padx=10, pady=5)
entry_name.bind("<KeyRelease>", check_mandatory_fields)

ttk.Label(root, text="Map*", font=("Segoe UI", 9)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_map = ttk.Entry(root, width=50)
entry_map.grid(row=2, column=1, padx=10, pady=5)
entry_map.bind("<KeyRelease>", check_mandatory_fields)

ttk.Label(root, text="Max Players (1-100)*", font=("Segoe UI", 9)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_max_players = ttk.Entry(root, width=10, validate="key", validatecommand=vcmd_max_players)
entry_max_players.grid(row=3, column=1, padx=10, pady=5, sticky="w")
entry_max_players.bind("<KeyRelease>", check_mandatory_fields)

ttk.Label(root, text="UDP Port (1-65535)*", font=("Segoe UI", 9)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_port = ttk.Entry(root, width=10, validate="key", validatecommand=vcmd_max_portnumber)
entry_port.grid(row=4, column=1, padx=10, pady=5, sticky="w")
entry_port.bind("<KeyRelease>", check_mandatory_fields)

ttk.Label(root, text="Server Password", font=("Segoe UI", 9)).grid(row=5, column=0, padx=10, pady=5, sticky="e")
entry_password = ttk.Entry(root, width=50, show="*")
entry_password.grid(row=5, column=1, padx=10, pady=5)
password_var = tk.BooleanVar()
show_password = ttk.Checkbutton(root, text="Show Password", variable=password_var, command=toggle_password_visibility)
show_password.grid(row=5, column=2, padx=10, pady=5, sticky="w")

# Game Server Login Token with hyperlink
token_label = ttk.Label(root, text="Game Server Login Token", font=("Segoe UI", 9, "underline"), foreground="blue", cursor="hand2")
token_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
token_label.bind("<Button-1>", open_token_url)
entry_token = ttk.Entry(root, width=50, show="*")
entry_token.grid(row=6, column=1, padx=10, pady=5)
token_var = tk.BooleanVar()
show_token = ttk.Checkbutton(root, text="Show Token", variable=token_var, command=toggle_token_visibility)
show_token.grid(row=6, column=2, padx=10, pady=5, sticky="w")

ttk.Label(root, text="RCON Password", font=("Segoe UI", 9)).grid(row=7, column=0, padx=10, pady=5, sticky="e")
entry_rcon_password = ttk.Entry(root, width=50, show="*")
entry_rcon_password.grid(row=7, column=1, padx=10, pady=5)
rcon_var = tk.BooleanVar()
show_rcon = ttk.Checkbutton(root, text="Show RCON", variable=rcon_var, command=toggle_rcon_visibility)
show_rcon.grid(row=7, column=2, padx=10, pady=5, sticky="w")

# Command Line Options with hyperlink
options_label = ttk.Label(root, text="Command Line Options", font=("Segoe UI", 9, "underline"), foreground="blue", cursor="hand2")
options_label.grid(row=8, column=0, padx=10, pady=5, sticky="e")
options_label.bind("<Button-1>", open_command_line_options_url)
entry_options = ttk.Entry(root, width=50)
entry_options.grid(row=8, column=1, padx=10, pady=5)

run_button = ttk.Button(root, text="Run Server", command=run_server)
run_button.grid(row=9, column=1, padx=10, pady=10, sticky="w")
run_button.state(["disabled"])

save_button = ttk.Button(root, text="Save Config", command=save_configuration)
save_button.grid(row=9, column=1, padx=10, pady=10, sticky="e")

# Load the configuration when the application starts
load_configuration()

root.mainloop()
