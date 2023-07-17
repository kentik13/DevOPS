# How to use

1. Install required modules

```shell 
pip install -r  requirements.txt
```

2. Put your settings to the config.py:
 - hostname
 - time (from/to)
 - name of output file
 - notes
 - etc ...

3. Start main script. **Start and don't touch your computer mouse until process not finished !!!** 
```shell
python report.py
```
### This script will make next steps:

 - Download *.csv files 
 - Parse *.csv files into html charts
 - Archivating report.html in to report.zip


## Files 
  - **report.py**: Main script
  - **config.py**: Config file
  - **report.html**: Output **html** file
  - **report.zip**: Output **zip** file
