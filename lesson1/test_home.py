from selenium import webdriver
from selenium.webdriver.common.by import By
import time

URL = 'https://www.saucedemo.com/'
ENDPOINT_PRODUCTS = 'inventory.html'
ENDPOINT_CART = 'cart.html'


def test_auth_success():
    """
    Авторизация используя корректные данные (standard_user, secret_sauce)
    """
    browser = webdriver.Chrome()
    browser.get(URL)

    browser.find_element(By.XPATH, '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    assert browser.current_url == URL + ENDPOINT_PRODUCTS, 'неправильный url'
    browser.quit()


def test_auth_failure():
    """
    Авторизация используя некорректные данные (standard_user, secret_sauce)
    """
    browser = webdriver.Chrome()
    browser.get(URL)

    error_message = 'Epic sadface: Username and password do not match any user in this service'
    browser.find_element(By.XPATH, '//*[@id="user-name"]').send_keys('standard_user2')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce2')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    # text = browser.find_element(By.XPATH, '//*[@id="login_button_container"]/div/form/h3').text
    # assert text == 'Epic sadface: Username and password do not match any user in this service'
    text_error = browser.find_element(By.XPATH, '//h3[contains(text(), "Username and password do not match")]')
    assert text_error.text == error_message, 'error text does not match expected'
    assert browser.current_url == URL, 'неправильный url'
    browser.quit()


def test_add_product_to_cart_from_catalog():
    """
    Добавление товара в корзину через каталог
    """
    browser = webdriver.Chrome()
    browser.get(URL)

    browser.find_element(By.XPATH, '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    browser.find_element(By.XPATH, '//*[@id="add-to-cart-sauce-labs-backpack"]').click()
    assert browser.find_element(By.XPATH, '//*[@class="shopping_cart_badge"]').text == '1', 'Товар не добавлен в корзину'
    browser.quit()


def test_remove_product_from_cart():
    """
    Удаление товара из корзины через корзину
    """
    browser = webdriver.Chrome()
    browser.get(URL)

    browser.find_element(By.XPATH, '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    browser.find_element(By.XPATH, '//*[@id="add-to-cart-sauce-labs-backpack"]').click()
    browser.find_element(By.XPATH, '//a[@class="shopping_cart_link"]').click()
    browser.find_element(By.XPATH, '//*[@id="remove-sauce-labs-backpack"]').click()
    removed_product = browser.find_element(By.XPATH, '//div[@class="removed_cart_item"]')
    assert removed_product.is_enabled(), 'продукт не удален из корзины'
    browser.quit()


def test_add_product_to_cart_from_item():
    """
    Добавление товара в корзину из карточки товара
    """
    browser = webdriver.Chrome()
    browser.get(URL)

    browser.find_element(By.XPATH, '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    browser.find_element(By.XPATH, '//a[@id="item_4_title_link"]').click()
    browser.find_element(By.XPATH, '//button[@id="add-to-cart"]').click()
    browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a').click()
    product = browser.find_element(By.XPATH, '//*[@id="item_4_title_link"]')
    assert product is not None, 'количество товаров не соответствует добавленному'
    browser.quit()


def test_remove_product_from_item():
    """
    Удаление товара из корзины через карточку товара
    """
    browser = webdriver.Chrome()
    browser.get(URL)

    browser.find_element(By.XPATH, '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    browser.find_element(By.XPATH, '//a[@id="item_4_title_link"]').click()
    browser.find_element(By.XPATH, '//button[@id="add-to-cart"]').click()
    browser.find_element(By.XPATH, '//button[@id="remove"]').click()
    browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a').click()
    assert not len(browser.find_elements(By.XPATH, '//div[@class="cart_item"]')), 'корзина не пустая'
    browser.quit()


def test_move_to_item_by_click_on_image():
    """
    Успешный переход к карточке товара после клика на картинку товара
    """
    browser = webdriver.Chrome()
    browser.get(URL)

    browser.find_element(By.XPATH, '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    browser.find_element(By.XPATH, '//*[@id="item_4_img_link"]').click()
    label = browser.find_element(By.XPATH, '//div[contains(text(), "Sauce Labs")]').text
    assert label == 'Sauce Labs Backpack', 'Товар не существует'
    browser.quit()


def test_move_to_item_by_click_on_title():
    """
    Успешный переход к карточке товара после клика на название товара
    """
    browser = webdriver.Chrome()
    browser.get(URL)

    browser.find_element(By.XPATH, '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    browser.find_element(By.XPATH, '//*[@id="item_4_title_link"]').click()
    label = browser.find_element(By.XPATH, '//div[contains(text(), "Sauce Labs")]').text
    assert label == 'Sauce Labs Backpack', 'Товар не существует'
    browser.quit()


def test_place_order_success():
    """
    Оформление заказа используя корректные данные
    """
    first_name = "Ivan"
    last_name = "Petrov"
    postal_code = "90004"
    browser = webdriver.Chrome()
    browser.get(URL)

    browser.find_element(By.XPATH, '//input[@id="user-name"]').send_keys("standard_user")
    browser.find_element(By.XPATH, '//input[@id="password"]').send_keys("secret_sauce")
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    browser.find_element(By.XPATH, '//button[@id="add-to-cart-sauce-labs-backpack"]').click()
    browser.find_element(By.XPATH, '//a[@class="shopping_cart_link"]').click()
    browser.find_element(By.XPATH, '//button[@id="checkout"]').click()
    browser.find_element(By.XPATH, '//input[@id="first-name"]').send_keys(first_name)
    browser.find_element(By.XPATH, '//input[@id="last-name"]').send_keys(last_name)
    browser.find_element(By.XPATH, '//input[@id="postal-code"]').send_keys(postal_code)
    browser.find_element(By.XPATH, '//input[@id="continue"]').click()
    browser.find_element(By.XPATH, '//button[@id="finish"]').click()
    message = browser.find_element(By.XPATH, '//h2[@class="complete-header"]').text
    assert message == "Thank you for your order!", 'Заказ не обработан'
    browser.quit()


def test_filter_az():
    """
    Проверка работоспособности фильтра (A to Z)
    """
    browser = webdriver.Chrome()
    browser.get(URL)

    browser.find_element(By.XPATH, '//input[@id="user-name"]').send_keys("standard_user")
    browser.find_element(By.XPATH, '//input[@id="password"]').send_keys("secret_sauce")
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    browser.find_element(By.XPATH, '//select/option[@value="az"]').click()
    products_name = browser.find_elements(By.XPATH, '//div[@class="inventory_item_description"]//a//div')
    list_products = [name.text for name in products_name]
    list_products_sort = sorted(list_products)
    assert list_products_sort == list_products, 'filter from A to Z does not work'
    browser.quit()


def test_filter_za():
    """
    Проверка работоспособности фильтра (Z to A)
    """
    browser = webdriver.Chrome()
    browser.get(URL)

    browser.find_element(By.XPATH, '//input[@id="user-name"]').send_keys("standard_user")
    browser.find_element(By.XPATH, '//input[@id="password"]').send_keys("secret_sauce")
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    browser.find_element(By.XPATH, '//select/option[@value="za"]').click()
    products_name = browser.find_elements(By.XPATH, '//div[@class="inventory_item_description"]//a//div')
    list_products = [name.text for name in products_name]
    list_products_sort = sorted(list_products, reverse=True)
    assert list_products_sort == list_products, 'filter from Z to A does not work'
    browser.quit()


def test_filter_lohi():
    """
    Проверка работоспособности фильтра (low to high)
    """
    browser = webdriver.Chrome()
    browser.get(URL)

    browser.find_element(By.XPATH, '//input[@id="user-name"]').send_keys("standard_user")
    browser.find_element(By.XPATH, '//input[@id="password"]').send_keys("secret_sauce")
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    browser.find_element(By.XPATH, '//select/option[@value="lohi"]').click()
    products_price = browser.find_elements(By.XPATH, '//div[@class="inventory_item_price"]')
    price_products = [float(price.text[1:]) for price in products_price]
    list_products_sort = sorted(price_products)
    assert list_products_sort == price_products, 'filter from low to high does not work'
    browser.quit()


def test_filter_hilo():
    """
    Проверка работоспособности фильтра (high to low)
    """
    browser = webdriver.Chrome()
    browser.get(URL)

    browser.find_element(By.XPATH, '//input[@id="user-name"]').send_keys("standard_user")
    browser.find_element(By.XPATH, '//input[@id="password"]').send_keys("secret_sauce")
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    browser.find_element(By.XPATH, '//select/option[@value="hilo"]').click()
    products_price = browser.find_elements(By.XPATH, '//div[@class="inventory_item_price"]')
    price_products = [float(price.text[1:]) for price in products_price]
    list_products_sort = sorted(price_products, reverse=True)
    assert list_products_sort == price_products, 'filter from low to high does not work'
    browser.quit()


def test_menu_logout():
    """
    Выход из системы
    """
    browser = webdriver.Chrome()
    browser.get(URL)

    browser.find_element(By.XPATH, '//input[@id="user-name"]').send_keys("standard_user")
    browser.find_element(By.XPATH, '//input[@id="password"]').send_keys("secret_sauce")
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    browser.find_element(By.XPATH, '//button[@id="react-burger-menu-btn"]').click()
    time.sleep(2)
    browser.find_element(By.XPATH, '//a[@id="logout_sidebar_link"]').click()
    assert browser.current_url == URL, 'url does not match expected'
    browser.quit()


def test_menu_about():
    """
    Проверка работоспособности кнопки "About" в меню
    """
    browser = webdriver.Chrome()
    browser.get(URL)

    browser.find_element(By.XPATH, '//input[@id="user-name"]').send_keys("standard_user")
    browser.find_element(By.XPATH, '//input[@id="password"]').send_keys("secret_sauce")
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    browser.find_element(By.XPATH, '//button[@id="react-burger-menu-btn"]').click()
    time.sleep(2)
    browser.find_element(By.XPATH, '//a[@id="about_sidebar_link"]').click()
    assert browser.current_url == 'https://saucelabs.com/', 'url does not match expected'
    browser.quit()


def test_menu_reset():
    """
    Проверка работоспособности кнопки "Reset App State"
    """
    browser = webdriver.Chrome()
    browser.get(URL)

    browser.find_element(By.XPATH, '//input[@id="user-name"]').send_keys("standard_user")
    browser.find_element(By.XPATH, '//input[@id="password"]').send_keys("secret_sauce")
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    browser.find_element(By.XPATH, '//button[@id="add-to-cart-sauce-labs-backpack"]').click()
    browser.find_element(By.XPATH, '//button[@id="react-burger-menu-btn"]').click()
    time.sleep(2)
    browser.find_element(By.XPATH, '//a[@id="reset_sidebar_link"]').click()
    count = len(browser.find_elements(By.XPATH, '//*[@class="shopping_cart_badge"]'))
    assert count == 0, 'button "Reset App State" does not work as expected'
    browser.quit()