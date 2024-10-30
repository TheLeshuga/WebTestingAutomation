import logging, os, json, sys
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, ElementClickInterceptedException, ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pages.List_of_controllers_page import listOfControllersPage
from selenium.webdriver.firefox.service import Service
from behave import given, when, then

logging.basicConfig(filename='REPORT.log', level=logging.INFO, filemode='a')

@given(u'I am on the login page')
def step_impl(context):
    load_dotenv('environment_variables.env')

    with open('configuration.json') as file:
        data = json.load(file)

    browser = context.config.userdata.get("BROWSER", data['browser_default'])

    if browser == data['browsers_enum'][0]:
        options = Options()
        options.add_argument('--headless')
        context.driver = webdriver.Chrome(options=options)
    elif browser == data['browsers_enum'][1]:
        gecko_service = Service(r'geckodriver', log_path=os.devnull)
        options = webdriver.FirefoxOptions()
        options.set_preference("dom.animations.enabled", False)
        options.add_argument('--headless')
        context.driver = webdriver.Firefox(service=gecko_service, options=options)
    elif browser == data['browsers_enum'][2]:
        options = webdriver.EdgeOptions()
        options.add_argument('--headless')
        context.driver = webdriver.Edge(options=options)
    else:
        print(f"\nERROR: The value '{browser}' does not match the possible browsers.")
        sys.exit(1)

    logging.getLogger('BROWSER').info("Running the test in %s\n", browser)

    agriculture_dev_link = os.getenv('AGRICULTURE_DEV_LINK')

    if agriculture_dev_link is None or agriculture_dev_link == "":
        print(f"\nERROR: AGRICULTURE_DEV_LINK is not initialized correctly.")
        sys.exit(1)

    context.driver.get(agriculture_dev_link)

@given(u'I sign in with valid credentials')
def step_impl(context):
    context.wait = WebDriverWait(context.driver, 10)
    context.bugs = 0

    loginElement = None
    try:
        loginElement = context.wait.until(EC.element_to_be_clickable((By.ID, "login")))
    except TimeoutException:
        context.bugs += 1
        logging.getLogger('BUG').error("'login' web element couldn't be found. The value of AGRICULTURE_DEV_LINK may be wrong.\n")

    login = os.getenv('ACCOUNT_LOGIN')

    if login == "" or login is None:
        print(f"\nERROR: ACCOUNT_LOGIN is not initialized.")
        sys.exit(1)

    if loginElement is not None:
        try:
            loginElement.send_keys(login)
        except ElementNotVisibleException:
            context.bugs += 1
            logging.getLogger('BUG').error("'login' web element couldn't be filled. It's not visible.\n")

    passwordElement = None
    try:
        passwordElement = context.driver.find_element(By.ID, "pass")
    except NoSuchElementException:
        context.bugs += 1
        logging.getLogger('BUG').error("'password' web element couldn't be found.\n")

    password = os.getenv('ACCOUNT_PASSWORD')

    if password == "" or password is None:
        print(f"\nERROR: ACCOUNT_PASSWORD is not initialized.")
        sys.exit(1)

    if passwordElement is not None:
        try:
            passwordElement.send_keys(password)
        except ElementNotVisibleException:
            context.bugs += 1
            logging.getLogger('BUG').error("'password' web element couldn't be filled. It's not visible.\n")

    button = None
    try:
        button = context.driver.find_element(By.CSS_SELECTOR, ".button")
    except NoSuchElementException:
        context.bugs += 1
        logging.getLogger('BUG').error("'button' web element couldn't be found.\n")

    if button is not None:
        try:
            button.click()
        except ElementClickInterceptedException:
            context.bugs += 1
            logging.getLogger('BUG').error("'button' web element couldn't be clicked. Another element is blocking the element.\n")

    sys.tracebacklimit = 0
    assert context.bugs == 0


