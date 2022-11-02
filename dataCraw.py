import requests
import pandas as pd
import time
import csv
import io
import json
#cookie 與 CSRF 過期必須更換
HEADERS={
    'Content-Type':"application/json",
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'Cookie':'webp=1; PHPSESSID=ves65p53u8grhhbo3cqjdbe6g1; is_new_index=1; is_new_index_redirect=1; T591_TOKEN=ves65p53u8grhhbo3cqjdbe6g1; _ga=GA1.3.822819763.1641189767; _gid=GA1.3.1607137866.1641189767; tw591__privacy_agree=0; newUI=1; _ga=GA1.4.822819763.1641189767; _gid=GA1.4.1607137866.1641189767; new_rent_list_kind_test=0; __auc=0fd26a3f17e23eef7e8274983f9; user_index_role=1; localTime=2; index_keyword_search_analysis=%7B%22role%22%3A%221%22%2C%22type%22%3A%222%22%2C%22keyword%22%3A%22%22%2C%22selectKeyword%22%3A%22%22%2C%22menu%22%3A%22%22%2C%22hasHistory%22%3A0%2C%22hasPrompt%22%3A0%2C%22history%22%3A0%7D; __utmc=82835026; __utmz=82835026.1641486460.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); userLoginHttpReferer=https%253A%252F%252Frent.591.com.tw%252F; last_search_type=8; __utma=82835026.822819763.1641189767.1641493208.1641570041.3; urlJumpIp=8; urlJumpIpByTxt=%E5%8F%B0%E4%B8%AD%E5%B8%82; user_browse_recent=a%3A5%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bi%3A11912705%3B%7Di%3A1%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bi%3A11890407%3B%7Di%3A2%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bi%3A11924064%3B%7Di%3A3%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bi%3A11086353%3B%7Di%3A4%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bi%3A9736985%3B%7D%7D; _gat=1; _dc_gtm_UA-97423186-1=1; XSRF-TOKEN=eyJpdiI6Imx6Rjg3V3lQSkpSNlZvUkdMVjd1b0E9PSIsInZhbHVlIjoiRjZiOHZhd3hBMXpDdnRiNWlTSkMrRlZ4c3ErbGhSQldQNkc5XC9CRkxxY3hLWWVXakoxcDA5OFpUS3dLeEpVQTEwS2t6Zjg4MmxxVDNhbDNPQTBva1wvdz09IiwibWFjIjoiOTJjZjVkMjYyOTAyMmYwNTQ4OGI0ZGE5MTVhMmFiZDQwNzViYmQ1NzVjNmRkNjJhNjNjMDk3ODA3OTZhOWVjNSJ9; _gat_UA-97423186-1=1; 591_new_session=eyJpdiI6ImgwM2lLVkt3MzF4MHBcL0VRZ2V6UXR3PT0iLCJ2YWx1ZSI6ImJwSitFbE80cCtrMFJ3RFRpT1JQYk9vVjY2M3hHSmVpdWRhNitXXC83VU1PakpHS1IyOHNlSzQxTXg5NUlBcVwvOFZHYW9iN1dtTWhocWVzY3V0SDB3bWc9PSIsIm1hYyI6Ijk0ZjMzOWQ4N2U2MzIzYWY3ZWVkM2E0YTI4ZGZiN2Q4M2JhNjQxOTRmYjJhYzE1NDcxYzZmNGNhNmY4MmVjOTcifQ%3D%3D',
    'X-CSRF-TOKEN': '8eFSKgoqKcKYTteCV4PsTLq7kKljdj9VWfGgZgrz'
}

url = "https://rent.591.com.tw/home/search/rsList?is_format_data=1&is_new_list=1&type=1"
# https://rent.591.com.tw/home/search/rsList?is_format_data=1&is_new_list=1&type=1&kind=2&firstRow=30 # kind=西屯區 firstRow=第二頁 
#負責做初步檢查最後回傳JSON動態資料
def get_ajax_webdata(url):
    request=requests.get(url,headers=HEADERS)
    if request.status_code!=200:
        print('Cookie過期',request.url)
    else:
        return request.json()
#取得每一頁的房屋url，每30個為一頁
def get_all_url(region,kind,section): #Ex:想要搜尋台中市(region=8)西屯區(section=104)的獨立套房(kind=2)的所有URL
    firstRow=0 #一律都從第一頁開始爬直到頁尾 
    #根據填的參數不同total_records的值也會改變
    resp=get_ajax_webdata("https://rent.591.com.tw/home/search/rsList?is_format_data=1&is_new_list=1&type=1"+"&region="+str(region)+"&kind="+str(kind)+"&section="+str(section)+"&firstRow="+str(firstRow))
    total_records=int(resp['records'].replace(',','')) #所有資料數，代表數字也就是頁尾，由於抓下來的record帶有,且還是str必須去除並轉型
    # print(total_records)
    house_url_list=[] #存放網址list
    while(firstRow < total_records): # records值等於總資料筆數
        firstRow+=30
        request_url = "https://rent.591.com.tw/home/search/rsList?is_format_data=1&is_new_list=1&type=1"+"&region="+str(region)+"&kind="+str(kind)+"&section="+str(section)+"&firstRow="+str(firstRow)
        house_url_list.append(request_url)
    # print(house_url_list)
    return house_url_list
#取得房屋資料
def get_house_detail(outputfile):
    with open(outputfile,"w",encoding="utf-8",newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["租屋標題","租屋價格","租屋地址","可養寵物或否","坪數","每坪租金"])
        all_url_list=get_all_url(region_arg,kind_arg,section_arg) #
        count=0
        # all_house_title=[]
        # all_hous1
        for url in all_url_list: #爬取經過篩選後的資料的每一頁
            resp=get_ajax_webdata(url)
            house_titles=resp['data']['data'] #所有的房屋data
            for key in house_titles:  #key=包在List裡面的一個個的dict
                # print(key)
                count+=1 #計算資料量
                house_title=key['title'] #
                house_price=key['price']
                house_size=key['area']
                house_location=key['section_name']
                rent_tags=key['rent_tag']
                try:
                    price_perSq=int(float(house_price.replace(",",'')))/int(float(house_size.replace(",",'')))
                    for key2 in rent_tags: #key2=包在rent_tag[]中的dict Ex.{'id': '16', 'name': '新上架'}
                        if('可養寵物' in key2.values()):
                            CAN_PET=1 
                        else:
                            CAN_PET=0 
                except Exception as e:
                    print(e)
                # all_house_title.append(house_title)
                # all_house_price.append(house_price)
                # all_house_location.append(house_location)
                # print(price_perSq)
                writer.writerow([house_title,house_price,house_location,CAN_PET,house_size,price_perSq])
            print("loading......")    
        # print(all_house_price)
        print("共有",count,"筆資料")
        # return all_house_title,all_house_price,all_house_location
        
if __name__ == '__main__':
    output_file_name="C:/Users/young/Desktop/591租屋資料.csv"
    region_arg=8 #設定縣市 台中市8,台北市1
    kind_arg=2  #租屋類型 整層住家1,獨立套房2,分租套房3,雅房4
    section_arg=0 #地區 西屯104,北區102,西區103,section
    get_all_url(region_arg,kind_arg,section_arg)
    # print(get_house_detail(output_file_name))
    get_house_detail(output_file_name)
   
    

