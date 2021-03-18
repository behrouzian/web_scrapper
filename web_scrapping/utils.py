from urllib.parse import \
    urlsplit, urlunsplit
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup


def url_path_join(*parts):
    """Normalize url parts and join them with a slash.

    example: path = utils.url_path_join('https://example.org/fizz', 'buzz')
    output: 'https://example.org/fizz/buzz'
    """
    schemes, netlocs, paths, queries, fragments = zip(*(urlsplit(part) for part in parts))
    scheme = first(schemes)
    netloc = first(netlocs)
    path = '/'.join(x.strip('/') for x in paths if x)
    query = first(queries)
    fragment = first(fragments)
    return urlunsplit((scheme, netloc, path, query, fragment))

def first(sequence, default=''):
    return next((x for x in sequence if x), default)


def make_soup(url, features = 'html.parser'):
    driver = webdriver.Chrome('C:\\Users\\baghba\\chromedriver.exe')
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    # time.sleep(1)
    # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".stock-quote")))
    page_source = driver.page_source
    driver.close()
    return BeautifulSoup(page_source, features)

def make_quick_soup(url, features = 'html.parser' ):
    content = requests.get(url)
    return BeautifulSoup(content.text, 'html.parser')

def clean_html(bad_html):
    tree = BeautifulSoup(bad_html)
    good_html = tree.prettify()
    return good_html

def get_logger(logger_name, create_file=False, logger_file_Path=None):
    import logging
    """Get a logger


    Parameters
    ----------
    logger_name : str 
    logger name

    create_file : bool
    True when create a file and False when not create a file

    Returns
    -------
    logger

    Examples
    --------
    >>> test_logger = utils.get_logger("test", create_file = True,
                               logger_file_Path=path)
        test_logger.info("Hi ")
        test_logger.error("Bye")
    """
    # create logger for prd_ci
    log = logging.getLogger(logger_name)
    log.setLevel(level=logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if create_file:
        # create file handler for logger.
        if logger_file_Path is not None:
            file_path = logger_file_Path + logger_name + ".log"
        else:
            file_path = logger_name + ".log"
        fh = logging.FileHandler(file_path)
        fh.setLevel(level=logging.DEBUG)
        fh.setFormatter(formatter)
    # reate console handler for logger.
    ch = logging.StreamHandler()
    ch.setLevel(level=logging.DEBUG)
    ch.setFormatter(formatter)

    # add handlers to logger.
    if create_file:
        log.addHandler(fh)

    log.addHandler(ch)
    return log