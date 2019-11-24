import subprocess
import sys

def install(package):
    subprocess.call([sys.executable, "-m", "pip3", "install", "--user", package])


install('spotipy')
