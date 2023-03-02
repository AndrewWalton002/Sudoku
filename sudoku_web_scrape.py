import requests
from bs4 import BeautifulSoup
import json

EASY = "easy"
MED = "medium"
HARD = "hard"
SUDOKU_BOARD_HTML_INDEX = 1
CONTENT_INDEX = 0
HTML_FILLER_SIZE = 18
NYT_URL = "https://www.nytimes.com/puzzles/sudoku/easy"

def get_data(difficulty):
    """
    Scrape the data for the current sudoku from the NYT website
    param difficulty: the difficulty of the sudoku
    return : the grid for the current difficulty
    """

    # Scrape the HMTL from the NYT website and set up BeautifulSoup
    r = requests.get(NYT_URL)
    soup = BeautifulSoup(r.content, "html.parser")

    div_children = []

    # Search through the HTML tree to find the data on the sudoku
    body = soup.find("body")
    body_children = body.findChildren(recursive=False)
    for child in body_children:
        if child.name == "div":
            div_children.append(child)

    # Find the JavaScript that contains the information about the sudoku
    for child in div_children[SUDOKU_BOARD_HTML_INDEX].findChildren():
        if child.name == "script":
            sudoku_info = child.contents[CONTENT_INDEX][HTML_FILLER_SIZE:]
    
    # Load the Javascript into JSON 
    json_info = json.loads(sudoku_info)

    # Return the information about the sudoku
    return json_info[difficulty]["puzzle_data"]["puzzle"]