# ALPHA IMG AUV

## Introduction
This is the configuration for our ALPHA IMG AUV, the imaging-sonar vehicle of the ALPHA family. It carries the Blueprint Oculus forward-looking sonar, the Blue Robotics Ping360 mechanically scanned sonar, a fisheye camera and, in the near future, a Cerulean Omniscan 3D. For the ROS 1 (Noetic) configuration, see the `noetic_devel` branch.
- ROS2 version Jazzy,
- Ubuntu 24.04

## Directory structure
- `alpha_img_auv`: Meta package for the ALPHA IMG AUV.

- `alpha_img_bringup`: Launch files and sensor/localization configurations to bring the vehicle/simulation up running

- `alpha_img_config`: Configuration files for the MVP helm (`mvp_mission_config`) and controller (`mvp_control_config`).

- `alpha_img_description`: URDF files, rviz configuration, and vehicle mesh

## Installation

### Install the Stonefish simulator
- We use [Stonefish](https://stonefish.readthedocs.io/en/latest/install.html) Simulator. You can clone it from [here](https://github.com/GSO-soslab/stonefish), a fork from the [original_repo](https://github.com/patrykcieslak/stonefish).

- Download the stonefish simulator **to another location outside your ROS workspace**
```bash
git clone https://github.com/GSO-soslab/stonefish
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
    cd alpha_img_auv
    git checkout jazzy-devel
    ```
- 

- Install pip and setup python3 as default
    ```bash
    sudo apt install python3-pip
    ```

### Install ROS-MVP 
Currently MVP packages should be build from the source.
Target platform must be Ubuntu 24.04 because of the dependencies.

Pull repository and other dependencies
```bash
git clone --single-branch --branch jazzy-devel https://github.com/uri-ocean-robotics/mvp_msgs
git clone --single-branch --branch jazzy-devel https://github.com/GSO-soslab/stonefish_ros2.git
git clone --single-branch --branch jazzy-devel https://github.com/uri-ocean-robotics/mvp_control
git clone --single-branch --branch jazzy-devel https://github.com/uri-ocean-robotics/mvp_mission
git clone --single-branch --branch jazzy-devel https://github.com/uri-ocean-robotics/mvp_utilities.git
git clone --single-branch --branch jazzy-devel https://github.com/GSO-soslab/world_of_stonefish
```

**stonefish_ros2** is the ROS2 interface for Stonefish simulator.

### Hardware drivers (Not needed for simulation)
- Clone **mvp_hardware_drivers** repo which include other hardware related source code, sensor drivers, and other utilities.

    ```bash
    git clone --single-branch --branch jazzy-devel https://github.com/uri-ocean-robotics/mvp_hardware_drivers.git
    ```

- Install dependencies for **mvp_hardware_drivers**
```
cd mvp_hardware_drivers
git submodule update --init --recursive
```

- Install a specific submodule 
```
git submodule update <specific path to submodule>
```


### Compile the code
go back to the ROS Workspace dir (e.g., ros2_ws), then do
```bash
colcon build
```

## Quick test
- Bring up the ALPHA IMG AUV with the Stonefish simulator. This needs the `ocean_img.scn` world and `alpha_img.scn` vehicle in `world_of_stonefish` (see Known gaps).

```bash
ros2 launch alpha_img_bringup bringup_simulation.launch.py
```

- Enable the controller in a separated terminal
```bash
ros2 service call /alpha_img/controller/set std_srvs/srv/SetBool data:\ true\ 
```

- Start a path following mission in local frame where your waypoint is defined in L78-81 under bhv_path_following in  `alpha_img_auv/alpha_img_bringup/config/bhv_params_sim.yaml` 

```bash
ros2 service call /alpha_img/mvp_helm/change_state mvp_msgs/srv/ChangeState "{state: 'survey', caller: 'user'}"
```

- You can put AUV in idle anytime by changing the state of the helm

```bash
ros2 service call /alpha_img/mvp_helm/change_state mvp_msgs/srv/ChangeState "{state: 'start', caller: 'user'}"
```

- Note: Make sure you selected the correct topics for the Markers in the RViz window. `/alpha_img/bhv_path_following/path` & `/alpha_img/bhv_path_following/segment`


## Payload bringup (hardware)
The imaging payload runs on the Jetson, the navigation sensors on the Pi.

```bash
ros2 launch alpha_img_bringup bringup_sonars.launch.py   # Ping360 MSIS + Oculus FLS
ros2 launch alpha_img_bringup bringup_camera.launch.py   # DWE fisheye camera (usb_cam)
```

## Known gaps
- `world_of_stonefish` (`jazzy-devel`) has no `alpha_img` vehicle or `ocean_img` world yet, so the simulation launch will not start until they are added there.
- The MVP control gains in `alpha_img_config/mvp_control_config` are Rise starting values, not tuned for IMG. Only the thruster layout, limits and polynomials are carried over from the ROS 1 setup.
- The Waterlinked DVL topic (`dvl/raw_twist`) and the Microstrain/Madgwick chain have not been checked against the ROS 2 drivers on the vehicle.


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
    author={Gezer, Emir Cem and Zhou, Mingxi and Zhao, LIN and McConnell, William},
    booktitle={OCEANS 2022: Hampton Roads},
    year={2022},
    organization={IEEE}
}
```



## Funding
This work is supported by the [National Science Foundation](https://www.nsf.gov/) award [#2154901](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2154901&HistoricalAwards=false) and award [#2221676](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2221676&HistoricalAwards=false)
