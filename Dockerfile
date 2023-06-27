FROM ubuntu:20.04

LABEL maintainer="Mirko Weber, M.Sc. <weber7@hs-mittweida.de>"
ENV DEBIAN_FRONTEND=noninteractive
ENV fretlabel_dir /usr/local/lib/python3.8/dist-packages/fretlabel
ENV fretraj_dir /usr/local/lib/python3.8/dist-packages/fretraj

ADD plugin /src/plugin

RUN apt-get update && \
    apt-get install -y --no-install-recommends pymol pip git python3-dev gcc g++ gfortran python3-tk && \
    pip install fretraj && \
    cp "$fretraj_dir"/fretraj_gui.py /usr/lib/python3/dist-packages/pmg_tk/startup && \
    pip install fretlabel && \
    cp "$fretlabel_dir"/fretlabel_gui.py /usr/lib/python3/dist-packages/pmg_tk/startup && \
    # cd /src && \
    # git clone https://github.com/RNA-FRETools/fretraj.git && \
    # cd fretraj && \
    cp -r /src/plugin /usr/lib/python3/dist-packages/pmg_tk/startup

# RUN wget https://pymol.org/installers/PyMOL-2.5.4_404-Linux-x86_64-py37.tar.bz2
# RUN tar -jxf ./PyMOL-2.5.4_404-Linux-x86_64-py37.tar.bz2
# RUN git clone https://github.com/felixErichson/pymol_RNAvis.git
# RUN cp -r pymol_RNAvis /src/pymol/share/pymol/data/startup/pymol_RNAvis/
# RUN git clone https://github.com/RNA-FRETools/fretlabel.git
# RUN cp -r fretlabel /src/pymol/share/pymol/data/startup/fretlabel/
# RUN git clone https://github.com/RNA-FRETools/fretraj.git
# RUN cp fretraj/src/fretraj/fretraj_gui.py /src/pymol/share/pymol/data/startup/fretraj
# RUN cp fretraj/src/fretraj/__init__.py /src/pymol/share/pymol/data/startup/fretraj
# ADD plugin /src/plugin
# ADD license.lic /src/pymol/share/pymol
# RUN cp -r /src/plugin /src/pymol/share/pymol/data/startup/plugin/
## FROM ubuntu:22.04
#FROM continuumio/anaconda3
#
#LABEL maintainer="Mirko Weber, M.Sc. <weber7@hs-mittweida.de>"
#
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    ca-certificates \
#    bzip2 \
#    ffmpeg \
#    libsm6 \
#    libxext6 \
#    git
#
#RUN conda create -n myenv python==3.7 -y
#SHELL ["/bin/sh", "-lc"]
#RUN conda init bash
#SHELL ["/bin/sh", "-c"]
#RUN conda activate myenv
#RUN conda list
#RUN conda install -c schrodinger pymol
#
#WORKDIR /src

###################################################################################################

#RUN wget https://pymol.org/installers/PyMOL-2.5.4_404-Linux-x86_64-py37.tar.bz2
#RUN tar -jxf ./PyMOL-2.5.4_404-Linux-x86_64-py37.tar.bz2

#RUN git clone https://github.com/felixErichson/pymol_RNAvis.git
#RUN cp -r pymol_RNAvis /src/pymol/share/pymol/data/startup/pymol_RNAvis/
#RUN git clone https://github.com/RNA-FRETools/fretlabel.git
#RUN cp -r fretlabel/src/fretlabel /src/pymol/share/pymol/data/startup/fretlabel/
#RUN git clone https://github.com/RNA-FRETools/fretraj.git
#RUN cp -r fretraj/src/fretraj/fretraj_gui.py /src/pymol/lib/python3.7/site-packages/pmg_tk/startup
#ADD fancy_vis /src/fancy_vis
#ADD license.lic /src/pymol/share/pymol
#COPY fancy_vis /src/pymol/share/pymol/data/startup/fancy_vis/