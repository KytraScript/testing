FROM nvidia/cuda:11.8.0-base-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y \
    git python3.10 python3-pip python3-opencv imagemagick ffmpeg

RUN ln -s /usr/bin/python3.10 /usr/bin/python \
    && rm /usr/bin/pip \
    && ln -s /usr/bin/pip3 /usr/bin/pip

RUN python -m pip install torch==2.0.0 torchvision==0.15.1 --index-url https://download.pytorch.org/whl/cu118
RUN python -m pip uninstall torchtext -y
RUN python -m pip install xformers==0.0.19
RUN python -m pip install requests mediapipe piexif safetensors lark Pillow==9.0.0 wget webdataset open_clip_torch opencv-python==4.5.5.64 pandas matplotlib fvcore ipywidgets==7.7.1 transformers==4.19.2 omegaconf einops "pytorch_lightning>1.4.1,<=1.7.7" scikit-image opencv-python ai-tools cognitive-face zprint kornia==0.5.0 lpips keras datetime timm==0.6.7 prettytable basicsr fairscale realesrgan

WORKDIR /content
RUN git clone https://github.com/Sxela/sxela-stablediffusion /content/stablediffusion && python -m pip install -e /content/stablediffusion
RUN git clone https://github.com/Sxela/ControlNet-v1-1-nightly /content/ControlNet
RUN python -m pip install -e git+https://github.com/CompVis/taming-transformers.git@master#egg=taming-transformers -e git+https://github.com/openai/CLIP.git@main#egg=clip
RUN git clone https://github.com/crowsonkb/guided-diffusion /content/guided-diffusion && pip install -e /content/guided-diffusion
RUN git clone https://github.com/Sxela/k-diffusion /content/k-diffusion && pip install -e /content/k-diffusion
RUN git clone https://github.com/assafshocher/ResizeRight.git /content/ResizeRight
RUN git clone https://github.com/salesforce/BLIP /content/BLIP
RUN git clone https://github.com/pengbo-learn/python-color-transfer /content/python-color-transfer

RUN ln -s /usr/local/lib/python3.10/dist-packages/torch/lib/libnvrtc-672ee683.so.11.2 /usr/local/lib/python3.10/dist-packages/torch/lib/libnvrtc.so

# The script you want to run when Docker container starts
ENTRYPOINT ["python", "init.py"]