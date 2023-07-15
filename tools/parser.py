from settings import *
import time

class Pars(Thread):
    def __init__(self, filepath, invisable=False) -> None:
        Thread.__init__(self)
        self.based_browser_startUp(invisable) # обычный запуск без dolphin
        self.wait = WebDriverWait(self.driver,5)
        self.action = ActionChains(self.driver,250)

        self.file_path = filepath
        self.max_count = 0
        self.count_now = 0
        self.finding_link = 0
        self.working = True

    def authorithation(self):
        pass

    def based_browser_startUp(self, invisable):
        options = Options()
        if invisable:
            options.add_argument('--headless')
        # Отключаем уведомления
        options.add_argument("--disable-notifications")
        # Отключаем логирование
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()),options=options)
        self.driver.set_window_size(1920, 1080)
    
    def read_excel(self):
        df = pd.read_excel(self.file_path, skiprows=6)  # Пропускаем первые 6 строк
        self.max_count = df.iloc[:,4].count()
        return df
    
    def write_excel(self, df:pd.DataFrame):
        # df = df.iloc[:,[4,11]]
        df.to_excel(self.file_path, index=False)  # Перезаписываем файл Excel

    def birank_fuck_off(self):
        time.sleep(0.25)
        try:
            self.driver.find_element(By.XPATH,'//section//input[@name="user[name]"]').send_keys("Отвалите")
            self.driver.find_element(By.XPATH,'//section//input[@name="user[phone]"]').send_keys("+78005553535")
            self.driver.find_element(By.XPATH,'//section//input[@name="user[email]"]').send_keys("fuck_this_form@cock.you")
            self.driver.find_element(By.XPATH,'//section//input[@class="button1"]').click()
        except:
            pass            
    
    def birank_join(self):
        self.driver.get("https://birank.com/ru-ru/")
        self.birank_fuck_off()
        
    
    def get_comp_link_bitrank(self,INN):
        try:
            self.driver.find_element(By.XPATH,'//input[@id="autocomplete"]').click()
            self.action.key_down(Keys.CONTROL).send_keys('A').perform()
            self.action.key_up(Keys.CONTROL).perform()
            self.action.send_keys(Keys.DELETE).perform()
            self.driver.find_element(By.XPATH,'//input[@id="autocomplete"]').send_keys(INN)
            self.action.send_keys(Keys.ENTER).perform()
            try:
                self.wait.until(EC.element_to_be_clickable((By.XPATH,'//article[@class="articleSearch"]/a')))
                self.driver.find_element(By.XPATH,'//article[@class="articleSearch"]/a').click()
            except:
                links = "-"
            
            try:
                links = self.driver.find_elements(By.XPATH,'//div[@class="cell-contents contact-wrapper"]//a[@class="content-link"]')
                links = ', '.join(list(map(lambda x: x.get_attribute('href'),links)))
                self.finding_link += 1 # НАЙДЕННЫХ ССЫЛОК
            except:
                links = "-"
            return(links)
        except:
            self.driver.get("https://birank.com/ru-ru/")
            logging.error(traceback.format_exc())
            pass

    def bitrank_parsing(self,df:pd.DataFrame):
        self.finally_data = df
        for i in range(self.max_count):
            self.count_now += 1
            if self.finally_data.iloc[i,11] != np.nan:
                self.finally_data.iloc[i,11] = self.get_comp_link_bitrank(str(df.iloc[i,4]))
        self.working = False
        self.write_excel(self.finally_data)
    
    
    def test(self):
        try:
            # df = self.read_excel()
            # print(df.iloc[6:,[4,11]])# выдает конкретно E и L колонки
            self.birank_join()
            print(self.get_comp_link_bitrank('6904008332'))
        except:
            logging.error(traceback.format_exc())
            time.sleep(1000)



    def test_pravki(self):
        pass

    def run(self):
        try: 
            while self.working:
                df = self.read_excel()
                self.birank_join()
                self.bitrank_parsing(df)
                print("Собрано ссылок:",self.finding_link)
        except:
            try:
                self.write_excel(self.finally_data)
            except:
                pass
            logging.info(traceback.format_exc())
            pass