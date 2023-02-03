#### Live plot OAK-D IMU Data with MatplotLib
That's a good idea to check that your data looks good. Let's use MatplotLib and have fun with cahrt-port

```bash
    conda create --name Live_Plot_IMU python=3.10 pip
    conda activate Live_Plot_IMU
    pip install -r requirements.txt
    python main.py # Don't forget to connect your camera
```

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

