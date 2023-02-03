import time
import depthai as dai
import time
import math
from ursina import *
from ahrs.filters import Mahony
import numpy as np

# IMU measurements / sec
IMU_FPS = 100
# Mahony AHRS Params
Kp = 0.5
Ki = 0.3


# Init Mahony AHRS
orientation = Mahony(frequency=IMU_FPS, kp=Kp, ki=Ki) # frequency=average_imu_sps, kp=1, ki=0.3, q0=[0.7071, 0.0, 0.7071, 0.0]
num_samples = 1
# Init start location Quaternion
Q = np.tile([1., 0., 0., 0.], (num_samples, 1))

# Init Ursina
app = Ursina()
bw_texture = load_texture('../assets/bw_texture.jpg')
cube = Entity(model="cube", texture=bw_texture, scale=4)

# Create DAI pipeline
pipeline = dai.Pipeline()
# Define sources and outputs
imu = pipeline.create(dai.node.IMU)
xlinkOut = pipeline.create(dai.node.XLinkOut)
xlinkOut.setStreamName("imu")
# enable ACCELEROMETER_RAW at X hz rate
imu.enableIMUSensor(dai.IMUSensor.ACCELEROMETER_RAW, IMU_FPS)
# enable GYROSCOPE_RAW at X hz rate
imu.enableIMUSensor(dai.IMUSensor.GYROSCOPE_RAW, IMU_FPS)
imu.setBatchReportThreshold(1)
imu.setMaxBatchReports(10)
# Link plugins IMU -> XLINK
imu.out.link(xlinkOut.input)

# Pipeline is defined, now we can connect to the device
device = dai.Device(pipeline)
# with dai.Device(pipeline) as device:
imuQueue = device.getOutputQueue(name="imu", maxSize=50, blocking=False)

# Define cube update function
i=0
# Get current cube location from Ursina
curr = cube.get_quat()
print(1)
def update():
    # https://docs.panda3d.org/1.10/python/reference/panda3d.core.LQuaterniond
    imuData = imuQueue.get()  # blocking call, will wait until a new data has arrived
    imuPackets = imuData.packets
    for imuPacket in imuPackets:
        acceleroValues = imuPacket.acceleroMeter
        gyroValues = imuPacket.gyroscope
        imuF = "{:.06f}"
        # print(f"Gyroscope [rad/s]: x: {imuF.format(gyroValues.x)} y: {imuF.format(gyroValues.y)} z: {imuF.format(gyroValues.z)} ")
        # print(f"Accelerometer [m/s^2]: x: {imuF.format(acceleroValues.x)} y: {imuF.format(acceleroValues.y)} z: {imuF.format(acceleroValues.z)}")

        # Update orientation quaternion
        Q[i] = orientation.updateIMU(Q[i - 1], gyr=[-1 * gyroValues.z, -1 * gyroValues.x, gyroValues.y], acc=[-1 * acceleroValues.z, -1 * acceleroValues.x, acceleroValues.y])

        curr.setX(Q[i][2])
        curr.setI(-Q[i][0])
        curr.setJ(Q[i][1])
        curr.setK(-Q[i][3])
        # Set new cube rotation
        cube.set_quat(curr)

# Assign cube update function to Ursina
cube.update = update

# Run Ursina app
app.run()

