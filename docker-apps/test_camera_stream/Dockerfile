FROM balenalib/rpi-python

ENV INITSYSTEM on

ENV UDEV=1

COPY requirements.txt requirements.txt
RUN READTHEDOCS=True pip install -r requirements.txt

WORKDIR /usr/src/app

COPY . ./

CMD [ "python", "-u", "test-scripts/test_camera_stream.py" ]
