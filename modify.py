from concurrent.futures import thread
from turtle import pos
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import csv
import requests
import os
import time
from PyQt5.QtWidgets import *
import ui_main
import sys
from datetime import datetime
import random
import threading
from ast import Continue, literal_eval

post_url = "https://www.reddit.com/r/nanocurrency/comments/ujtlh7/nano_in_the_carbon_almanac_can_we_persuade_seth/"
comment_url = "https://www.reddit.com/r/nanocurrency/comments/ukx5q0/comment/i7vlblb/"

class Main(QDialog, ui_main.Ui_Dialog):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.pushButton_start.clicked.connect(self.fnStartPostVote)
        self.pushButton_start_comment.clicked.connect(self.fnStartCommentVote)
        self.lineEdit_url.setText(post_url)
        self.lineEdit_url_comment.setText(comment_url)
        self.postbutton_state = 0
        self.commentbutton_state = 0
    def fnparseTarget(self, url):
        x = url[22:].split('/')
        temp = ""
        for i in range(0, 5):
            temp += x[i] + "/"
        return temp
    def fnparsePosturl(self, url):
        x = url[8:].split('/')
        temp = "https://"
        for i in range(0, 3):
            temp += x[i] + "/"
        return temp
    def fnparseCommentUrl(self, url):
        x = url[8:].split('/')
        temp = "https://"
        for i in range(0, 5):
            temp += x[i] + "/"
        temp += "comment/"
        return temp
    def fnStartCommentVote(self):
        if self.commentbutton_state == 0:
            m_url_comment = self.lineEdit_url_comment.text()
            m_target_comment = self.fnparseTarget(m_url_comment)
            m_active_comment = self.comboBox_type_comment.currentText()
            m_account_number = self.spinBox_vote_comment.value()
            m_window_number = self.spinBox_account_comment.value()
            m_profile_list = []
            try:
                with open("profile.csv") as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        m_profile_list.append(row[0])
            except:
                QMessageBox.warning(self, "File doesn't exist Error", "'Profile.csv' file isn't exist\n\n Please check file")
                return
            if len(m_profile_list) < m_account_number:
                m_current_time = datetime.now()
                m_string_current_time = m_current_time.strftime("%d/%m/%Y %H:%M:%S")
                with open("Reddit_log.txt", "a") as fp:
                    fp.write(m_string_current_time + " Account number is not enough than Threads number")
                    fp.write('\n')
                QMessageBox.warning(self, "Account number is not enough", "Account number is not enough than Threads number")
                return
            else:
                self.pushButton_start_comment.setText("Stop")
                self.commentbutton_state = 1
                m_random_account = random.sample(m_profile_list, m_account_number)
                print("Account number", m_random_account)
                m_thread_list = []
                for i in range(0, int(m_account_number), int(m_window_number)):
                    block_list = m_random_account[i:i + m_window_number]
                    m_thread_list.append(block_list)
                    print(block_list)
                for i in range(0, len(m_thread_list)):
                    x = CommentStartButtonThread(m_thread_list[i], m_url_comment, m_target_comment, m_active_comment)
                    x.run()
                    x.join()
                self.pushButton_start_comment.setText("Start")
                self.commentbutton_state = 0
        elif self.commentbutton_state == 1:
            self.pushButton_start.setText("Start")
            self.postbutton_state = 0
            for i in range(0, len(m_random_account)):
                try:
                    stop_url = 'http://127.0.0.1:35000/profile/stop/'+m_random_account[i]
                    resp = requests.get(stop_url)
                except:
                    Continue

    def fnStartPostVote(self):
        if self.postbutton_state == 0:
            m_url_post = self.lineEdit_url.text()
            m_target_post = self.fnparseTarget(m_url_post)
            m_active_post = self.comboBox_type.currentText()
            m_account_number = self.spinBox_vote.value()
            m_window_number = self.spinBox_account.value()
            
            print("Post url ", m_url_post, "Post target ", m_target_post, "Post active ", m_active_post, "Post Account number ", str(m_account_number), "Post Window number ", str(m_window_number))
            
            m_profile_list = []
            try:
                with open("profile.csv") as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        m_profile_list.append(row[0])
            except:
                QMessageBox.warning(self, "File doesn't exist Error", "'Profile.csv' file isn't exist\n\n Please check file")
                return
            
            if len(m_profile_list) < m_account_number:
                m_current_time = datetime.now()
                m_string_current_time = m_current_time.strftime("%d/%m/%Y %H:%M:%S")
                with open("Reddit_log.txt", "a") as fp:
                    fp.write(m_string_current_time + " Account number is not enough than Threads number")
                    fp.write('\n')
                QMessageBox.warning(self, "Account number is not enough", "Account number is not enough than Threads number")
                return
            else:
                self.pushButton_start.setText("Stop")
                self.postbutton_state = 1
                m_random_account = random.sample(m_profile_list, m_account_number)
                print("Account number", m_random_account)
                m_thread_list = []
                for i in range(0, int(m_account_number), int(m_window_number)):
                    block_list = m_random_account[i:i + m_window_number]
                    m_thread_list.append(block_list)
                    print(block_list)
                for i in range(0, len(m_thread_list)):
                    x = PostStartButtonThread(m_thread_list[i], m_url_post, m_target_post, m_active_post)
                    x.run()
                    x.join()
                self.pushButton_start.setText("Start")
                self.postbutton_state = 0
        elif self.postbutton_state == 1:
            self.pushButton_start.setText("Start")
            self.postbutton_state = 0
            for i in range(0, len(m_random_account)):
                try:
                    stop_url = 'http://127.0.0.1:35000/profile/stop/'+m_random_account[i]
                    resp = requests.get(stop_url)
                except:
                    Continue
