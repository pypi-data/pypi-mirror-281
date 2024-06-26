import ast
import base64
import io
import json
import os
import re
import shutil
import time
from bs4 import BeautifulSoup
import pinecone
import cv2
import joblib
import mysql.connector
import numpy as np
from mysql.connector import Error
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model
from element_info import ElementInfo
from web_element_info import WebElementInfo
from PIL import Image
import google.generativeai as genai
import openai

genai.configure(api_key='AIzaSyBBsGt10cUr9emQWrF4p-RxptsQg1U3YNI')
import tensorflow_hub as hub
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from pinecone import ServerlessSpec
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

load_dotenv(find_dotenv(), override=True)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

openai.api_key = OPENAI_API_KEY

pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)


def load_document(file):
    import pandas as pd
    from docx import Document
    name, extension = os.path.splitext(file)

    if extension == ".pdf":
        from langchain.document_loaders import PyPDFLoader
        loader = PyPDFLoader(file)

    elif extension == ".docx":
        from langchain.document_loaders import Docx2txtLoader
        loader = Docx2txtLoader(file)

    elif extension == ".csv":
        data = pd.read_csv(file)
        doc = Document()
        table = doc.add_table(rows=1, cols=len(data.columns))
        hdr_cells = table.rows[0].cells
        for i, column in enumerate(data.columns):
            hdr_cells[i].text = column
        for index, row in data.iterrows():
            row_cells = table.add_row().cells
            for i, cell in enumerate(row):
                row_cells[i].text = str(cell)
        docx_path = "uploaded_doc.docx"
        doc.save(docx_path)

        from langchain.document_loaders import Docx2txtLoader
        loader = Docx2txtLoader(docx_path)
    elif extension == ".md":
        from langchain_community.document_loaders import TextLoader
        loader = TextLoader(file, "utf-8")

    else:
        print(f"Document format {extension} not supported")
        return None

    data = loader.load()
    return data


def chunk_data(data, chunk_size=256, chunk_overlap=20):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(data)
    return chunks


def insert_or_fetch_embeddings(chunks):
    from langchain.vectorstores import FAISS
    from langchain.embeddings.openai import OpenAIEmbeddings

    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store


def qa_chain_gpt(vector_store, q):
    from langchain.chains import RetrievalQA
    from langchain.chat_models import ChatOpenAI
    llm = ChatOpenAI(model='gpt-4-turbo', temperature=0)
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 6})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    response = chain.run(q)
    return response


def url_to_index_name(url):
    lower_url = url.lower()
    no_protocol_url = re.sub(r'^https?://', '', lower_url)
    valid_index_name = re.sub(r'[^a-z0-9]+', '-', no_protocol_url)
    valid_index_name = valid_index_name.strip('-')
    while len(valid_index_name) >= 45:
        parts = valid_index_name.split('-')
        if len(parts) > 1:
            valid_index_name = '-'.join(parts[1:])
        else:
            valid_index_name = valid_index_name[1:]
    return valid_index_name


label_encoder = LabelEncoder()

try:
    login_model = load_model('login_page_model_backup.h5')
except Exception as e:
    print(f"Error loading model: {e}")

try:
    label_encoder = joblib.load('label_encoder_biller_backup.pkl')
except Exception as e:
    print(f"Error loading label encoder: {e}")


