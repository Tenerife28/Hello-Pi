# Hello Pi!

Hello Pi! Is a smart home assistant that uses local hosted AI to process its work. It uses the following:

* Raspberry Pi 4b
* 1.8inch 128x160 RGB TFT LCD on SPI
* INMP441 digital mic on i2s
* PAM8403 two channel amp
* 4ohm stereo speakers
* TTP223 capacitive button
* Gemma 4 e4b q4_k_m 7.5B

## LCD Pinout

| Pin | Function | Wire Color | Connection |
| :--- | :--- | :--- | :--- |
| GND | Ground | BLACK | GND |
| VCC | 3.3V | WHITE | 3V3 |
| SCL | Serial Clock | GREY | GPIO11 |
| SDA | Serial data input | VIOLET | GPIO10 |
| RES | Reset display (high for n/o) | BLUE | GPIO4 |
| DC | Select Channel | GREEN | GPIO17 |
| CS | Chip Select | YELLOW | GPIO8 |
| BLK | Backlight Control | ORANGE | GPIO22 |

## MIC Pinout

| Pin | Function | Wire Color | Connection |
| :--- | :--- | :--- | :--- |
| VDD | 3.3V | GREY | 3V3 |
| GND | Ground | WHITE | GND |
| SCK | I2S clock BCLK | BLUE | GPIO18 |
| WS | I2S word select LRCLK | GREEN | GPIO19 |
| SD | I2S data out | VIOLET | GPIO20 |
| L/R | Select Channel | YELLOW | GPIO23 |

## BUTTON Pinout

| Pin | Function | Wire Color | Connection |
| :--- | :--- | :--- | :--- |
| VDD | 3.3V | RED | GPIO6 |
| I/O | Low/High | BROWN | GPIO26 |
| GND | GROUND | BLACK | GND |
