from urllib import request
import json
import time
from datetime import datetime
from datetime import timedelta
import json
import os
#请求数据连接
def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }
    req = request.Request(url, headers=headers)
    response = request.urlopen(req)
    if response.getcode() == 200:
        return response.read()
    return None



#获取当前系统桌面绝对路径
def path_d():
    return os.path.join(os.path.expanduser("~"), 'Desktop')

#获取相关的JSON 数据
def parse_data(html):
    data = json.loads(html)['cmts']  # 将str转换为json
    comments = []
    for item in data:
        comment = {
            'id': item['id'],
            'nickName': item['nickName'],
            'cityName': item['cityName'] if 'cityName' in item else '',  # 处理cityName不存在的情况
            'content': item['content'].replace('\n', ' ', 10),  # 处理评论内容换行的情况
            'score': item['score'],
            'startTime': item['startTime']
        }
        comments.append(comment)
    return comments


#存储数据
def save_to_txt():
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间，从当前时间向前获取
    end_time = '2019-01-01 00:00:00'
    while start_time > end_time:
        url = 'http://m.maoyan.com/mmdb/comments/movie/1203084.json?_v_=yes&offset=0&startTime=' + start_time.replace(' ', '%20')
              #'http://m.maoyan.com/mmdb/comments/movie/1200486.json?_v_=yes&offset=0&startTime=2018-07-28%2022%3A25%3A03'
        html = None
        '''
            问题：当请求过于频繁时，服务器会拒绝连接，实际上是服务器的反爬虫策略
            解决：1.在每个请求间增加延时0.1秒，尽量减少请求被拒绝
                 2.如果被拒绝，则0.5秒后重试
        '''
        try:
            html = get_data(url)
        except Exception as e:
            time.sleep(0.5)
            html = get_data(url)
        else:
            time.sleep(0.1)

        comments = parse_data(html)
       # print(comments)
        start_time = comments[14]['startTime']  # 获得末尾评论的时间
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=-1)  # 转换为datetime类型，减1秒，避免获取到重复数据
        start_time = datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')  # 转换为str
        print(path_d())
        #
        for item in comments:
            with open(path_d()+'/comments.txt', 'a', encoding='utf-8') as f:
                f.write('账号ID:'+str(item['id'])+'   账号名称:'+item['nickName'] + '  城市:' + item['cityName'] + '   评论内容:' + item['content'] + '   评论星数:' + str(item['score'])+ '   评论时间:' + item['startTime'] + '\n')






#数据图形数据表开源 https://pyecharts.org/#/zh-cn/intro

if __name__ == '__main__':
    #html = get_data('http://m.maoyan.com/mmdb/comments/movie/1200486.json?_v_=yes&offset=0&startTime=2018-07-28%2022%3A25%3A03')
    #comments = parse_data(html)
    #print(comments)
    # path =  path_d()
    # f = open (path+'/films1.txt','wb')
    #f.write(comments,"wb")
    #f.closed
    save_to_txt()


