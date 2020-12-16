from bs4 import BeautifulSoup
import requests
import json
from selenium.webdriver.common.keys import Keys
import openpyxl

excel_file = openpyxl.Workbook()
excel_sheet = excel_file.active
excel_sheet.column_dimensions['B'].width = 100

num = 0
excel_sheet.append(['제품명', '가격','inf','찜수','url'])

file = open("./naver.json", "w")
keyword = '측정기'
url = 'https://search.shopping.naver.com/search/all.nhn?where=all&frm=NVSCTAB&query={}'.format(keyword)
html = requests.get(url)
soup = BeautifulSoup(html.text, 'lxml')
cnt = len(soup.findAll('div',class_='basicList_title__3P9Q7'))

''' dd '''
for i in range(cnt):
    naver = {}
    metadata = soup.find_all('div', class_='basicList_title__3P9Q7')[i]
    title = metadata.a.get('title')
    print("<제품명> : ", title)               # title
    
    price = soup.find_all('span', class_='price_num__2WUXn')[i].text
    print("<가격> : ", price)                # 가격
    
    inf = soup.find_all('div', class_='basicList_etc_box__1Jzg6')[i].text
    print('<', inf,'>')
    
    zzim = soup.find_all('em', class_='basicList_num__1yXM9')[i].text
    print("찜수:"+zzim)

    url = metadata.a.get('href')
    print("<url> : ", url)                  # url
         
    print("===================================================")
    
    naver = {'제품명' : title , '가격' : price, 'url' : url,'inf':inf ,'zzim':zzim}
    excel_sheet.append([title, price,inf,zzim,url])
    file.write(json.dumps(naver))
file.close() 

cell_A1 = excel_sheet['A1']
cell_A1.alignment = openpyxl.styles.Alignment(horizontal="center")

cell_B1 = excel_sheet['B1']
cell_B1.alignment = openpyxl.styles.Alignment(horizontal="center")

excel_file.save('02.xlsx')
excel_file.close()