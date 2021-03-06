# -*- coding: utf-8 -*-
import os
from os.path import normpath, join

from selenium.common.exceptions import NoSuchElementException

from component import Component
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from tests.components.cloud_file import CloudFile
from tests.components.mail_file import MailFile


class WriteLetter(Component):
    BASE = '//*[@data-qa-id="compose-app"][@message-uid]'

    # Inputs
    THEME_INPUT = BASE + '//*[@data-test-id="subject"]//input'
    TO_INPUT = BASE + '//*[@data-test-id="to"]//input'
    WHOM_COPY_INPUT = BASE + \
        '//*[@data-test-id="cc"]//*[@data-type="cc"]//input'
    WHOM_HIDDEN_COPY_INPUT = BASE + \
        '//*[@data-test-id="bcc"]//*[@data-type="bcc"]//input'
    TEXT_INPUT = BASE + '//*[@data-test-id="editor"]' \
        '//div[contains(concat(" ", normalize-space(@class), " "),' + \
                        ' " cke_editable ")]'
    SIGNATURE_INPUT = TEXT_INPUT + \
        '//div[contains(concat(" ", normalize-space(@class), " "),' + \
        ' " cke_widget_editable ")]'

    # Buttons
    SAVE_BUTTON = BASE + '//*[@data-qa-id="save"]'
    SEND_BUTTON = BASE + '//*[@data-qa-id="send"]'
    CLOSE_BUTTON = BASE + '//*[@data-test-id="close"]'
    PRIORITY_BUTTON = BASE + '//*[@data-qa-id="priority"]'
    PRIORITY_BUTTON_ACTIVE = PRIORITY_BUTTON + \
        '//div[contains(concat(" ", normalize-space(@class), " "), " b-selected-0-1-23 ")]'
    RECEIPT_BUTTON = BASE + '//*[@data-qa-id="receipt"]'
    RECEIPT_BUTTON_ACTIVE = RECEIPT_BUTTON + \
        '//div[contains(concat(" ", normalize-space(@class), " "), " b-selected-0-1-23 ")]'
    ADD_WHOM_COPY_INPUT_BUTTON = BASE + '//*[@data-test-id="cc"]'
    REMIND_BUTTON = BASE + '//*[@data-qa-id="remind"]'
    REMIND_BUTTON_ACTIVE = REMIND_BUTTON + \
        '//div[contains(concat(" ", normalize-space(@class), " "), " c-selected-0-1-13 ")]'
    SCHEDULE_BUTTON = BASE + '//*[@data-qa-id="schedule"]'
    SCHEDULE_BUTTON_ACTIVE = SCHEDULE_BUTTON + \
        '//div[contains(concat(" ", normalize-space(@class), " "), " b-selected-0-1-5 ")]'
    ADD_WHOM_HIDDEN_COPY_INPUT_BUTTON = BASE + '//*[@data-test-id="bcc"]'
    ATTACH_CONTROLS = BASE + '//*[@data-test-id="attach-controls"]'
    FILE_ATTACH_BUTTON = ATTACH_CONTROLS + '//*[@data-test-id="attach-file"]'
    CLOUD_ATTACH_BUTTON = ATTACH_CONTROLS + '//*[@data-test-id="attach-cloud"]'
    MAIL_ATTACH_BUTTON = ATTACH_CONTROLS + '//*[@data-test-id="attach-mail"]'

    TO_CHECK = BASE + \
        '//*[@data-test-id="to"]//*[@data-test-id="operand:base:{}"]'
    WHOM_COPY_CHECK = BASE + \
        '//*[@data-test-id="cc"]//*[@data-test-id="operand:base:{}"]'
    WHOM_HIDDEN_COPY_CHECK = BASE + \
        '//*[@data-test-id="bcc"]//*[@data-test-id="operand:base:{}"]'

    ATTACHED_FILES = BASE + '//*[@data-test-id="attach-slider"]'
    ATTACH_FILE_CHECK = ATTACHED_FILES + \
        '//*[@data-test-id="attach:{}:loaded"]'

    NOTIFICATION = '//*[@data-qa-id="message"][contains(text(), "{}")]'
    CLOSE_WINDOW_AFTER_SENDING_LETTER = '//*[@data-qa-id="close"]'

    def set_theme(self, theme):
        set_theme_input = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.THEME_INPUT)
        )
        set_theme_input.clear()
        set_theme_input.send_keys(theme)

    def save(self):
        try_again = True
        while try_again:
            save_button = WebDriverWait(self.driver, 30, 0.1).until(
                ec.element_to_be_clickable((By.XPATH, self.SAVE_BUTTON))
            )
            save_button.click()
            try:
                WebDriverWait(self.driver, 5, 0.1).until(
                    lambda d: d.find_element_by_xpath(
                        self.NOTIFICATION.format('Сохранено'))
                )
                try_again = False
            except:
                try_again = True

    def close(self):
        close_button = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.CLOSE_BUTTON)
        )
        close_button.click()

    def set_important(self):
        important_button = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.PRIORITY_BUTTON)
        )
        important_button.click()

    def check_important_is_set(self):
        try:
            WebDriverWait(self.driver, 30, 0.1).until(
                lambda d: d.find_element_by_xpath(self.PRIORITY_BUTTON_ACTIVE)
            )
            return True
        except NoSuchElementException:
            return False

    def set_whom(self, whom):
        whom_input = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TO_INPUT)
        )
        whom_input.clear()
        whom_input.send_keys(whom)

    def check_whom(self, whom):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TO_CHECK.format(whom))
        )

    def set_notify(self):
        receipt_button = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.RECEIPT_BUTTON)
        )
        receipt_button.click()

    def check_notify_is_set(self):
        try:
            WebDriverWait(self.driver, 30, 0.1).until(
                lambda d: d.find_element_by_xpath(self.RECEIPT_BUTTON_ACTIVE)
            )
            return True
        except NoSuchElementException:
            return False

    def set_whom_copy(self, whom_copy):
        add_whom_copy_input_button = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.ADD_WHOM_COPY_INPUT_BUTTON)
        )
        add_whom_copy_input_button.click()
        whom_copy_input = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.WHOM_COPY_INPUT)
        )
        whom_copy_input.clear()
        whom_copy_input.send_keys(whom_copy)
        self.driver.find_element_by_xpath(self.THEME_INPUT).click()

    def check_whom_copy(self, whom_copy):
        try:
            WebDriverWait(self.driver, 30, 0.1).until(
                lambda d: d.find_element_by_xpath(
                    self.WHOM_COPY_CHECK.format(whom_copy))
            )
            return True
        except NoSuchElementException:
            return False

    def set_remind_after(self):
        remind_button = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.REMIND_BUTTON)
        )
        remind_button.click()

    def check_remind_after_is_set(self):
        try:
            WebDriverWait(self.driver, 30, 0.1).until(
                lambda d: d.find_element_by_xpath(self.REMIND_BUTTON_ACTIVE)
            )
            return True
        except NoSuchElementException:
            return False

    def set_schedule(self):
        schedule_button = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.SCHEDULE_BUTTON)
        )
        schedule_button.click()

    def set_whom_hidden_copy(self, whom_hidden_copy):
        add_whom_hidden_copy_button = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(
                self.ADD_WHOM_HIDDEN_COPY_INPUT_BUTTON)
        )
        add_whom_hidden_copy_button.click()
        whom_hidden_copy_input = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.WHOM_HIDDEN_COPY_INPUT)
        )
        whom_hidden_copy_input.clear()
        whom_hidden_copy_input.send_keys(whom_hidden_copy)

    def check_whom_hidden_copy(self, whom_hidden_copy):
        try:
            WebDriverWait(self.driver, 30, 0.1).until(
                lambda d: d.find_element_by_xpath(
                    self.WHOM_HIDDEN_COPY_CHECK.format(whom_hidden_copy))
            )
            return True
        except NoSuchElementException:
            return False

    def add_file(self, file_path):
        add_file_input = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.FILE_ATTACH_BUTTON)
        )
        add_file_input.send_keys(normpath(join(os.getcwd(), file_path)))

    def check_added_file(self, filename):
        try:
            WebDriverWait(self.driver, 30, 0.1).until(
                ec.element_to_be_clickable(
                    (By.XPATH, self.ATTACH_FILE_CHECK.format(filename)))
            )
            return True
        except NoSuchElementException:
            return False

    def open_add_cloud_file(self):
        add_file_cloud_button = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.CLOUD_ATTACH_BUTTON)
        )
        add_file_cloud_button.click()

    def open_add_mail_file(self):
        add_file_mail_button = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MAIL_ATTACH_BUTTON)
        )
        add_file_mail_button.click()

    def wait_for_save(self, seconds):
        WebDriverWait(self.driver, seconds, 0.1).until(
            lambda d: d.find_element_by_xpath(
                self.NOTIFICATION.format('Сохранено'))
        )

    def set_text(self, text):
        text_input = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TEXT_INPUT)
        )
        text_input.send_keys(text)

    def get_text(self):
        text_input = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.TEXT_INPUT)
        )
        return text_input.text

    def set_signature(self, text):
        signature_input = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.SIGNATURE_INPUT)
        )
        signature_input.clear()
        signature_input.send_keys(text)

    def get_signature(self):
        signature_input = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.SIGNATURE_INPUT)
        )
        return signature_input.text

    def send_letter(self):
        send_letter = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.SEND_BUTTON)
        )
        send_letter.click()

    def close_window(self):
        close_window = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(
                self.CLOSE_WINDOW_AFTER_SENDING_LETTER)
        )
        close_window.click()

    def add_mail_file(self, folder, file):
        self.open_add_mail_file()
        mail_file = MailFile(self.driver)
        mail_file.change_folder(folder)
        mail_file.attach_mail_file(file)

    def add_cloud_file(self, file):
        self.open_add_cloud_file()
        cloud_file = CloudFile(self.driver)
        cloud_file.attach_cloud_file(file)
