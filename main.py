import os
import json
import asyncio
import subprocess
import pty
import psutil
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

if not os.path.exists("static"):
    os.makedir("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/containers/list")
async def list_containers():
    try:
        cmd = ["docker", "ps", "-a", "--format", "{{.Names}}"]
        output = subprocess.check_output(cmd).decode("utf-8").strip()
        containers = output.split("\n") if output else []
        return {"containers": [c for c in containers if c]}
    except Exception as e:
        return {"containers": [], "error": str(e)}

@app.get("/api/system/stats")
async def get_stats(container_id: str = "main-node"):
    disk = psutil.disk_usage('/')

    if container_id == "main-node":
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        return {
            "container_id": container_id,
            "cpu_percent": cpu,
            "ram_used_gb": round(ram.used / (1024**3), 2),
            "ram_total_gb": round(ram.total / (1024**3), 2),
            "ram_percent": ram.percent,
            "disk_used_gb": round(disk.used / (1024**3), 2),
            "disk_total_gb": round(disk.total / (1024**3), 2),
            "disk_percent": disk.percent
        }
    else:
        try:
            cmd = ["docker", "stats", container_id, "--no-stream", "--format", "{{.CPUPerc}}|{{MemUsage}}|{{.MemPerc}}"]
            output = subprocess.check_output(cmd).decode("utf-8").strip()
            cpu_str, mem_str, mem_perc_str = output.split("|")

            return {
                "container_id": container_id,
                "cpu_percent": float(cpu_str.replace("%", "").strip()),
                "ram_used_gb": mem_str.split("/")[0].strip(),
                "ram_total_gb": mem_str.split("/")[1].strip(),
                "ram_percent": float(mem_perc_str.replace("%", "").strip()),
                "disk_used_gb": round(disk.used / (1024**3), 2),
                "disk_total_gb": round(disk.total / (1024**3), 2),
                "disk_percent": disk.percent
            }
        except Exception:
            return {
                "cpu_percent": 0, "ram_used_gb": "0", "ram_total_gb": "0", "ram_percent": 0,
                "disk_used_gb": round(disk.used / (1024**3), 2),
                "disk_total_gb": round(disk.total / (1024**3), 2),
                "disk_percent": disk.percent
            }
@app.get("/api/store/catalog")
async def get_catalog():
    return {
        "ollama": {
            "name": "Ollama AI (Official)",
            "image": "ollama/ollama:latest",
            "ports": "-p 11434:11434"
        },
        "homeassistant": {
            "name": "Home Assistant",
            "image": "ghcr.io/home-assistant/home-assistant:stable",
            "ports": "-p 8123:8123"
        },
        "jellyfin": {
            "name": "Jellyfin Media Server",
            "image": "jellyfin/jellyfin:latest",
            "ports": "-p 8096:8096"
        },
        "sunshine": {
            "name": "Sunshine Game Streaming",
            "image": "lscr.io/linuxserver/sunshine:latest",
            "ports": "-p 47989>47989 -p 47990:47990 -p 48010>48010"
        }
    }

class ResorceRequest(BaseModel):
    preset_app: str

@app.post("/api/resources/create")
async def create_resource(req: ResourceRequest):
    try:
        catalog = await get_catalog()
        if req.preset_app not in catalog:
            return {"status": "error", "message": "Unknown app"}

        app_info = catalog[req.preset_app]
        container_name = f"{req.preset_app}-node"
        image = app_info["image"]
        ports = app_info["ports"]

        # Important: Delete the old container, if there was a unsuccesful attempt
        subprocess.run(f"docker rm -f {container_name}", shell=True, stderr=subprocess.DEVNULL)

        # Start a new clean official container, which will always run
        run_cmd = f"docker run -d --name {container_name} {ports} --restart unless-stopped {image}"

        subprocess.Popen(run_cmd, shell=True)
        return {"status": "ok", "message": f"Starting container {container_name}!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.websocket("/ws/console/{container_id}")
async def websocket_endpoint(websocket: WebSocket, container_id: str):
    await websocket.accept()

    if container_id == "main-node":
        cmd = ["/bin/bash"]
    else:
       # Start /bin/sh or /bin/bash inside of the container
       cmd = ["docker", "exec", "-it", container_id, "/bin/sh"]

    master_fd, slave_fd = pty.openpty()

    proc = await asyncio.create_subproccess_exec(
        *cmd,
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        close_fds=True
    )
    os.close(slave_fd)

    loop = asyncio.get_running_loop()

    def on_pty_read():
        try:
            data = os.read(master_fd, 2048)
            if data:
                asyncio.create_task(websocket.send_text(data.decode('utf-8', errors='ignore')))
        except Exception:
            pass

    loop.add_reader(master_fd, on_pty_read)

    try:
        while True:
            msg = await websocket.recieve_text()
            os.write(master_fd, msg.encode('utf-8'))
    except Exception:
        pass
    if proc.returncode is None:
        proc.kill()