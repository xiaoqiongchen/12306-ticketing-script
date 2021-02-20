from selenium import webdriver
from captcha import Code
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class buy_ticket:

    def __init__(self,driver,login_url,user_name,password,fromStation,toStationText,train_date,passenger_list):

        self.driver=driver#webdriver驱动
        self.login_url=login_url#登录URL
        self.user_name=user_name#登录账号
        self.password=password#登录密码
        self.fromStation=fromStation#出发地
        self.toStationText=toStationText#目的地
        self.train_date=train_date#出发日期
        self.passenger_list=passenger_list#乘客列表


    def login(self):#登录

        self.driver.get(login_url)#获取登录网页源码
        time.sleep(0.5)#登录首页有2个div进行切换，一个是二维码登录div，一个是账号登录div。默认显示二维码登录div，隐藏账号登录div.
                       #如果不在此等0.5s可能导致二维码登录div正在加载状态时，点击了账号登录div，此时账号登录div与二维码登录div会同时重叠展现
        self.driver.find_element_by_xpath("//div[@class='login-box']/ul/li[2]/a").click()#通过xpath定位登录页"账号登录"元素
        self.driver.find_element_by_id("J-userName").send_keys(self.user_name)#通过id定位"用户名"元素
        self.driver.find_element_by_id("J-password").send_keys(self.password)#通过id定位"密码"元素

        c=Code(self.driver)#实例化验证码类
        c.main()#调用验证码main方法
        driver.implicitly_wait(3)#隐式等待3s
        self.driver.find_element_by_xpath("//div[@class='dzp-confirm']/div[2]/div[3]/a").click()#通过xpath定位获取div浮层进行点击(处理登录成功后弹出的div浮层，浮层内容为"根据有关部门要求...")
        self.driver.find_element_by_xpath("//li[@id='J-index']/a").click()#通过xpath定位获取导航栏"首页"标签元素进行点击

        self.ticket_index()#调用购票首页方法


    def ticket_index(self):#跳转到购票首页
        #输入起始地
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'fromStationText'))
        )#显式等待"出发地"元素是否已被加载出来

        self.driver.find_element_by_id("fromStationText").click()#如果"出发地"元素被加载出来则进行点击
        self.driver.find_element_by_id("fromStationText").send_keys(self.fromStation)#点击完成后往"出发地"输入框输入出发地
        self.driver.find_element_by_id("fromStationText").send_keys(Keys.ENTER)#模拟键盘操作回车键

        #输入目的地（目的地操作与出发地一致，不赘述）
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'toStationText'))
        )

        self.driver.find_element_by_id("toStationText").click()
        self.driver.find_element_by_id("toStationText").send_keys(self.toStationText)
        self.driver.find_element_by_id("toStationText").send_keys(Keys.ENTER)

        # 输入日期
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'train_date'))
        )#显式等待"出发日期"元素是否已被加载出来

        js="document.getElementById('train_date').removeAttribute('readonly')"#因12306日期属性为只读，所以需执行js操作将日期的只读属性去掉便于下面输入日期
        self.driver.execute_script(js)
        self.driver.find_element_by_id("train_date").clear()#清空默认日期值
        self.driver.find_element_by_id("train_date").send_keys(self.train_date)#往"出发日期"输入框输入日期
        time.sleep(0.5)

        js1="document.querySelector('body > div.cal-wrap').style.display='none'"
        self.driver.execute_script(js1)#用js操作将日期日历控件隐藏

        #点击高铁/动车
        WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.ID,'isHighDan'))
        )#显示等待"高铁/动车"复选框元素
        self.driver.find_element_by_id('isHighDan').click()#点击"高铁/动车"复选框元素
        #点击"查询"按钮

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'search_one'))
        )#显示等待"查询"按钮元素
        self.driver.find_element_by_id("search_one").click()#点击"查询"按钮元素

        self.check_tickets()#调用购票方法


    def check_tickets(self):#跳转至购票页检查二等座是否有票，有票开始购买
        all_handles=self.driver.window_handles#页面跳转后，会有新页面，获取所有页面
        self.driver.switch_to.window(all_handles[-1])#用索引切换到最后一个页面，则为你所要操作的页面
        trs=self.driver.find_elements_by_xpath("//div[@id='t-list']/table/tbody[1]/tr")#xpath定位车次信息列表

        for tr in trs:#循环遍历车次信息
            left_ticket = tr.find_element_by_xpath('//td[4]').text#xpath定位二等座文本
            if left_ticket == '有' or left_ticket.isdigit:#判断二等座文本为"有"或者"数字"则代表有座
                orderBtn = tr.find_element_by_class_name('btn72')#用class定位"预定"按钮元素
                orderBtn.click()#点击"预定"按钮
                driver.implicitly_wait(2)#隐式等待2s
                self.confirm_Passenger()#调用乘客确认方法
                break#只要有一个符合条件则结束循环，如果不符合则继续循环


    def confirm_Passenger(self):#乘客确认页，选择要购票乘客
        all_handles = self.driver.window_handles
        self.driver.switch_to.window(all_handles[-1])#切换页面，与购票页意思一样，不赘述
        driver.implicitly_wait(3)#隐式等待3s
        li_list=self.driver.find_elements_by_xpath("//ul[@id='normal_passenger_id']/li")#xpath定位乘车人信息列表

        for li in li_list:#外层循环遍历乘车人信息列表
            passenger=li.find_element_by_xpath('./label').text#xpath找到乘车人信息文本
            for pger in self.passenger_list:#内层循环遍历你想要购票的乘车人
                if passenger==pger:#如果两者信息一致
                    li.find_element_by_xpath("./label").click()#点击所购票乘车人

        self.driver.find_element_by_id("submitOrder_id").click()#通过id定位"提交订单"按钮

        driver.implicitly_wait(1)#隐式等待1s

        self.driver.find_element_by_xpath("//div[@id='erdeng1']/ul[2]/li[1]/a").click()#通过xpath定位二等座D座位
        self.driver.find_element_by_xpath("//div[@id='erdeng1']/ul[2]/li[2]/a").click()#通过xpath定位二等座F座位
        # 点击"确认"按钮

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'qr_submit_id'))
        )#显示等待"确认"按钮
        #self.driver.find_element_by_id("qr_submit_id").click()#一天内购票取消3次，当日不能购票，避免此种情况出现注释此行代码

if __name__=="__main__":
    options = webdriver.ChromeOptions()  # 设置浏览器属性
    options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69"'
            )  # 添加UA属性
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 设置开发者模式启动，该模式下webdriver属性为正常值
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()#窗口最大化
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                          get: () => undefined
                        })
                      """
        })  # 增加反爬机制，防止被12306封

    login_url="https://kyfw.12306.cn/otn/resources/login.html"#12306登录页URL
    bt=buy_ticket(driver,login_url,"username","password","北京","武汉","2021-01-30",["passenger1","passenger2"])#实例化购票类
    bt.login()#调登录方法