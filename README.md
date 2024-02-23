## SCRAPERTRON1000, a Python Amazon Web Scraper/Tracker
### Usage:
IMPORTANT!! The files `urls.txt` and `priceLog.txt` are OPTIONAL downloads with 7 example Amazon links and a few example logs. `scrapertron.py` can work as a standalone program and will create any needed files.

Make sure you `cd` to the correct folder where scrapertron.py is located before running. Otherwise, the program may not be able to read files.

To add links to `urls.txt` via console, use `CTRL + Shift + V` to paste links when prompted.

Always leave an extra empty line at the bottom of the text files so the program can properly append new info.

### Dependencies:
- BeautifulSoup4 `pip install bs4`
- urllib
- smtplib
- datetime
- sys

### Command line:
- Make sure you `cd` to the correct folder where scrapertron.py is located before running.
- Enter 0 or 1 to skip first prompt and go straight to scraping/adding urls
- Add your email (2nd arg) to skip email prompt

`python3 scrapertron.py` `python3 scrapertron.py 0` `python3 scrapertron.py 1 johndoe@gmail.com`

### Rubric (20/50)
- [ ] Writeup (10)
     - [ ] Research (8)
     - [ ] Works Cited (2)
- [ ] Presentation (20)
     - [ ] Well-Designed Slides (5)
     - [ ] Engaging (10)
     - [ ] Responds to questions well (5)
- [x] Program (18)
     - [x] Version Control (4)
     - [x] Demonstration (10)
     - [x] Run via comand line and add arguments (4)
- [x] README.md (2)
     - [x] Dependencies (1)
     - [x] Commands and arguments to run (1)
