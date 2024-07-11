# ALPHA IMG AUV

## Introduction
This is the configuration for our ALPHA IMG AUV.
- ROS version Noetic,
- Ubuntu 20.04


## Directory structure
- `alpha_img_auv`: Meta package for the standard ALPHA AUV.

- `alpha_img_bringup`: Launch files to bring the vehicle/simulation up runnning

- `alpha_img_config`: Configuration files for helm, controller, and devices. `mvp_mission` state machine is configured in `/mission/config/helm.yaml`. Parameters for different behaviors program for the helm is located in `/mission/param`. `mvp_control` configuration is under `/config/control.yaml`.

- `alpha_img_description`: URDF files, rviz configuration, and vehicle mesh

## Installation

### Install the Stonefish simulator
- We use [Stonefish](https://stonefish.readthedocs.io/en/latest/install.html) Simulator. You can clone it from [here](https://github.com/uri-ocean-robotics/stonefish), a fork from the [original_repo](https://github.com/patrykcieslak/stonefish).

- Download the stonefish simulator **to another location outside your ROS workspace**
```bash
git clone https://github.com/uri-ocean-robotics/stonefish
```

- Install dependencies using `sudo apt install` (instruction from the [Stonefish](https://github.com/patrykcieslak/stonefish))
    * **OpenGL Mathematics library** (libglm-dev, version >= 0.9.9.0)
    * **SDL2 library** (libsdl2-dev, may need the following fix!)
        1. Install SDL2 library from the repository.
        2. `cd /usr/lib/x86_64-linux-gnu/cmake/SDL2/`
        3. `sudo vim sdl2-config.cmake`
        4. Remove space after "-lSDL2".
        5. Save file.
    * **Freetype library** (libfreetype6-dev)

- Build and install the stonefish
    ```bash
    cd stonefish
    mkdir build
    cd build
    cmake -DCMAKE_BUILD_TYPE=Release ..
    make -j$(nproc)
    sudo make install
    ```

### Setup ALPHA IMG Repo
- Clone `alpha_img_auv` repo
    ```bash
    git clone https://github.com/GSO-soslab/alpha_img_auv
    ```
- You can run the similar commands for other AUVs.
- Install pip and setup python3 as default
    ```bash
    sudo apt install python3-pip
    ```    

### Install ROS-MVP 
Currently MVP packages should be build from the source.
Target platform must be Ubuntu 20.04 because of the dependencies.

Pull repository and other dependencies
```bash
git clone --single-branch --branch noetic-devel https://github.com/uri-ocean-robotics/mvp_msgs
git clone --single-branch --branch noetic-devel https://github.com/uri-ocean-robotics/mvp_control
git clone --single-branch --branch noetic-devel https://github.com/uri-ocean-robotics/mvp_mission
git clone --single-branch --branch noetic-devel https://github.com/GSO-soslab/mvp_utilities.git
git clone --single-branch --branch noetic-devel https://github.com/uri-ocean-robotics/stonefish_mvp
git clone --single-branch --branch main https://github.com/GSO-soslab/world_of_stonefish.git
```    

**stonefish_mvp** is a wrapper modified from [stonefish_ros](https://github.com/patrykcieslak/stonefish_ros) for ROS interface with ROS-MVP.

### Hardware drivers (Not needed for simulation)
- Clone [mvp_core] repo which include other hardware related source code, sensor drivers, and other utilities.

    ```bash
    git clone --single-branch --branch noetic-devel https://github.com/GSO-soslab/mvp_core.git
    ```

- Install Dependencies

Install all submodules for `mvp_core`
```sh
cd mvp_core
git submodule update --init --recursive
```

- Install a specific submodule 
```sh
cd mvp_core
git submodule update <specific path to submodule>
```

- Install required submodules of Pi for ALPHA IMG AUV
```sh
cd mvp_core/external
git submodule update --init --recursive ROS_MSCL power_monitor waterlinked_dvl bluerobotics_pressure uno_lqe xsens_mti_ros_driver
```
- Install required submodules of Jetson for ALPHA IMG AUV
```sh
cd mvp_core/external
git submodule update --init --recursive bluerobotics_ping360 blueprint_oculus_sonar
```

Install dependencies for required ROS packages
```bash
cd /Your_WorkSpace/
rosdep install --from-paths src --ignore-src --rosdistro ${ROS_DISTRO} -y
```

### Compile the code
go back to the ROS Workspace dir (e.g., catkin_ws), then do
```bash
catkin_make
```


## Quick test
- Bring up the ALPHA Standard AUV with the Stonefish simualtor.

```bash
roslaunch alpha_img_bringup bringup_simulation.launch
```

- Enable the controller in a separated terminal
```bash
rosservice call /alpha_img_auv/controller/enable
```

- Start a path following mission in local frame where your waypoint is defined in `alpha_img_config/mission/param/path_local.yaml`

```bash
rosservice call /alpha_img_auv/helm/change_state "state: 'survey_3d'"
```

- You can put AUV in idle anytime by changing the state of the helm

```bash
rosservice call /alpha_img_auv/helm/change_state "state: 'start'"
```

- Note: Make sure you selected the correct topics for the Markers in the RViz window.


## Citation

The ALPHA paper:

```
@inproceedings{
    ALPHA_PAPER,
    title = {Acrobatic Low-cost Portable Hybrid AUV (ALPHA): System Design and Preliminary Results},
    author={Zhou, Mingxi and Gezer, Emir Cem and McConnell, William and Yuan, Chengzhi},
    booktitle={OCEANS 2022: Hampton Roads},
    year={2022},
    organization={IEEE}
}
```

The MVP paper:

```
@inproceedings{
    ALPHA_PAPER,
    title = {Working toward the development of a generic marine vehicle framework: ROS-MVP},
    author={Gezer, Emir Cem and Zhou, Mingxi and Zhao, Lin and McConnell, William},
    booktitle={OCEANS 2022: Hampton Roads},
    year={2022},
    organization={IEEE}
}
```


## Funding
This work is supported by the [National Science Foundation](https://www.nsf.gov/) award [#2154901](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2154901&HistoricalAwards=false) and award [#2221676](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2221676&HistoricalAwards=false)
