# Я добавляю новые строки, чтобы проверить изменения в Гите
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

retail= pd.read_csv('D:/Курсы IT/[StepikUdemy] Python для начинающих/[SW.BAND] 5/[SW.BAND] 5/[SW.BAND] Задания/data.csv.zip',
                    compression='zip', encoding='ISO-8859-1')
retail_columns=retail.columns.tolist()
print(retail_columns)
unique=retail.nunique()
print(unique)
enrows_original=retail.shape[0]
retail.drop_duplicates(inplace=True)
enrows=retail.shape[0]
diff=enrows_original - enrows
print(diff)
print(retail)
cancel=retail.InvoiceNo.str.startswith('C').sum()
print('Всего отменили заказов ',cancel)
retail.query('Quantity > 0',inplace=True)
otbor=retail.shape[0]
print('Заказы с количеством >0', otbor)
german_buyers=retail.query('Country == "Germany"')\
              .groupby('CustomerID',as_index=False)\
              .agg({'InvoiceNo':pd.Series.nunique})\
            .rename(columns={'InvoiceNo':'orders_numbers'})
print(german_buyers)
percentage=german_buyers.orders_numbers.quantile(q=0.8)
german_top=german_buyers.query('orders_numbers>@percentage').CustomerID
print(german_top)
top_retail_germany=retail.query('CustomerID in @german_top')
print(top_retail_germany)
# zadacha=top_retail_germany.groupby('StockCode',as_index=False)\
#                         .agg({'InvoiceNo':'count'})\
#                         .query('StockCode !="POST"')\
#                         .sort_values('InvoiceNo',ascending=False)
zadacha=top_retail_germany.query('StockCode !="POST"').StockCode.value_counts()
print(zadacha)
retail['Revenue']=retail['Quantity'] * retail['UnitPrice']
retail.drop(columns='Revenue', inplace=True)
retail = retail.assign( Revenue = retail.UnitPrice * retail.Quantity)
print(retail)
total_revenue= retail \
    .groupby('InvoiceNo', as_index=False)\
    .agg({'Revenue':'sum'})\
    .sort_values('Revenue',ascending=False)\
    .InvoiceNo[:5]
print(total_revenue.str.cat(sep=', '))

