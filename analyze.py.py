#資料要先預處理
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#匯入爬出來的csv檔
#CSV檔案是使用big5編碼，所以範例中需使用encoding關鍵字參數來進行指定，否則會出現亂碼。
df = pd.read_csv('591租屋資料.csv',encoding=('big5'))

#計算每一區的平均值
Price= df.groupby('租屋地址').agg('mean')
print(Price)


#解決中文亂碼
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
#解決負號不能顯示
plt.rcParams['axes.unicode_minus']=False


#畫圖表，設定長條圖顏色+寬度，分三張   
Price.plot.bar(
    secondary_y=("坪數","可養寵物或否",'每坪租金'),
    width=0.5,
    figsize=(28,20),
    subplots =  True,
    )

plt.xticks(rotation=90)
plt.show()

#把結果寫到excel裡
writer = pd.ExcelWriter('591租屋資料_分析.xlsx')
Pricebook = writer.book
Price.to_excel(writer,sheet_name='591租屋資料_分析')
worksheet = writer.sheets['591租屋資料_分析']

#繪製圖表
chart = Pricebook.add_chart({'type':'column'})
for i,v in enumerate(Price.columns):
    col = chr(ord('b')+i)
    chart.add_series({
        'name':f'{v}',
        'categories':'591租屋資料_分析!a2:a26',#欄位的總欄
        'values':f'=591租屋資料_分析!{col}2:{col}26'
        })
worksheet.insert_chart('F2',chart)#輸出圖表的位置
writer.save()