class PostStartButtonThread(threading.Thread):
    def __init__(self, profilename_list, post_url, target_url, active_type):
        threading.Thread.__init__(self)
        self.profilename_list = profilename_list
        self.post_url = post_url
        self.target_url = target_url
        self.active_type = active_type
    def run(self):
        length_thread = len(self.profilename_list)
        threads_list = []
        for i in range(0, int(length_thread)):
            thread_post = PostThread(self.profilename_list[i], self.post_url, self.target_url, self.active_type)
            thread_post.start()
            threads_list.append(thread_post)
        for i in range(0, len(threads_list)):
            threads_list[i].join()

class CommentStartButtonThread(threading.Thread):
    def __init__(self, profilename_list, comment_url, target_url, active_type):
        threading.Thread.__init__(self)
        self.profilename_list = profilename_list
        self.comment_url = comment_url
        self.target_url = target_url
        self.active_type = active_type
    def run(self):
        length_thread = len(self.profilename_list)
        threads_list = []
        for i in range(0, len(length_thread)):
            thread_post = CommentThread(self.profilename_list[i], self.comment_url, self.target_url, self.active_type)
            thread_post.start()
            threads_list.append(thread_post)
        for i in range(0, len(threads_list)):
            threads_list[i].join()

class CommentThread(threading.Thread):
    def __init__(self, profilename, comment_url, target_url, active_type):
        threading.Thread.__init__(self)
        self.profilename = profilename
        self.comment_url = comment_url
        self.target_url = target_url
        self.active_type = active_type
    def run(self):
        print ("Starting " + self.profilename)
        try:
            incogniton_url = 'http://127.0.0.1:35000/automation/launch/python/'+ self.profilename
            resp = requests.get(incogniton_url)
            incomingJson = resp.json()
            driver = webdriver.Remote(
                        command_executor = incomingJson['url'],
                        desired_capabilities = literal_eval(incomingJson['dataDict']) )
        except:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            with open("Reddit_log.txt", "a") as fp:
                fp.write(dt_string + " " + self.profile_id + " Iconginte Driver Runtime Error")
                fp.write("\n")
            return
        try:
            try:
                driver.get(self.comment_url)
            except:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                with open("Reddit_log.txt", "a") as fp:
                    fp.write(dt_string + " " + self.profile_id + " can not get url")
                    fp.write("\n")
                try:
                    stop_url = 'http://127.0.0.1:35000/profile/stop/'+self.profilename
                    resp = requests.get(stop_url)
                except:
                    current_time = datetime.now()
                    dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
                    with open("Reddit_log.txt", "a") as fp:
                        fp.write(dt_string + " " + self.profilename +" can not stop.")
                        fp.write("\n")
                    return
                return
            result_flag = 0
            for i in range(0, 10):
                try:
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    time.sleep(10)
                    comment_array = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "Comment")))
                    for m_post_url_id in range(0, len(comment_array)-1):
                        print(self.profilename, str(comment_array[m_post_url_id].get_attribute('href')))
                        if str(comment_array[m_post_url_id].get_attribute('href')).find(self.target_url) != -1:
                            if self.active_type == "Up":
                                x = WebDriverWait(comment_array[m_post_url_id], 30).until(EC.visibility_of_element_located((By.TAG_NAME, "button")))
                                driver.execute_script("arguments[0].click();", x[1])
                                comment_array.pop(m_post_url_id)
                                result_flag = 1
                                break
                            elif self.active_type == "Down":
                                x = WebDriverWait(comment_array[m_post_url_id], 30).until(EC.visibility_of_element_located((By.TAG_NAME, "button")))
                                driver.execute_script("arguments[0].click();", x[2])
                                comment_array.pop(i)
                                self.flag = 1
                                break
                    if result_flag == 1:
                        other_comment = random.randint(2,5)
                        random_list = random.sample(comment_array, other_comment)
                        for k in range(0, len(random_list)):
                            if self.active_type == "Up":
                                x = WebDriverWait(random_list[k], 30).until(EC.visibility_of_element_located((By.TAG_NAME, "button")))
                                driver.execute_script("arguments[0].click();", x[1])
                                delay_random = random.randint(5,30)
                                time.sleep(delay_random)
                            elif self.active_type == "Down":
                                x = WebDriverWait(random_list[k], 30).until(EC.visibility_of_element_located((By.TAG_NAME, "button")))
                                driver.execute_script("arguments[0].click();", x[2])
                                delay_random = random.randint(5,30)
                                time.sleep(delay_random)
                        current_time = datetime.now()
                        dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
                        with open("Reddit_log.txt", "a") as fp:
                            fp.write(dt_string + " " + self.profilename +" is Success")
                            fp.write("\n")
                            break
                except:
                    try:
                        stop_url = 'http://127.0.0.1:35000/profile/stop/'+self.profilename
                        resp = requests.get(stop_url)
                    except:
                        current_time = datetime.now()
                        dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
                        with open("Reddit_log.txt", "a") as fp:
                            fp.write(dt_string + " " + self.profilename +" Network error happen.")
                            fp.write("\n")
                        return
            if result_flag == 0:
                current_time = datetime.now()
                dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
                with open("Reddit_log.txt", "a") as fp:
                    fp.write(dt_string + " " + self.profilename +" can not find target post.")
                    fp.write("\n")
            try:
                stop_url = 'http://127.0.0.1:35000/profile/stop/'+self.profilename
                resp = requests.get(stop_url)
            except:
                current_time = datetime.now()
                dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
                with open("Reddit_log.txt", "a") as fp:
                    fp.write(dt_string + " " + self.profilename +" can not stop.")
                    fp.write("\n")
                return
        except:
            try:
                stop_url = 'http://127.0.0.1:35000/profile/stop/'+self.profilename
                resp = requests.get(stop_url)
            except:
                current_time = datetime.now()
                dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
                with open("Reddit_log.txt", "a") as fp:
                    fp.write(dt_string + " " + self.profilename +" can not stop.")
                    fp.write("\n")
                return
        print ("Exiting " + self.profilename)

