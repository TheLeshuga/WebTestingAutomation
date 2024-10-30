# Name

Controllers list page test cases.

# Description

This project aims at tesing the filter by alerts option from the "List of controllers"
section from 'Smart Green' web page. Within this project can be found tests of functionality,
acceptance and usability for the filter option.

The test cases are features, where the scenarios to test are devised, as well as the
steps of each test case. Moreover, these tests can be tested in different browsers.

The available browsers that can be used to run the tests in the can be found in the
enum variable from 'configuration.json'. 

Within the pages directory, the page object of the web page is located.
In said python file, you can see all the web elements from the web page, as well as 
the functions used for testing.


# Installation

Use this command to install all necessary packages with pip

```bash
pip install -r requirements.txt
```

Or separately:
```bash
pip install selenium==4.10.0

pip install behave==1.2.6

pip install python-dotenv=1.0.0
```

# Configuration

In this project you will need an environment variables file in the root directory.

You can use this command line to create the file and the necessary variables:
```bash
echo -e "AGRICULTURE_DEV_LINK=\nACCOUNT_LOGIN=\nACCOUNT_PASSWORD=" > environment_variables.env
```
Then you need to fill the first variable with the URL of the Smart Green web page.
Then add the email or nickname of your Smart Green account in the second variable,
and lastly, its corresponding password in the last variable.

In order to run the tests, you require the driver of each browser.
The browsers list that are supported can be found in the json file: 

```json
{
  "browsers_enum" :  ["chrome", "firefox", "edge"]
}
```

You can download Chrome's driver [here](https://chromedriver.chromium.org/downloads), 
Firefox's driver [here](https://github.com/mozilla/geckodriver/releases)
and Microsoft Edge's driver [here](https://developer.microsoft.com/es-es/microsoft-edge/tools/webdriver/)

Pay close attention to the version of your browser to know which version you have to download.

When you have the driver downloaded, you can create a "drivers" folder in the root of the project directory and 
add the executable there.

When you are going to run a test, you will need to write the browser name in the command line. Keep in mind that you 
will have to type them as in the "browsers enum" is shown, and only those shown there as well.

Nonetheless, if you want to run all the tests in one browser, you can write a browser by default, also
found in the json file:

```json
{
  "browser_default" : "chrome"
}
```
The default browser is chrome, but you can change it to other one among the available ones.

# Tests

In the project, you can find one test with two scenarios:

- **User gets a list of all controllers (no filters applied)**: With this scenario you can check all the controllers shown
in the "Todos" option. Its tag is **@todos**.


- **User filters a list of controllers by active alerts**: With this scenario you can check whether those controllers that got at least one alert are 
displayed in the filter by alert option. Furthermore, it will check if any controller with at least one alert is missing between the controllers displayed 
by the filter by alerts option. Its tag is **@alerts**.

Both of these tests work with >= 0 controllers registered. The test tag is **@listofcontrollers**.

# Run tests

Before running the tests, ensure that you installed correctly all the packages found in 'requirements.txt',
as well as following the configuration section instructions.

If you want to run all the tests of the project at once you can use (the browser used is the default):

```bash
behave 
```

If you want to run all the tests, but choosing the browser using the command line:

```bash
behave -D BROWSER=<BROWSER>
```

If you want to run the tests or scenarios of certain tag, first make sure you are in the root of the project directory, and use this command:

```bash
 python main.py <BROWSER>[,<BROWSER2>...] <tag_name>[,<tag_name2>...]
```

Example to run a test:
```bash
python main.py chrome,edge todos
```

You can check the tags available in the 'Tests' section within this README.

Another way to run a test is by the feature file name, it will run all the scenarios and test cases located in the feature:

```bash
python main.py <BROWSER>[,<BROWSER2>...] ./features/<test_name>.feature
```

Example to run a test:
```bash
python main.py chrome ./features/listOfControllers.feature
```

Here is the structure of the project (with the "drivers" directory added).
```vbnet
WebPageAutomation/
├── drivers/
├── features/
│   └── listOfControllers.feature
├── steps/
│   └── (...)
├── requirements.txt
├── main.py
└── (...)
```

After you execute one command, a log file named 'REPORT.log' will be generated in the root of the project. 
This log will contain useful information about the run, showing all the data collected from the test. 
Be wary that every time you run a command, the log file will remove the previous execution.

# Project status

This project is completed as the internship is finished. 