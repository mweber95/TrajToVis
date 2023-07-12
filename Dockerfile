FROM ubuntu:20.04

LABEL maintainer="Mirko Weber, M.Sc. <weber7@hs-mittweida.de>"
ENV DEBIAN_FRONTEND=noninteractive
ENV trajtovis_dir /usr/local/lib/python3.8/dist-packages/trajtovis
RUN apt-get update && \
    apt-get install -y --no-install-recommends pymol pip

ADD requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt

ADD trajtovis /src/trajtovis
RUN cp -r /src/trajtovis "$trajtovis_dir"
RUN cp /src/trajtovis/trajtovis_gui.py /src/trajtovis/trajtovis.ui /src/trajtovis/pdb_show.ui\
    /usr/lib/python3/dist-packages/pmg_tk/startup
