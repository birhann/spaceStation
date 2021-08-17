appConfig = {
    "UDP_IP_ADDRESS": "192.168.137.8",
    "ESP_IP_ADDRESS": "192.168.137.154",
    "UDP_PORT_NO": "44444",
    "GRAPHIC_SIMULATION": False,
    "GPS_SIMULATION": False,
    "CAMERA_SIMULATION": False,
    "GYRO_SIMULATION": False,
}

graphAxisRanges = {
    "SEC_AXIS_RANGE": 7,
    "TEMPERATURE": {
        "MIN": 0,
        "MAX": 60,
    },
    "HEIGHT": {
        "MIN": 0,
        "MAX": 1000,
    },
    "VOLTAGE": {
        "MIN": 11,
        "MAX": 12.5,
    },
    "PRESSURE": {
        "MIN": 900,
        "MAX": 1050,
    },
    "DESCENT_RATE": {
        "MIN": 0,
        "MAX": 20,
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
