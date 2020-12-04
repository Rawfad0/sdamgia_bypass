from time import sleep
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
except Exception as ex:
    print(ex)
    print('Install "selenium" using this command: "pip3 install selenium"')


class TestSolver:

    def __init__(self, test_id, test_time):
        path = './chromedriver'
        self.auth = webdriver.Chrome(path)

        file = open('./inputs.txt', 'r')
        self.log = file.readline()
        self.pas = file.readline()
        file.close()

        self.test_id = test_id
        self.test_time = test_time

        self.url_list = []
        self.answers = []

        options = Options()
        options.add_argument("--headless")
        self.anon = webdriver.Chrome(path, options=options)

    @staticmethod
    def num2url(nums):
        if str(type(nums)) == "<class 'list'>":
            url_list = [f'https://rus-ege.sdamgia.ru/problem?id={num}' for num in nums]
            return url_list
        if (str(type(nums)) == "<class 'str'>") or (str(type(nums)) == "<class 'int'>"):
            num = nums
            url = f'https://rus-ege.sdamgia.ru/problem?id={num}'
            return url

    @staticmethod
    def url2num(urls):
        if str(type(urls)) == "<class 'list'>":
            num_list = [url[url.index('=') + 1:] for url in urls]
            return num_list
        if (str(type(urls)) == "<class 'str'>") or (str(type(urls)) == "<class 'int'>"):
            url = urls
            num = url[url.index('=') + 1:]
            return num

    # вход в аккаунт
    def authorisation(self):
        self.auth.get('https://inf-ege.sdamgia.ru/')
        auth_form = list(self.auth.find_elements_by_tag_name('input')[1:3])
        auth_form[0].send_keys(self.log)
        auth_form[1].send_keys(self.pas)
        self.auth.find_elements_by_tag_name('button')[0].click()

    def auth_check(self):
        target_object = self.auth.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/script[1]')
        target_text = target_object.get_attribute('textContent')
        target_bool = target_text[target_text.index('=') + 2:target_text.index(';')]
        if target_bool is True:
            return False
        elif target_bool is False:
            return True
        else:
            raise Exception

    # переход на страницу теста и парсинг ссылок на страницы с заданиями
    def exercise_parsing(self):
        self.auth.get(f'https://inf-ege.sdamgia.ru/test?id={self.test_id}')
        sleep(3)
        exercises = self.auth.find_elements_by_class_name('prob_nums')
        href_list = [num.find_element_by_partial_link_text('').get_attribute('href') for num in exercises]
        self.url_list = href_list

    def parse_answer(self, url):
        self.anon.get(url)
        sleep(0.1)
        raw_answer = self.anon.find_element_by_class_name('answer')
        answer = raw_answer.get_attribute('textContent')
        answer = answer[answer.index(':')+1:]
        return answer

    def answers_parsing(self):
        url_list = self.url_list
        answers = [self.parse_answer(url) for url in url_list]
        self.anon.quit()
        self.answers = answers

    def answers_print(self):
        answers = self.answers
        print('№\tid\t\tanswer')
        for i in range(len(answers)):
            print(f'{i + 1}:\t{answers[i]}')

    def answer_change(self, num, answer):
        self.answers[num+1] = answer

    @staticmethod
    def scroll(driver, target):
        driver.execute_script("return arguments[0].scrollIntoView(true);", target)

    def answers_input(self):
        answers = self.answers
        inp_list = list(self.auth.find_elements_by_tag_name('input')[7:-1])
        for i in range(len(answers)):
            self.auth.execute_script("return arguments[0].scrollIntoView(true);", inp_list[i])
            sleep(1)
            print(i + 1, end=' ')
            inp_list[i].send_keys(answers[i])
        print('\n')
        sleep(self.test_time)
        self.auth.find_elements_by_tag_name('input')[-1].click()
        sleep(3)

    def input_parsing(self):
        pass

    def input_answers(self):
        pass

    def finish_test(self):
        pass

    def table_parse(self):
        pass

    def table_print(self):
        pass
