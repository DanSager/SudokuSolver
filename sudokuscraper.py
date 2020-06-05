""" Scrape randomly generated sudokus via www.websudoku.com """

from urllib.request import urlopen, Request
# pip install bs4
from bs4 import BeautifulSoup as Soup
from bs4 import Comment as Com
from selenium import webdriver
import time
import re


directory = 'puzzles/'


# difficulty: 1 very-easy, 2 easy, 3 medium, 4 hard, 5 very-hard
def extract_data(iterations, selection):
    for difficulty in selection:
        url = 'https://sudoku9x9.com/?level=' + str(difficulty)
        title = ""
        if difficulty == 1:
            title = "very-easy"
        elif difficulty == 2:
            title = "easy"
        elif difficulty == 3:
            title = "medium"
        elif difficulty == 4:
            title = "hard"
        elif difficulty == 5:
            title = "very-hard"

        for i in range(0, iterations):
            # opening website and grabbing page
            uClient = urlopen(url)
            page_html = uClient.read()
            uClient.close()

            # html parsing
            page_soup = Soup(page_html, "html.parser")

            # read sudoku board
            year_container = page_soup.find("div", {"id": "playtable"})

            divs = year_container.findAll("div", {"class": "t1"})

            line = ""
            j = 0
            for div in divs:
                if div.text == "":
                    line += '0'
                else:
                    line += div.text
                j += 1
                if j == 9:
                    j = 0
                    line += '\n'

            filename = directory + title + str(i)
            file = open(filename, 'w')
            file.write(line)
            file.close()
            a = 8


def main():
    """ Main """
    start_time = time.time()
    extract_data(100, [1, 2, 3, 4, 5])
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
