from plotly.offline import plot
import pandas as pd
import plotly.graph_objects as go
import zipfile
from selenium import webdriver
import time

from selenium.common.exceptions import NoSuchElementException
import os
from config import *
import subprocess

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger()
level = logging.INFO
logger.setLevel(level)
_formater = logging.Formatter('%(asctime)s - %(message)s')
shandler = logging.StreamHandler()
shandler.setFormatter(_formater)
logger.addHandler(shandler)
path = "Download/"


charts = [['software',
           {'Connected Panels': 'panel-50','Discovery count (relative)': 'panel-52',
            'Online BBA and GPRS events': 'panel-54','Offline BBA and GPRS events': 'panel-56',
            'Total/video events rate': 'panel-64','Processed films frames': 'panel-62',
            'itv2, fibro and pmax events rate': 'panel-58','Smart Comm': 'panel-96',
            'itv2, fibro and pmax events latency': 'panel-60','Latency of sending Smart Comm event to Central Station': 'panel-98',
            'Smart Comm latency': 'panel-99','Application processing queues': 'panel-66',
            'DCODE changes on Pmax panels': 'panel-70','ITv2 notifications rate': 'panel-78',
            'ITv2 notifications latency': 'panel-80','Fibro transmitters count': 'panel-76',
            'Push notifications': 'panel-68','Interactive logins count': 'panel-72',
            'Processes count': 'panel-82','Threads waiting DB': 'panel-86',
            'Sent emails': 'panel-90','Sent SMS': 'panel-92'
            }],
          ['hardware',
           {'CPU': 'panel-98', 'CPU System': 'panel-134',
            'CPU User': 'panel-102', 'Load avarage': 'panel-100',
            'Memory': 'panel-17', 'Context switches': 'panel-136',
            'virtual memory': 'panel-106', 'resident memory': 'panel-108',
            'Num processes': 'panel-104', 'Num threads': 'panel-138',
            'Count of processes restart (exits)': 'panel-140',
            'TCP connections': 'panel-145',
            'Established TCP connections': 'panel-128', 'Conntrack Entries Limit': 'panel-132',
            'UDP Stats': 'panel-130', 'Disk IOs per Device': 'panel-118',
            'Disk Utilization per Device': 'panel-116', 'read bytes': 'panel-110',
            'write bytes': 'panel-112', 'Disk Space Used': 'panel-114',
            'Disk Throughput per Device': 'panel-120', 'Disk Queue Length': 'panel-122',
            'Open filedescs': 'panel-142', 'Worst filedesc ratio': 'panel-143',
            'Wchan threads': 'panel-144'
            }],
          ['mysql',
           {'MySQL Connections': 'panel-92', 'MySQL Client Thread Activity': 'panel-10',
            'MySQL Questions': 'panel-53', 'MySQL Thread Cache': 'panel-11',
            'MySQL Temporary Objects': 'panel-22', 'MySQL Select Types': 'panel-311',
            'MySQL Sorts': 'panel-30', 'MySQL Slow Queries': 'panel-48',
            'MySQL Aborted Connections': 'panel-47', 'MySQL Table Locks': 'panel-32',
            'MySQL Network Traffic': 'panel-9', 'MySQL Network Usage Hourly': 'panel-381',
            'MySQL Internal Memory Overview': 'panel-50', 'Top Command Counters': 'panel-14',
            'Top Command Counters Hourly': 'panel-39', 'MySQL Handlers': 'panel-8',
            'MySQL Transaction Handlers': 'panel-28', 'Process States': 'panel-40',
            'Top Process States Hourly': 'panel-49', 'MySQL Query Cache Memory': 'panel-46',
            'MySQL Query Cache Activity': 'panel-45', 'MySQL File Openings': 'panel-43',
            'MySQL Open Files': 'panel-41', 'MySQL Table Open Cache Status': 'panel-44',
            'MySQL Open Tables': 'panel-42'
            }],
#removed 'InnoDB Checkpoint Age': 'panel-19' and 'InnoDB Change Buffer Activity': 'panel-40' and 'Index Condition Pushdown (ICP)': 'panel-48' and
# 'InnoDB Change Buffer': 'panel-39'because of broken metric
          ['innodb',
           {'InnoDB Transactions': 'panel-20',
            'InnoDB Row Operations': 'panel-23', 'InnoDB Row Lock Time': 'panel-46',
            'InnoDB I/O': 'panel-38', 'InnoDB Log File Usage Hourly': 'panel-37',
            'Innodb Logging Performance': 'panel-50', 'InnoDB Deadlocks': 'panel-47',
            'InnoDB Buffer Pool Content': 'panel-42',
            'InnoDB Buffer Pool Pages': 'panel-3', 'InnoDB Buffer Pool I/O': 'panel-21',
            'InnoDB Buffer Pool Requests': 'panel-41', 'Innodb Read-Ahead': 'panel-49'
            }]
          ]



