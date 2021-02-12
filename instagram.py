from datetime import date
import itertools
from explicit import waiter, XPATH
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import sqlite3

conn = sqlite3.connect('followers.sqlite')
cur = conn.cursor()

cur.execute("SELECT * FROM Followers")
rows = cur.fetchall()
oldlist = []
for row in rows:
    oldlist.append(row)

cur.executescript('''
DROP TABLE IF EXISTS Followers;

CREATE TABLE Followers (
    count     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    follower   TEXT UNIQUE
);''')


def login(driver):
    username = "hw_amazingart"  # <username here>
    password = ""  # <password here>

    # Load page
    driver.get("https://www.instagram.com/accounts/login/")
    sleep(3)
    # Login
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    submit = driver.find_element_by_tag_name('form')
    submit.submit()

    # click "Not Now" element
    sleep(3)
    acpt = driver.find_element_by_xpath("//*[contains(@class, 'sqdOP yWX7d    y3zKF     ')]")
    acpt.click()

    # Wait for the user dashboard page to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.LINK_TEXT, "See All")))


def scrape_followers(driver, account):
    # Load account page
    driver.get("https://www.instagram.com/{0}/".format(account))

    # Click the 'Follower(s)' link
    # driver.find_element_by_partial_link_text("follower").click
    sleep(2)
    driver.find_element_by_partial_link_text("follower").click()

    # Wait for the followers modal to load
    waiter.find_element(driver, "//div[@role='dialog']", by=XPATH)
    allfoll = int(driver.find_element_by_xpath("//li[2]/a/span").text)
    # At this point a Followers modal pops open. If you immediately scroll to the bottom,
    # you hit a stopping point and a "See All Suggestions" link. If you fiddle with the
    # model by scrolling up and down, you can force it to load additional followers for
    # that person.

    # Now the modal will begin loading followers every time you scroll to the bottom.
    # Keep scrolling in a loop until you've hit the desired number of followers.
    # In this instance, I'm using a generator to return followers one-by-one
    follower_css = "ul div li:nth-child({}) a.notranslate"  # Taking advange of CSS's nth-child functionality
    for group in itertools.count(start=1, step=12):
        for follower_index in range(group, group + 12):
            if follower_index > allfoll:
                raise StopIteration
            yield waiter.find_element(driver, follower_css.format(follower_index)).text

        # Instagram loads followers 12 at a time. Find the last follower element
        # and scroll it into view, forcing instagram to load another 12
        # Even though we just found this elem in the previous for loop, there can
        # potentially be large amount of time between that call and this one,
        # and the element might have gone stale. Lets just re-acquire it to avoid
        # tha
        last_follower = waiter.find_element(driver, follower_css.format(group+11))
        driver.execute_script("arguments[0].scrollIntoView();", last_follower)


if __name__ == "__main__":

    account = "hw_amazingart"  # <account to check>
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    list = []
    try:
        login(driver)

        # display number of followers right now
        print('Followers of the "{}" account'.format(account))
        for count, follower in enumerate(scrape_followers(driver, account=account), 1):
            list.append((count, follower))
        print(len(list))

        # insert into table
        for index in range(len(list)):
            count = list[index][0]
            follower = list[index][1]
            cur.execute('''INSERT OR IGNORE INTO Followers (count,follower)
                        VALUES (?,?)''',(count,follower))
            conn.commit()

        # compare old list and new list
        for i in range(len(oldlist)):
            # old item is in new list exactly as is
            if oldlist[i] in list:
                pass
            # old item disappeared or index changed
            else:
                ii = 0
                slist = []
                while ii < len(list) and (oldlist[i][1] not in list[ii]):
                    slist.append("f")
                    ii += 1
                if ii == len(list):
                    cur.execute('''INSERT OR IGNORE INTO Unfollowers (count,follower,unfollow)
                                    VALUES (?,?,?)''', (oldlist[i][0], oldlist[i][1], date.today()))
                    conn.commit()

        conn.close()
    finally:
        driver.quit()