class PostThread(threading.Thread):
    def __init__(self, profilename, post_url, target_url, active_type):
      threading.Thread.__init__(self)
      self.profilename = profilename
      self.post_url = post_url
      self.target_url = target_url
      self.active_type = active_type
    def run(self):
        print ("Starting " + self.profilename)
        try:
            incogniton_url = 'http://127.0.0.1:35000/automation/launch/python/'+ self.profilename
            resp = requests.get(incogniton_url)
            incomingJson = resp.json()
            driver = webdriver.Remote(
                        command_executor = incomingJson['url'],
                        desired_capabilities = literal_eval(incomingJson['dataDict']) )
        except:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            with open("Reddit_log.txt", "a") as fp:
                fp.write(dt_string + " " + self.profile_id + " Iconginte Driver Runtime Error")
                fp.write("\n")
            return
        try:
            try:
                driver.get(self.post_url)
            except:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                with open("Reddit_log.txt", "a") as fp:
                    fp.write(dt_string + " " + self.profile_id + " can not get url")
                    fp.write("\n")
                try:
                    stop_url = 'http://127.0.0.1:35000/profile/stop/'+self.profilename
                    resp = requests.get(stop_url)
                except:
                    current_time = datetime.now()
                    dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
                    with open("Reddit_log.txt", "a") as fp:
                        fp.write(dt_string + " " + self.profilename +" can not stop.")
                        fp.write("\n")
                    return
                return
            result_flag = 0
            for i in range(0, 10):
                try:
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    time.sleep(10)
                    post_list = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='_23h0-EcaBUorIHC-JZyh6J']")))
                    m_button_list = []
                    for m_post_id in range(0, len(post_list)-1):
                        if self.active_type == "Up":
                            m_button_list.append(post_list[m_post_id].find_elements(By.TAG_NAME, 'button')[0])
                        if self.active_type == "Down":
                            m_button_list.append(post_list[m_post_id].find_elements(By.TAG_NAME, 'button')[1])
                    post_url_array = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//a[@class="SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"]')))
                    for m_post_url_id in range(0, len(post_url_array)-1):
                        print(self.profilename, str(post_url_array[m_post_url_id].get_attribute('href')))
                        if str(post_url_array[m_post_url_id].get_attribute('href')).find(self.target_url) != -1:
                            driver.execute_script("arguments[0].click();", m_button_list[m_post_url_id])
                            m_button_list.pop(m_post_url_id)
                            random_post = random.randint(2,5)
                            random_list = random.sample(m_button_list, random_post)
                            self.target_id = m_post_url_id
                            for kk in range(0, len(random_list)):                            
                                driver.execute_script("arguments[0].click();", random_list[kk])
                                delay_random_time = random.randint(5,30)
                                time.sleep(delay_random_time)
                            current_time = datetime.now()
                            dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
                            with open("Reddit_log.txt", "a") as fp:
                                fp.write(dt_string + " " + self.profilename +" is Success")
                                fp.write("\n")
                            result_flag = 1
                            break
                    if result_flag == 1:
                        break
                    else:
                        continue
                except:
                    try:
                        stop_url = 'http://127.0.0.1:35000/profile/stop/'+self.profilename
                        resp = requests.get(stop_url)
                    except:
                        current_time = datetime.now()
                        dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
                        with open("Reddit_log.txt", "a") as fp:
                            fp.write(dt_string + " " + self.profilename +" Network error happen.")
                            fp.write("\n")
                        return
            if result_flag == 0:
                current_time = datetime.now()
                dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
                with open("Reddit_log.txt", "a") as fp:
                    fp.write(dt_string + " " + self.profilename +" can not find target post.")
                    fp.write("\n")
            try:
                stop_url = 'http://127.0.0.1:35000/profile/stop/'+self.profilename
                resp = requests.get(stop_url)
            except:
                current_time = datetime.now()
                dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
                with open("Reddit_log.txt", "a") as fp:
                    fp.write(dt_string + " " + self.profilename +" can not stop.")
                    fp.write("\n")
                return
        except:
            try:
                stop_url = 'http://127.0.0.1:35000/profile/stop/'+self.profilename
                resp = requests.get(stop_url)
            except:
                current_time = datetime.now()
                dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
                with open("Reddit_log.txt", "a") as fp:
                    fp.write(dt_string + " " + self.profilename +" can not stop.")
                    fp.write("\n")
                return
        print ("Exiting " + self.profilename)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main()
    form.show()
    app.exec_()