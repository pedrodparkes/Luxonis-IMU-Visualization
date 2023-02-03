Here I collect small scripts that may help you understand Luxonis camera's
IMU a bit better.

#### 0. Read the manual first:
[Liuxonis » Nodes » IMU](https://docs.luxonis.com/projects/api/en/latest/components/nodes/imu/)

#### 1. Know your hardware:
There are 2 IMU options for Luxonis cameras. Bosch [BMI270](https://www.bosch-sensortec.com/products/motion-sensors/imus/bmi270/) and Bosch [BNO085](https://www.ceva-dsp.com/wp-content/uploads/2019/10/BNO080_085-Datasheet.pdf).
I have the one with [BMI270](https://www.bosch-sensortec.com/products/motion-sensors/imus/bmi270/).

Easiest way to check the installed IMU version is to ask it for ```GYROSCOPE_CALIBRATED``` data.
**BNO085** will work.
**BMI270** will rise an error:
```shell
    RuntimeError: IMU(0) - IMU invalid settings!: 
    GYROSCOPE_CALIBRATED output is unsupported. 
    BMI270 supports only ACCELEROMETER_RAW and/or GYROSCOPE_RAW outputs.
```

#### 2. Understand Camera axis directions:
#### [OAK-D IMU](https://docs.luxonis.com/projects/api/en/latest/components/nodes/imu/) Coordinate system. Camera look at you:
```shell
  CW rotation around any axis gives Positive Gyro Values
    Imagine looking from a positive point on the axis and turing the entity right.
            X
            |
            |
            *--------Y  
             \ 
              \ 
               Z
```


#### [Rotate 3D cube with IMU](3D_Cube_AHRS/README.md).
That's a good idea to check that your axis mapping is correct. Let's use [AHRS](https://pypi.org/project/AHRS/)
and [Ursina](https://www.ursinaengine.org) for visualization.

```bash
cd 3D_Cube_AHRS
conda create --name 3D_Cube_AHRS python=3.10 pip
conda activate 3D_Cube_AHRS
pip install -r requirements.txt
python main.py
```