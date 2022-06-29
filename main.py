from PyQt5.QtWidgets import *
import ui_main
import sys
import threading
from selenium import webdriver
from random import randrange
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pathlib
import csv
import requests
from ast import literal_eval
import random
import ctypes
from datetime import datetime
import time

default_url  = "https://www.reddit.com/r/nanocurrency/comments/ujtlh7/nano_in_the_carbon_almanac_can_we_persuade_seth/"

class Main(QDialog, ui_main.Ui_Dialog):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.flag = 1
        self.flag_comment = 1
        self.pushButton_start.clicked.connect(self.fnStart)
        self.lineEdit_url.setText(default_url)
        self.pushButton_start_comment.clicked.connect(self.fnComment)
    def parsetargetposturl(self, url):
        x = url[22:].split('/')
        temp = ""
        for i in range(0, 5):
            temp += x[i] + "/"
        return temp
    def parsePosturl(self, url):
        x = url[8:].split('/')
        temp = "https://"
        for i in range(0, 3):
            temp += x[i] + "/"
        return temp
    def parseCommentUrl(self, url):
        x = url[8:].split('/')
        temp = "https://"
        for i in range(0, 5):
            temp += x[i] + "/"
        temp += "comment/"
        return temp
    def get_id(self):
 
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def raise_exception(self, id):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
      
    def fnStart(self):
        if self.flag == 1:
            self.url = self.lineEdit_url.text()
            self.target = self.parsetargetposturl(self.url)
            self.url =  self.parsePosturl(self.url)
            self.active = self.comboBox_type.currentText()
            self.vote_count = self.spinBox_vote.value()
            self.window_count = self.spinBox_account.value()
            profile = []
            try:
                with open("profile.csv") as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        profile.append(row[0])
            except:
                QMessageBox.warning(self, "Error", "Profile.csv file isn't exist")
            if len(profile) < self.vote_count:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                with open("Reddit_log.txt", "a") as fp:
                    fp.write(dt_string + " Profile number is not enough than windows number")
                    fp.write('\n')
            self.pushButton_start.setText("Stop")              
            self.flag = 0
            print(self.vote_count)
            self.random_list = random.sample(profile, self.vote_count)
            print(self.random_list)
            self.thread_list = []
            
            self.currentthread_list = []
            if int(self.vote_count) <= int(self.window_count):
                self.window_count = self.vote_count
            for k in range(0, int(self.vote_count), int(self.window_count)):
                self.thread_list = self.random_list[k:k+self.window_count]
                self.per_list = []
                for i in range(0, len(self.thread_list)):
                    fnthread = AutoReddit(self.thread_list[i], self.url, self.active, self.target)
                    t = threading.Thread(target=fnthread.startAutomation)
                    self.per_list.append(t)
                    self.currentthread_list.append(self.thread_list[i])
                for i in range(0, int(self.window_count)):
                    self.per_list[i].start()
                for i in range(0, int(self.window_count)):
                    self.per_list[i].join()
        else:
            self.pushButton_start.setText("Start")
            for i in range(0, len(self.currentthread_list)):
                try:
                    stop_url = 'http://127.0.0.1:35000/profile/stop/'+self.currentthread_list[i]
                    resp = requests.get(stop_url)
                except:
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    with open("Reddit_log.txt", "a") as fp:
                        fp.write(dt_string + " " + self.currentthread_list[i] + " Exit Session Error")
                        fp.write("\n")
            self.flag = 1
    def fnComment(self):
        if self.flag_comment == 1:
            self.url_comment = self.lineEdit_url_comment.text()
            self.target_comment = str(self.url_comment[8:]).split('/')[-2:][0]

            self.url_comment = self.parseCommentUrl(self.url_comment)

            self.active_comment = self.comboBox_type_comment.currentText()
            self.vote_count_comment = self.spinBox_vote_comment.value()
            self.window_count_comment = self.spinBox_account_comment.value()
            profile = []
            try:
                with open("profile.csv") as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        profile.append(row[0])
            except:
                QMessageBox.warning(self, "Error", "Profile.csv file isn't exist")
            if len(profile) < self.vote_count_comment:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                with open("Reddit_log.txt", "a") as fp:
                    fp.write(dt_string + " Profile number is not enough than windows number")
                    fp.write('\n')
            self.pushButton_start_comment.setText("Stop")              
            self.flag_comment = 0
            self.random_list_comment = random.sample(profile, self.vote_count_comment)
            self.thread_list_comment = []
            
            self.currentthread_list_comment = []
            if int(self.vote_count_comment) <= int(self.window_count_comment):
                self.window_count_comment = self.vote_count_comment
            for k in range(0, int(self.vote_count_comment), int(self.window_count_comment)):
                self.thread_list_comment = self.random_list_comment[k:k+self.window_count_comment]
                self.per_list_comment = []
                for i in range(0, len(self.thread_list_comment)):
                    fnthread = AutoReddit(self.thread_list_comment[i], self.url_comment, self.active_comment, self.target_comment)
                    t = threading.Thread(target=fnthread.startComment)
                    self.per_list_comment.append(t)
                    self.currentthread_list_comment.append(self.thread_list_comment[i])
                for i in range(0, int(self.window_count_comment)):
                    self.per_list_comment[i].start()
                for i in range(0, int(self.window_count_comment)):
                    self.per_list_comment[i].join()
        else:
            self.pushButton_start_comment.setText("Start")
            for i in range(0, len(self.currentthread_list_comment)):
                try:
                    stop_url = 'http://127.0.0.1:35000/profile/stop/'+self.currentthread_list_comment[i]
                    resp = requests.get(stop_url)
                except:
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    with open("Reddit_log.txt", "a") as fp:
                        fp.write(dt_string + " " + self.currentthread_list_comment[i] + " Exit Session Error")
                        fp.write("\n")
            self.flag_comment = 1



