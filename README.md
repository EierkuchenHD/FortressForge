# FortressForge

FortressForge is a user-friendly graphical interface designed to simplify the process of creating and managing a 64bit Team Fortress 2 server. This application allows users to customize their server settings through an intuitive GUI and easily launch the server without needing to manually handle command-line options.

<p align="center">
<img src="https://github.com/EierkuchenHD/FortressForge/assets/68472374/2e8de135-a787-4486-b355-8fd575b6ca5c"/>
</p>

## Features

- **Executable Path Selection**: Easily locate the `srcds_win64.exe` file required to run the server.
- **Host Name**: Set a custom name for your server.
- **Map Selection**: Choose the initial map for your server.
- **Maximum Players**: Define the maximum number of players allowed on the server (1-100).
- **UDP Port**: Set the port on which your server will run, defaulting to 27015.
- **Server Password**: Optionally set a password for server access.
- **Game Server Login Token (GSLT)**: Let your server remain in users' favorites list even if your IP/Port changes.
- **RCON Password**: Set a remote console (RCON) password to manage your server remotely.
- **Command Line Options**: Add any additional command-line options as needed.

## Getting Started

### Prerequisites

- [Python 3.x](https://www.python.org/downloads/)

### Installation

Download the latest release of FortressForge under [Releases](https://github.com/EierkuchenHD/FortressForge/releases/tag/v1.0.0). It is recommended to put this file into your server directory where `srcds_win64.exe` is located.

## Acknowledgements

- Thanks to the AlliedModders community for helping me out with server issues I had!
- Thanks to AndrSator, creator of [SteamCMD-GUI](https://github.com/AndrSator/SteamCMD-GUI)
- Thanks to everyone who playtested my community server!
