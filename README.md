# HackMox something like proxmox

Like the name suggests it works like proxmox but not exactly like proxmox it uses docker to make the containers.
Did i mention this took me 11 hours to make

## System Requirements / things you absolutely need
- **OS:** Linux (Debian/Ubuntu and mint like me recommended) or macOS / Windows with WSL
- **Python:** 3.9 or higher
- **Permissions:** Root / sudo access (for container management and execution)

## Some of the features that you can see and use not only see
- **Live Terminal** It's a fully working terminal that's running with websocket isn't that cool.(`xterm.js`).
- **System Monitoring** Like the name suggests it monitors your system resources like your CPU, Ram and your storage. So that means that you can see all the things you always worry about like the most precious thing ever Ram and why don't people optimize programs instead of making them ram hungry looking at you Chrome 
- **Container Management** You can switch between your containers and your system. So you have your main node that's your PC and your containers that are like sandboxes and did you play in sandboxes as a kid
- **One-Click Shop** It means you can install ollama, home assistant etc. by just one click. It's me approved I hope that means something.

1. **Install Dependencies**
```bash 
pip install -r requirements.txt

2. Run the server or website how you wanna call it
```bash```
python main.py

3. Open it in your browser
Go to http://localhost:8000 or https://127.0.0.1:8000