class AutoReddit():
    def __init__(self, profile_id,  url , active, target_url):
        self.url = url
        self.profile_id = profile_id
        self.active = active
        self.target_url = target_url
        self.flag = 0
    def startComment(self):
        print("comment")
        try:
            incogniton_url = 'http://127.0.0.1:35000/automation/launch/python/'+ self.profile_id
            resp = requests.get(incogniton_url)
            incomingJson = resp.json()

            python_dict = literal_eval(incomingJson['dataDict'])
            driver = webdriver.Remote(
                        command_executor = incomingJson['url'],
                        desired_capabilities = literal_eval(incomingJson['dataDict']) )
        except:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            with open("Reddit_log.txt", "a") as fp:
                fp.write(dt_string + " " + self.profile_id + " Iconginte Driver Runtime Error")
                fp.write("\n")
        try:
            driver.get(self.url)
            for i in range(0, 10):
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(10)                                            
                comment_array = driver.find_elements(By.CLASS_NAME, 'Comment')    
                vote_list = []
                for i in range(0, len(comment_array)):
                    if str(comment_array[i].get_attribute('class')).find(self.target_url) != -1:
                        if self.active == "Up":
                            print(i,comment_array[i].get_attribute('class'))
                            x = comment_array[i].find_elements(By.TAG_NAME, 'button')
                            driver.execute_script("arguments[0].click();", x[1])
                            # x[1].send_keys(Keys.SPACE)
                            comment_array.pop(i)
                            self.flag = 1
                            break
                        elif self.active == "Down":
                            x = comment_array[i].find_elements(By.TAG_NAME, 'button')
                            # x[2].send_keys(Keys.SPACE)
                            driver.execute_script("arguments[0].click();", x[2])
                            comment_array.pop(i)
                            self.flag = 1
                            break
                if self.flag == 1:
                    count = random.randint(2,5)
                    random_list = random.sample(comment_array, count)
                    for i in range(0, len(random_list)):
                        if self.active == "Up":
                            x = random_list[i].find_elements(By.TAG_NAME, 'button')
                            driver.execute_script("arguments[0].click();", x[1])
                            # x[1].send_keys(Keys.SPACE)
                            delay_random = random.randint(5,30)
                            time.sleep(delay_random)
                        elif self.active == "Down":
                            x = random_list[i].find_elements(By.TAG_NAME, 'button')
                            driver.execute_script("arguments[0].click();", x[2])
                            # x[2].send_keys(Keys.SPACE)
                            delay_random = random.randint(5,30)
                            time.sleep(delay_random)
                        time.sleep(2)
                    print(5)
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    with open("Reddit_log.txt", "a") as fp:
                        fp.write(dt_string + " " + self.profile_id +" Success")
                        fp.write("\n")
                    break
                
            if self.flag == 0:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                with open("Reddit_log.txt", "a") as fp:
                    fp.write(dt_string + " " + self.profile_id +" Can not find comment.")
                    fp.write("\n")
        except:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            with open("Reddit_log.txt", "a") as fp:
                fp.write(dt_string + " " + self.profile_id +" Can not find articles.")
                fp.write("\n")
        
        try:
            stop_url = 'http://127.0.0.1:35000/profile/stop/'+self.profile_id
            resp = requests.get(stop_url)
        except:
            print("Failed to stop")
    def startAutomation(self):
        try:
            incogniton_url = 'http://127.0.0.1:35000/automation/launch/python/'+ self.profile_id
            resp = requests.get(incogniton_url)
            incomingJson = resp.json()

            python_dict = literal_eval(incomingJson['dataDict'])
            driver = webdriver.Remote(
                        command_executor = incomingJson['url'],
                        desired_capabilities = literal_eval(incomingJson['dataDict']) )
        except:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            with open("Reddit_log.txt", "a") as fp:
                fp.write(dt_string + " " + self.profile_id + " Iconginte Driver Runtime Error")
                fp.write("\n")
        try:
            driver.get(self.url)
            for k in range(0, 10):
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(10)
                self.vote_list = []
                post_list = driver.find_elements(By.XPATH, "//div[@class='_23h0-EcaBUorIHC-JZyh6J']")
                for i in range(0, len(post_list)-1):
                    if self.active == "Up":
                        z = post_list[i].find_elements(By.TAG_NAME, 'button')
                        self.vote_list.append(post_list[i].find_elements(By.TAG_NAME, 'button')[0])
                    if self.active == "Down":
                        self.vote_list.append(post_list[i].find_elements(By.TAG_NAME, 'button')[1])
                temp = []
                driver.implicitly_wait(15)
                # for k in range(0, len(vote_list), 2):
                #     temp.append(vote_list[k])
                # vote_list = temphttps://www.reddit.com/r/Verasity/comments/ulnjak/stake_and_forget_for_your_mental_health/
                post_array = driver.find_elements(By.XPATH, '//a[@class="SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"]')
                for i in range(0, len(post_array)-1):
                    print(str(post_array[i].get_attribute('href')))
                    if str(post_array[i].get_attribute('href')).find(self.target_url) != -1:
                        driver.execute_script("arguments[0].click();", self.vote_list[i])
                        # self.vote_list[i].send_keys(Keys.ENTER)
                        count = random.randint(2,5)
                        self.target_id = i
                        for kk in range(0, count):
                            vak = random.randint(1, len(self.vote_list)-1)
                            if vak == self.target_id:
                                continue
                            else:
                                driver.execute_script("arguments[0].click();", self.vote_list[vak])
                                # self.vote_list[vak].send_keys(Keys.ENTER)
                                delay_random = random.randint(5,30)
                                time.sleep(delay_random)    
                        self.flag = 1
                        self.vote_list.pop(i)
                        break
                if self.flag == 1:
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    with open("Reddit_log.txt", "a") as fp:
                        fp.write(dt_string + " " + self.profile_id +" Success")
                        fp.write("\n")
                    break
            if self.flag == 0:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                with open("Reddit_log.txt", "a") as fp:
                    fp.write(dt_string + " " + self.profile_id +" Can not find articles.")
                    fp.write("\n")
        except:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            with open("Reddit_log.txt", "a") as fp:
                fp.write(dt_string + " " + self.profile_id +" Can not find articles.")
                fp.write("\n")
        
        try:
            stop_url = 'http://127.0.0.1:35000/profile/stop/'+self.profile_id
            resp = requests.get(stop_url)
        except:
            print("Failed to stop")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main()
    form.show()
    app.exec_()
