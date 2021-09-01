appConfig = {
    "UDP_IP_ADDRESS": "192.168.137.232",
    "ESP_IP_ADDRESS": "192.168.137.209",
    "UDP_PORT_NO": "44444",
    "GRAPHIC_SIMULATION": True,
    "GPS_SIMULATION": True,
    "CAMERA_SIMULATION": False,
    "GYRO_SIMULATION": True,
}

graphAxisRanges = {
    "SEC_AXIS_RANGE": 7,
    "TEMPERATURE": {
        "MIN": 30,
        "MAX": 34,
    },
    "HEIGHT": {
        "MIN": 530,
        "MAX": 540,
    },
    "VOLTAGE": {
        "MIN": 3.3,
        "MAX": 4.5,
    },
    "PRESSURE": {
        "MIN": 1034,
        "MAX": 1019,
    },
    "DESCENT_RATE": {
        "MIN": -1,
        "MAX": 2,
    },
    "ROLLING_COUNT": {
        "MIN": 0,
        "MAX": 50,
    }
}

simulationConf = {
    "PROC_TIME": 1000000,
    "INTERVAL": 1
}

# Time (sec)
# Height (m) 1000
# Voltage (v) 11 - 12.5
# Pressure (Pa) 900 - 1050 bar
# Descent Rate 0 - 20 m/s
# Rolling Count 0 - 1200

# print(uniform(1, 1.3))
