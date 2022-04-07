import pandas as pd
import numpy as np
%matplotlib inline
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

sales_team = pd.read_csv('/sales_team.csv')
order_leads = pd.read_csv('/order_leads.csv')
invoices = pd.read_csv('/invoices.csv')
# предобработка данных
order_leads['Date'] = pd.to_datetime(order_leads.Date)
order_leads = order_leads.rename(columns={'Order ID':'Order_ID',
                                          'Company ID': 'Company_ID',
                                          'Company Name':'Company_name',
                                          'Order Value':'Order_value'})
team_data = team_data.rename(columns={'Company Name':'Company_Name',
                                          'Company ID': 'Company_ID',
                                          'Sales Rep':'Sales_Rep',
                                          'Sales Rep ID':'Sales_Rep_ID'})
#проверка нужности распределения по дням
order_leads.groupby('Date')\
            .agg({'Company_ID':'count'})\
            .sort_values('Date')
#вычисляем СК
cr_by_day = order_leads.groupby('Date')\
            .agg({'Converted':'mean'})\
            .rename(columns={'Converted':'CR'})\
            .sort_values('Date')
# ставим в самое начало, чтобы сделать первичную установку
sns.set(
        font_scale=2,
        style='whitegrid',
        rc={'figure.figsize':(20,7)}
)

ax=cr_by_day.rolling(30).mean().plot()
ax.set_title('Conversion rate by day\n')
ax.set_xlabel('\nDate')
ax.set_ylabel('\nConversion Rate')

ax_set_ytickslabels=[{':0%'}.format for n in ax.yticks()]

# можно сделать скрипт функции для любого датафрейма

def get_plot(df, xlabel='', ylabel='', title=''):
    ax=df.plot()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax_set_ytickslabels = [{':0%'}.format for n in ax.yticks()]
    sns.despine()

    cr_by_day_rolling = cr_by_day.rolling.reset_index().dropna()
    fig = px.line(cr_by_day_rolling, x="Date", y="CR", title='Conversion Rate')
    fig.show()

order_leads_by_team_data = order_leads.merge(team_data, how='left', on=['Company_Name','Company_ID'])

top_sales=order_leads_by_team_data\
                                    .groupby('Sales_Rep', as_index=False)\
                                    .agg({'Converted':'mean'})\
                                    .sort_values('Converted', ascending=False)\
                                    .head(10)
ax=sns.barplot(data=top_sales, x='Sales_Rep', y='Converted')
ax.set_xticklabels(top.sales.Sales_Rep, rotation=45)
all_sales=order_leads_by_team_data\
                                    .groupby('Sales_Rep', as_index=False)\
                                    .agg({'Converted':'mean'})\
                                    .sort_values('Converted', ascending=False)
sns.distplot(x='all_sales.Converted', kde=False)