# Unit test for adding collections
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_ll(self):
        driver = self.driver
        driver.maximize_window()
        user = "testuser"
        pwd = "test123"
        driver.get("http://127.0.0.1:8000/admin")
        time.sleep(3)
        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        time.sleep(3)
        elem.send_keys(Keys.RETURN)
        driver.get("http://127.0.0.1:8000")
        time.sleep(3)

        driver.find_element(By.XPATH, "//a[contains(., 'My Collection')]").click()

        time.sleep(3)

        driver.find_element(By.XPATH, "//a[contains(., 'Add Collection')]").click()
        elem = driver.find_element(By.ID, "id_name")
        elem.send_keys("Test case add a collection")
        time.sleep(3)
        elem = driver.find_element(By.ID, "id_notes")
        elem.send_keys("Test case add a collection")
        time.sleep(3)
        elem = driver.find_element(By.ID, "id_new_collection_type")
        elem.send_keys("Test case add a collection")
        time.sleep(3)

        submit_button = driver.find_element(By.XPATH, '//input[@type="submit" and @value="Submit"]')

        submit_button.click()
        time.sleep(3)

        try:

            elem = driver.find_element(By.LINK_TEXT, "Test case add a collection")
            self.driver.close()
            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("Test Failed - Was not able to create a collection as a registered user")

    time.sleep(2)


if __name__ == "__main__":
    unittest.main()
