from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import smtplib
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

PROMISED_DOWN = 1000
PROMISED_UP = 1000
CHROME_DRIVER_PATH = "/opt/homebrew/bin/chromedriver"
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
RECIEVER_EMAIL = os.environ.get("RECIEVER_EMAIL")

class InternetSpeedMailBot:

    def __init__(self) -> None:
        self.driver = webdriver.Chrome(CHROME_DRIVER_PATH)
        self.up = None
        self.down = None
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.time = datetime.now().strftime("%H:%M")

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        time.sleep(3)
        self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()              # Accept Cookies
        self.driver.find_element(By.CLASS_NAME, "js-start-test").click()                    # Click start button
        time.sleep(45)                                                                      # Wait for test to complete, adjust this number as neccesary
        self.down = float(self.driver.find_element(By.CLASS_NAME, "download-speed").text)
        self.up = float(self.driver.find_element(By.CLASS_NAME, "upload-speed").text)
        self.driver.quit()
    
    def notify_company(self):
        if self.down < PROMISED_DOWN or self.up < PROMISED_UP:
            with open("message_template.txt") as message_file:
                message = message_file.readlines()
                message = ''.join(message)
                message = message.replace("[DATE]", self.date)
                message = message.replace("[TIME]", self.time)
                message = message.replace("[DOWN]", str(self.down))
                message = message.replace("[UP]", str(self.up))
            
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=RECIEVER_EMAIL,
                    msg=message.encode("utf8")
                )

def main():
    bot = InternetSpeedMailBot()
    bot.get_internet_speed()
    bot.notify_company()

if __name__ == "__main__":
    main()
