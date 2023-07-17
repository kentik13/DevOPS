# Fibro Central Station emulator
## Description
We use Central Station emulators on staff machines for Performance testing.

Used protocols: 
- Fibro
## Setup
Setup Central Station on IPMP server

- Go to IPMP->SETTINGS->Central Stations tab and click on "+ ADD CENTRAL STATION"
-	Enter data: 
	 - Name - Fibro(or any)
	 - Protocol - Fibro SIA or CID
	 - Host - 94.125.123.159 (or any other staff machine)
	 - Port - 13062 (or any other)
	 - All other values stay in default 



## RUN CS EMULATOR
- For launch cs emulator use command on staff machine: 

    `./launch.sh 13062 1200`

    (where 13062 - port)
    (where 1200 - CS's count)
- Set events forwarding for Main Group to Central station emulators
