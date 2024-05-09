from selene import browser, by, be, have
from selene.support.shared.jquery_style import s, ss
from time import sleep
import allure


def visit(url):
    browser.open(url)


def start():
    s('//*[@id="startTest"]').click()


def login():
    s('#login').type('login')
    s('#password').type('password')
    s('#agree').click()
    browser.element(by.text('Зарегистрироваться')).click()


def success_message_have_text(text):
    s('#successMessage').should(have.text(text))
