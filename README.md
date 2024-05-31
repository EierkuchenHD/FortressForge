# FortressForge

![FortressForge Main Window](images\FortressForgeEmpty.png)

FortressForge is a user-friendly graphical interface designed to simplify the process of creating and managing a 64bit Team Fortress 2 server. This application allows users to customize their server settings through an intuitive GUI and easily launch the server without needing to manually handle command-line options.

## Features

- **Executable Path Selection**: Easily locate the `srcds_win64.exe` file required to run the server.
- **Host Name**: Set a custom name for your server.
- **Map Selection**: Choose the initial map for your server.
- **Maximum Players**: Define the maximum number of players allowed on the server (1-100).
- **Password Protection**: Optionally set a password for server access.
- **UDP Port**: Set the port on which your server will run, defaulting to 27015.
- **Game Server Login Token (GSLT)**: Let your server remain in users' favorites list even if your IP/Port changes.
- **RCON Password**: Set a remote console (RCON) password to manage your server remotely.
- **Command Line Options**: Add any additional command-line options as needed.

## Getting Started

### Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- Tkinter library (usually included with Python)

### Installation

Download the latest release of FortressForge under **Releases**.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to the Valve Developer Community for providing extensive documentation on command-line options and server management.
- Inspired by the need to simplify TF2 server management for casual and competitive play.

---

### Notes

- Ensure you have the necessary permissions and firewall settings configured to run a server on your machine.
- For detailed guidance on obtaining and using a Game Server Login Token, refer to the [Steam Community](https://steamcommunity.com/dev/managegameservers).
