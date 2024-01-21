#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

totalUnfollowed = 0
browser = None
action_follow = "Follow"
action_unfollow = "Following"
max_conn_pages_available = 100

def switch_to_main_window(browser, main_window):
	browser.close()
	browser.switch_to.window(main_window)

def get_connections():	
	return browser.find_elements(By.CSS_SELECTOR, "li.reusable-search__result-container .entity-result__title-text a")	

def get_action_type(actions):
	for i in range(len(actions)):
		action_type = actions[i].find_element(By.CSS_SELECTOR, "span").text
		if action_type == action_follow or action_type == action_unfollow:
			return i, action_type
	return -1, None
		
def scroll_to_bottom():
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")	
	html = browser.find_element(By.TAG_NAME, 'html')
	html.send_keys(Keys.END)

def unfollow():
	global totalUnfollowed
	main_window = browser.current_window_handle
	wait = WebDriverWait(browser, 10)
	conns = get_connections()
	seq = 0
	while True:
		conn = conns[seq]
		href = conn.get_attribute('href')
		print("Visiting ", href);
		browser.switch_to.new_window('tab')
		browser.get(href)
		wait.until(EC.number_of_windows_to_be(2))
		connName = browser.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge").text
		print("Analysing profile page for ", connName)
		moreBtn = browser.find_elements(By.CSS_SELECTOR, "button[aria-label='More actions']")[1]
		moreBtn.click()
		actions = browser.find_elements(By.CSS_SELECTOR, ".artdeco-dropdown__content-inner div[role='button']")
		idx, action_type = get_action_type(actions)
		if action_type == action_follow:
			print("Already unfollowed ", connName, "; moving to next connection...")
		elif action_type == action_unfollow:
			print("Unfollowing ", connName)
			actions[idx].click()
			confirmBtn = browser.find_element(By.CSS_SELECTOR, "div[role='alertdialog'] button.artdeco-button--primary")
			confirmBtn.click()
			print("Unfollowed ", connName)
			totalUnfollowed += 1
		switch_to_main_window(browser, main_window)
		seq += 1
		conns = get_connections()
		if seq >= len(conns):
			break

if __name__ == '__main__':
	print('Begin unfollowing connections...')
	browser = webdriver.Chrome()
	browser.get('https://www.linkedin.com/')
	browser.find_element(By.ID, "session_key").send_keys("your-email")
	browser.find_element(By.ID, "session_password").send_keys("your-password")
	browser.find_element(By.CLASS_NAME, "sign-in-form__submit-btn--full-width").click()
	browser.implicitly_wait(100)	
	pageNo = 1	
	browser.get('https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&page='+str(pageNo))
	while True:
		print("Browsing page #", pageNo)
		unfollow()
		print("Done with page #", pageNo, " | total unfollowed: ", totalUnfollowed)
		scroll_to_bottom()
		nxt = browser.find_element(By.CSS_SELECTOR, "button[aria-label='Next']")
		pageNo += 1
		if nxt == None or pageNo == max_conn_pages_available:
			break
		nxt.click()
