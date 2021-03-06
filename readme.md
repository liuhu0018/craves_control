# Introduction

This repository is the control module of [CRAVES](http://craves.ai/). 
This repository contains hardware drivers, pose estimator, a PID-like controller, and a RL-based controller.  

## Hardware Requirement:

- USB Camera (Logitech C920)
- Robotic Arm (OWI-535)

## Software Requirement:

- Python>=2.7, Gym, CV2, Matplotlib, Numpy, Pytorch, Pyusb

It is easy to install craves_control, just run
```bash
git clone https://github.com/zfw1226/craves_control.git
cd craves_control
pip install -e . 
```

### Modify Permission in Linux
If your OS is Linux, you need modify your system to allow all users access to the arm via usb, 
just copy the file `42-usb-arm-permissions.rules` to `/etc/udev/rules.d`, running as:

```bash
sudo cp 42-usb-arm-permissions.rules /etc/udev/rules.d/42-usb-arm-permissions.rules
```

### Virtual Environment
If you want to train/evaluate a new RL agent in virtual environment, 
please install [Gym-UnrealCV](https://github.com/zfw1226/gym-unrealcv).

# Usage

## Running A Simple Demo
Firstly, please place the camera to a position viewing the arm.
After that run the following command:
```
python craves_control/demo_control.py --kp --pose 0 0 0 0
```
The arm will move to an expected pose ``(0, 0, 0, 0)`` in a few seconds.

## Reacher
The reacher aims to move the arm to make the grip reach a expected location. 
The policy network is trained by [DDPG](https://arxiv.org/abs/1509.02971), a conventional RL algorithm for continuous action.
Firstly, you can evaluate the policy network in virtual environment, running:
```
cd ddpg
python main.py --gpu-ids 0 --rescale --test --env UnrealArm-ContinuousPose-v1 --model-dir models/best.pt
```
After that, the arm will move to nine points sequentially, as:
![reach-virtual](./figs/reach-virtual.gif)

If your hardware is ready, you can run the pose estimator and RL controller jointly:
```bash
python main.py --gpu-ids 0 --rescale --test --env RealArm --model-dir models/best.pt 
```
After running, the arm will automatically move to an initial position at first, 
and then reach a set of points one by one, as:
![reach1](./figs/reach1.gif)

It is also robust to different viewpoint, as:
![reach2](./figs/reach2.gif)

## Citation
If you found CRAVES useful, please consider citing:
```bibtex
@article{zuo2019craves,
  title={CRAVES: Controlling Robotic Arm with a Vision-based, Economic System},
  author={Zuo, Yiming and Qiu, Weichao and Xie, Lingxi and Zhong, Fangwei and Wang, Yizhou and Yuille, Alan L},
  journal={CVPR},
  year={2019}
}
```

## Related Work
- Maplin/OWI USB Robot Arm Driver: https://github.com/eoinwoods/robot_arm
- Gym-UnrealCV: https://github.com/zfw1226/gym-unrealcv.git
- UnrealCV: https://github.com/unrealcv/unrealcv.git
- CRAVES: https://github.com/zuoym15/craves.ai.git