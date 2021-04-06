# Description

This Selenium program plays a notification sound if either a class is added to MyASU, or if the number of students enrolled in any class changes.

# Usage
There are two mandatory command-line arguments. The first is the subject code, and the second is the course number.  There is also a third optional integer argument, which specifies the number of minutes the program will run.  If not provided, the program will run indefinitely.

For example, to monitor CSE 340 for 24 hours (1440 minutes), the command would be
```
python3 main.py CSE 340 1440
```
