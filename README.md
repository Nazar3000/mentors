Python version: 3.6.5
pip version: 18.0
To setup project run the following commands in your python environment:
- pip install -r requirements.txt

There is issue with FFVideo, so run the following commands to fix to
(from https://askubuntu.com/questions/1034023/cant-install-python-ffvideo-package)

download FFVideo without installing
- sudo apt install python-dev cython libavcodec-dev libavformat-dev libswscale-dev python-pip

- pip download FFVideo

unpack tar file
- tar -xvf FFVideo-0.0.13.tar.gz

replace deprecated references
- sed -i -e 's/avcodec_alloc_frame/av_frame_alloc/g' FFVideo-0.0.13/ffvideo/ffvideo.c

- sed -i -e 's/PIX_FMT_RGB24/AV_PIX_FMT_RGB24/g' FFVideo-0.0.13/ffvideo/ffvideo.c

- sed -i -e 's/PIX_FMT_GRAY8/AV_PIX_FMT_GRAY8/g' FFVideo-0.0.13/ffvideo/ffvideo.c

- sed -i -e 's/PIX_FMT_YUV420P/AV_PIX_FMT_YUV420P/g' FFVideo-0.0.13/ffvideo/ffvideo.c

pack it
- tar -zcvf FFVideo-0.0.13.tar.gz FFVideo-0.0.13

install
- pip install --upgrade FFVideo-0.0.13.tar.gz

Also it is required to add postges HStore extension

- psql you_db_name -c 'create extension hstore;'