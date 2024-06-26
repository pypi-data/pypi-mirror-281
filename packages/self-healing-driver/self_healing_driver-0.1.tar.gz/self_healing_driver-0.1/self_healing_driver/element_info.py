from typing import Dict
from selenium.webdriver.remote.webelement import WebElement


class ElementInfo:
    def __init__(self, tag_name, attributes, text_content, element, element_screenshot):
        self.tag_name = tag_name
        self.attributes = attributes
        self.text_content = text_content
        self.element = element
        self.element_screenshot = element_screenshot

    def get_tag_name(self):
        return self.tag_name

    def get_attributes(self):
        return self.attributes

    def get_text_content(self):
        return self.text_content

    def get_element(self):
        return self.element

    def get_element_screenshot(self):
        return self.element_screenshot
