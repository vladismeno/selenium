from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest


def test_auth_positive():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/v1/')

    browser.find_element(By.XPATH, '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    assert browser.current_url == 'https://www.saucedemo.com/v1/inventory.html', 'неправильный url'
    browser.quit()
