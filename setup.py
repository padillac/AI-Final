#This script will automatically use Pip to install any dependencies that you don't already have installed
#It will install new packages to your user directory only to avoid permissions issues
import subprocess
import sys




def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", "--user", package])


install('spotipy')
install('tqdm')
install('graphviz')
install('pydot')
install('keras')
