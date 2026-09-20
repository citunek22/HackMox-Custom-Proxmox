<img width="950" height="596" alt="1000043287" src="https://github.com/user-attachments/assets/afe97458-2a32-4208-8451-0a6645a1539c" />

# HackMox
something like proxmox

Like the name suggests it works like proxmox but not exactly like proxmox it uses docker to make the containers.
Did i mention this took me 11 hours to make
also here is a link to see it works 
https://youtu.be/-h0IKcTE2pg?si=gPwrRQaUgzqlNd_Z

## System Requirements / things you absolutely need
- **OS:** Linux (Debian/Ubuntu and mint like me recommended) or macOS / Windows with WSL
- **Python:** 3.9 or higher
- **Permissions:** Root / sudo access (for container management and execution)

## Some of the features that you can see and use not only see
- **Live Terminal** It's a fully working terminal that's running with websocket isn't that cool.(`xterm.js`).
- **System Monitoring** Like the name suggests it monitors your system resources like your CPU, Ram and your storage. So that means that you can see all the things you always worry about like the most precious thing ever Ram and why don't people optimize programs instead of making them ram hungry looking at you Chrome 
- **Container Management** You can switch between your containers and your system. So you have your main node that's your PC and your containers that are like sandboxes and did you play in sandboxes as a kid
- **One-Click Shop** It means you can install ollama, home assistant etc. by just one click. It's me approved I hope that means something.
## Installation guide
### Option A: Windows (it's the easiest)
1. Go to the releases page here on GitHub (because where else would you download the code)
2. Download the file `hackmox-windows-exe.zip`. (don't worry that it's a zip inside the zip is the exe)
3. So Double click on the zip and select extract all (even tho there is one file it's better that way)
4. So now go to the extracted folder and open the exe it should be something like main.exe
5. Open your web browser and go to `http://localhost:8000`.

---

### Option B: Linux (Debian/Ubuntu)
1. Like in the windows option go to releases (again here on GitHub not anywhere else) and download the file named `hackmox_1.0.0_amd64.deb`.
2. Open your terminal in the folder where you downloaded the file.
3. Run this command to install:
   ```bash
   sudo dpkg -i hackmox_1.0.0_amd64.deb
   ```
4. Run the app by typing hackmox in the terminal 
## Option C
1. Clone this repo
git clone [https://github.com/citunek22/hackmox.git](https://github.com/citunek22/hackmox.git)
cd hackmox
2. **Install Dependencies**
```bash 
pip install -r requirements.txt
```
3. Run the server or website how you wanna call it
```bash
python main.py
```
4. Open it in your browser
Go to http://localhost:8000 or https://127.0.0.1:8000
