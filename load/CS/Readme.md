# Central Station emulator
## Description
We use Central Station emulators on staff machines for Performance testing.

Used protocols: 
- MLR 
- FEP
- VISNAP

## Setup
Setup Central Station on IPMP server

- Go to IPMP->SETTINGS->Central Stations tab and click on "+ ADD CENTRAL STATION"
-	Enter data: 
	 - Name - SG (or FEP,VIS)
	 - Protocol - MLR2 MAS SIA L3(or FEP XML/SIA,VIS NAP/SIA)
	 - Host - 94.125.123.149 (or any other staff machine)
	 - Port - 1111 (or any other)
	 - All other values stay in default 



## RUN CS EMULATOR
- For launch cs emulator use command on staff machine: 

	`cs 1111 SG -logname=sg.log -logsize 100 --per_account_log -events_db_size=10000`

	(where 1111 - port, SG - mlr2 or FEP - fep or VIS - visnap,sg.log = logname of log file,logsize - 100MB,per_account_log - separate log file and pictures by folders,events_db_size - size of buffer of saved events in local db)
- Set events forwarding for Main Group to Central station emulators

***Note:***

**At first, we make setup then launch cs emulator and, then we can launch forwarding**

Activate environment before launch emulator

In **launch.sh** we can start 3 emulator from one shell script.

For --per_account_log parameter need to change limit of opened files
```
/etc/security/limits.conf
*     soft   nofile  102400
```

