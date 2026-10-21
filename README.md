# RGB Lamp

A electronic shelving (1.8m) to put your other projects here. This is simple shelving called electronic because the shleving have a 8 RGB Lamps in top every shelf. You can just download materials and print/solder this :)

## Why I made this
I find shelving like this in marketplace but not electronic and take idea :D

## Features

- 7 modes: Aqua, White, Yellow, Red, Purple, Blue, Green, Lime, Indigo, Soft Peach
- Brightness from 10% to 100% in steps of 10%
- Settings (mode and brightness) are saved and restored after power loss
- Custom round PCB designed in KiCad
- USB-C powered

## Pictures

### Full 3D model
<img width="1581" height="786" alt="Снимок экрана 2026-10-20 182552" src="https://github.com/user-attachments/assets/bd889908-8a5e-4d59-9107-14e9b28497de" />

### PCB
<img width="1675" height="891" alt="Снимок экрана 2026-10-18 222913" src="https://github.com/user-attachments/assets/04f3a367-f86c-4f67-8f1c-4ad8be2ebef6" />

## How it works
It works (RGB Lamps) with batery and firmware. Without firmware this shelving transforms to defoult shelving. Prease use with firmware!

## Controls

| Action                          | Result                          |
|---------------------------------|---------------------------------|
| Button 1: hold for 2 seconds    | Turn the lamp on / off (fade)   |
| Button 1: short press           | Next mode                       |
| Button 1: double press          | Brightness +10%                 |
| Button 2: short press           | Previous mode                   |
| Button 2: quick repeated press  | Brightness −10%                 |

## How to assemble
1. Print the PCB from JLPPCB's website or app
2. Print all .step files
3. Upload firmware to PCB
4. Collect all components(Take a look at the screenshots if you're having trouble)
5. Place it on your room and continue doing your other projects.

## Role of hack club
All this project will be sponsered by Hack club forge. A lot of thanks for you. You helped me do my dreams in real life. Hack club is working since 2015 so A new era of engineers is approaching. 

## How to flash

1. Install [Thonny](https://thonny.org/).
2. Flash MicroPython to the ESP32 (Thonny: *Tools → Options → Interpreter → Install or update MicroPython*).
3. Open `firmware/firmware.py` in Thonny.
4. Save it to the board as `main.py` (*File → Save as → MicroPython device*).
5. Restart the board. The OLED shows a loading bar and the lamp is ready.

## Bill of Materials (BOM)
|Name                                |Cost   |Link                                                                                                                                                           |
|------------------------------------|-------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
|ESP32 C3                            |$1.8   |https://aliexpress.ru/item/1005007676793679.html?shpMethod=AE_CN_SUPER_ECONOMY_G&sku_id=12000041769821205&spm=a2g2w.productlist.search_results.4.677f53633EnYjH|
|Diodes 1n4148                       |$0.7   |https://aliexpress.ru/item/1005007807649334.html?shpMethod=AE_CN_SUPER_ECONOMY_G&sku_id=12000042270438468&spm=a2g2w.productlist.search_results.2.1b7fad9fg6OJxq|
|RGB diodes                          |$18.54 |https://aliexpress.ru/item/1005002055349908.html?shpMethod=AE_CN_SUPER_ECONOMY_G&sku_id=12000034806960298&spm=a2g2w.productlist.search_results.2.7ffc338eJBxLZL|
|OLED display                        |$1.35  |https://aliexpress.ru/item/1005004572487969.html?shpMethod=AE_CN_SUPER_ECONOMY_G&sku_id=12000029674573173&spm=a2g2w.productlist.search_results.0.52ee537fxKO4CA|
|Buttons                             |$1.1   |https://aliexpress.ru/item/1005008653041072.html?shpMethod=CAINIAO_STANDARD&sku_id=12000046105949461&spm=a2g2w.productlist.search_results.17.67561fadfEL0GK    |
|Buzzer                              |$1.36  |https://aliexpress.ru/item/1005006000025929.html?shpMethod=AE_CN_SUPER_ECONOMY_G&sku_id=12000059707835705&spm=a2g2w.productlist.search_results.3.17d02d3defQwav|
|Socket                              |$2.08  |https://aliexpress.ru/item/1005009725016771.html?spm=a2g2w.cart.cart_split.15.6b284aa6VQwMUn&sku_id=12000049959236831                                          |
|Felament price for all of step files|       |                                                                                                                                                               |
|All step files                      |$489.45|                                                                                                                                                               |
| Print PCB | $11 |


## Credits
- CAD: Blender, PCB: KiCad
- Everything else (design, PCB, firmware): Rasul
