from bs4 import BeautifulSoup
import requests
import json
from selenium.webdriver.common.keys import Keys
import openpyxl

#엑셀 넓이 및 셀 이름 추가
excel_file = openpyxl.Workbook()
excel_sheet = excel_file.active
excel_sheet.column_dimensions['B'].width = 100

num = 0
excel_sheet.append(['제품명', '가격','정보','찜수','url'])


#네이버 제이슨 파일 열기
file = open("./naver.json", "w")
#키워드 입력칸
keyword = '측정기'
#페이지 범위 지정 (시작페이지, 끝페이지)
ran = range(1,21)
#주소 입력(키워드 입력은 비우기)
url = 'https://search.shopping.naver.com/search/all.nhn?where=all&frm=NVSCTAB&query={}'.format(keyword)
url_list = []
for r in ran:
    url_list.append(url+str(r))
print(url_list)
html = requests.get(url)
soup = BeautifulSoup(html.text, 'lxml')
cnt = len(soup.findAll('div',class_='basicList_title__3P9Q7'))

result = []
#페이지 반복문
for url in url_list:
    #제품명, 가격, 정보 출력 반복문        
    for i in range(cnt):
        naver = {}
        metadata = soup.find_all('div', class_='basicList_title__3P9Q7')[i]
        title = metadata.a.get('title')
        print("<제품명> : ", title)               # title
        
        price = soup.find_all('span', class_='price_num__2WUXn')[i].text
        print("<가격> : ", price)                # 가격
        
        inf = soup.find_all('div', class_='basicList_etc_box__1Jzg6')[i].text
        print('<', inf,'>')
        
       
        url = metadata.a.get('href')
        print("<url> : ", url)                  # url
            
        print("===================================================")
        
        naver = {'제품명' : title , '가격' : price, 'url' : url,'정보':inf }
        excel_sheet.append([title, price,inf,url])
        
    file.close() 
#엑셀 셀 위치
cell_A1 = excel_sheet['A1']
cell_A1.alignment = openpyxl.styles.Alignment(horizontal="center")

cell_B1 = excel_sheet['B1']
cell_B1.alignment = openpyxl.styles.Alignment(horizontal="center")
#엑셀 이름 저장
excel_file.save('naver_shopping_crawling.xlsx')
excel_file.close()