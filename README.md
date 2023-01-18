# qsbc

## Specs

- i.MX8M Mini 4x 1.8GHz ARM Cortex-A53
- 4GB LPDDR4
- 4MB QSPI Flash
- 64GB eMMC
- M.2 2230 Slot
- MicroSD card slot
- 2x USB Type-C DRP
- USB Type-C Power in
- USB Type-C debug port
- 10/100/1000 Ethernet
- Displayport output

![](img/qsbc_top.png)
![](img/qsbc_bottom.png)
![](img/qsbc_top_blank.png)

## Flashing u-boot

1. Get `u-boot`

    ```
    git clone https://gitlab.com/quentin-z80/u-boot.git
    ```

2. Build `TF-A`

    ```
    git clone https://git.trustedfirmware.org/TF-A/trusted-firmware-a.git
    cd trusted-firmware-a
    TF_LDFLAGS="--no-warn-rwx-segment" make plat=imx8mm bl31
    cp build/imx8mm/release/bl31.bin ../u-boot/
    ```

3. Get i.MX8MM DDR Firmware

    ```
    wget https://www.nxp.com/lgfiles/NMG/MAD/YOCTO/firmware-imx-8.9.bin
    chmod +x firmware-imx-8.9.bin
    ./firmware-imx-8.9.bin
    cp firmware-imx-8.9/firmware/ddr/synopsys/lpddr4*.bin u-boot/
    ```

4. Build `u-boot` for SD card boot

    ```
    cd u-boot
    export CROSS_COMPILE=aarch64-linux-gnu- ARCH=arm64
    make qsbc_imx8mm_defconfig
    make
    sudo dd if=flash.bin of=/dev/mmcblk0 bs=1024 seek=32 conv=notrunc
    ```

5. Flash and boot `u-boot` from sd card

    ```
    sudo dd if=flash.bin of=/dev/mmcblk0 bs=1024 seek=32 conv=notrunc
    sudo tio -b 115200 /dev/ttyACM0
    ```

6. Build `u-boot` for QSPI boot

    ```
    make qsbc_imx8mm_fspi_defconfig
    make
    ```

7. Flash `u-boot` to QSPI

    ```
    u-boot=> run dfuspi
    sudo dfu-util -D flash.bin
    ```

## TODO

- USB-UART ICs need to have VDDIO derived from USB VBUS so they do not reset
on board reset

- USB VBUS fault pins need to be connected to usb phy oc pads, not gpio pins

- UART1 TXO is connected to the wrong pad

- Test displayport out, waiting for [imx8mm DSI support](https://lore.kernel.org/linux-arm-kernel/CAMty3ZC9TtnupJKF4LA9e-jnYMux28u4Pn3femJZXi4ogV+drA@mail.gmail.com/T/) to be mainlined