class SelfHealingDriver:
    connection: mysql.connector.connection.MySQLConnection  # Type-hinting for connection
    count: int

    def __init__(self, user_id, password, browser='chrome'):
        self.connection = self.get_connection()

        val_query = "SELECT password, name FROM user_details WHERE user_id = %s"
        cursor = self.connection.cursor()
        cursor.execute(val_query, (user_id,))
        val_pass = cursor.fetchone()
        print(val_pass)
        if val_pass:
            if password == val_pass[0]:
                print("validation completed...!")
                self.tester_name = val_pass[1]
            else:
                print("wrong username or password")
        else:
            print("wrong username or password")

        if browser.lower() == 'edge':
            self.driver = webdriver.Edge(service=webdriver.EdgeService("drivers/msedgedriver.exe"))
        else:
            self.driver = webdriver.Chrome(service=webdriver.ChromeService("drivers/chromedriver.exe"))

        self.count = 0
        self.id = None
        self.key = None
        self.value = None
        self.attribute = None
        self.screenshot = None
        self.self_heal_dynamic_xpath = None
        self.self_heal_cnn = None
        self.dynamic_xpath = None
        self.new_screenshot = None

    def start(self):
        self.driver.maximize_window()
        print("Driver started.")

    def navigate(self, url):
        if self is not None:
            self.driver.get(url)
        else:
            print("Driver is not started.")

    def close(self):
        if self.driver is not None:
            self.driver.quit()
            print("Driver closed.")
        else:
            print("Driver is not started.")

    def scroll_Into_View(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def url_to_pinecone_index(self, url):
        lower_url = url.lower()
        no_protocol_url = re.sub(r'^https?://', '', lower_url)
        valid_index_name = re.sub(r'[^a-z0-9]+', '-', no_protocol_url)
        valid_index_name = valid_index_name.strip('-')

        return valid_index_name

    def find_element_by_xpath(self, xpath):
        element_key = "xpath"
        element_value = xpath
        return self.find_element_by_locator(element_key, element_value)

    def find_element_by_id(self, id):
        element_key = "id"
        element_value = id
        return self.find_element_by_locator(element_key, element_value)

    def find_element_by_name(self, name):
        element_key = "name"
        element_value = name
        return self.find_element_by_locator(element_key, element_value)

    def find_element_by_class_name(self, class_name):
        element_key = "class_name"
        element_value = class_name
        return self.find_element_by_locator(element_key, element_value)

    def find_element_by_locator(self, element_key, element_value):
        valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-'
        ele_id = ''.join(c for c in element_value if c in valid_chars)
        self.id = ele_id
        self.key = element_key
        self.value = element_value
        att_json = None
        web_info = WebElementInfo()
        url = self.driver.current_url
        attrs = {}
        info = self.get_element_attributes(element_key, element_value, attrs)
        json_query = "SELECT attributes_json FROM web_element_data WHERE element_key = %s AND tester_name = %s"
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(json_query, (element_value, self.tester_name,))
        result_set1 = cursor.fetchone()
        if result_set1:
            att_json = result_set1[0]
        status = self.compare_json(att_json, info.get_attributes())
        status = True
        nn = info.get_tag_name()
        if (info.get_tag_name() is None or not info.get_attributes()) or status is False:
            select_query = "SELECT attributes_json, tag_name FROM web_element_data WHERE element_key = %s AND tester_name = %s"
            try:
                cursor.execute(select_query, (element_value, self.tester_name,))
                result_set = cursor.fetchone()
                if result_set:
                    attributes_json = result_set[0]
                    tag_name_info = result_set[1]
                    attributes = json.loads(attributes_json)
                    valid_xpaths = self.create_dynamic_xpath_from_attributes(tag_name_info, attributes)
                    dynamic_xpath = None
                    ct = 0
                    tot = 0
                    # for valid_xpath in valid_xpaths:
                    #     try:
                    #         self.driver.find_element(By.XPATH, valid_xpath)
                    #         dynamic_xpath = valid_xpath
                    #         info = self.get_element_attributes("xpath", valid_xpath, attrs)
                    #         ct += 1
                    #         web_info.set_element(info.get_element())
                    #         web_info.set_dynamic_xpath(valid_xpath)
                    #         print("Dynamic XPath: " + dynamic_xpath)
                    #         self.self_heal_dynamic_xpath = "True"
                    #         self.dynamic_xpath = valid_xpath
                    #         update_query = "UPDATE web_element_data SET self_heal_dynamic_xpath = %s, dynamic_xpath = %s WHERE element_key = %s AND tester_name = %s"
                    #         cursor.execute(update_query,
                    #                        (self.self_heal_dynamic_xpath, self.dynamic_xpath, element_value,
                    #                         self.tester_name))
                    #         connection.commit()
                    #         break
                    #     except NoSuchElementException:
                    #         # Element not found
                    #         pass
                    if ct == 0:
                        # fetch_query = "SELECT vector FROM vector_store WHERE url = %s"
                        # fetch_data = (self.driver.current_url,)
                        # cursor.execute(fetch_query, fetch_data)
                        # result = cursor.fetchone()
                        # print(f"previous dom {result}")
                        page_source = str(self.driver.page_source)
                        output_file_path = 'output.md'
                        with open(output_file_path, 'w', encoding='utf-8') as file:
                            file.write(page_source)
                        data = load_document(output_file_path)
                        chunks = chunk_data(data)
                        vector_store = insert_or_fetch_embeddings(chunks)
                        print(tag_name_info, attributes)
                        print(element_value)
                        question_prompt = f"""
                        There was an Product in this dom. Now it is changed.
                        Find the possible element which will be altered from {element_value}\n\n
                        Return all of the possible working relative new xpaths of the updated element detected. Only return the xpaths.
                        Response format: [newxpath1, newxpath2, newxpath3 ..].
                        """

                        print(question_prompt)
                        response = qa_chain_gpt(vector_store, question_prompt)
                        print(response)
                        valid_xpaths_rag = ast.literal_eval(response)
                        for valid_xpath in valid_xpaths_rag:
                            try:
                                self.driver.find_element(By.XPATH, valid_xpath)
                                dynamic_xpath = valid_xpath
                                info = self.get_element_attributes("xpath", valid_xpath, attrs)
                                ct += 1
                                web_info.set_element(info.get_element())
                                web_info.set_dynamic_xpath(valid_xpath)
                                print("Dynamic XPath: " + dynamic_xpath)
                                self.self_heal_cnn = "True"
                                snip = self.capture_screenshot_of_element_rag(element_value)
                                self.new_screenshot = snip
                                update_query = "UPDATE web_element_data SET self_heal_dynamic_xpath = %s, dynamic_xpath = %s WHERE element_key = %s AND tester_name = %s"
                                cursor.execute(update_query,
                                               (self.self_heal_dynamic_xpath, self.dynamic_xpath, element_value,
                                                self.tester_name))
                                connection.commit()
                                break
                            except NoSuchElementException:
                                pass

                    self.count += 1

                else:
                    print(element_key + " not found in the database: " + element_value)

            except Error as e:
                print("error first", e)
        attributes_json = json.dumps({k: v.decode('utf-8') if isinstance(v, bytes) else v for k, v in attrs.items()})
        select_count_query = "SELECT COUNT(*) FROM web_element_data WHERE element_key = %s AND tester_name = %s"
        try:
            cursor.execute(select_count_query, (element_value, self.tester_name,))
            count = cursor.fetchone()[0]
            tag_name_value = str(info.get_tag_name()) if info.get_tag_name() else None
            current_url_value = self.driver.current_url if self is not None else None

            if count == 0:
                element_screenshot_binary = self.get_element_screenshot_as_base64(element_key, element_value)

                insert_query = "INSERT INTO web_element_data (element_key, tester_name, attributes_json, url, " \
                               "tag_name, ele_id, ele_key, ele_value, self_heal_dynamic_xpath, self_heal_cnn, dynamic_xpath, new_screenshot, element_screenshot) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                insert_data = (element_value, self.tester_name, attributes_json, str(current_url_value), tag_name_value,
                               self.id, self.key, self.value,
                               self.self_heal_dynamic_xpath,
                               self.self_heal_cnn,
                               self.dynamic_xpath,
                               self.new_screenshot,
                               element_screenshot_binary)
                # if self.driver.current_url not in urls:
                #     page_source = self.driver.page_source
                #     soup = BeautifulSoup(page_source, 'lxml')
                #     html_string = str(soup)
                #     check_query = "SELECT 1 FROM vector_store WHERE url = %s LIMIT 1"
                #     check_data = (self.driver.current_url,)
                #     cursor.execute(check_query, check_data)
                #     result = cursor.fetchone()
                #     print(f"result{result}")
                #     if not result:
                #         html_insert_query = "INSERT INTO vector_store (url, vector) VALUES (%s, %s)"
                #         html_insert_data = (self.driver.current_url, html_string)
                #         cursor.execute(html_insert_query, html_insert_data)
                #         connection.commit()

                try:
                    cursor.execute(insert_query, insert_data)
                    connection.commit()
                except Error as e:
                    print("error second", e)
            else:
                select_attributes_query = "SELECT attributes_json FROM web_element_data WHERE element_key = %s AND tester_name = %s"
                cursor.execute(select_attributes_query, (element_value, self.tester_name,))
                attributes_result_set = cursor.fetchone()
                if attributes_result_set:
                    existing_attributes_json = attributes_result_set[0]
                    if existing_attributes_json != attributes_json:
                        element_screenshot_binary = self.get_element_screenshot_as_base64(element_key, element_value)
                        delete_query = "DELETE FROM web_element_data WHERE element_key = %s AND tester_name = %s"
                        cursor.execute(delete_query, (element_value, self.tester_name,))
                        connection.commit()

                        insert_query = "INSERT INTO web_element_data (element_key, tester_name, attributes_json, url, " \
                                       "tag_name, ele_id, ele_key, ele_value, self_heal_dynamic_xpath, self_heal_cnn, dynamic_xpath, new_screenshot, element_screenshot) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        insert_data = (
                            element_value, self.tester_name, attributes_json, str(current_url_value), tag_name_value,
                            self.id, self.key, self.value,
                            self.self_heal_dynamic_xpath,
                            self.self_heal_cnn,
                            self.dynamic_xpath,
                            self.new_screenshot,
                            element_screenshot_binary)
                        cursor.execute(insert_query, insert_data)
                        connection.commit()
                    else:
                        update_query = "UPDATE web_element_data SET attributes_json = %s WHERE element_key = %s AND tester_name = %s"
                        cursor.execute(update_query, (attributes_json, element_value, self.tester_name))
                        connection.commit()
            self.id = info.element.id
            self.key = element_key
            self.value = element_value
            self.dynamic_xpath = web_info.dynamic_xpath
        except Error as e:
            print("error third", e)

        finally:
            cursor.close()
            connection.close()

        return info.get_element()

    def compare_json(self, stored_json, current_attributes):
        if stored_json is None:
            return True
        else:
            try:
                stored_json_node = json.loads(stored_json)
                for key, value in current_attributes.items():
                    stored_value_node = stored_json_node.get(key)
                    if stored_value_node is None or stored_value_node != value:
                        if stored_value_node is None and value == "":
                            continue
                        print("Difference found for key: " + key)
                        return False

                return True

            except Exception as e:
                return False

    def get_count(self):
        return self.count

    def save_images_to_directory(self, image_list, directory, format='PNG'):
        # Create the directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

        # Delete all existing images in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

        # Save the images to the directory
        for idx, image_data in enumerate(image_list):
            try:
                # Convert bytes to PIL Image if necessary
                if isinstance(image_data, bytes):
                    image = Image.open(io.BytesIO(image_data))
                else:
                    image = image_data

                file_path = os.path.join(directory, f'image_{idx + 1}.{format.lower()}')
                image.save(file_path, format=format)
                print(f'Saved image to {file_path}')
            except Exception as e:
                print(f'Failed to save image {idx + 1}. Reason: {e}')

    def fetch_screenshot_from_directory(self, element_key):
        directory = "element_pics"
        try:
            # Preprocess the element key to make it suitable for XPath expressions
            valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-'
            element_key = ''.join(c for c in element_key if c in valid_chars)

            # Get a list of all files in the directory
            files = os.listdir(directory)

            # Filter files based on the element key
            matching_files = [file for file in files if file.startswith(element_key) and file.endswith('.jpg')]

            # If there are matching files, return the first one
            if matching_files:
                first_matching_file = matching_files[0]
                file_path = os.path.join(directory, first_matching_file)
                with open(file_path, "rb") as file:
                    screenshot_data = file.read()
                return screenshot_data
            else:
                print("No matching screenshot found")
                return None
        except Exception as e:
            print(f"Error fetching screenshot: {e}")
            return None

    def extract_dom_elements(self):
        query = "//div[@id='billerDetailsDiv']//*[not(self::script) and not(self::style) and not(child::*)]"
        elements = self.driver.find_elements(By.XPATH, query)
        ids = []
        for element in elements:
            ids.append(element.id)
        print(ids)
        return elements

    def get_element_attributes(self, element_key, element_value, attrs):
        try:
            if element_key == "xpath" and isinstance(element_value, str):
                element = self.driver.find_element(By.XPATH, element_value)
            elif element_key == "id" and isinstance(element_value, str):
                element = self.driver.find_element(By.ID, element_value)
            elif element_key == "name" and isinstance(element_value, str):
                element = self.driver.find_element(By.NAME, element_value)
            elif element_key == "class_name" and isinstance(element_value, str):
                element = self.driver.find_element(By.CLASS_NAME, element_value)
            else:
                element = element_value
            tag_name = element.tag_name
            executor = self.driver
            items = executor.execute_script("""
                    var items = {};
                    for (index = 0; index < arguments[0].attributes.length; ++index) {
                        items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value
                    }
                    return items;
                """, element)

            attrs.update(items)
            text_content = element.text
            attrs["text"] = text_content
            return ElementInfo(tag_name, attrs, text_content, element, None)

        except (StaleElementReferenceException, NoSuchElementException) as e:
            print(e)
            print(f"Element with {element_key} '" + element_value + "' not found on the webpage.")
            return ElementInfo(None, None, None, None, None)

        except Exception as e:
            print(e)
            return ElementInfo(None, None, None, None, None)

    def create_dynamic_xpath_from_attributes(self, tag_name, attributes):
        valid_xpaths = []
        matching_elements_count = {}
        class_attr = attributes.get("class", "")
        text_attr = attributes.get("text", "")
        present_attributes = {key: value for key, value in attributes.items() if key != "class" and value != ""}

        for attr, value in present_attributes.items():
            xpath = f"//{tag_name}[@{attr}='{value}']"
            try:
                elements = self.driver.find_elements(By.XPATH, xpath)  # Corrected line
                matching_elements_count[xpath] = len(elements)
                if len(elements) == 1:
                    valid_xpaths.append(xpath)
            except NoSuchElementException:
                # Element not found
                pass

        for valid_xpath in valid_xpaths:
            matching_elements_count.pop(valid_xpath, None)

        if not valid_xpaths and text_attr != "":
            text_xpath = f"//{tag_name}[text()='{text_attr}']"
            try:
                elements = self.driver.find_elements(By.XPATH, text_xpath)
                if len(elements) >= 1:
                    valid_xpaths.append(text_xpath)
            except NoSuchElementException:
                pass

        if not valid_xpaths and class_attr != "":
            class_xpath = f"//{tag_name}[contains(@class, '{class_attr}')]"
            try:
                elements = self.driver.find_elements(By.XPATH, class_xpath)
                if len(elements) >= 1:
                    valid_xpaths.append(class_xpath)
            except NoSuchElementException:
                pass

        if not valid_xpaths:
            all_attributes = {key: value for key, value in present_attributes.items()}
            for attr, value in all_attributes.items():
                xpath = f"//{tag_name}[@{attr}='{value}'][1]"
                try:
                    elements = self.driver.find_elements(By.XPATH, xpath)  # Corrected line
                    matching_elements_count[xpath] = len(elements)
                    if len(elements) == 1:
                        valid_xpaths.append(xpath)
                except NoSuchElementException:
                    pass

        return valid_xpaths

    def get_element_screenshot_as_base64(self, element_key, element_value):
        try:
            query = "//body//*[not(self::script) and not(self::style) and not(child::*)]"
            elements = self.driver.find_elements(By.XPATH, query)
            element = None
            if element_key == "xpath":
                element = self.driver.find_element(By.XPATH, element_value)
            elif element_key == "id":
                element = self.driver.find_element(By.ID, element_value)
            elif element_key == "name":
                element = self.driver.find_element(By.NAME, element_value)
            else:
                element = self.driver.find_element(By.CLASS_NAME, element_value)

            if element.size['width'] > 0 and element.size['height']:
                self.driver.execute_script(
                    "window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.pageYOffset + arguments[1]);",
                    element,
                    -100)
                x = element.location['x']
                y = element.location['y']
                width = element.size['width']
                height = element.size['height']

                js_code = """
                                            var elementToExclude = arguments[0];
                                            var query = '//body//*[not(self::script) and not(self::style) and not(child::*)]';
                                            var elements = document.evaluate(query, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                                            setTimeout(function() {
                                               for (var i = 0; i < elements.snapshotLength; i++) {
                                                     var element = elements.snapshotItem(i);
                                                     if (element !== elementToExclude) {
                                                        element.style.filter = 'blur(4px)';
                                                    }
                                                }
                                            }, 0);
                                            """

                self.driver.execute_script(js_code, element)

                rect = self.driver.execute_script('''
                                   var rect = document.createElement("div");
                                   rect.style.position = "absolute";
                                   rect.style.left = arguments[0] + "px";
                                   rect.style.top = arguments[1] + "px";
                                   rect.style.width = arguments[2] + "px";
                                   rect.style.height = arguments[3] + "px";
                                   rect.style.border = "2px solid green";
                                   rect.style.zIndex = "9999";
                                   document.body.appendChild(rect);
                                   return rect;
                               ''', x, y, width, height)

                # Get the screenshot as PNG
                element_screenshot = self.driver.get_screenshot_as_png()

                # Remove the blur effect and overlay from the webpage
                js = """
                                        var elementToExclude = arguments[0];
                                        var query = '//body//*[not(self::script) and not(self::style) and not(child::*)]';
                                        var elements = document.evaluate(query, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                                        setTimeout(function() {
                                            for (var i = 0; i < elements.snapshotLength; i++) {
                                                var element = elements.snapshotItem(i);
                                                   if (element !== elementToExclude) {
                                                        element.style.filter = '';  // Remove the blur effect
                                                  }
                                            }
                                        }, 0);
                                        """

                # Execute the JavaScript code passing the element to exclude
                self.driver.execute_script(js, element)
                self.driver.execute_script('document.body.removeChild(arguments[0]);', rect)
                element_screenshot_base64 = base64.b64encode(element_screenshot).decode('utf-8')
                return element_screenshot_base64
        except:
            return None

    def capture_screenshot_of_element(self, element_key, element_value):
        directory = "training_data"
        os.makedirs(directory, exist_ok=True)

        try:
            element = None
            if element_key == "xpath":
                print("xpath")
                element = self.driver.find_element(By.XPATH, element_value)
            elif element_key == "id":
                print("id")
                element = self.driver.find_element(By.ID, element_value)
            elif element_key == "name":
                print("name")
                element = self.driver.find_element(By.NAME, element_value)
            else:
                print("classname")
                element = self.driver.find_element(By.CLASS_NAME, element_value)

            valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-'
            element_name = ''.join(c for c in element_value if c in valid_chars)

            if element.size['width'] > 0 and element.size['height']:
                tag_name = element.tag_name
                self.driver.execute_script(
                    "window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.pageYOffset + arguments[1]);",
                    element,
                    -0)
                x = element.location['x']
                y = element.location['y']
                width = element.size['width']
                height = element.size['height']
                screenshot_folder = os.path.join(directory, element_name)
                os.makedirs(screenshot_folder, exist_ok=True)
                js_code = """
                            var elementToExclude = arguments[0];
                            var query = '//body//*[not(self::script) and not(self::style) and not(child::*)]';
                            var elements = document.evaluate(query, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                            setTimeout(function() {
                               for (var i = 0; i < elements.snapshotLength; i++) {
                                     var element = elements.snapshotItem(i);
                                     if (element !== elementToExclude) {
                                        element.style.filter = 'blur(4px)';
                                    }
                                }
                            }, 0);
                            """

                self.driver.execute_script(js_code, element)

                rect = self.driver.execute_script('''
                                var rect = document.createElement("div");
                                rect.style.position = "absolute";
                                rect.style.left = arguments[0] + "px";
                                rect.style.top = arguments[1] + "px";
                                rect.style.width = arguments[2] + "px";
                                rect.style.height = arguments[3] + "px";
                                rect.style.border = "2px solid green";
                                rect.style.zIndex = "9999";
                                document.body.appendChild(rect);
                                return rect;
                            ''', x, y, width, height)

                # Capture element screenshot and add to the folder
                image = f"{tag_name}.jpg"
                screenshot_path = os.path.join(screenshot_folder, image)
                self.driver.save_screenshot(screenshot_path)

                num_copies = 500
                for i in range(1, num_copies + 1):
                    copy_path = os.path.join(screenshot_folder, f"{tag_name}_{i}.jpg")
                    shutil.copy(screenshot_path, copy_path)

                # Remove the blur effect and overlay from the webpage
                js = """
                        var elementToExclude = arguments[0];
                        var query = '//body//*[not(self::script) and not(self::style) and not(child::*)]';
                        var elements = document.evaluate(query, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                        setTimeout(function() {
                            for (var i = 0; i < elements.snapshotLength; i++) {
                                var element = elements.snapshotItem(i);
                                   if (element !== elementToExclude) {
                                        element.style.filter = '';  // Remove the blur effect
                                  }
                            }
                        }, 0);
                        """

                # Execute the JavaScript code passing the element to exclude
                self.driver.execute_script(js, element)
                self.driver.execute_script('document.body.removeChild(arguments[0]);', rect)
        except Exception as e:
            print("unable to do this operation", e)
            return None
        finally:
            # Return the dictionary of screenshots
            return None

    def capture_screenshot_of_element_rag(self, element_value):
        element = self.driver.find_element(By.XPATH, element_value)

        if element.size['width'] > 0 and element.size['height']:
            tag_name = element.tag_name
        self.driver.execute_script(
            "window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.pageYOffset + arguments[1]);",
            element,
            -0)
        x = element.location['x']
        y = element.location['y']
        width = element.size['width']
        height = element.size['height']

        rect = self.driver.execute_script('''
                                var rect = document.createElement("div");
                                rect.style.position = "absolute";
                                rect.style.left = arguments[0] + "px";
                                rect.style.top = arguments[1] + "px";
                                rect.style.width = arguments[2] + "px";
                                rect.style.height = arguments[3] + "px";
                                rect.style.border = "2px solid green";
                                rect.style.zIndex = "9999";
                                document.body.appendChild(rect);
                                return rect;
                            ''', x, y, width, height)

        element_screenshot = self.driver.get_screenshot_as_png()
        return element_screenshot

    def fetch_dom_element_screenshots(self):
        screenshots_dict = {}

        try:
            query = "//body//*[not(self::script) and not(self::style) and not(child::*)]"
            elements = self.driver.find_elements(By.XPATH, query)

            # Iterate over elements to mark and capture screenshots
            for index, element in enumerate(elements):
                if element.size['width'] > 0 and element.size['height']:
                    self.driver.execute_script(
                        "window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.pageYOffset + arguments[1]);",
                        element,
                        -0)
                    # Get the position of the element using JavaScript
                    x = element.location['x']
                    y = element.location['y']
                    width = element.size['width']
                    height = element.size['height']

                    # Blur all other elements except the current one
                    js_code = """
                                                                    var elementToExclude = arguments[0];
                                                                    var query = '//body//*[not(self::script) and not(self::style) and not(child::*)]';
                                                                    var elements = document.evaluate(query, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                                                                    setTimeout(function() {
                                                                       for (var i = 0; i < elements.snapshotLength; i++) {
                                                                             var element = elements.snapshotItem(i);
                                                                             if (element !== elementToExclude) {
                                                                                element.style.filter = 'blur(4px)';
                                                                            }
                                                                        }
                                                                    }, 0);
                                                                    """

                    self.driver.execute_script(js_code, element)

                    # Execute JavaScript to overlay a rectangle onto the webpage
                    rect = self.driver.execute_script('''
                            var rect = document.createElement("div");
                            rect.style.position = "absolute";
                            rect.style.left = arguments[0] + "px";
                            rect.style.top = arguments[1] + "px";
                            rect.style.width = arguments[2] + "px";
                            rect.style.height = arguments[3] + "px";
                            rect.style.border = "2px solid green";
                            rect.style.zIndex = "9999";
                            document.body.appendChild(rect);
                            return rect;
                        ''', x, y, width, height)

                    # Capture element screenshot and add to the dictionary
                    element_screenshot = self.driver.get_screenshot_as_png()
                    # os.makedirs("cnnimage", exist_ok=True)
                    # self.save_screenshot(f'{element.id}.png')
                    directory = "PracticeCNN"
                    os.makedirs(directory, exist_ok=True)
                    screenshot_folder = os.path.join(directory, self.id)
                    os.makedirs(screenshot_folder, exist_ok=True)
                    image = f"{element.id}.jpg"
                    screenshot_path = os.path.join(screenshot_folder, image)
                    self.driver.save_screenshot(screenshot_path)
                    screenshots_dict[element] = element_screenshot

                    # Remove the blur effect and overlay from the webpage
                    js = """
                                                  var elementToExclude = arguments[0];
                                                  var query = '//body//*[not(self::script) and not(self::style) and not(child::*)]';
                                                  var elements = document.evaluate(query, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                                                  setTimeout(function() {
                                                  for (var i = 0; i < elements.snapshotLength; i++) {
                                                        var element = elements.snapshotItem(i);
                                                        if (element !== elementToExclude) {
                                                             element.style.filter = '';  // Remove the blur effect
                                                        }
                                                  }
                                                  }, 0);
                                                  """

                    # Execute the JavaScript code passing the element to exclude
                    self.driver.execute_script(js, element)
                    self.driver.execute_script('document.body.removeChild(arguments[0]);', rect)
        finally:
            # Return the dictionary of screenshots
            return screenshots_dict

    def preprocess_image(self, image):
        try:
            image_resized = cv2.resize(image, (128, 128))
            # Normalize pixel values
            image_normalized = image_resized / 255.0
            return image_normalized
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None

    def get_prediction(self, screenshot):
        try:
            nparr = np.frombuffer(screenshot, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is not None:
                resized_img = cv2.resize(img, (128, 128))
                normalized_img = resized_img / 255.0
                element_screenshot = normalized_img.reshape(1, 128, 128, 3)
                predictions = login_model.predict(element_screenshot)
                decoded_predictions = label_encoder.inverse_transform(np.argmax(predictions, axis=1))
                probabilities = np.squeeze(np.exp(predictions) / np.sum(np.exp(predictions), axis=-1))
                confidence = np.max(probabilities) * 100
                return decoded_predictions[0], confidence
            else:
                print("Error decoding image. Input data may be corrupted.")
                return None
        except Exception as e:
            print(f"Error processing screenshot: {e}")
            return None

    def get_directory_modification_time(self):
        try:
            modification_time = os.path.getmtime("training_data")
            return modification_time
        except OSError:
            print(f"Error: Unable to get modification time for directory")
            return None

    def process_images(self, image_file, target_size=(128, 128)):
        image = Image.open(io.BytesIO(image_file))
        resized_image = image.resize(target_size)
        return resized_image

    def get_image_index(self, dom_dict, target_image):
        image_list = []
        for im in dom_dict:
            im_ls = self.process_images(im)
            image_list.append(im_ls)
        print(f"dom dict ------------ ", image_list)
        print(f"target image", target_image)
        prompt = f"""
            You are a computer vision model to identify the element changed in the dom.
            Given a list of elements screenshots in which
            elements are highlighted and background blurred which was captured from the previous dom \n image list:{image_list} \n
            Now the element is modified and it's screenshot is given:\n target image :{target_image}\n
            search through the list and find out the image which has the most similarity that the element  might be an old version of target image.
            Return the index of the image in the list. Respond only the index value. Return None if there is no image.

            """
        try:
            generation_config = {
                "temperature": 0,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            model = genai.GenerativeModel(
                model_name="gemini-pro-vision",
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            convo = model.start_chat(history=[])
            convo.send_message([prompt, target_image])
            image_index = convo.last.text
            return image_index
        except Exception as e:
            print(f"some error occured {e}")
            return None

    def get_connection(self):
        db_url = "jdbc:mysql://localhost:3306/sampledb"
        db_user = "root"
        db_password = ""
        try:
            self.connection = mysql.connector.connect(host="localhost", user="root", password="", database="sampledb")
        except Error as e:
            print(e)

        return self.connection
