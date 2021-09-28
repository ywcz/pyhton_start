import csv
import urllib3
import re
import time

http = urllib3.PoolManager()
count = 0
errcount = 0

pre = 'https://www.sogou.com/sogou?ie=utf8&insite=wenwen.sogou.com&query='

def parseCsv(path,pre=''):
    temp = open(path,'r')
    with temp:
        reader = csv.reader(temp)
        for row in reader:
            for item in row:
                yield pre + item

def dataFilter(data):
    return re.sub('</?\w+[^>]*>|<!--\w+-->|答：|最佳答案','',data)

def getData(url, hp):
    r = hp.request('GET',url)
    if r.status == 200:
        data = r.data.decode('utf-8')
        results = re.findall(r'<div class="str-text-info">(.+)</span>',data)
        return map(dataFilter,results)

def writeData(data):
    f = open('data/'+str(count)+'.txt','w')
    for temp in data:
        f.writelines(str(temp)+'\r\n')
    print('成功采集'+str(count)+'条数据')


for keyword in parseCsv('./test.csv',pre):
    # print(list(getData(keyword,http)))
    while True:
        data = list(getData(keyword,http))
        if data:
            writeData(data)
            count+=1
            break
        else:
            getData(keyword,http)
            print('未读取到数据，重复提交')
            time.sleep(1)

