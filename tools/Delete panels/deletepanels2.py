from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time


server="https://XXX"


login="XXX"

passwd="XXX"

while(True):
    # option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    # driver = webdriver.Chrome(options=option)
    driver = webdriver.Chrome()
#open server window and login
    driver.get(server)
    #driver.maximize_window()
    time.sleep(2)
    driver.find_element(By.XPATH,"//*[@id='root']/div/form/div/div[2]/label[1]/span/input").send_keys(login)
    driver.find_element(By.XPATH,"//*[@id='root']/div/form/div/div[2]/label[2]/span/input").send_keys(passwd)
    driver.find_element(By.XPATH,"//*[@id='root']/div/form/div/div[3]/button/span").click()
    time.sleep(5)

#select 800 panels
    time.sleep(2)
    driver.find_element(By.XPATH,"//*[@id='root']/div/div[2]/div[1]/div[2]/div[1]/span/label/span").click()
    time.sleep(4)
    driver.find_element(By.XPATH,"//*[@id='root']/div/div[2]/div[1]/div[2]/div[5]/div[2]/button[2]").click()
    time.sleep(9)
    driver.find_element(By.XPATH,"//*[@id='root']/div/div[2]/div[1]/div[2]/div[1]/span/label/span").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//*[@id='root']/div/div[2]/div[1]/div[2]/div[5]/div[2]/button[2]").click()
    time.sleep(9)
    driver.find_element(By.XPATH,"//*[@id='root']/div/div[2]/div[1]/div[2]/div[1]/span/label/span").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//*[@id='root']/div/div[2]/div[1]/div[2]/div[5]/div[2]/button[2]").click()
    time.sleep(9)
    driver.find_element(By.XPATH,"//*[@id='root']/div/div[2]/div[1]/div[2]/div[1]/span/label/span").click()
    time.sleep(2)

#service->delete->yes
    driver.find_element(By.XPATH,"//*[@id='root']/div/div[2]/div[1]/div[2]/div[2]/span").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div/div/div[9]").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//*[@id='root']/div/div[3]/div[2]/div/div/div[3]/button[2]/span").click()
    time.sleep(15)

#quit
    driver.find_element(By.XPATH,"//*[@id='root']/div/div[1]/div").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div/div/div[2]/div[5]").click()
    driver.quit()