def archive_html():
    logger.info(f"Make archive from {html} file")

    with zipfile.ZipFile('./report.zip', 'w') as _zip:
        _zip.write(html, compress_type=zipfile.ZIP_DEFLATED)
        _zip.close()


class HtmlGenerator:

    def __init__(self, _logger: object, chart_dict: list):
        self.logger = _logger
        self.chart_dict = chart_dict
        self.title: str
        self.path: str
        self.chart = []

    def graphic_creator(self):
        dataframe = pd.read_csv(self.path, sep=',')
        lines = sorted(dataframe)
        lines.remove('Time')
        data = []
        for i in lines:
            values = go.Scatter(
                x=dataframe['Time'],
                y=dataframe[i],
                name=i
            )
            data.append(values)
        layout = go.Layout(title=self.title)

        figure = go.Figure(data=data, layout=layout)
        f2 = go.FigureWidget(figure)
        return plot(f2, include_plotlyjs=False, output_type='div')

    def chart_creator(self):
        self.logger.info(f"Parsing CSV from 'data' dir")

        for property in self.chart_dict:
            self.chart.append('<indent><h3> ' + property[0].title() + ' metrics </h3></indent>')
            for name, id in property[1].items():
                self.title = name
                self.path = f'./data/{property[0]}/{id}.csv'
                if os.path.isfile(self.path):
                    self.chart.append(self.graphic_creator())

    def gen_html(self):

        str_chart = '\n'.join(self.chart)
        self.html_str = f"""
        
        <!doctype html>
        
        <html lang="en">
        <head>
          <meta charset="utf-8">
        
          <title>Report</title>
          <meta name="description" content="Report">
          <meta name="author" content="SitePoint">
          <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
          <link rel="stylesheet" href="css/styles.css?v=1.0">
        
        </head>
        
        <body>
            <indent><h4> Notes:</h4></indent>
            <p>{notes}</p>
             {str_chart}
        </body>
        </html>
        """
        return self.html_str

    def write_html(self):
        self.chart_creator()
        logger.info(f"Write date to the {html} file")
        with open(html, "w") as htm:
            htm.write(self.gen_html())
            htm.close()


