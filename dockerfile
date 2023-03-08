FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get install -y libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pyzbar pdf2img PyPDF3 opencv-python

CMD [ "python3", "script.py" ]
