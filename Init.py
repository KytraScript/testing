import os
import subprocess
import sys
import requests


def gitclone(url, recursive=False, dest=None):
    command = ['git', 'clone', url]
    if dest: command.append(dest)
    if recursive: command.append('--recursive')
    res = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(res)

def pipi(modulestr):
    res = subprocess.run(['python','-m','pip', '-q', 'install', modulestr], stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(res)

def wget_p(url, outputdir):
    res = subprocess.run(['wget', url, '-P', f'{outputdir}'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(res)

# Define the root directory
root_path = os.getcwd()

def createPath(filepath):
    os.makedirs(filepath, exist_ok=True)

initDirPath = os.path.join(root_path,'init_images')
createPath(initDirPath)
outDirPath = os.path.join(root_path,'images_out')
createPath(outDirPath)

model_path = os.path.join(root_path, 'models')
createPath(model_path)



# Check and print GPU info
nvidiasmi_output = subprocess.run(['nvidia-smi', '-L'], stdout=subprocess.PIPE).stdout.decode('utf-8')
print(nvidiasmi_output)

# Check if PyTorch is installed and print its version
def get_version(package):
    proc = subprocess.run(['pip','show', package], stdout=subprocess.PIPE)
    out = proc.stdout.decode('UTF-8')
    returncode = proc.returncode
    if returncode != 0:
        return -1
    return out.split('Version:')[-1].split('\n')[0]

torchver = get_version('torch')
if torchver == -1:
    print('Torch not found.')
else:
    print('Found torch:', torchver)

# If PyTorch is not installed, or its version is not 2.0.0, install PyTorch 2.0.0
if torchver != '2.0.0':
    print('Installing torch v2.')
    subprocess.run(['python', '-m', 'pip', '-q', 'install', 'torch==2.0.0', 'torchvision==0.15.1', '--upgrade'], stdout=subprocess.PIPE)
    import torch
    if not torch.cuda.is_available():
        print('Failed installing torch v2.')
    else:
        print('Successfully installed torch v2.')

from IPython.utils import io
os.makedirs('./embeddings', exist_ok=True)

import pathlib, shutil, os, sys

if not is_colab:
  # If running locally, there's a good chance your env will need this in order to not crash upon np.matmul() or similar operations.
  os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'

PROJECT_DIR = os.path.abspath(os.getcwd())
USE_ADABINS = False

if is_colab:
  if google_drive is not True:
    root_path = f'/content'
    model_path = '/content/models'
else:
  root_path = os.getcwd()
  model_path = f'{root_path}/models'

sys.path.append(f'{PROJECT_DIR}/BLIP')
sys.path.append(f'{PROJECT_DIR}/ResizeRight')
sys.path.append(f'{PROJECT_DIR}/guided-diffusion')