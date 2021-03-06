# coding=utf-8
import unittest
import os

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from tests.components.cloud_file import CloudFile
from tests.components.mail_file import MailFile
from tests.components.write_letter import WriteLetter
from tests.pages.auth_page import AuthPage
from tests.pages.drafts_page import DraftsPage
from tests.pages.main_page import MainPage

from selenium.webdriver import DesiredCapabilities, Remote


class Test(unittest.TestCase):
    USER_EMAIL = 'ttexnopark@mail.ru'
    PASSWORD = os.environ['PASSWORD']

    TEST_THEME = 'Testing mail.ru octavius'
    TEST_WHOM = 'test123@mail.ru'
    TEST_WHOM_COPY = 'test456@mail.ru'
    TEST_WHOM_HIDDEN_COPY = 'test789@mail.ru'
    TEST_MESSAGE = u'Много текста\n\n\nДА ДА ДА МНОГО'
    TEST_SIGNATURE = u'Тут был Вася'
    TEST_FILE = 'requirements.txt'
    SECONDS_TO_AUTOSAVE = 10
    TEST_CLOUD_FILE = 'Берег.jpg'
    TEST_MAIL_FOLDER = 'Корзина'
    TEST_MAIL_FILE = 'Берег.jpg'

    def setUp(self):
        browser = os.environ.get('BROWSER', 'CHROME')

        # self.driver = webdriver.Chrome('./chromedriver')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        auth_page = AuthPage(self.driver)  # Авторизация
        auth_page.form.authorize(self.USER_EMAIL, self.PASSWORD)

        self.main_page = MainPage(self.driver)
        self.main_page.sidebar.go_to_folder('Черновики')
        drafts_page = DraftsPage(self.driver)
        drafts_page.clear_letters()

    def tearDown(self):
        drafts_page = DraftsPage(self.driver)
        drafts_page.clear_letters()
        self.driver.quit()

    def testAdditionsFromMail(self):
        drafts_page = DraftsPage(self.driver)
        drafts_page.sidebar.write_letter()
        write_letter = WriteLetter(self.driver)
        write_letter.set_theme(self.TEST_THEME)
        write_letter.add_mail_file(self.TEST_MAIL_FOLDER, self.TEST_MAIL_FILE)
        write_letter.save()
        write_letter.close()
        drafts_page.letters.open_letter_by_subject(self.TEST_THEME)
        self.assertTrue(
            write_letter.check_added_file(self.TEST_MAIL_FILE),
            'No added file, expected {}'.format(self.TEST_MAIL_FILE)
        )
        write_letter.close()

    def testAdditionsFromUser(self):
        drafts_page = DraftsPage(self.driver)
        drafts_page.sidebar.write_letter()
        write_letter = WriteLetter(self.driver)
        write_letter.set_theme(self.TEST_THEME)
        write_letter.add_file(self.TEST_FILE)
        write_letter.save()
        write_letter.close()
        drafts_page.letters.open_letter_by_subject(self.TEST_THEME)
        self.assertTrue(
            write_letter.check_added_file(self.TEST_FILE),
            'No added file, expected {}'.format(self.TEST_FILE)
        )
        write_letter.close()

    def testAdditionsFromCLoud(self):
        drafts_page = DraftsPage(self.driver)
        drafts_page.sidebar.write_letter()
        write_letter = WriteLetter(self.driver)
        write_letter.set_theme(self.TEST_THEME)
        write_letter.add_cloud_file(self.TEST_CLOUD_FILE)
        write_letter.save()
        write_letter.close()
        drafts_page.letters.open_letter_by_subject(self.TEST_THEME)
        self.assertTrue(
            write_letter.check_added_file(self.TEST_CLOUD_FILE),
            'No added file, expected {}'.format(self.TEST_CLOUD_FILE)
        )
        write_letter.close()

    def testTheme(self):
        drafts_page = DraftsPage(self.driver)
        drafts_page.sidebar.write_letter()
        write_letter = WriteLetter(self.driver)
        write_letter.set_theme(self.TEST_THEME)
        write_letter.set_important()
        write_letter.save()
        write_letter.close()
        drafts_page.letters.open_letter_by_subject(self.TEST_THEME)
        self.assertTrue(
            write_letter.check_important_is_set(),
            'Important mark is not set, but was set before saving the draft'
        )
        write_letter.close()

    def testWhom(self):
        drafts_page = DraftsPage(self.driver)
        drafts_page.sidebar.write_letter()
        write_letter = WriteLetter(self.driver)
        write_letter.set_whom(self.TEST_WHOM)
        write_letter.set_theme(self.TEST_THEME)
        write_letter.set_notify()
        write_letter.save()
        write_letter.close()
        drafts_page.letters.open_letter_by_subject(self.TEST_THEME)
        write_letter.check_whom(self.TEST_WHOM)
        self.assertTrue(
            write_letter.check_notify_is_set(),
            'Notify mark is not set, but was set before saving the draft'
        )
        write_letter.close()

    def testCopy(self):
        drafts_page = DraftsPage(self.driver)
        drafts_page.sidebar.write_letter()
        write_letter = WriteLetter(self.driver)
        write_letter.set_whom_copy(self.TEST_WHOM_COPY)
        write_letter.set_remind_after()
        write_letter.save()
        write_letter.close()
        drafts_page.letters.open_rand()
        self.assertTrue(
            write_letter.check_whom_copy(self.TEST_WHOM_COPY),
            'Copy is addressed not to {}, but was set to it before saving the draft'.format(self.TEST_WHOM_COPY)
        )
        self.assertTrue(
            write_letter.check_remind_after_is_set(),
            'Remind mark is not set, but was set before saving the draft'
        )
        write_letter.close()

    def testHiddenCopy(self):
        drafts_page = DraftsPage(self.driver)
        drafts_page.sidebar.write_letter()
        write_letter = WriteLetter(self.driver)
        write_letter.set_whom_hidden_copy(self.TEST_WHOM_HIDDEN_COPY)
        write_letter.set_theme(self.TEST_THEME)
        write_letter.set_schedule()
        write_letter.save()
        write_letter.close()
        drafts_page.letters.open_letter_by_subject(self.TEST_THEME)
        self.assertTrue(
            write_letter.check_whom_hidden_copy(self.TEST_WHOM_HIDDEN_COPY),
            'Hidden copy is addressed not to {}, but was set to it before saving the draft'.format(
                self.TEST_WHOM_HIDDEN_COPY
            )
        )
        write_letter.close()

    def testText(self):
        drafts_page = DraftsPage(self.driver)
        drafts_page.sidebar.write_letter()
        write_letter = WriteLetter(self.driver)
        write_letter.set_text(self.TEST_MESSAGE)
        write_letter.set_theme(self.TEST_THEME)
        write_letter.wait_for_save(65)
        write_letter.close()
        drafts_page.letters.open_letter_by_subject(self.TEST_THEME)
        self.assertEqual(self.TEST_MESSAGE, write_letter.get_text()[:len(self.TEST_MESSAGE)],
                         'Текст в поле сообщения черновика не соответствует ранее заданному')
        write_letter.close()

    def testSignature(self):
        drafts_page = DraftsPage(self.driver)
        drafts_page.sidebar.write_letter()
        write_letter = WriteLetter(self.driver)
        write_letter.set_signature(self.TEST_SIGNATURE)
        write_letter.set_theme(self.TEST_THEME)
        write_letter.save()
        write_letter.close()
        drafts_page.letters.open_letter_by_subject(self.TEST_THEME)
        self.assertEqual(self.TEST_SIGNATURE, write_letter.get_signature(),
                         'Текст в поле подписи черновика не соответствует ранее заданному')
        write_letter.close()
