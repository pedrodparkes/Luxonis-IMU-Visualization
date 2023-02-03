#!/usr/bin/env python3

import depthai as dai
import matplotlib
# Select matplotlib backend for window
matplotlib.use('MacOSX')
from matplotlib import pyplot as plt
import collections

sources=['acceleroValues', 'gyroValues']
DATA_SOURCE=1

# IMU measurements / sec
ACC_FPS = 500
GYRO_FPS = 400
# Number of measurements in stack
PTS_N = 100

A_x = collections.deque(maxlen=PTS_N)
A_y = collections.deque(maxlen=PTS_N)
B_x = collections.deque(maxlen=PTS_N)
B_y = collections.deque(maxlen=PTS_N)
C_x = collections.deque(maxlen=PTS_N)
C_y = collections.deque(maxlen=PTS_N)
(line_gx,) = plt.plot(A_x, A_y, linestyle="--", label=sources[DATA_SOURCE]+'_X', color='red')
(line_gy,) = plt.plot(B_x, B_y, linestyle="--", label=sources[DATA_SOURCE]+'_Y', color='green')
(line_gz,) = plt.plot(C_x, C_y, linestyle="--", label=sources[DATA_SOURCE]+'_Z', color='blue')


plt.legend([line_gx, line_gy, line_gz], [sources[DATA_SOURCE]+'_X', sources[DATA_SOURCE]+'_Y', sources[DATA_SOURCE]+'_Z'], loc='upper left')

def realtime_plot(line_num, line_num_x, line_num_y, val_x, val_y):
    line_num_x.append(val_x)
    line_num_y.append(val_y)
    line_num.set_xdata(line_num_x)
    line_num.set_ydata(line_num_y)
    plt.gca().relim()
    plt.gca().autoscale_view()


# Create pipeline
pipeline = dai.Pipeline()
# Define sources and outputs
imu = pipeline.create(dai.node.IMU)
xlinkOut = pipeline.create(dai.node.XLinkOut)
xlinkOut.setStreamName("imu")
# enable ACCELEROMETER_RAW at ACC_FPS hz rate
imu.enableIMUSensor(dai.IMUSensor.ACCELEROMETER_RAW, ACC_FPS)
# enable GYROSCOPE_RAW at GYRO_FPS hz rate
imu.enableIMUSensor(dai.IMUSensor.GYROSCOPE_RAW, GYRO_FPS)
# it's recommended to set both setBatchReportThreshold and setMaxBatchReports to 20 when integrating in a pipeline with a lot of input/output connections
# above this threshold packets will be sent in batch of X, if the host is not blocked and USB bandwidth is available
imu.setBatchReportThreshold(1)
# maximum number of IMU packets in a batch, if it's reached device will block sending until host can receive it
# if lower or equal to batchReportThreshold then the sending is always blocking on device
# useful to reduce device's CPU load  and number of lost packets, if CPU load is high on device side due to multiple nodes
imu.setMaxBatchReports(10)
# Link plugins IMU -> XLINK
imu.out.link(xlinkOut.input)

# Pipeline is defined, now we can connect to the device
with dai.Device(pipeline) as device:

    def timeDeltaToMilliS(delta) -> float:
        return delta.total_seconds()*1000
    # Output queue for imu bulk packets
    imuQueue = device.getOutputQueue(name="imu", maxSize=50, blocking=False)
    baseTs = None
    while True:
        imuData = imuQueue.get()  # blocking call, will wait until a new data has arrived
        imuPackets = imuData.packets
        for imuPacket in imuPackets:
            acceleroValues = imuPacket.acceleroMeter
            gyroValues = imuPacket.gyroscope
            acceleroTs = acceleroValues.getTimestampDevice()
            gyroTs = gyroValues.getTimestampDevice()
            if baseTs is None:
                baseTs = acceleroTs if acceleroTs < gyroTs else gyroTs
            acceleroTs = timeDeltaToMilliS(acceleroTs - baseTs)
            gyroTs = timeDeltaToMilliS(gyroTs - baseTs)

            imuF = "{:.06f}"
            tsF  = "{:.03f}"

            # print(f"Accelerometer timestamp: {tsF.format(acceleroTs)} ms")
            # print(f"Accelerometer [m/s^2]: x: {imuF.format(acceleroValues.x)} y: {imuF.format(acceleroValues.y)} z: {imuF.format(acceleroValues.z)}")
            # print(f"Gyroscope timestamp: {tsF.format(gyroTs)} ms")
            print(f"Gyroscope [rad/s]: x: {imuF.format(gyroValues.x)} y: {imuF.format(gyroValues.y)} z: {imuF.format(gyroValues.z)} ")

            # Plot live data
            realtime_plot(line_gx, A_x, A_y, gyroTs, vars()[sources[DATA_SOURCE]].x)
            realtime_plot(line_gy, B_x, B_y, gyroTs, vars()[sources[DATA_SOURCE]].y)
            realtime_plot(line_gz, C_x, C_y, gyroTs, vars()[sources[DATA_SOURCE]].z)

            plt.pause(0.1)
