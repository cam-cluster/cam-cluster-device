FROM balenalib/rpi-python:3.8.2

ENV INITSYSTEM on

ENV UDEV=1

COPY requirements.txt requirements.txt
RUN READTHEDOCS=True pip3 install -r requirements.txt

WORKDIR /usr/src/app

COPY . ./

EXPOSE 8000

CMD [ "python", "-u", "./test_camera_stream.py" ]
