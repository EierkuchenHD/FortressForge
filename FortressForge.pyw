import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import os
import subprocess
import webbrowser
from ttkthemes import ThemedTk

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

    # Debugging if-statement
    if not host_name or not port or not max_players or not map_name:
        messagebox.showwarning("Input Error", "Host Name, UDP Port, Maximum Amount of Players, and Map are required fields.")
        return

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

# Function to browse for the srcds_win64.exe file
def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
    if filename:
        entry_exe.delete(0, tk.END)
        entry_exe.insert(0, filename)
    check_mandatory_fields()

# Function to save the configuration (Placeholder function)
def save_configuration():
    # Implement saving logic here
    messagebox.showinfo("Save", "Saving has not been added as a functionality yet. Too bad!")

# Function to validate that only numbers are entered
def validate_number(P):
    if str.isdigit(P) or P == "":
        return True
    else:
        return False

# Function to validate the range of max players
def validate_max_players(P):
    if P.isdigit() and 1 <= int(P) <= 100:
        return True
    elif P == "":
        return True
    else:
        return False

# Function to open the Steam Guide URL
def open_steam_guide():
    webbrowser.open_new("https://steamcommunity.com/sharedfiles/filedetails/?id=3256322927")

# Function to open the SourceMod URL
def open_sourcemod():
    webbrowser.open_new("https://www.sourcemod.net/downloads.php?branch=stable")

# Function to open the MetaMod:Source URL
def open_metamod_source():
    webbrowser.open_new("https://www.sourcemm.net/downloads.php?branch=master&all=1")

# Function to open the GitHub repository URL
def open_github_repo():
    webbrowser.open_new("https://github.com/EierkuchenHD/FortressForge")

# Function to open the Steam Game Server Login Token page
def open_token_url(event):
    webbrowser.open_new("https://steamcommunity.com/dev/managegameservers")

# Function to open the Command Line Options page
def open_command_line_options_url(event):
    webbrowser.open_new("https://developer.valvesoftware.com/wiki/Command_line_options")

def open_github_releases():
    webbrowser.open_new("https://github.com/EierkuchenHD/FortressForge/releases/")

def open_upnp_portmapper_page():
    webbrowser.open_new("https://github.com/kaklakariada/portmapper/releases/")

# Function to check if mandatory fields are filled
def check_mandatory_fields(*args):
    if entry_name.get() and entry_port.get() and entry_max_players.get() and entry_map.get():
        run_button.state(["!disabled"])
    else:
        run_button.state(["disabled"])

def switch_theme(new_theme):
    root.set_theme(new_theme)

# Initialize the GUI window with a modern theme
root = ThemedTk(theme="breeze")  # You can replace "arc" with any other theme provided by ttkthemes
root.title("FortressForge")

# Menu bar
menubar = tk.Menu(root)

pluginmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Plugins", menu=pluginmenu)
pluginmenu.add_command(label="Open SourceMod Download Page", command=open_sourcemod)  # Added command for SourceMod
pluginmenu.add_command(label="Open MetaMod:Source Download Page", command=open_metamod_source)  # Added command for MetaMod:Source

themes_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Themes", menu=themes_menu)
for theme in root.get_themes():
    themes_menu.add_command(label=theme, command=lambda t=theme: switch_theme(t))

helpmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Open Steam Guide", command=open_steam_guide)
helpmenu.add_command(label="Download UPnP Portmapper", command=open_upnp_portmapper_page)
helpmenu.add_command(label="Open GitHub Repository", command=open_github_repo)
helpmenu.add_command(label="Check for new releases", command=open_github_releases)

root.config(menu=menubar)

# Input validation for numerical fields
vcmd = (root.register(validate_number), '%P')
vcmd_max_players = (root.register(validate_max_players), '%P')

# Executable file path
ttk.Label(root, text="Path to srcds_win64.exe OR scrds.exe*").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_exe = ttk.Entry(root, width=50)
entry_exe.grid(row=0, column=1, padx=10, pady=5)
entry_exe.bind("<KeyRelease>", check_mandatory_fields)
browse_button = ttk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=0, column=2, padx=10, pady=5)

# Host Name
ttk.Label(root, text="Host Name*").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_name = ttk.Entry(root, width=50)
entry_name.grid(row=1, column=1, padx=10, pady=5)
entry_name.bind("<KeyRelease>", check_mandatory_fields)

