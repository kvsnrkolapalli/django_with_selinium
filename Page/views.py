from selenium.webdriver.support.ui import Select
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.by import By       
from django.http import HttpResponse 
from django.shortcuts import render           
from selenium import webdriver          
from bs4 import BeautifulSoup
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from pandas import DataFrame
from datetime import date 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browse_params=False

class SEC:
    browser, service = None, None

    # Initialise the webdriver with the path to chromedriver.exe
    def __init__(self, driver: str):
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('window-size=1920x1080')
        options.add_argument('--disable-dev-shm-usage')
        self.service = Service(driver)
        if browse_params:
            self.browser=webdriver.Chrome()
            # self.browser = webdriver.Chrome(service=self.service)
        else:
            self.browser= webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.browser.maximize_window()

    def open_page(self, url: str):
        self.browser.get(url)

    def close_browser(self):
        self.browser.close()
        
    def add_input(self, by: By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)

    def click_button(self, by: By, value: str):
        button = self.browser.find_element(by=by, value=value)
        button.click()


def UI(request):
    if request.method == 'POST':
        try:    
            BFM = date.today() + relativedelta(months=-5)
            browser=SEC('')
            main_link='https://www.sec.gov/edgar/search/'
            browser.open_page(main_link)
            self=browser
            driver=self.browser
            self.click_button(by=By.XPATH,value='/html/body/div[2]/div/form/div/div[1]/span/a')
            print(BFM)
            Date_search=str(BFM)
            self.browser.find_element(By.ID, 'keywords').clear()
            self.browser.find_element(By.ID, 'keywords').send_keys('13F')
            # time.sleep(1)
            self.browser.find_element(By.ID, 'entity-full-form').clear()
            self.browser.find_element(By.ID, 'entity-full-form').send_keys('Greenlight Capital')
            self.browser.find_element(By.ID, 'entity-full-form').send_keys(Keys.ENTER)
            # time.sleep(1)
            select = Select(self.browser.find_element(By.ID,'date-range-select'))
            # select.select_by_value('custom')
            select.select_by_visible_text('Custom')
            time.sleep(1)
            self.browser.find_element(By.ID, 'date-from').send_keys(Keys.COMMAND,'a')
            self.browser.find_element(By.ID, 'date-from').send_keys(Date_search)
            self.browser.find_element(By.ID, 'date-from').send_keys(Keys.ENTER)
            self.click_button(by=By.ID,value='search')
            time.sleep(2)
            # Get the HTML source
            html_source = self.browser.page_source

            # Save the HTML source to a file
            with open("page_source1.html", "w", encoding="utf-8") as file:
                file.write(html_source)
            self.browser.get_screenshot_as_file("screenshot2.png")
            if len(driver.find_elements(By.CLASS_NAME, 'preview-file')) > 0:
                IFF = []
                IRF = []
                IFEP = []
                for (ff, rf, en) in zip(driver.find_elements(By.CLASS_NAME, 'preview-file'), driver.find_elements(By.CLASS_NAME, 'enddate')[1:], driver.find_elements(By.CLASS_NAME, 'entity-name')[1:]):
                    if '13F-HR ' in ff.text:
                        IFF.append(ff.text)
                        IRF.append(rf.text)
                        IFEP.append(en.text)     
                if len(IFF) > 0:
                    FF = []
                    RF = []
                    FEP = [] 
                    for (i, j) in zip(IFEP, range(len(IFEP))):
                        if IFEP.count(i) > 1:
                            if FEP.count(i) == 0:
                                FF.append(IFF[j])
                                FEP.append(IFEP[j])
                                DL = []
                                for k in range(len(IRF)):
                                    if IFEP[k] == i and IFEP[k] != '':
                                        DL.append(datetime(int(str(IRF[k]).split('-')[0]), int(str(IRF[k]).split('-')[1]), int(str(IRF[k]).split('-')[2])))
                                RF.append(str(max(DL)).split(' ')[0])         
                        else:
                            FF.append(IFF[j])
                            RF.append(IRF[j])
                            FEP.append(IFEP[j]) 
                    time.sleep(1)    
                    df = DataFrame({'Col1': FF, 'Col2': RF, 'Col3': FEP})
                    response = HttpResponse(content_type='application/xlsx')
                    response['Content-Disposition'] = f'attachment; filename='+str('Greenlight Capital').replace(' ','_')+'.xlsx'
                    with pd.ExcelWriter(response) as writer:
                        df.to_excel(writer, sheet_name=str('Greenlight Capital').replace(' ','_'))
                    return response
                else:
                    return render(request, "index.html", {'message': 'No results for this company!'})
            else:
                return render(request, "index.html", {'message': 'No results for this company!'})        
        except Exception as e:
            print(e)
            return render(request, "index.html", {'message': 'Something bad happened!'})
    else:    
        return render(request, "index.html")
