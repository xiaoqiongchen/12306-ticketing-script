# 12306-ticketing-script
实现思路：

1.selenium 定位登录12306;
2.登录后跳转至index.html页，自动输入行程+日期，选择"高铁/动车",点击"查询"按钮；
3.跳转至购票页https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%8C%97%E4%BA%AC%E5%8C%97,VAP&ts=%E6%AD%A6%E6%B1%89,WHN&date=2021-01-30&flag=N,Y,Y，用selenium定位到
车次列表详细信息，循环遍历车次列表信息，判断余票（本次实例仅判断了二等座余票），如果有则点击"预定"按钮；
4.跳转至乘客确认页，选择购票乘客；
5.乘客选择完弹出div浮层，选择"1D"、“1F” 座位，点击"确认"按钮后完成购票。
注：因12306购票，每天只能取消3次，所以最后一个点击"确认"按钮慎用。

代码：共2个py文件（buy_tickets_by_selenium.py、captcha.py）
buy_tickets_by_selenium.py文件为主要核心流程
captcha.py文件为验证码实现流程+滑动解锁功能
