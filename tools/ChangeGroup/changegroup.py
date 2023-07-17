from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


server="http://XXX"

login="XXX"
passwd="XXX"

while(True): # each 6 min
    driver = webdriver.Chrome()
    #open server window and login
    driver.get(server)
    driver.maximize_window()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='root']/div/form/div/div[2]/label[1]/span/input").send_keys(login)
    driver.find_element_by_xpath("//*[@id='root']/div/form/div/div[2]/label[2]/span/input").send_keys(passwd)
    driver.find_element_by_xpath("//*[@id='root']/div/form/div/div[3]/button/span").click()
    time.sleep(1)

    #uncomment only first time for choose by 200 panels
    #time.sleep(1)
    #driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[2]/div[3]/div[1]").click()
    #time.sleep(1)
    #driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div/div/div[4]").click()

    #change group to default
    driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div/label/input").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div/label/div/div/div/div[13]").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div/label/div/div/div/div[1]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div/label/input").click()
    time.sleep(1)
    # driver.find_element_by_xpath("/html/body/div/div/div[2]/div[1]/div[1]/div/div[1]/div[2]/div/label/div/div/div/div[14]").click()
    # time.sleep(1)
    # driver.find_element_by_xpath("//*[text()='HS3248']").click()
    # time.sleep(2)

    #
    #
    #select 800 panels
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[2]/div[1]/span/label/span").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[2]/div[1]/span/label/span").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[2]/div[5]/div[2]/button[2]").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[2]/div[1]/span/label/span").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[2]/div[5]/div[2]/button[2]").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[2]/div[1]/span/label/span").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[2]/div[5]/div[2]/button[2]").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[2]/div[1]/span/label/span").click()
    time.sleep(1)
    # driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[2]/div[5]/div[2]/button[2]").click()
    # time.sleep(1)
    # driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[2]/div[1]/span/label/span").click()
    # time.sleep(3)s
    #
    #
    #
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[2]/div[2]/span/span").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div/div[1]").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='root']/div/div[3]/div[2]/div/form/div/div[2]/div/div/label/span/input").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[text()='SECOND']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='root']/div/div[3]/div[2]/div/form/div/div[3]/button[2]/span").click()
    time.sleep(30)
    # driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div[1]/div[2]/div[1]/span").click()
    # time.sleep(1)
    # driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div/div[3]").click()
    # time.sleep(1)
    #
    #
    #
    #
    #quit
    driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div").click()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div/div[2]/div[5]").click()
    driver.quit()