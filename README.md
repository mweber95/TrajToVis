# TrajToVis

TrajToVis is a PyMol plugin which is capable of making publication ready images. It can also split trajectories
and rejoin them to create videos with aligned structures on a self chosen core region.

## How to run
1.) Clone the repository

2.) Change directory into repository folder

3.) Build Docker Image with:
```shell
docker build -t <your_image_name>:latest .
```
4.) Run Docker container with:
```shell
docker run --rm -ti
-e USERID=$UID \
-e USER=$USER \
-e DISPLAY=$DISPLAY \
-v /var/db:/var/db:Z \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-v $HOME/.Xauthority:/home/developer/.Xauthority \
--device /dev/dri/ \
<your_image_name>:latest \
pymol
```
If above command fails, try running ```xhost +``` first.

**NOTE:**

You can also skip step 3.) and 4.) and just use:
```shell
bash trajtovis.sh
```