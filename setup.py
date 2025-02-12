import subprocess
import sys
import platform

def install_system_dependencies():
    try:
        subprocess.check_call(["sudo", "apt-get", "update"])
        subprocess.check_call(["sudo", "apt-get", "install", "-y", "libxcb-cursor0", "libxcb-render0", "libxcb-shm0", "libxcb-util1", "libxcb-image0", "libxcb-keysyms1", "libxcb-randr0", "libxcb-icccm4"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing system dependencies: {e}")
        sys.exit(1)

def install_dependencies():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if platform.system() == "Linux":
        install_system_dependencies()
    install_dependencies()