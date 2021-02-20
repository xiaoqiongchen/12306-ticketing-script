import time
import base64
import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.support import wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Code():
    def __init__(self, browser):
        self.browser = browser
        self.verify_url = 'http://littlebigluo.qicp.net:47720/'#验证码识别网址，返回识别结果

    #获取验证码图片
    def get_captcha(self):
        element = self.browser.find_element_by_class_name('imgCode')
        #time.sleep(0.5)
        img = base64.b64decode(element.get_attribute('src')[len('data:image/jpg;base64,'):])
        with open('captcha.png', 'wb') as f:
            f.write(img)

        #验证码解析
    def parse_img(self):
        pic_name = 'captcha.png'
        # 打开保存到本地的验证码图片
        files={'pic_xxfile':(pic_name,open(pic_name,'rb'),'image/png')}
        response = requests.post(self.verify_url, files=files)
        try:
            num = response.text.split('<B>')[1].split('<')[0]
        except IndexError:  #验证码没识别出来的情况
            print('验证码未能识别！重新识别验证码...')
            return
        try:
            if int(num):
                print('验证码识别成功！图片位置：%s' % num)
                return [int(num)]
        except ValueError:
            try:
                num = list(map(int,num.split()))
                print('验证码识别成功！图片位置：%s' % num)
                return num
            except ValueError:
                print('验证码未能识别')
                return

        #识别结果num都以列表形式返回，方便后续验证码的点击
        #还有可能验证码没能识别出来
        #实现验证码自动点击
    def move(self):
        num = self.parse_img()
        if num:
            try:
                element = self.browser.find_element_by_class_name('loginImg')
                for i in num:
                    if i <= 4:
                        ActionChains(self.browser).move_to_element_with_offset(element,40+72*(i-1),73).click().perform()#鼠标移动到图片位置点击，40+72*(i-1)代表x坐标，73代表Y坐标
                        #ActionChains 处理鼠标相关的操作，行为事件存储在ActionChains对象队列，当使用perform()时，对象事件按顺序依次执行
                    else :
                        i -= 4
                        ActionChains(self.browser).move_to_element_with_offset(element,40+72*(i-1),145).click().perform()
                self.browser.find_element_by_class_name('login-btn').click()
                self.slider()
            except Exception as e:
                print(e)
                #print('元素不可选！')
        else:
            self.browser.find_element_by_class_name('lgcode-refresh').click()  #刷新验证码
            time.sleep(1.5)
            self.main()

    def ease_out_quart(self, x):
        return 1 - pow(1 - x, 4)

    #处理滑动验证码
    def slider(self):
        track = [30, 50, 90, 140]  #滑动轨迹可随意，只要距离大于300
        try:
            slider = wait.WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'nc_iconfont.btn_slide')))
            ActionChains(self.browser).click_and_hold(slider).perform()
            for i in track:
                ActionChains(self.browser).move_by_offset(xoffset=i, yoffset=0).perform()
        except:
            print('验证码识别错误！等待验证码刷新，重新识别验证码...')
            time.sleep(2.1)  #验证码刷新需要2秒
            self.main()

    def main(self):
        self.get_captcha()
        self.move()

