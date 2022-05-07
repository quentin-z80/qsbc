# qsbc

## About

Specs:

- i.MX6ULL ARM Cortex-A7
- 512MB DDR3L
- 4MB QSPI Flash
- MicroSD card slot
- USB Type-C DRP and USB Type-A port
- 10/100M Ethernet
- Dual 36 pin GPIO headers
- PF1510 PMIC
- USB Type-C Power in

![](img/qsbc_top.png)
![](img/qsbc_bottom.png)

## Setup

### Flashing u-boot

  1. Build `imx_usb_loader`

        ```
        git clone git@github.com:boundarydevices/imx_usb_loader.git
        cd imx_usb_loader
        make
        ```

  2. Build `u-boot`

        ```
        git clone git@gitlab.com:quentin-z80/u-boot.git
        cd u-boot
        export CROSS_COMPILE=arm-linux-gnueabi- ARCH=arm
        make qsbc_defconfig
        make
        ```

  3. Build `qspi-header`

        ```
        cd tools/qspi-header
        ./qspi-header.sh qspi-nor-winbond-w25q32jv-config qspi-config.bin
        ```

  4. Connect to board over serial and load `u-boot` over usb

        ```
        screen /dev/ttyUSB0 115200
        ./imx_usb_loader /path/to/u-boot/u-boot-dtb.imx
        ```

  5. Transfer `qspi-header` over XMODEM or any other method and flash

        ```
        sf probe
        sf erase 0x0 0x400000
        loadx
        ```

        in screen hit `Ctrl-A` followed by `:`

        ```
        exec !! sx /path/to/qspi-header/qspi-config.bin
        sf write $loadaddr 0x400 $filesize
        ```

  6. Transfer `u-boot` over XMODEM or any other method and flash

        ```
        loadx
        ```

        in screen hit `Ctrl-A` followed by `:`

        ```
        exec !! sx /path/to/u-boot/u-boot-dtb.imx
        sf write $loadaddr 0x1000 $filesize
        ```

  7. Blow fuses to boot from qspi

        ```
        fuse prog -y 0 5 0x10 #BOOT_CFG1[4] = 1
        fuse prog -y 0 6 0x10 #BT_FUSE_SEL = 1
        ```

## TODO

### Rev 3
- Use interrupt for ETH PHY
- Swap USB-A and USB-C Locations

### Linux
- Port PF1510 driver
