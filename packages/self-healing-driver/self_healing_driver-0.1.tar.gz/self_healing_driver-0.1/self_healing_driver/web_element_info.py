from selenium.webdriver.remote.webelement import WebElement


class WebElementInfo:
    def __init__(self):
        self.element = None
        self.dynamic_xpath = None

    def get_element(self):
        return self.element

    def set_element(self, element):
        self.element = element

    def get_dynamic_xpath(self):
        return self.dynamic_xpath

    def set_dynamic_xpath(self, dynamic_xpath):
        self.dynamic_xpath = dynamic_xpath

    def __str__(self):
        return f"web_element_info [element={self.element}, dynamic_xpath={self.dynamic_xpath}]"
