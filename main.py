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

        self.href_list = []
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

    def parse_answer(self):
        pass

    # вход в аккаунт
    def authorisation(self):
        self.auth.get('https://inf-ege.sdamgia.ru/')
        auth_form = list(self.auth.find_elements_by_tag_name('input')[1:3])
        auth_form[0].send_keys(self.log)
        auth_form[1].send_keys(self.pas)
        self.auth.find_elements_by_tag_name('button')[0].click()

    def auth_check(self):
        pass

    # переход на страницу теста и парсинг ссылок на страницы с заданиями
    def exercise_parsing(self):
        self.auth.get(f'https://inf-ege.sdamgia.ru/test?id={self.test_id}')
        sleep(3)
        exercises = self.auth.find_elements_by_class_name('prob_nums')
        href_list = list(map(lambda num: num.find_element_by_partial_link_text('').get_attribute('href'), exercises))
        self.href_list = href_list

    # парсинг и вывод ответов из страниц с заданиями
    def answers_parsing(self):
        href_list = self.href_list
        answers = []
        for i in range(len(href_list)):
            href = href_list[i]
            self.anon.get(href)
            sleep(0.1)
            raw_answer = self.anon.find_element_by_class_name('answer')
            answer = raw_answer.get_attribute('textContent').strip('Ответ: ')
            answers.append(answer)
        self.anon.quit()
        self.answers = answers

    def answers_print(self):
        answers = self.answers
        inp_list = list(self.auth.find_elements_by_tag_name('input')[7:-1])
        for i in range(len(answers)):
            self.auth.execute_script("return arguments[0].scrollIntoView(true);", inp_list[i])
            sleep(1)
            print(i+1, end=' ')
            inp_list[i].send_keys(answers[i])
        print('\n')
        sleep(self.test_time)
        self.auth.find_elements_by_tag_name('input')[-1].click()
        sleep(3)

    def answer_change(self, num, answer):
        self.answers[num+1] = answer

    def input_parsing(self):
        pass

    def input_answers(self):
        pass

    def finish_test(self):
        pass
