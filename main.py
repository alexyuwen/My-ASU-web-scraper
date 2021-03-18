
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from time import time, sleep
from subprocess import call
import sys


def main():
    """
    Plays notification sound if either a class is added or the number of students enrolled in any class changes
    """
    PATH = "/Users/alexyuwen/myasu-webscraper/chromedriver"
    driver = webdriver.Chrome(PATH)
    driver.get("https://webapp4.asu.edu/catalog/classlist?t=2207&hon=F&promod=F&e=open&page=1")
    sleep(4)  # wait for page to load since MyAsu's class search page can be buggy sometimes
    repeatingInterval = 15  # in seconds
    courses = {}  # Dict[classNum: seatsOpen]
    try:
        minutesToRun = int(sys.argv[1])
        timeEnd = time() + 60 * minutesToRun
    except IndexError:
        timeEnd = float("inf")  # positive infinity

    updateCoursesList(driver, courses, initialized=False)
    while time() < timeEnd:  # Todo: take command line argument of total minutes to run so that program doesn't run indefinitely
        updateCoursesList(driver, courses)
        sleep(repeatingInterval - (time() % repeatingInterval))

def updateCoursesList(driver, courses, initialized=True):
    select = Select(driver.find_element_by_id("term"))
    select.select_by_visible_text('Fall 2020')

    search = driver.find_element_by_id("subjectEntry")
    search.send_keys("CSE")

    search = driver.find_element_by_id("catNbr")
    search.clear()
    search.send_keys("340")
    search.send_keys(Keys.RETURN)
    sleep(3)  # wait for results to load

    try:
        mytable = driver.find_element_by_id('CatalogList')
        rows = mytable.find_elements_by_css_selector('tr')[1:]  # excludes first element, which is an empty list
    except NoSuchElementException:
        rows = []
    except:
        rows = []
        print("Something went wrong.")

    for row in rows:
        classNum = row.find_elements_by_tag_name('td')[2].text
        seatsOpen = row.find_elements_by_tag_name('td')[10].text
        if classNum not in courses:
            courses[classNum] = seatsOpen
            if initialized:
                print("A new course has been added.")
                call(["afplay", "notification_sound.wav"])  # play notification sound
        elif courses.setdefault(classNum, seatsOpen) != seatsOpen and initialized:
            print("The number of open seats has changed.")
            call(["afplay", "notification_sound.wav"])  # play notification sound
    # print(courses)


if __name__ == "__main__":
    main()