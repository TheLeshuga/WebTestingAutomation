import logging, time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class listOfControllersPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)

        for i in range(5):
            try:
                self.filterByAlerts = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='filter_by_alerts']")))

                break
            except TimeoutException:
                time.sleep(2)
                self.driver.refresh()

    def searchByAlerts(self):
        self.driver.execute_script("arguments[0].click();", self.filterByAlerts)


    def getListOfCards(self):
        try:
            self.findCards = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card")))
        except TimeoutException:
            self.findCards = []

        return self.findCards

    def getListOfCardsAfterFilter(self):
        self.driver.execute_script('''
         window.filterAppliedReceived = false;
            window.addEventListener("message", function(event) {
                if (event.data.event === "filterApplied") {
                    window.filterAppliedReceived = true;
                }
            });
        ''')

        try:
            self.wait.until(lambda driver: self.driver.execute_script('return window.filterAppliedReceived === true;'))
        except TimeoutException:
            assert False, logging.getLogger('BUG').error("'filterApplied' event couldn't be found in the last 5 seconds.")

        try:
            self.findCards = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card")))
        except TimeoutException:
            self.findCards = []

        return self.findCards

    def dictionaryOfCards(self, all_controllers):
        dict = []

        for controller in all_controllers:
            try:
                controller_name = self.extractCardName(controller)

                controller_number_alerts = controller.find_element(By.CSS_SELECTOR, ".card .content:nth-of-type(3) .left").text
                controller_date = controller.find_element(By.CSS_SELECTOR, ".card .content:nth-of-type(3) .right").text
                controller_model = controller.find_element(By.CSS_SELECTOR, "div.meta").text
            except NoSuchElementException:
                assert False, logging.getLogger('BUG').error(" One or more of the controller variables couldn't be found.\n")

            dict.append({'name': controller_name, 'alerts': controller_number_alerts, 'date': controller_date, 'model': controller_model})

        return dict

    def writeInLogControllersInformation(self, all_controllers_plus_info, log):
        for controller in all_controllers_plus_info:
            for key, value in controller.items():
                logging.getLogger(log).info("%s: %s", key, value)
            logging.getLogger(log).info("\n")


    def extractCardName(self, controller):
        controller_name = controller.find_element(By.CSS_SELECTOR, ".card .header").text
        controller_name = controller_name.replace("\n", " - ")
        return controller_name