import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

LOGIN_LINK = 'https://accounts.google.com/o/oauth2/v2/auth/identifier?client_id' \
        '=1096011445005-sdea0nf5jvj14eia93icpttv27cidkvk.apps' \
        '.googleusercontent.com&response_type=token&redirect_uri=https%3A%2F' \
        '%2Fwww.tiktok.com%2Flogin%2F&state=%7B%22client_id%22%3A' \
        '%221096011445005-sdea0nf5jvj14eia93icpttv27cidkvk.apps' \
        '.googleusercontent.com%22%2C%22network%22%3A%22google%22%2C' \
        '%22display%22%3A%22popup%22%2C%22callback%22%3A%22_hellojs_cg1m61ow' \
        '%22%2C%22state%22%3A%22%22%2C%22redirect_uri%22%3A%22https%3A%2F' \
        '%2Fwww.tiktok.com%2Flogin%2F%22%2C%22scope%22%3A%22basic%22%7D' \
        '&scope=openid%20profile&approval_prompt=force&flowName' \
        '=GeneralOAuthFlow'

COMMENT_TEXT_XPATH = '//*[contains(@class, "DivCommentItemContainer")]/div/div/p/span' 
USER_NAME_XPATH = '//*[contains(@class, "DivCommentItemContainer")]/div[1]/div[1]/a/span' 
USER_LINK_XPATH = '//*[contains(@class, "DivCommentItemContainer")]/div[1]/div[1]/a' 
COMMENTS_XPATH = '//*[contains(@class, "DivCommentListContainer")]' 
COMMENT_LIKES_XPATH = '//*[contains (@class, "DivLikeWrapper")]/span'

def id_by_link(link: str):
    # https://www.tiktok.com/@margaritaxaibith?lang=en -> @margaritaxaibith
    return link.split('/')[3].split('?')[0]


def fetch_data_from_comments(driver):
    comment_texts = [element.text for element in driver.find_elements(By.XPATH, COMMENT_TEXT_XPATH)]
    user_names = [element.text for element in driver.find_elements(By.XPATH, USER_NAME_XPATH)]
    user_links = [element.get_attribute('href') for element in driver.find_elements(By.XPATH, USER_LINK_XPATH)]
    comment_likes = [element.text for element in driver.find_elements(By.XPATH, COMMENT_LIKES_XPATH)]
    user_ids = [id_by_link(link) for link in user_links]
    return comment_texts, user_names, user_links, comment_likes, user_ids


def loading_comments(driver, comments_limit):
    while True:
        comment_xpath = '//*[contains(@class, "comment-item")]'
        comments = driver.find_elements(By.XPATH, comment_xpath)
        if comments_limit != -1 and len(comments) > comments_limit:
            break
        last_comment = comments[-1]
        last_comment.location_once_scrolled_into_view
        # Use that to wait while loading
        # subscribe = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//yt-formatted-string[text()='Subscribe']")))


def export_comments_to_csv(user_ids, user_names, user_links, comment_texts, comment_likes):
    with open('comments.csv', 'w') as out:
        writer = csv.writer(out)
        for row in zip(user_ids, user_names, user_links, comment_texts, comment_likes):
            writer.writerow(row)


def create_driver():
    options = webdriver.ChromeOptions()
    from fake_useragent import UserAgent
    ua = UserAgent()
    user_agent = 'Googlebot'
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('window-size=800x841')
    driver = webdriver.Chrome(options=options)
    return driver


def login_with_google(driver, email, password):
    login = LOGIN_LINK
    driver.get(login)
    email_el = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
    email_el.send_keys(email)
    email_el.send_keys(Keys.ENTER)
    time.sleep(2.0)
    password_el = driver.find_elements(By.CSS_SELECTOR,'input')
    password_el.send_keys(password)
    password_el.send_keys(Keys.ENTER)


def parse_comments_by_link():
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    comments_limit = int(os.getenv('COMMENTS_LIMIT'))
    if email is None or password is None or comments_limit is None:
        raise Exception('Error: Not all the env vars are set.')
    link = input()

    driver = create_driver()
    login_with_google(driver, email, password)
    time.sleep(15.0)

    driver.get(link)

    elem_comments = driver.find_element(By.XPATH, COMMENTS_XPATH)
    elem_comments.click()
    time.sleep(1.0)

    loading_comments(driver, comments_limit)

    comment_texts, user_names, user_links, comment_likes, user_ids = fetch_data_from_comments(driver)
    export_comments_to_csv(user_ids, user_names, user_links, comment_texts, comment_likes)
    driver.quit()


if __name__ == '__main__':
    parse_comments_by_link()
