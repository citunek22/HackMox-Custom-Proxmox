# HackMox Control Panel

Lightweigth web control panel for my custom proxmox which works on Docker so when you press "ollama" on the website it will actally create an ollama docker container
Did i mention this took me 11 hours to make

## 📋 System Requirements
- **OS:** Linux (Debian/Ubuntu recommended) or macOS / Windows with WSL
- **Python:** 3.9 or higher
- **Permissions:** Root / sudo access (for container management and execution)

## Some of the features that you can see
- **Live Terminal** It's a fully interactive terminal via WebSocket (`xterm.js`).
- **System Monitoring** Like the name suggests it monitors your system resources like your CPU, Ram and your storage.
- **Container Management** You can switch between your containers and your system.
- **One-Click Shop** It means you can install ollama, home assistant etc. by just one click.

1. ** Install Dependencies**
```bash
pip install -r requirements.txt

2. Run the server
```bash
python main.py

3. Open it in your browser
Go to http://localhost:8000
