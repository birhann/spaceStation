appConfig = {
    "UDP_IP_ADDRESS": "192.168.137.232",
    "ESP_IP_ADDRESS": "192.168.137.209",
    "UDP_PORT_NO": "44444",
    "GRAPHIC_SIMULATION": False,
    "GPS_SIMULATION": False,
    "CAMERA_SIMULATION": False,
    "GYRO_SIMULATION": False,
}

graphAxisRanges = {
    "SEC_AXIS_RANGE": 7,
    "TEMPERATURE": {
        "MIN": 25,
        "MAX": 29,
    },
    "HEIGHT": {
        "MIN": 530,
        "MAX": 540,
    },
    "VOLTAGE": {
        "MIN": 1.50,
        "MAX": 1.65,
    },
    "PRESSURE": {
        "MIN": 1010,
        "MAX": 1020,
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
