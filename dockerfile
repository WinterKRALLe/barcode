FROM python:3.8-slim-buster
ENV LD_LIBRARY_PATH=/usr/lib

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get install -y pkg-config libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/

RUN apt-get update \
    && apt-get install -y poppler-utils \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get install -y libgl1-mesa-glx libzbar-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pyzbar pdf2img PyPDF3 opencv-python

CMD [ "python3", "script.py" ]