# Map
ttk.Label(root, text="Map*").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_map = ttk.Entry(root, width=50)
entry_map.insert(0, "plr_hightower")
entry_map.config(foreground="grey")
def on_map_focus_in(event):
    if entry_map.get() == "plr_hightower":
        entry_map.delete(0, tk.END)
        entry_map.config(foreground="black")
def on_map_focus_out(event):
    if not entry_map.get():
        entry_map.insert(0, "plr_hightower")
        entry_map.config(foreground="grey")
entry_map.bind("<FocusIn>", on_map_focus_in)
entry_map.bind("<FocusOut>", on_map_focus_out)
entry_map.bind("<KeyRelease>", check_mandatory_fields)
entry_map.grid(row=2, column=1, padx=10, pady=5)

# Maximum Amount of Players
ttk.Label(root, text="Maximum Amount of Players*").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_max_players = ttk.Entry(root, validate='key', validatecommand=vcmd_max_players, width=10)
entry_max_players.grid(row=3, column=1, padx=10, pady=5, sticky="w")
entry_max_players.insert(0, "24")
entry_max_players.bind("<KeyRelease>", check_mandatory_fields)

# UDP Port
ttk.Label(root, text="UDP Port*").grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_port = ttk.Entry(root, validate='key', validatecommand=vcmd, width=10)  # Change width to 10
entry_port.grid(row=4, column=1, padx=10, pady=5, sticky="w")  # Add sticky="w" to align with the max players field
entry_port.insert(0, "27015")
entry_port.bind("<KeyRelease>", check_mandatory_fields)

# Server Password
ttk.Label(root, text="Server Password").grid(row=5, column=0, padx=10, pady=5, sticky="e")
entry_password = ttk.Entry(root, width=50)
entry_password.grid(row=5, column=1, padx=10, pady=5)

# Game Server Login Token
token_label = ttk.Label(root, text="Game Server Login Token")
token_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
token_link = tk.Label(root, text="(Get Token)", font=("Segoe UI", 8), fg="blue", cursor="hand2")
token_link.grid(row=6, column=2, padx=10, pady=5, sticky="w")
token_link.bind("<Button-1>", open_token_url)
entry_token = ttk.Entry(root, width=50, show="*")
entry_token.grid(row=6, column=1, padx=10, pady=5)

# RCON Password
ttk.Label(root, text="RCON Password").grid(row=7, column=0, padx=10, pady=5, sticky="e")
entry_rcon_password = ttk.Entry(root, width=50)
entry_rcon_password.grid(row=7, column=1, padx=10, pady=5)

# Command Line Options
command_line_label = ttk.Label(root, text="Command Line Options")
command_line_label.grid(row=8, column=0, padx=10, pady=5, sticky="e")
command_line_link = tk.Label(root, text="(More Info)", font=("Segoe UI", 8), fg="blue", cursor="hand2")
command_line_link.grid(row=8, column=2, padx=10, pady=5, sticky="w")
command_line_link.bind("<Button-1>", open_command_line_options_url)
entry_options = ttk.Entry(root, width=50)
entry_options.grid(row=8, column=1, padx=10, pady=5)

# Run and Save Buttons
button_frame = ttk.Frame(root)
button_frame.grid(row=9, column=0, columnspan=3, pady=10)
run_button = ttk.Button(button_frame, text="Run", command=run_server)
run_button.grid(row=0, column=0, padx=5)
run_button.state(["disabled"])  # Initially disabled
save_button = ttk.Button(button_frame, text="Save", command=save_configuration)
save_button.grid(row=0, column=1, padx=5)

# Mandatory Fields Note
mandatory_note = tk.Label(root, text="Fields marked with * are mandatory.", font=("Segoe UI", 8, "italic"))
mandatory_note.grid(row=10, column=0, columnspan=3, pady=5)

# Track changes in mandatory fields to enable/disable the Run button
entry_name.bind("<KeyRelease>", check_mandatory_fields)
entry_port.bind("<KeyRelease>", check_mandatory_fields)
entry_max_players.bind("<KeyRelease>", check_mandatory_fields)
entry_map.bind("<KeyRelease>", check_mandatory_fields)

# Main loop to run the GUI
root.mainloop()
