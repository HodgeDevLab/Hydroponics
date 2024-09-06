# pin_config.py

# Power pins
P3V3_PIN_1 = 1    # 3.3V Power
P3V3_PIN_17 = 17  # 3.3V Power
P5V_PIN_2 = 2     # 5V Power
P5V_PIN_4 = 4     # 5V Power

# Ground pins
GND_PIN_6 = 6     # Ground
GND_PIN_9 = 9     # Ground
GND_PIN_14 = 14   # Ground
GND_PIN_20 = 20   # Ground
GND_PIN_25 = 25   # Ground
GND_PIN_30 = 30   # Ground
GND_PIN_34 = 34   # Ground
GND_PIN_39 = 39   # Ground

# GPIO pins (General Purpose I/O)
GPIO17_GEN0 = 11       # GPIO 17, General Purpose I/O
GPIO27_GEN2 = 13       # GPIO 27, General Purpose I/O
GPIO22_GEN3 = 15       # GPIO 22, General Purpose I/O
GPIO23_GEN4 = 16       # GPIO 23, General Purpose I/O
GPIO24_GEN5 = 18       # GPIO 24, General Purpose I/O
GPIO25_GEN6 = 22       # GPIO 25, General Purpose I/O
GPIO05_GEN1 = 29       # GPIO 5, General Purpose I/O
GPIO06_GEN2 = 31       # GPIO 6, General Purpose I/O
GPIO16_GEN4 = 36       # GPIO 16, General Purpose I/O
GPIO26_GEN7 = 37       # GPIO 26, General Purpose I/O
GPIO_ALL = (GPIO17_GEN0, GPIO27_GEN2, GPIO22_GEN3, GPIO23_GEN4,
            GPIO24_GEN5, GPIO25_GEN6)

# PWM pins (Pulse Width Modulation)
GPIO18_PWM0 = 12       # GPIO 18, PWM0 Output
GPIO12_PWM1 = 32       # GPIO 12, PWM1 Output
GPIO13_PWM1 = 33       # GPIO 13, PWM1 Output

# I2C pins
GPIO02_SDA1 = 3        # GPIO 2, I2C1 SDA (Data Line)
GPIO03_SCL1 = 5        # GPIO 3, I2C1 SCL (Clock Line)
GPIO00_ID_SD = 27      # GPIO 0, ID EEPROM I2C SDA
GPIO01_ID_SC = 28      # GPIO 1, ID EEPROM I2C SCL

# UART pins
GPIO14_TXD0 = 8        # GPIO 14, UART0 TXD (Transmit Data)
GPIO15_RXD0 = 10       # GPIO 15, UART0 RXD (Receive Data)

# SPI pins (Serial Peripheral Interface)
GPIO10_MOSI = 19       # GPIO 10, SPI0 MOSI (Master Out Slave In)
GPIO09_MISO = 21       # GPIO 9, SPI0 MISO (Master In Slave Out)
GPIO11_SCLK = 23       # GPIO 11, SPI0 SCLK (Serial Clock)
GPIO08_CE0 = 24        # GPIO 8, SPI0 CE0 (Chip Enable 0)
GPIO07_CE1 = 26        # GPIO 7, SPI0 CE1 (Chip Enable 1)
GPIO19_MISO1 = 35      # GPIO 19, SPI1 MISO (Master In Slave Out)
GPIO20_MOSI1 = 38      # GPIO 20, SPI1 MOSI (Master Out Slave In)
GPIO21_SCLK1 = 40      # GPIO 21, SPI1 SCLK (Serial Clock)
