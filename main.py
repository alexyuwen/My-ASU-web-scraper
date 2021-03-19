
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
    PATH = "./chromedriver"
    driver = webdriver.Chrome(PATH)
    driver.get("https://webapp4.asu.edu/catalog/classlist?t=2207&hon=F&promod=F&e=open&page=1")
    sleep(4)  # wait for page to load since MyASU's class search page can be buggy sometimes
    repeatingInterval = 15  # in seconds
    courses = {}  # Dict[classNum: seatsOpen]
    try:
        minutesToRun = int(sys.argv[3])
        timeEnd = time() + 60 * minutesToRun
    except IndexError:
        timeEnd = float("inf")  # positive infinity

    updateCoursesList(driver, courses, initialized=False)
    while time() < timeEnd:
        updateCoursesList(driver, courses)
        sleep(repeatingInterval - (time() % repeatingInterval))

def updateCoursesList(driver, courses, initialized=True):
    try:
        subject = sys.argv[1]
        number = sys.argv[2]
    except:
        print("Either you did not provide command-line arguments or the ones you provided are invalid.")

    select = Select(driver.find_element_by_id("term"))
    select.select_by_visible_text('Fall 2021')

    search = driver.find_element_by_id("subjectEntry")
    search.send_keys(subject)

    search = driver.find_element_by_id("catNbr")
    search.clear()
    search.send_keys(number)
    search.send_keys(Keys.RETURN)
    sleep(3)  # wait for results to load

    try:
        table = driver.find_element_by_id('CatalogList')
        rows = table.find_elements_by_css_selector('tr')[1:]  # excludes first element, which is an empty list
    except NoSuchElementException:
        rows = []
    except:
        rows = []
        print("Something went wrong.")

    for row in rows:
        classNum = row.find_elements_by_tag_name('td')[2].text
        seatsOpen = row.find_elements_by_tag_name('td')[10].text
        teacher = row.find_elements_by_tag_name('td')[3].text
        if classNum not in courses:
            courses[classNum] = seatsOpen
            if initialized:
                print("\n----------------------------------------------------------------------------------------------")
                print("\nEither a new course has been added or a new spot for an existing course has opened.")
                print("\n----------------------------------------------------------------------------------------------\n")
                call(["afplay", "notification_sound.wav"])  # play notification sound
        elif courses.setdefault(classNum, seatsOpen) != seatsOpen and initialized:
            print("\n----------------------------------------------------------------------------------------------")
            print(f"The number of open seats in {teacher}'s section has changed from {courses[classNum]} to {seatsOpen}.")
            print("\n----------------------------------------------------------------------------------------------\n")
            call(["afplay", "notification_sound.wav"])  # play notification sound
            courses[classNum] = seatsOpen

        # # for debugging
        # i = -1
        # for cell in row.find_elements_by_tag_name('td'):
        #     i += 1
        #     print(f"{i:4}| {cell.text}")

   # print(list(courses.values()))


if __name__ == "__main__":
    main()