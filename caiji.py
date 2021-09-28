import urllib3
import re
import csv

http = urllib3.PoolManager()

f = open('./test.csv','r')

pre = 'https://www.sogou.com/sogou?ie=utf8&insite=wenwen.sogou.com&query='

with f:
    reader = csv.reader(f)
    i = 0
    for row in reader:
        for item in row:
            r = http.request('GET',pre+item)
            if r.status == 200:
                data = r.data.decode('utf-8')
                results = re.findall(r'<div class="str-text-info">(.+)</span>',data)
                if len(results) == 0:
                    temp = open('./error.html','w')
                    temp.write(data)
                    exit()
                else:
                    temp = open('data/'+str(i)+'.txt','w')
                    for result in results:
                        realdata = re.sub('</?\w+[^>]*>|<!--\w+-->|答：|最佳答案','',result)
                        temp.writelines(str(realdata)+'\r\n')
                    print('成功采集'+str(i)+'条数据')
        i += 1
