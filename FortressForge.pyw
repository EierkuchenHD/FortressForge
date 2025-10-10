import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
from tkinter import ttk
import os
import subprocess
import webbrowser
import json
import threading
import queue
from datetime import datetime
from typing import Optional

class TF2ServerLauncher:
    """Enhanced Team Fortress 2 Server Launcher with improved architecture."""
    
    # Constants
    DEFAULT_CONFIG = {
        "exe": "",
        "name": "My TF2 Server",
        "map": "cp_badlands",
        "max_players": "24",
        "port": "27015",
        "password": "",
        "token": "",
        "rcon_password": "",
        "options": "",
        "force_restart": False
    }
    
    VALID_EXECUTABLES = ("srcds.exe", "srcds_win64.exe")
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("FortressForge v2.0.0")
        self.root.minsize(800, 650)
        
        # Get script directory
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file_path = os.path.join(self.script_dir, "server_config.json")
        self.log_file_path = os.path.join(self.script_dir, "server_log.log")
        
        # Server state management (thread-safe)
        self.process: Optional[subprocess.Popen] = None
        self.server_thread: Optional[threading.Thread] = None
        self.running = threading.Event()
        self.output_queue = queue.Queue()
        self.force_restart_var = tk.BooleanVar()
        
        # Password visibility variables
        self.password_var = tk.BooleanVar()
        self.token_var = tk.BooleanVar()
        self.rcon_var = tk.BooleanVar()
        
        # Build UI
        self.setup_menu()
        self.setup_ui()
        self.setup_console()
        
        # Bind closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Load configuration and start status updates
        self.load_configuration()
        self.update_server_status()
        self.process_output_queue()
    
    def setup_menu(self):
        """Create menu bar with downloads and help sections."""
        menubar = tk.Menu(self.root)
        
        # Downloads menu
        downloads_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Downloads", menu=downloads_menu)
        
        download_items = {
            "SteamCMD": "https://developer.valvesoftware.com/wiki/SteamCMD",
            "UPnP Portmapper": "https://github.com/kaklakariada/portmapper/releases/",
            "KVManager": "https://forums.alliedmods.net/showthread.php?t=81160",
            "SourceMod": "https://www.sourcemod.net/downloads.php?branch=stable",
            "MetaMod:Source": "https://www.sourcemm.net/downloads.php?branch=master&all=1"
        }
        
        for label, url in download_items.items():
            downloads_menu.add_command(label=label, command=lambda u=url: webbrowser.open_new(u))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        help_items = {
            "Open Steam Guide": "https://steamcommunity.com/sharedfiles/filedetails/?id=3256322927",
            "Open GitHub Repository": "https://github.com/EierkuchenHD/FortressForge"
        }
        
        for label, url in help_items.items():
            help_menu.add_command(label=label, command=lambda u=url: webbrowser.open_new(u))
        
        self.root.config(menu=menubar)
    
    def setup_ui(self):
        """Create main UI elements."""
        # Main frame for inputs
        input_frame = ttk.Frame(self.root)
        input_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Path to executable
        ttk.Label(input_frame, text="Path to srcds_win64.exe OR srcds.exe*", font=("Segoe UI", 9)).grid(
            row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_exe = ttk.Entry(input_frame, width=50)
        self.entry_exe.grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_file).grid(
            row=0, column=2, padx=10, pady=5)
        
        # Host Name
        ttk.Label(input_frame, text="Host Name*", font=("Segoe UI", 9)).grid(
            row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_name = ttk.Entry(input_frame, width=50, 
                                     validate="key", 
                                     validatecommand=(self.root.register(self.validate_server_name), '%P'))
        self.entry_name.grid(row=1, column=1, padx=10, pady=5)
        
        # Map
        ttk.Label(input_frame, text="Map*", font=("Segoe UI", 9)).grid(
            row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_map = ttk.Entry(input_frame, width=50,
                                    validate="key",
                                    validatecommand=(self.root.register(self.validate_map_name), '%P'))
        self.entry_map.grid(row=2, column=1, padx=10, pady=5)
        
        # Max Players
        ttk.Label(input_frame, text="Max Players (1-100)*", font=("Segoe UI", 9)).grid(
            row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_max_players = ttk.Entry(input_frame, width=5,
                                           validate="key",
                                           validatecommand=(self.root.register(self.validate_max_players), '%P'))
        self.entry_max_players.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        # UDP Port
        ttk.Label(input_frame, text="UDP Port (1-65535)*", font=("Segoe UI", 9)).grid(
            row=4, column=0, padx=10, pady=5, sticky="e")
        self.entry_port = ttk.Entry(input_frame, width=7,
                                     validate="key",
                                     validatecommand=(self.root.register(self.validate_port), '%P'))
        self.entry_port.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        
        # Server Password
        ttk.Label(input_frame, text="Server Password", font=("Segoe UI", 9)).grid(
            row=5, column=0, padx=10, pady=5, sticky="e")
        self.entry_password = ttk.Entry(input_frame, width=50, show="*")
        self.entry_password.grid(row=5, column=1, padx=10, pady=5)
        ttk.Checkbutton(input_frame, text="Show", variable=self.password_var,
                       command=lambda: self.toggle_visibility(self.entry_password, self.password_var)).grid(
            row=5, column=2, padx=10, pady=5, sticky="w")
        
        # Game Server Login Token
        token_label = ttk.Label(input_frame, text="Game Server Login Token", 
                               font=("Segoe UI", 9, "underline"), 
                               foreground="blue", cursor="hand2")
        token_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
        token_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://steamcommunity.com/dev/managegameservers"))
        self.entry_token = ttk.Entry(input_frame, width=50, show="*")
        self.entry_token.grid(row=6, column=1, padx=10, pady=5)
        ttk.Checkbutton(input_frame, text="Show", variable=self.token_var,
                       command=lambda: self.toggle_visibility(self.entry_token, self.token_var)).grid(
            row=6, column=2, padx=10, pady=5, sticky="w")
        
        # RCON Password
        ttk.Label(input_frame, text="RCON Password", font=("Segoe UI", 9)).grid(
            row=7, column=0, padx=10, pady=5, sticky="e")
        self.entry_rcon_password = ttk.Entry(input_frame, width=50, show="*")
        self.entry_rcon_password.grid(row=7, column=1, padx=10, pady=5)
        ttk.Checkbutton(input_frame, text="Show", variable=self.rcon_var,
                       command=lambda: self.toggle_visibility(self.entry_rcon_password, self.rcon_var)).grid(
            row=7, column=2, padx=10, pady=5, sticky="w")
        
        # Other Command Line Options
        options_label = ttk.Label(input_frame, text="Other Command Line Options", 
                                 font=("Segoe UI", 9, "underline"),
                                 foreground="blue", cursor="hand2")
        options_label.grid(row=8, column=0, padx=10, pady=5, sticky="e")
        options_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://developer.valvesoftware.com/wiki/Command_line_options"))
        self.entry_options = ttk.Entry(input_frame, width=50)
        self.entry_options.grid(row=8, column=1, padx=10, pady=5)
        
        # Force Restart on Server Crash
        ttk.Checkbutton(input_frame, text="Force Restart on Server Crash", 
                       variable=self.force_restart_var).grid(
            row=9, column=1, padx=10, pady=5, sticky="w")
        
        # Button frame
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, pady=10)
        
        ttk.Button(button_frame, text="Save Config", command=self.save_configuration).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Config", command=self.load_configuration).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_to_defaults).pack(
            side=tk.LEFT, padx=5)
        
        # Server control buttons
        control_frame = ttk.Frame(self.root)
        control_frame.grid(row=2, column=0, pady=5)
        
        self.run_button = ttk.Button(control_frame, text="▶ Start Server", 
                                     command=self.run_server, style="Accent.TButton")
        self.run_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="⏹ Stop Server", 
                                      command=self.stop_server, state="disabled")
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="🗑 Clear Console", 
                  command=self.clear_console).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(self.root, text="● Server Status: Stopped", 
                                     font=("Segoe UI", 10, "bold"), foreground="#dc3545")
        self.status_label.grid(row=3, column=0, pady=5)
        
        # Mandatory fields note
        note_label = tk.Label(self.root, text="Fields marked with * are mandatory.", 
                             font=("Segoe UI", 8, "italic"))
        note_label.grid(row=4, column=0, pady=2)
    
    def setup_console(self):
        """Create console output area."""
        console_frame = ttk.LabelFrame(self.root, text="Server Console Output", padding=5)
        console_frame.grid(row=5, column=0, sticky="nsew", padx=10, pady=5)
        
        self.console_output = scrolledtext.ScrolledText(console_frame, 
                                                        height=12, 
                                                        wrap=tk.WORD,
                                                        font=("Consolas", 9),
                                                        bg="#1e1e1e",
                                                        fg="#d4d4d4",
                                                        state="disabled")
        self.console_output.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for resizing
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def log_to_console(self, message: str, tag: str = ""):
        """Thread-safe console logging."""
        self.console_output.config(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console_output.insert(tk.END, f"[{timestamp}] {message}\n", tag)
        self.console_output.see(tk.END)
        self.console_output.config(state="disabled")
        
        # Also log to file
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as log_file:
                log_file.write(f"[{timestamp}] {message}\n")
        except Exception:
            pass  # Fail silently if logging fails
    
    def clear_console(self):
        """Clear console output."""
        self.console_output.config(state="normal")
        self.console_output.delete(1.0, tk.END)
        self.console_output.config(state="disabled")
    
    def create_command(self) -> Optional[str]:
        """Create the server launch command with validation."""
        server_exe = self.entry_exe.get().strip()
        host_name = self.entry_name.get().strip()
        map_name = self.entry_map.get().strip()
        max_players = self.entry_max_players.get().strip()
        port = self.entry_port.get().strip()
        password = self.entry_password.get()
        token = self.entry_token.get()
        rcon_password = self.entry_rcon_password.get()
        command_line_options = self.entry_options.get()
        
        # Validate required fields
        if not all([host_name, port, max_players, map_name]):
            messagebox.showwarning("Input Error", 
                                 "Host Name, UDP Port, Maximum Players, and Map are required fields.")
            return None
        
        # Validate executable exists
        if not os.path.isfile(server_exe):
            messagebox.showerror("File Not Found", 
                               f"The file '{server_exe}' does not exist.")
            return None
        
        # Validate executable name
        exe_name = os.path.basename(server_exe).lower()
        if exe_name not in self.VALID_EXECUTABLES:
            response = messagebox.askyesno("Invalid Executable",
                                          f"The selected file '{exe_name}' may not be a valid TF2 server executable.\n"
                                          f"Expected: {' or '.join(self.VALID_EXECUTABLES)}\n\n"
                                          f"Do you want to continue anyway?")
            if not response:
                return None
        
        # Build command
        base_command = (f'"{server_exe}" -game tf -console -secure '
                       f'-port {port} +maxplayers {max_players} '
                       f'+map {map_name} +hostname "{host_name}"')
        
        if password:
            base_command += f' +sv_password "{password}"'
        if token:
            base_command += f' +sv_setsteamaccount "{token}"'
        if rcon_password:
            base_command += f' +rcon_password "{rcon_password}"'
        if command_line_options:
            base_command += f' {command_line_options}'
        
        return base_command
    
    def run_server(self):
        """Start the TF2 server in a separate thread."""
        if self.running.is_set():
            messagebox.showinfo("Server Running", "Server is already running!")
            return
        
        command = self.create_command()
        if command is None:
            return
        
        self.log_to_console("=== Starting TF2 Server ===")
        self.log_to_console(f"Command: {command}")
        
        # Update UI
        self.run_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        # Start server thread
        self.running.set()
        self.server_thread = threading.Thread(target=self._run_server_thread, 
                                              args=(command,), 
                                              daemon=True)
        self.server_thread.start()
    
    def _run_server_thread(self, command: str):
        """Server thread worker function."""
        while self.running.is_set():
            try:
                self.log_to_console("Launching server process...")
                
                self.process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.PIPE,
                    bufsize=1,
                    universal_newlines=True
                )
                
                # Read output
                for line in iter(self.process.stdout.readline, ''):
                    if not self.running.is_set():
                        break
                    self.output_queue.put(("output", line.rstrip()))
                
                # Wait for process to complete
                return_code = self.process.wait()
                
                if return_code != 0:
                    self.output_queue.put(("error", f"Server exited with code {return_code}"))
                else:
                    self.output_queue.put(("info", "Server stopped normally"))
                
                # Check if we should restart
                if not self.force_restart_var.get() or not self.running.is_set():
                    break
                
                self.output_queue.put(("info", "Restarting server in 3 seconds..."))
                for i in range(3):
                    if not self.running.is_set():
                        break
                    threading.Event().wait(1)
                
            except Exception as e:
                self.output_queue.put(("error", f"Error running server: {str(e)}"))
                break
        
        self.running.clear()
        self.output_queue.put(("status", "stopped"))
    
    def stop_server(self):
        """Stop the running server."""
        if not self.running.is_set():
            messagebox.showinfo("Server Not Running", "No server is currently running.")
            return
        
        self.log_to_console("=== Stopping Server ===")
        self.running.clear()
        
        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.log_to_console("Server didn't stop gracefully, forcing...")
                self.process.kill()
            except Exception as e:
                self.log_to_console(f"Error stopping server: {str(e)}")
        
        # Wait for thread
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(timeout=1)
        
        self.log_to_console("Server stopped successfully")
    
    def process_output_queue(self):
        """Process messages from the output queue (runs in main thread)."""
        try:
            while True:
                msg_type, message = self.output_queue.get_nowait()
                
                if msg_type == "output":
                    self.log_to_console(message)
                elif msg_type == "error":
                    self.log_to_console(f"ERROR: {message}")
                elif msg_type == "info":
                    self.log_to_console(f"INFO: {message}")
                elif msg_type == "status":
                    pass  # Status updates handled by update_server_status
                    
        except queue.Empty:
            pass
        
        self.root.after(100, self.process_output_queue)
    
    def update_server_status(self):
        """Update server status display."""
        if self.running.is_set() and (self.process is None or self.process.poll() is None):
            self.status_label.config(text="● Server Status: Running", foreground="#28a745")
            self.run_button.config(state="disabled")
            self.stop_button.config(state="normal")
        else:
            self.status_label.config(text="● Server Status: Stopped", foreground="#dc3545")
            self.run_button.config(state="normal")
            self.stop_button.config(state="disabled")
            
        self.root.after(1000, self.update_server_status)
    
    def browse_file(self):
        """Open file browser for executable selection."""
        filename = filedialog.askopenfilename(
            title="Select Server Executable",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if filename:
            self.entry_exe.delete(0, tk.END)
            self.entry_exe.insert(0, filename)
    
    def save_configuration(self):
        """Save current configuration to JSON file."""
        config = {
            "exe": self.entry_exe.get(),
            "name": self.entry_name.get(),
            "map": self.entry_map.get(),
            "max_players": self.entry_max_players.get(),
            "port": self.entry_port.get(),
            "password": self.entry_password.get(),
            "token": self.entry_token.get(),
            "rcon_password": self.entry_rcon_password.get(),
            "options": self.entry_options.get(),
            "force_restart": self.force_restart_var.get()
        }
        
        try:
            # Backup existing config
            if os.path.isfile(self.config_file_path):
                backup_path = self.config_file_path + ".backup"
                with open(self.config_file_path, "r") as src:
                    with open(backup_path, "w") as dst:
                        dst.write(src.read())
            
            # Save new config
            with open(self.config_file_path, "w") as config_file:
                json.dump(config, config_file, indent=4)
            
            messagebox.showinfo("Save", "Configuration saved successfully!")
            self.log_to_console("Configuration saved to server_config.json")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save configuration: {str(e)}")
    
    def load_configuration(self):
        """Load configuration from JSON file."""
        if not os.path.isfile(self.config_file_path):
            self.log_to_console("No configuration file found, using defaults")
            self.reset_to_defaults()
            return
        
        try:
            with open(self.config_file_path, "r") as config_file:
                config = json.load(config_file)
            
            # Load values
            self.entry_exe.delete(0, tk.END)
            self.entry_exe.insert(0, config.get("exe", ""))
            
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, config.get("name", self.DEFAULT_CONFIG["name"]))
            
            self.entry_map.delete(0, tk.END)
            self.entry_map.insert(0, config.get("map", self.DEFAULT_CONFIG["map"]))
            
            self.entry_max_players.delete(0, tk.END)
            self.entry_max_players.insert(0, config.get("max_players", self.DEFAULT_CONFIG["max_players"]))
            
            self.entry_port.delete(0, tk.END)
            self.entry_port.insert(0, config.get("port", self.DEFAULT_CONFIG["port"]))
            
            self.entry_password.delete(0, tk.END)
            self.entry_password.insert(0, config.get("password", ""))
            
            self.entry_token.delete(0, tk.END)
            self.entry_token.insert(0, config.get("token", ""))
            
            self.entry_rcon_password.delete(0, tk.END)
            self.entry_rcon_password.insert(0, config.get("rcon_password", ""))
            
            self.entry_options.delete(0, tk.END)
            self.entry_options.insert(0, config.get("options", ""))
            
            self.force_restart_var.set(config.get("force_restart", False))
            
            self.log_to_console("Configuration loaded successfully")
            
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load configuration: {str(e)}")
            self.reset_to_defaults()
    
    def reset_to_defaults(self):
        """Reset all fields to default values."""
        for key, value in self.DEFAULT_CONFIG.items():
            if key == "force_restart":
                self.force_restart_var.set(value)
            else:
                entry = getattr(self, f"entry_{key}")
                entry.delete(0, tk.END)
                entry.insert(0, value)
        
        self.log_to_console("Configuration reset to defaults")
    
    def toggle_visibility(self, entry: ttk.Entry, var: tk.BooleanVar):
        """Toggle password field visibility."""
        entry.config(show='' if var.get() else '*')
    
    # Validation methods
    @staticmethod
    def validate_server_name(P: str) -> bool:
        return len(P) <= 63
    
    @staticmethod
    def validate_map_name(P: str) -> bool:
        return all(c.isalnum() or c in '_-' for c in P) or P == ""
    
    @staticmethod
    def validate_max_players(P: str) -> bool:
        if P == "":
            return True
        try:
            val = int(P)
            return 1 <= val <= 100
        except ValueError:
            return False
    
    @staticmethod
    def validate_port(P: str) -> bool:
        if P == "":
            return True
        try:
            val = int(P)
            return 1 <= val <= 65535
        except ValueError:
            return False
    
    def on_closing(self):
        """Handle application closing."""
        if self.running.is_set():
            response = messagebox.askyesno("Server Running", 
                                          "Server is still running. Stop it and exit?")
            if not response:
                return
            
            self.stop_server()
        
        self.root.destroy()


def main():
    """Application entry point."""
    root = tk.Tk()
    app = TF2ServerLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()