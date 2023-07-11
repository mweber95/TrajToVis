FROM ubuntu:20.04

LABEL maintainer="Mirko Weber, M.Sc. <weber7@hs-mittweida.de>"
ENV DEBIAN_FRONTEND=noninteractive
ENV fretlabel_dir /usr/local/lib/python3.8/dist-packages/fretlabel
ENV fretraj_dir /usr/local/lib/python3.8/dist-packages/fretraj
ENV trajtovis_dir /usr/local/lib/python3.8/dist-packages/trajtovis

RUN apt-get update && \
    apt-get install -y --no-install-recommends pymol pip git python3-dev gcc g++ gfortran python3-tk 2>&1 && \
    python3 -m pip install -U pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip install fretraj && \
    cp "$fretraj_dir"/fretraj_gui.py /usr/lib/python3/dist-packages/pmg_tk/startup && \
    pip install numpy==1.23.5 && \
    echo {\"root_path\": \"/root\", \"browser\": null, \"local_docs\": null} > "$fretraj_dir"/.fretraj_settings.json && \
    pip install fretlabel && \
    cp "$fretlabel_dir"/fretlabel_gui.py /usr/lib/python3/dist-packages/pmg_tk/startup

ADD trajtovis /src/trajtovis
# ADD trajtovis/trajtovis_gui.py /src
# ADD trajtovis/trajtovis.ui /src
RUN cp -r /src/trajtovis "$trajtovis_dir"
RUN cp /src/trajtovis/trajtovis_gui.py /src/trajtovis/trajtovis.ui /src/trajtovis/pdb_show.ui\
    /usr/lib/python3/dist-packages/pmg_tk/startup
