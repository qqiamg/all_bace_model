from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait  # 显性等待


option = Options()
option.add_experimental_option('excludeSwitches', ['enable-automation']) #开发者模式
# broswer = webdriver.Firefox()
broswer = webdriver.Chrome(options=option, executable_path='./chromedriver.exe')
wait = WebDriverWait(broswer, 60) #显性等待时间

#显性等待写法
wait.until(lambda the_browser: the_browser.find_element_by_xpath(
                '//*[@class="s-result-list s-search-results sg-row"]/div'))

#执行js
broswer.execute_script('js')
#切入iframe
broswer.switch_to_frame()
#切出iframe
broswer.switch_to_default_content()

#切换窗口
handles = broswer.window_handles
broswer.switch_to_window(handles[1])

#打开新窗口
broswer.execute_script('window.open("https://www.sogou.com");')