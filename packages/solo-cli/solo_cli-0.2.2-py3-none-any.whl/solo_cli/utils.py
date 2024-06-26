import os
import platform
import requests
import subprocess
from tqdm import tqdm

def download_file(url, filename):
    if os.path.exists(filename):
        print(f"{filename} already exists. Skipping download.")
        return
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    t = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            t.update(len(data))
            file.write(data)
    t.close()
    if total_size != 0 and t.n != total_size:
        print("ERROR: Something went wrong")
    else:
        print(f"{filename} downloaded successfully.")

def set_permissions(filename):
    if platform.system() in ['Linux', 'Darwin', 'BSD']:
        subprocess.run(['chmod', '+x', filename], check=True)
    elif platform.system() == 'Windows':
        new_filename = f"{filename}.exe"
        os.rename(filename, new_filename)
        return new_filename
    return filename

def start_ngrok_service(port):
    system = platform.system()
    config_path = "path/to/config.yml"

    if system == "Linux":
        if os.path.exists("/etc/systemd/system/"):
            with open("/etc/systemd/system/ngrok.service", "w") as service_file:
                service_file.write(
                    f"""
                    [Unit]
                    Description=Ngrok
                    After=network.service

                    [Service]
                    Type=simple
                    User={os.getenv("USER")}
                    WorkingDirectory={os.getenv("HOME")}
                    ExecStart=/usr/bin/ngrok start --all --config="{config_path}" --port={port}
                    Restart=on-failure

                    [Install]
                    WantedBy=multi-user.target
                    """
                )
            subprocess.run(["systemctl", "enable", "ngrok.service"], check=True)
            subprocess.run(["systemctl", "start", "ngrok.service"], check=True)
        else:
            subprocess.run(["nohup", "ngrok", "start", "--all", "--config", config_path, f"--port={port}", "&"], check=True)
    elif system == "Darwin":
        subprocess.run(["nohup", "ngrok", "start", "--all", "--config", config_path, f"--port={port}", "&"], check=True)
    elif system == "Windows":
        subprocess.run(["nssm", "install", "ngrok", "ngrok", "start", "--all", "--config", config_path, f"--port={port}"], check=True)
        subprocess.run(["sc", "start", "ngrok"], check=True)
    else:
        print(f"Unsupported operating system: {system}")

    print(f"Ngrok service started. Port {port} is available on the internet.")

def kill_ngrok(port):
    system = platform.system()
    if system in ['Linux', 'Darwin', 'BSD']:
        subprocess.run(["pkill", "ngrok"], check=True)
    elif system == "Windows":
        subprocess.run(["taskkill", "/F", "/IM", "ngrok.exe"], check=True)
    else:
        print(f"Unsupported operating system: {system}")
    print(f"Ngrok process on port {port} killed.")

def kill_process(port):
    system = platform.system()
    if system in ['Linux', 'Darwin', 'BSD']:
        subprocess.run(["fuser", "-k", f"{port}/tcp"], check=True)
    elif system == "Windows":
        subprocess.run(["netstat", "-ano", "|", "findstr", f":{port}"], check=True)
        subprocess.run(["taskkill", "/PID", f"{port}", "/F"], check=True)
    else:
        print(f"Unsupported operating system: {system}")
    print(f"Process on port {port} killed.")

def start_model():
    # Placeholder for start model functionality
    print("Starting model...")