class GetCSV:
    def __init__(self, _logger: object, chart: list):
        self.logger = _logger
        self.driver: object
        self.chrome: str
        self.chart = chart

    def check_dir(self, dir: str):
        if not os.path.isdir(dir):
            logger.info(f"Cteate dir {dir}")
            os.mkdir(dir)

    def check_dirs(self):
        pwd = os.getcwd()

        self.chrome = f'{pwd}/chromedriver'  # put your path to chrome driver!
        self.download_directory = f"{pwd}/Download/"  # put your path!

        self.check_dir(self.download_directory)
        self.check_dir(f'{pwd}/data')
        self.check_dir(f'{pwd}/data/hardware')
        self.check_dir(f'{pwd}/data/innodb')
        self.check_dir(f'{pwd}/data/mysql')
        self.check_dir(f'{pwd}/data/software')

        self.logger.info("DELETE old *.csv files")
        subprocess.Popen(["find", "./data", "-type", "f", "-name", "*.csv", "-delete"],
                         stdout=subprocess.PIPE).communicate()

    def check_exists_by_xpath(self):
        try:
            self.driver.find_element(By.XPATH, "//*[text()='Series joined by time']")
        except NoSuchElementException:
            return False
        return True

    def login(self):
        self.logger.info("Login")
        options = Options()
        preferances = {"download.default_directory": self.download_directory}
        options.add_experimental_option("prefs", preferances)
        options.headless = False

        self.driver = webdriver.Chrome(self.chrome, options=options)

        # open url
        self.driver.maximize_window()
        self.driver.get(f"{grafana_host}/login")
        # login
        self.driver.find_element(By.NAME, "user").send_keys(user)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        time.sleep(1)
        # self.driver.find_element_by_xpath("/html/body/grafana-app/div/div/react-container/div/div/div[2]/div/div/form/button").click()
        self.driver.find_element(By.XPATH, "//*[@id='reactRoot']/div/div[2]/div[3]/div/div[2]/div/div/form/button").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, f"//*[text()='Load / Software stats and limits']").click()
        time.sleep(1)

    def set_up(self, property: str):
        self.logger.info(f"Set up GUI graphics property:{property}")
        if property == "software":
            # server selection
            self.logger.info("Set server")
            get_url = self.driver.current_url
            time.sleep(1)
            self.driver.get(f"{get_url}&var-instance={server}")
            self.logger.info("Set time range selection")
            # time range selection:
            time.sleep(2)
            self.driver.find_element(By.XPATH, "//*[text()='Last 1 hour']").click()
            time.sleep(1)
            #time from
            self.driver.find_element(By.XPATH,
                "//*[@id='reactRoot']/div/div[2]/div[3]/div[1]/div/div[6]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/input").clear()
            self.driver.find_element(By.XPATH,
                "//*[@id='reactRoot']/div/div[2]/div[3]/div[1]/div/div[6]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/input").click()
            self.driver.find_element(By.XPATH,
                "//*[@id='reactRoot']/div/div[2]/div[3]/div[1]/div/div[6]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div/input").send_keys(
                time_from)
            # self.driver.find_element_by_xpath("//*[text()='now-1h']").send_keys(time_from)
            time.sleep(10)
            # time to
            self.driver.find_element(By.XPATH,
                "//*[@id='reactRoot']/div/div[2]/div[3]/div[1]/div/div[6]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[3]/div[2]/div/div/input").clear()
            self.driver.find_element(By.XPATH,
                "//*[@id='reactRoot']/div/div[2]/div[3]/div[1]/div/div[6]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[3]/div[2]/div/div/input").click()
            self.driver.find_element(By.XPATH,
                "//*[@id='reactRoot']/div/div[2]/div[3]/div[1]/div/div[6]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[3]/div[2]/div/div/input").send_keys(
                time_to)
            time.sleep(1)
            # Apply
            self.logger.info("Apply settings on the GUI")
            self.driver.find_element(By.XPATH,"//*[text()='Apply time range']").click()
            time.sleep(10)


        elif property == "hardware":
            self.driver.find_element(By.XPATH, "//*[text()='Load / Hardware stats and limits']").click()
            time.sleep(20)

        elif property == "innodb":
            self.driver.find_element(By.XPATH, "//*[text()='MySQL InnoDB Metrics']").click()
            time.sleep(20)

        elif property == "mysql":
            self.driver.find_element(By.XPATH, "//*[text()='MySQL Overview']").click()
            time.sleep(20)

    def get_csv(self):

        for property in self.chart:
            self.set_up(property=property[0])
            for k, v in property[1].items():
                self.logger.info(f"Get chart: {k} from id {v}")
                time.sleep(1)
                self.driver.find_element(By.XPATH, f"//*[text()='{k}']").location_once_scrolled_into_view
                self.driver.find_element(By.XPATH, f"//*[text()='{k}']").click()
                time.sleep(5)
                # self.driver.find_element_by_xpath(f"//*[@id='reactRoot']/div/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/div/div[1]/div/div[1]/div/div/div[2]/div/ul/li[4]/a/span[1]").click() #оттута
                self.driver.find_element(By.XPATH, f"//*[text()='Inspect']").click() #тут2
                time.sleep(2)
                self.driver.find_element(By.XPATH, "//*[text()='Data options']").click()
                self.driver.find_element(By.XPATH, f"/html/body/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]").click()
                if self.check_exists_by_xpath() == True:
                    self.driver.find_element(By.XPATH, f"//*[text()='Series joined by time']").click()
                    self.driver.find_element(By.XPATH, f"//*[text()='Download CSV']").click()
                else:
                    self.driver.find_element(By.XPATH, f"/html/body/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]").click()
                    time.sleep(1)
                    self.driver.find_element(By.XPATH, f"//*[text()='Download CSV']").click()

                time.sleep(3)
                self.driver.find_element(By.XPATH, f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/button[2]").click()
                time.sleep(3)
                filename = os.listdir(path)
                os.rename(path + filename[0],  f'data/{property[0]}/{v}.csv')
                time.sleep(2)


    def exit(self):
        self.driver.quit()


if __name__ == "__main__":
    logger.info("### PART 1 ### /////////// Download CSV files => ")
    csv = GetCSV(_logger=logger, chart=charts)
    csv.check_dirs()
    csv.login()
    csv.get_csv()
    time.sleep(10)
    csv.exit()

    logger.info("### PART 2 ### /////////// Parse CSV files => ")
    Htm = HtmlGenerator(_logger=logger, chart_dict=charts)
    Htm.write_html()
    archive_html()
