from selene import browser, by, be, have
from selene.support.shared.jquery_style import s, ss
import allure
from pages import auth

# browser.config.window_height = 500
# browser.config.window_height = 100

url = 'https://victoretc.github.io/selenium_waits/'


@allure.title("Авторизация")
def test_login():
    auth.visit(url)
    auth.start()
    auth.login()
    auth.success_message_have_text('Вы успешно зарегистрированы!')
    # browser.element('//*[@id="startTest"]').with_(timeout=10).click()