@given(u'I click the list of controllers section')
def step_impl(context):
    try:
        controllersSection = context.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".three .dashboard-menu-item:nth-of-type(3) .ballicon")))
    except TimeoutException:
        assert False, logging.getLogger('BUG').error(" 'controllers section' web element couldn't be found. The value of ACCOUNT_LOGIN or ACCOUNT_PASSWORD may be wrong.\n")

    try:
        controllersSection.click()
    except ElementClickInterceptedException:
        assert False, logging.getLogger('BUG').error("'controllers section' web element couldn't be clicked. Another element is blocking the element.\n")


@when(u'I click the "View with alerts" option')
def step_impl(context):
    context.page = listOfControllersPage(context.driver)
    context.page.searchByAlerts()

@then(u'the page shows a controllers list that have alerts, if any')
def step_impl(context):
    all_controllers = context.page.getListOfCardsAfterFilter()
    number_ON = len(all_controllers)
    logging.getLogger('@alerts').info("Number of controllers with at least one alert (filter ON): %d\n", number_ON)

    context.all_controllers_plus_info = context.page.dictionaryOfCards(all_controllers)
    context.page.searchByAlerts()

    all_controllers = context.page.getListOfCardsAfterFilter()

    no_controller_on_list = 0
    controller_with_alert = 0
    for controller in all_controllers:
        try:
            controller_name = context.page.extractCardName(controller)

            controller_number_alerts = controller.find_element(By.CSS_SELECTOR, ".card .content:nth-of-type(3) .left").text.strip()
            controller_number_alerts = int(controller_number_alerts)

            status_circle = controller.find_element(By.CSS_SELECTOR, "#image2")
        except NoSuchElementException:
            assert False, logging.getLogger('BUG').error("One or more of the controller variables couldn't be found.\n")

        try:
            isRed = status_circle.value_of_css_property("border")
            isRed = "rgb(219, 40, 40)" in isRed
        except Exception:
            assert False, logging.getLogger('BUG').error("An error happened when searching the 'border' CSS property of the status circle.\n")

        try:
            warning = controller.find_element(By.CSS_SELECTOR, '.exclamation.triangle.full.icon[style*="rgb(219, 40, 40)"]')
        except NoSuchElementException:
            warning = False

        name_on_list = controller_name in [item['name'] for item in context.all_controllers_plus_info]

        if controller_number_alerts >= 1 and isRed and warning and name_on_list:
            logging.getLogger('@alerts').info("%s is in the list.\n", controller_name)
            controller_with_alert += 1
        elif controller_number_alerts >= 1 and isRed and warning and not name_on_list:
            no_controller_on_list += 1

    logging.getLogger('@alerts').info("Number of controllers with at least one alert (filter OFF): %d\n\n", controller_with_alert)

    assert number_ON <= controller_with_alert, logging.getLogger('@alerts').error("There are %d more controllers shown in filter by alert option", number_ON - controller_with_alert)

    logging.info("Controllers information that got at least one alert in the list:\n")
    context.page.writeInLogControllersInformation(context.all_controllers_plus_info, '@alerts')

    assert no_controller_on_list == 0, logging.getLogger('@alerts').error("%d controllers aren't on the list and have at least one alert.", no_controller_on_list)

    logging.getLogger('@alerts').info("All controllers with at least one alert are on the list.\n\n")

    context.driver.quit()

@then(u'the page shows a list of controllers, if any')
def step_impl(context):
    context.page = listOfControllersPage(context.driver)

    all_controllers = context.page.getListOfCards()

    if len(all_controllers) == 0:
        context.driver.refresh()
        all_controllers = context.page.getListOfCards()

    logging.getLogger('@todos').info("Number of controllers: %d\n", len(all_controllers))

    logging.getLogger('@todos').info("Controllers information:\n")
    context.page.writeInLogControllersInformation(context.page.dictionaryOfCards(all_controllers), '@todos')

    context.driver.quit()
