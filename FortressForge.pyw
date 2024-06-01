import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import os
import subprocess
import webbrowser

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

# Function to validate the range of max portnumber
def validate_max_portnumber(P):
    if P.isdigit() and 1 <= int(P) <= 99999:
        return True
    elif P == "":
        return True
    else:
        return False

def open_kvmanager_page():
    webbrowser.open_new("https://forums.alliedmods.net/showthread.php?t=81160")

def open_upnp_portmapper_page():
    webbrowser.open_new("https://github.com/kaklakariada/portmapper/releases/")

def open_sourcemod():
    webbrowser.open_new("https://www.sourcemod.net/downloads.php?branch=stable")

def open_metamod_source():
    webbrowser.open_new("https://www.sourcemm.net/downloads.php?branch=master&all=1")

def open_steam_guide():
    webbrowser.open_new("https://steamcommunity.com/sharedfiles/filedetails/?id=3256322927")

def open_github_repo():
    webbrowser.open_new("https://github.com/EierkuchenHD/FortressForge")

def open_token_url(event):
    webbrowser.open_new("https://steamcommunity.com/dev/managegameservers")

def open_command_line_options_url(event):
    webbrowser.open_new("https://developer.valvesoftware.com/wiki/Command_line_options")

def open_steamcmd_page():
    webbrowser.open_new("https://developer.valvesoftware.com/wiki/SteamCMD")

# Function to check if mandatory fields are filled
def check_mandatory_fields(*args):
    if entry_name.get() and entry_port.get() and entry_max_players.get() and entry_map.get():
        run_button.state(["!disabled"])
    else:
        run_button.state(["disabled"])

def toggle_token_visibility():
    if token_var.get():
        entry_token.config(show='')
    else:
        entry_token.config(show='*')

def toggle_rcon_visibility():
    if rcon_var.get():
        entry_rcon_password.config(show='')
    else:
        entry_rcon_password.config(show='*')

def toggle_password_visibility():
    if password_var.get():
        entry_password.config(show='')
    else:
        entry_password.config(show='*')

# Initialize the GUI window with a modern theme
root = tk.Tk()
root.title("FortressForge v1.1.1")
root.minsize(650, 400)

# Menu bar
menubar = tk.Menu(root)

# Define menu items and their corresponding functions in a dictionary
menu_items = {
    "SteamCMD": open_steamcmd_page,
    "UPnP Portmapper": open_upnp_portmapper_page,
    "KVManager": open_kvmanager_page,
    "SourceMod": open_sourcemod,
    "MetaMod:Source": open_metamod_source
}

# Create downloads menu using the dictionary
downloadsmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Downloads", menu=downloadsmenu)
for label, function in menu_items.items():
    downloadsmenu.add_command(label=label, command=function)


# Define menu items and their corresponding functions in a dictionary for Help menu
help_menu_items = {
    "Open Steam Guide": open_steam_guide,
    "Open GitHub Repository": open_github_repo
}

# Create help menu using the dictionary
helpmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
for label, function in help_menu_items.items():
    helpmenu.add_command(label=label, command=function)


root.config(menu=menubar)

# Input validation for numerical fields
# Max Players
vcmd = (root.register(validate_number), '%P')
vcmd_max_players = (root.register(validate_max_players), '%P')
# Port Ranges
vcmd_max_portnumber = (root.register(validate_max_portnumber), '%P')

# Executable file path
ttk.Label(root, text="Path to srcds_win64.exe OR srcds.exe*",font=("Segoe UI", 9)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_exe = ttk.Entry(root, width=50)
entry_exe.grid(row=0, column=1, padx=10, pady=5)
entry_exe.bind("<KeyRelease>", check_mandatory_fields)
browse_button = ttk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=0, column=2, padx=10, pady=5)

# Host Name
ttk.Label(root, text="Host Name*",font=("Segoe UI", 9)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_name = ttk.Entry(root, width=50)
entry_name.grid(row=1, column=1, padx=10, pady=5)
entry_name.bind("<KeyRelease>", check_mandatory_fields)

# Map
ttk.Label(root, text="Map*",font=("Segoe UI", 9)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
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
ttk.Label(root, text="Maximum Amount of Players*",font=("Segoe UI", 9)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_max_players = ttk.Entry(root, validate='key', validatecommand=vcmd_max_players, width=10)
entry_max_players.grid(row=3, column=1, padx=10, pady=5, sticky="w")
entry_max_players.insert(0, "24")
entry_max_players.bind("<KeyRelease>", check_mandatory_fields)

# UDP Port
ttk.Label(root, text="UDP Port*",font=("Segoe UI", 9)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_port = ttk.Entry(root, validate='key', validatecommand=vcmd_max_portnumber, width=10)  # Change width to 10
entry_port.grid(row=4, column=1, padx=10, pady=5, sticky="w")  # Add sticky="w" to align with the max players field
entry_port.insert(0, "27015")
entry_port.bind("<KeyRelease>", check_mandatory_fields)

# Server Password
ttk.Label(root, text="Server Password", font=("Segoe UI", 9)).grid(row=5, column=0, padx=10, pady=5, sticky="e")
entry_password = ttk.Entry(root, width=50, show="*")
entry_password.grid(row=5, column=1, padx=10, pady=5)

password_var = tk.BooleanVar()
password_checkbox = ttk.Checkbutton(root, text="Show", variable=password_var, command=toggle_password_visibility)
password_checkbox.grid(row=5, column=2, padx=10, pady=5)

# Game Server Login Token (Hyperlink)
token_label = tk.Label(root, text="Game Server Login Token", font=("Segoe UI", 9, "underline"), fg="blue", cursor="hand2")
token_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
token_label.bind("<Button-1>", open_token_url)

entry_token = ttk.Entry(root, width=50, show="*")
entry_token.grid(row=6, column=1, padx=10, pady=5)

token_var = tk.BooleanVar()
token_checkbox = ttk.Checkbutton(root, text="Show", variable=token_var, command=toggle_token_visibility)
token_checkbox.grid(row=6, column=2, padx=10, pady=5)

# RCON Password
ttk.Label(root, text="RCON Password",font=("Segoe UI", 9)).grid(row=7, column=0, padx=10, pady=5, sticky="e")

entry_rcon_password = ttk.Entry(root, width=50, show="*")
entry_rcon_password.grid(row=7, column=1, padx=10, pady=5)

rcon_var = tk.BooleanVar()
rcon_checkbox = ttk.Checkbutton(root, text="Show", variable=rcon_var, command=toggle_rcon_visibility)
rcon_checkbox.grid(row=7, column=2, padx=10, pady=5)

# Command Line Options (Hyperlink)
command_line_label = tk.Label(root, text="Command Line Options", font=("Segoe UI", 9, "underline"), fg="blue", cursor="hand2")
command_line_label.grid(row=8, column=0, padx=10, pady=5, sticky="e")
command_line_label.bind("<Button-1>", open_command_line_options_url)

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
# Note that srcds_win64.exe is not compatible with 64bit
bit_note = tk.Label(root, text="SourceMod is not compatible with srcds_win64.exe yet.", font=("Segoe UI", 8, "italic"))
bit_note.grid(row=11, column=0, columnspan=3, pady=5)

# Track changes in mandatory fields to enable/disable the Run button
entry_name.bind("<KeyRelease>", check_mandatory_fields)
entry_port.bind("<KeyRelease>", check_mandatory_fields)
entry_max_players.bind("<KeyRelease>", check_mandatory_fields)
entry_map.bind("<KeyRelease>", check_mandatory_fields)

# Main loop to run the GUI
root.mainloop()
