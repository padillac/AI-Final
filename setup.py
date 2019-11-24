import subprocess
import sys

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", "--user", package])


install('spotipy')
