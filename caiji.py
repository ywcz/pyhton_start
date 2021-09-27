import urllib3
import re

http = urllib3.PoolManager()

r = http.request('GET','https://www.sogou.com/sogou?ie=utf8&insite=wenwen.sogou.com&query=短信营销');

if r.status == 200:
    # print(r.data.decode('utf-8'))
    data = r.data.decode('utf-8')
    result = re.findall(r'<div class="str-text-info">(.+)</span>',data)
    # print(result)
    for i in result:
        print(re.sub('</?\w+[^>]*>|<!--\w+-->','',i))
