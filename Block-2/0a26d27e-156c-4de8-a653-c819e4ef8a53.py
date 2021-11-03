#!/usr/bin/env python
# coding: utf-8

# <div style="border:solid green 2px; padding: 20px">
# <b>Елизавета, привет!</b>
# 
# Меня зовут Евгений Дащенко, и я буду проверять твой проект. Предлагаю общаться на «ты» 😊 Но если это не удобно - дай знать, и мы перейдем на "вы". 
# 
# Моя основная цель — не указать на совершенные тобою ошибки, а поделиться своим опытом и помочь тебе стать аналитиком данных. Ты уже проделал большую работу над проектом, но давай сделаем его еще лучше. Ниже ты найдешь мои комментарии - пожалуйста, не перемещай, не изменяй и не удаляй их. Я буду использовать цветовую разметку:
# 
# <div class="alert alert-danger">
# <b>Комментарий ревьюера:</b> Так выделены самые важные замечания. Без их отработки проект не будет принят. </div>
# 
# <div class="alert alert-warning">
# <b>Комментарий ревьюера:</b> Так выделены небольшие замечания. Одна-два таких замечания в проекте допустимы, но если их будет больше - тебе будет необходимо внести исправления. Это как тестовое задание при приеме на работу: очень много мелких ошибок могут стать причиной отказа кандидату. 
# 
# </div>
# 
# <div class="alert alert-success">
# <b>Комментарий ревьюера:</b> Так я выделяю все остальные комментарии.</div>
# 
# Давай работать над проектом в диалоге: если ты что-то меняешь в проекте или отвечаешь на мои комменатри — пиши об этом. Мне будет легче отследить изменения, если ты выделишь свои комментарии:
# <div class="alert alert-info"> <b>Комментарий студента:</b> Например, вот так.</div>
# 
# Всё это поможет выполнить повторную проверку твоего проекта оперативнее. 

# #  Определение перспективного тарифа для телеком-компании

# Клиентам предлагают два тарифных плана: «Смарт» и «Ультра». Чтобы скорректировать рекламный бюджет, коммерческий департамент хочет понять, какой тариф приносит больше денег.
# 
# Предстоит сделать предварительный анализ тарифов на небольшой выборке клиентов. В распоряжении данные 500 пользователей «Мегалайна»: кто они, откуда, каким тарифом пользуются, сколько звонков и сообщений каждый отправил за 2018 год. Нужно проанализировать поведение клиентов и сделать вывод — какой тариф лучше. 

# <div class="alert alert-success">
# <b>Комментарий ревьюера:</b>
# 
# Здорово, когда есть вступление в сам проект, каждый сможет быстрее разобраться в концепции / деталях работы. 
# 
# </div>

# ## Изучение данных из файла

# In[1]:


import pandas as pd 
import matplotlib.pyplot as plt
from IPython.display import display
import numpy as np
import warnings 
from scipy import stats as st
warnings.filterwarnings('ignore')

def read(data):  #<функция вывода таблиц>
    display(data.head(10))
    print('Содержание пропусков:')
    print(data.isnull().sum())
    print('')
    print('Количество дубликатов: ', data.duplicated().sum())
    print('')
    print(data.info())
    
df_calls = pd.read_csv('/datasets/calls.csv')
df_internet = pd.read_csv('/datasets/internet.csv')
df_messages = pd.read_csv('/datasets/messages.csv')
df_tariffs = pd.read_csv('/datasets/tariffs.csv')
df_users = pd.read_csv('/datasets/users.csv')

datas = [df_calls, 
         df_internet, 
         df_messages, 
         df_tariffs, 
         df_users]

datas_name = ['информация о звонках', 
              'информация об интернет-сессиях',
              'информация о сообщениях',
              'информация о тарифах',
              'информация о пользователях']

for i,j in zip(datas, datas_name) : 
    print(j)
    read(i)
    print('')


# <div class="alert alert-success">
# <b>Комментарий ревьюера:</b>
# 
# Отличная функция для первичной оценки наших данных 👍
# </div>

# Рассмотрим полученную информацию более подробно:
# 
# У нас 5 таблиц с разными данными, а именно:
# * users
# * calls
# * messages
# * internet
# * tariffs
# 
# Обратим внимание на каждую таблицу отдельно, рассмотрим какие столбцы и типы данных она содержит внутри себя: 
# - Таблица users (информация о пользователях):
#  * user_id — уникальный идентификатор пользователя
#  * first_name — имя пользователя
#  * last_name — фамилия пользователя
#  * age — возраст пользователя (годы)
#  * reg_date — дата подключения тарифа (день, месяц, год)
#  * churn_date — дата прекращения пользования тарифом (если значение пропущено, то тариф ещё действовал на момент выгрузки данных)
#  * city — город проживания пользователя
#  * tarif — название тарифного плана
# 8 столбцов, в которых встречаются данные типа int64(2), object(6)
# 
# 
# - Таблица calls (информация о звонках):
#  * id — уникальный номер звонка
#  * call_date — дата звонка
#  * duration — длительность звонка в минутах
#  * user_id — идентификатор пользователя, сделавшего звонок
# 4 столбца, в которых встречаются данные типа float64(1), int64(1), object(2)
# 
# 
# - Таблица messages (информация о сообщениях):
#  * id — уникальный номер сообщения
#  * message_date — дата сообщения
#  * user_id — идентификатор пользователя, отправившего сообщение
# 3 столбца, в которых встречаются данные типа int64(1), object(2)
# 
# 
# - Таблица internet (информация об интернет-сессиях):
#  * Unnamed: 0 - ?
#  * id — уникальный номер сессии
#  * mb_used — объём потраченного за сессию интернет-трафика (в мегабайтах)
#  * session_date — дата интернет-сессии
#  * user_id — идентификатор пользователя
# 5 столбцов, в которых встречаются данные типа float64(1), int64(2), object(2); Однако в задании было указано 4 столбца, выявлен столбец *Unnamed: 0* неизвестного содержания, обработаем его в следующем шаге. 
# 
# 
# - Таблица tariffs (информация о тарифах):
#  * tariff_name — название тарифа
#  * rub_monthly_fee — ежемесячная абонентская плата в рублях
#  * minutes_included — количество минут разговора в месяц, включённых в абонентскую плату
#  * messages_included — количество сообщений в месяц, включённых в абонентскую плату
#  * mb_per_month_included — объём интернет-трафика, включённого в абонентскую плату (в мегабайтах)
#  * rub_per_minute — стоимость минуты разговора сверх тарифного пакета (например, если в тарифе 100 минут разговора в месяц, то со 101 минуты будет взиматься плата)
#  * rub_per_message — стоимость отправки сообщения сверх тарифного пакета
#  * rub_per_gb — стоимость дополнительного гигабайта интернет-трафика сверх тарифного пакета (1 гигабайт = 1024 мегабайта)
# 8 столбцов, в которых встречаются данные типа int64(7), object(1)
# 
# 
# **Вывод:**
# 
# В данных не содежится дубликатов и пропусков, кроме столбца *churn_date*, но эти пропуски обусловлены тем, что тариф ещё действовал на момент выгрузки таблиц. Однако встречаются неправильные типы, которые будут заменены в следующем шаге. Более того надо будет также проверить данные на наличие ошибок. 

# <div class="alert alert-success">
# <b>Комментарий ревьюера:</b>
# 
# Достаточно детально изучили наши первичные данные, давай теперь их обработаем. 
#     
# 
#     
# </div>

# ## Подготовка данных
# 
# ### Предобработка

# Так как таблиц довольно много будем обрабатывать их отдельно. 
# 
# Начнем с таблицы *users*: в двух столбцах *churn_date* и *reg_date* значения передаются в качестве строковых данных, для успешного анализа переведем значения в формат даты 

# In[2]:


columns_users_time = ['churn_date', 'reg_date']

for i in columns_users_time:
    df_users[i] = pd.to_datetime(df_users[i], format='%Y-%m-%d')


# Проверим данные таблицы на наличие ошибок: выведем методом *unique()* содержимое столбцов *age*, *city* и *tariff*

# In[3]:


columns_users_check = ['age', 'city', 'tariff']

for i in columns_users_check:
    print(df_users[i].unique())
    print('******************')


# Ошибок в данных не наблюдается.
# 
# Перейдем к таблице *calls*: так как все звонки, сколько бы секунд они не длились, округляются в большую сторону, проведем эту операцию и заменим тип на целочисленный. А так же переведем в формат даты значение столбца *call_date*

# In[4]:


df_calls['duration'] = np.ceil(df_calls['duration'])
df_calls['duration'] = df_calls['duration'].astype('int')

df_calls['call_date'] = pd.to_datetime(df_calls['call_date'], format='%Y-%m-%d')


# <div class="alert alert-success">
# <b>Комментарий ревьюера:</b>
# 
# Хорошо, что учитываем условия работы оператора связи и применяем метод `np.ceil`
#     
#     
# </div>

# <div class="alert alert-warning">
# <b>Комментарий ревьюера:</b>
# 
# <s>Однако метод `np.ceil` лучше применять ко всему столбцу целиком, так вычисления будут работать быстрее.  
#     
# `np.ceil(df['column'])`
#     
# </div>

# Проверим данные таблицы на наличие ошибок: посмотрим методами *min()* и *max()* проверим содержимое столбца *duration* на наличие выбросов:

# In[5]:


print(df_calls['duration'].min())
print(df_calls['duration'].max())


# Заметных выбросов не наблюдается.  
# 
# Перейдем к таблице *messages*: приведем только столбец *message_date* в формат даты:

# In[6]:


df_messages['message_date'] = pd.to_datetime(df_messages['message_date'], format='%Y-%m-%d')


# В таблице *internet* столбец *mb_used* вычисляется в мегабайтах, так как стоимость снимается за целое число гигабайт, переведем значения в гигабайты, но пока округлять не будем, потому что для каждого пользователя передана информация не о сумме использования гигабайт, а о каждой сессии отдельно, так же обработаем столбец *session_date* в формат даты.

# In[7]:


df_internet['mb_used'] = df_internet['mb_used'] / 1000

df_internet['session_date'] = pd.to_datetime(df_internet['session_date'], format='%Y-%m-%d')


# Однако в таблице встречается столбец, которого нет в описании данных, и у него непонятное название. Определим его методом *columns()* и проверим его содержимое методом *unique()*:

# In[8]:


print(df_internet.columns)
print(df_internet['Unnamed: 0'].unique())


# Предположительно столбец дублирует индексы, тогда можно протсо избавиться от него. 

# In[9]:


df_internet.drop('Unnamed: 0', axis=1, inplace=True)


# Перейдем к таблице *tariffs*: в ней указаны неправильные значения в столбце *mb_per_month_included*, ведь у тарифа «Смарт» должно быть ровно 15 Гб, а у «Ультра» - 30 Гб, исправим это. 

# In[10]:


df_tariffs['mb_per_month_included'][0] = 15000
df_tariffs['mb_per_month_included'][1] = 30000


# Проверим данные после обработки:

# In[11]:


for i,j in zip(datas, datas_name) : 
    print(j)
    print(i.info())
    print('')


# **Вывод**:
# 
# Большинство из представленных данных были неправильного типа, какие то таблицы имели ошибки: неверные значения, лишние столбцы, однако по итогу предобработки данные готовы к анализу. 

# ### Расчеты затрат для каждого пользователя

# #### Расчет количества совершенных звонков, смс и интернет сессий
# 
# Посчитаем количество сделанных звонков и израсходованных минут разговора по месяцам для каждого пользователя:

# In[12]:


month =[]
for i in range(1,13):
    month.append(i)

df_month_calls_num = pd.DataFrame(index=df_users['user_id'].unique(), columns = month)
df_month_minutes_num = pd.DataFrame(index=df_users['user_id'].unique(), columns = month)

for i in df_users['user_id'].unique() :
    df_tmp = df_calls[df_calls['user_id'] == i]
    for j in month:
        df_tmp2 = df_tmp[df_tmp['call_date'].dt.month == j]
        df_month_calls_num[j][i] = df_tmp2.shape[0]
        df_month_minutes_num[j][i] = df_tmp2['duration'].sum()
        df_tmp2 = 0
    df_tmp = 0

display(df_month_calls_num.head(10)) 
display(df_month_minutes_num.head(10))


# Для того, чтоб справиться с поставленной задачей, будем использовать 2 цикла, где первый будет создавать таблицу по каждому пользователю, а второй генерирует таблицы по ежемесячному использованию сотовой сввязи. Таким образом мы будем получать ежемесячные временные таблицы, состояющие из данных по каждому пользователю, размер которых есть число вызовов, а количество потраченных минут на разговоры - сумма столбца *duration*.
# 
# Посчитаем количество отправленных сообщений и объем израсходованного интернет-трафика по месяцам по тому же принципу, что и считали ранее:

# In[13]:


df_month_messages_num = pd.DataFrame(index=df_users['user_id'].unique(), columns = month)
df_month_internet_num = pd.DataFrame(index=df_users['user_id'].unique(), columns = month)

for i in df_users['user_id'].unique() :
    df_tmp = df_messages[df_messages['user_id'] == i]
    for j in month:
        df_tmp2 = df_tmp[df_tmp['message_date'].dt.month == j]
        df_month_messages_num[j][i] = df_tmp2.shape[0]
        df_tmp2 = 0
    df_tmp = 0
    
for i in df_users['user_id'].unique() :
    df_tmp = df_internet[df_internet['user_id'] == i]
    for j in month:
        df_tmp2 = df_tmp[df_tmp['session_date'].dt.month == j]
        df_month_internet_num[j][i] = df_tmp2['mb_used'].sum()
        df_tmp2 = 0
    df_tmp = 0

display(df_month_messages_num.head(10)) 
display(df_month_internet_num.head(10)) 


# Прежде чем вычислять помесячную прибыль приведем таблицы в подобающий вид:

# In[14]:


options = [df_month_calls_num, 
           df_month_minutes_num, 
           df_month_messages_num,
           df_month_internet_num]

col = ['январь', 'февраль', 'март', 
       'апрель', 'май', 'июнь', 
       'июль', 'август', 'сентябрь', 
       'октябрь', 'ноябрь', 'декабрь']

for i,j in zip(options, col):
    i.rename(columns={1: 'январь', 
                      2: 'февраль', 
                      3: 'март', 
                      4: 'апрель', 
                      5: 'май', 
                      6: 'июнь', 
                      7: 'июль', 
                      8: 'август', 
                      9: 'сентябрь', 
                      10: 'октябрь', 
                      11: 'ноябрь', 
                      12: 'декабрь'}, inplace=True)
    
    i[j] = i[j].astype('int')


# <div class="alert alert-warning">
# <b>Комментарий ревьюера:</b>
# 
# Я бы рекомендовал не использовать атрибут `inplace`, так как в последующих обновлениях библотеки `pandas` он будет удален.
#     
# Лучше всего переопределять переменные. 
#     
# </div>

# <div class="alert alert-info"> <b>Комментарий студента:</b> Помогите, пожалуйста это сделать, потому что, есля я пишу i = i.rename...., то выдает ошибку</div>

# <div class="alert alert-success">
# <b>Комментарий ревьюера (2):</b>
# 
# На самом деле решение такого характера для нас подходит, но лучше иметь в виду на будущее по поводу `inplace`
#     
#     
# </div>

# <div class="alert alert-success">
# <b>Комментарий ревьюера:</b>
# 
# Кстати для расчетов лучше использовать линейную структуру данных, это когда в строках у нас хранятся данные в следующем формате: 
# 
# пользователь - месяц - израсходованные услуги
#     
# Таким образом мы сможем сделать наш расчет проще и быстрее.
#     
#     
# </div>

# Отдельно проработаем каждую таблицу на изменение индекса и введения нового столбца *user_id*:

# In[15]:


df_month_calls_num = df_month_calls_num.reset_index()
df_month_minutes_num = df_month_minutes_num.reset_index()
df_month_messages_num = df_month_messages_num.reset_index()
df_month_internet_num = df_month_internet_num.reset_index()

df_month_calls_num.rename(columns={'index': 'user_id'}, inplace=True)
df_month_minutes_num.rename(columns={'index': 'user_id'}, inplace=True)
df_month_messages_num.rename(columns={'index': 'user_id'}, inplace=True)
df_month_internet_num.rename(columns={'index': 'user_id'}, inplace=True)


# Соединим таблицы с расходами и информацией о пользователях, чтоб получить доступ к тарифам, и удалим из полученной таблицы ненужные столбцы. 

# In[16]:


df_calls_new = df_users.merge(df_month_minutes_num, on='user_id')
df_messages_new = df_users.merge(df_month_messages_num, on='user_id')
df_internet_new = df_users.merge(df_month_internet_num, on='user_id')

drop_columns = ['age', 'churn_date',
                'first_name', 
                'last_name', 'reg_date']

for i in drop_columns:
    df_calls_new = df_calls_new.drop(i, 1)
    df_messages_new = df_messages_new.drop(i, 1)
    df_internet_new = df_internet_new.drop(i, 1)


# В новых таблицах найдем перерасход по параметрам, где 1 - использованный тариф *smart* не был привышен, 2 - использованный тариф *ultra* не был привышен и пользователь заплатил просто абонентскую плату, 0 - не использовал тариф, больше 3 - сумма, которая потрачена на оплату дополнительных параметров сверх тарифа.

# In[17]:


def tariff_price(df, colum, smart_lim, ultra_lim, smart_price, ultra_price):
    for i in colum:
        for j in range(0, 500):
            if df['tariff'][j] == 'smart':
                if df[i][j] > smart_lim:
                    df[i][j] = (df[i][j] - smart_lim) * smart_price
                else: 
                    if (df[i][j] <= smart_lim and df[i][j] != 0):
                        df[i][j] = 1
                    if  df[i][j] == 0 :
                        df[i][j] = 0
            if df['tariff'][j] == 'ultra':
                if df[i][j] > ultra_lim:
                    df[i][j] = (df[i][j] - ultra_lim) * ultra_price
                else: 
                    if (df[i][j] <= ultra_lim and df[i][j] != 0):
                        df[i][j] = 2
                    if  df[i][j] == 0 :
                        df[i][j] = 0
    return df

df_calls_new = tariff_price(df_calls_new, 
                            col, 
                            df_tariffs['minutes_included'][0], 
                            df_tariffs['minutes_included'][1], 
                            df_tariffs['rub_per_minute'][0], 
                            df_tariffs['rub_per_minute'][1])

df_messages_new = tariff_price(df_messages_new, 
                               col, 
                               df_tariffs['messages_included'][0], 
                               df_tariffs['messages_included'][1], 
                               df_tariffs['rub_per_message'][0], 
                               df_tariffs['rub_per_message'][1])

df_internet_new = tariff_price(df_internet_new, 
                               col, 
                               df_tariffs['mb_per_month_included'][0], 
                               df_tariffs['mb_per_month_included'][1], 
                               df_tariffs['rub_per_gb'][0], 
                               df_tariffs['rub_per_gb'][1])

display(df_calls_new.head(10))
display(df_messages_new.head(10))
display(df_internet_new.head(10))


# #### Содание общей таблицы расходов по каждому пользователю
# 
# Создадим таблицу, содержащую полностью все траты на различные параметры в течение года:

# In[18]:


all_costs = pd.DataFrame(columns = col)
all_costs = df_users.join(all_costs)

drop_columns = ['age', 'churn_date', 
                'first_name', 
                'last_name', 'reg_date']

for i in drop_columns:
    all_costs = all_costs.drop(i, 1)
    
ultra_cost = df_tariffs['rub_monthly_fee'][1]
smart_cost = df_tariffs['rub_monthly_fee'][0]

for i in col:
    for j in range(0,500) :
        if (df_calls_new[i][j] == 0 and df_messages_new[i][j] == 0 and df_internet_new[i][j] ==0):
            all_costs[i][j] = 0
        else:        
            penalty = 0
            if (df_calls_new[i][j] > 2) :
                penalty += df_calls_new[i][j]
            if (df_messages_new[i][j] > 2) :
                penalty += df_messages_new[i][j]
            if (df_internet_new[i][j] > 2) :
                penalty += df_internet_new[i][j]
            if (all_costs['tariff'][j] ==  'smart') :
                all_costs[i][j] = 550 + penalty
            else :
                all_costs[i][j] = 1950 + penalty
display(all_costs.head(10))         
            


# **Вывод:**
# 
# После полной обработки данных, и произведенных необходимых вычислений, получили окончательную таблицу *all_costs*, которая содержит все расходы каждого пользователя сумарно по всем параметрам. Теперь ее можно использовать для произведения анализа в следующих шагах.   

# <div class="alert alert-success">
# <b>Комментарий ревьюера:</b>
# 
# Выручка посчитана верно, теперь любая фин.отчетность нам не помеха 😊
#     
# 
#     
# </div>

# ## Анализ данных

# Проанализируем отдельно каждый параметр на предмет необходимости пользователям каждого тарифа. Создадим отдельно каждому параметру таблицы по тарифам и найдем среднее значение использования тарифа:   

# In[19]:


df_calls_new2 = df_users.merge(df_month_minutes_num, on='user_id')
df_messages_new2 = df_users.merge(df_month_messages_num, on='user_id')
df_internet_new2 = df_users.merge(df_month_internet_num, on='user_id')

for i in drop_columns:
    df_calls_new2 = df_calls_new2.drop(i, 1)
    df_messages_new2 = df_messages_new2.drop(i, 1)
    df_internet_new2 = df_internet_new2.drop(i, 1)

def mean_value(df, columns):
    df_tariffs_parametrs = pd.DataFrame(columns=['smart', 'ultra'], index = col)
    df_smart_parametr = df.query('tariff == "smart"')
    df_ultra_parametr = df.query('tariff == "ultra"')
    df_smart_parametr = df_smart_parametr.reset_index(drop=True)
    df_ultra_parametr = df_ultra_parametr.reset_index(drop=True)
    
    tmp = 0
    array_tmp = []
    for i in columns:
        for j in range(0, df_smart_parametr.shape[0]):
            if df_smart_parametr[i][j] != 0:
                tmp += df_smart_parametr[i][j]
                array_tmp.append(df_smart_parametr[i][j])
        df_tariffs_parametrs['smart'][i] = tmp / len(array_tmp)
        tmp = 0
        array_tmp = []
    for i in columns:
        for j in range(0, df_ultra_parametr.shape[0]):
            if df_ultra_parametr[i][j] != 0:
                tmp += df_ultra_parametr[i][j]
                array_tmp.append(df_ultra_parametr[i][j])
        df_tariffs_parametrs['ultra'][i] = tmp / len(array_tmp)
        tmp = 0
        array_tmp = []
        
    df_tariffs_parametrs.plot(y='smart', 
                         style='-', 
                         grid=True) 
    plt.title('График распределения средних значений в тарифе smart:')
    plt.show()
    df_tariffs_parametrs.plot(y='ultra', 
                         style='-', 
                         grid=True) 
    plt.title('График распределения средних значений в тарифе ultra:')
    plt.show()
    display(df_tariffs_parametrs)
    
dfs = [df_calls_new2,
       df_messages_new2,
       df_internet_new2]

names = ['информация о минутах', 
         'информация о сообщениях', 
         'информация об интернет сессиях']

for i, j in zip(dfs, names):
    print(j)
    mean_value(i, col)


# Плученные графики свидетельствуют о сильном увеличении использования связи к концу года, это скорее всего связанно с ростом числа пользователей в каждом месяце. Чтоб удостовериться в правоте суждений, проверим сколько приблизительно пользователей присоединилось в каждом месяце. Для этого посчитаем количество значений не равных 0 в таблице какого нибудь из тарифов:

# <div class="alert alert-success">
# <b>Комментарий ревьюера:</b>
# 
# Отличные инсайты 👍
#     
#     
# </div>

# <div class="alert alert-success">
# <b>Комментарий ревьюера:</b>
# 
# Здорово, когда графики и их оси подписаны 😊👍
#     
# Так быстрее понять о чем идёт речь на самом графике.
#     
# </div>

# In[20]:


cnt = 0
for i in col:
    for j in range(0, 500) :
        if df_month_calls_num[i][j] != 0:
            cnt += 1
    print('В месяце "', i, '" количество активных ползователей составляет:', cnt)
    cnt = 0


# Действительно, в среднем количество пользователей в каждом месяце растет примерно в 1,5-2 раза по сравнению с предыдущем.
# 
# Найдем ежемесячную дисперсию и среднеквадратическое отклонение:

# In[21]:


def var_value(df, columns):
    df_tariffs_parametrs = pd.DataFrame(columns=['smart', 'ultra'], index = col)
    df_smart_parametr = df.query('tariff == "smart"')
    df_ultra_parametr = df.query('tariff == "ultra"')
    df_smart_parametr = df_smart_parametr.reset_index(drop=True)
    df_ultra_parametr = df_ultra_parametr.reset_index(drop=True)
    
    array_tmp = []
    for i in columns:
        for j in range(0, df_smart_parametr.shape[0]):
            if df_smart_parametr[i][j] != 0:
                array_tmp.append(df_smart_parametr[i][j])
        df_tariffs_parametrs['smart'][i] = np.var(array_tmp, ddof=0)
        array_tmp = []
    for i in columns:
        for j in range(0, df_ultra_parametr.shape[0]):
            if df_ultra_parametr[i][j] != 0:
                array_tmp.append(df_ultra_parametr[i][j])
        df_tariffs_parametrs['ultra'][i] = np.var(array_tmp, ddof=0)
        array_tmp = []

    print('Дисперсия')
    display(df_tariffs_parametrs)
    for i in ['smart', 'ultra']:
        for j in col :
            df_tariffs_parametrs[i][j] = np.sqrt(df_tariffs_parametrs[i][j])
    print('Среднеквадратическое отклонение')
    display(df_tariffs_parametrs)
    df_tariffs_parametrs.plot(y='smart', 
                         style='-', 
                         grid=True) 
    plt.title('График распределения среднеквадратического отклонения в тарифе smart:')
    plt.show()
    df_tariffs_parametrs.plot(y='ultra', 
                         style='-', 
                         grid=True) 
    plt.title('График распределения среднеквадратического отклонения в тарифе ultra:')
    plt.show()

for i, j in zip(dfs, names):
    print(j)
    print('')
    var_value(i, col)


# <div class="alert alert-success">
# <b>Комментарий ревьюера:</b>
# 
# Кстати имея линейную структуру данных мы могли бы весь этот расчет сделать с помощью одной сводной таблицы.
#     
# Где в атрибуте `aggfunc` мы указали бы нужные нам метрики – `aggfunc = [np.var, np.std,]` и т.д.
#     
# </div>

# **Вывод**
# 
# Полученные данные предоставляют полную картину о распределении имеющихся данных, а именно: можно точно узнать в каком диапозоне находится 95% данных, какие значения являются средними для каждого месяца, и как количество пользователей в каждом месяце влияет на спрос и выручку. 

# <div class="alert alert-success">
# <b>Комментарий ревьюера:</b>
# 
# Очень детально проверили наш анализ пользователей, выводы абсолютно логичны и даже придраться не к чему 😊👍
#     
# Предлагаю приступить к проверке наших гипотез.
#     
# </div>

# ## Проверка гипотез
# 
# ### Сравнение средней выручки пользователей разных тарифов

# Будем использовать t-распределение Стъюдента для расчета гипотез. 
# 
# Сформулируем нулевую гипотезу: средняя выручка с тарифа ultra равна средней выручке тарифа smart;
# Тогда альтернативная гипотеза будет гласить: выручки с обоих тарифов отличаются. 
# 
# Для работы над гипотезой будем использоваать таблицу *all_costs*, полученную в 3 пункте, которая содержит в себе информацию о прибыли с каждого пользователя обоих тарифов. 

# <div class="alert alert-success">
# <b>Комментарий ревьюера:</b>
# 
# Гипотезы сформулированы верно.
#     
#     
# **Best practies:**
#     
# Перед проверкой гипотезы рекомендую проверить дисперсии выборок, чтобы корректно определить атрибут `equal_val` в Т–тесте.
#     
# В том числе стоит визуализировать распределение каждой выборки, чтобы определить нормальное ли у них распределение или нет.
#     
# Так мы покажем логичность и последовательность наших действий.
#     
# </div>

# <div class="alert alert-info"> <b>Комментарий студента:</b> Не подскажете, пожалуйста, как построить график с распределением частот?</div>

# <div class="alert alert-success">
# <b>Комментарий ревьюера (2):</b>
# 
# Если правильно понял, то в этом нам помогут `xlim` / `ylim` и подписи осей.
#     
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.xlim.html
# 
#     
# https://stackoverflow.com/questions/3100985/plot-with-custom-text-for-x-axis-points
#     
#     
# </div>

# In[22]:


smart_query = all_costs.query('tariff == "smart"')
ultra_query = all_costs.query('tariff == "ultra"')

def tariff_m(tariff_query):
    tariff_query = tariff_query.reset_index(drop=True)
    tariff_mean = []
    for i in col:
        for j in range(0, tariff_query.shape[0]):
            if tariff_query[i][j] != 0:
                tariff_mean.append(tariff_query[i][j])
    return tariff_mean

smart_mean = tariff_m(smart_query)
ultra_mean = tariff_m(ultra_query)

smart_var = np.var(smart_mean)
ultra_var = np.var(ultra_mean)

if (smart_var == ultra_var) :
    print('использовать equal_val = True')
else:
    print('использовать equal_val = False')


# In[23]:


results = st.ttest_ind(smart_mean, ultra_mean, equal_var = False)
print('p-значение: ', results.pvalue)


# P-значение равно нулю, это связанно с тем что все значения тарифа *ultra* равны 1950, то есть никто не превысил заданных лимитов, в связи с чем дисперсия равна нулю. Следовательно можно с уверенностью отвергнуть нулевую гипотезу о том, что средняя выручка с клиентов разных тарифов равна, а именно, если быть точнее, средняя выручка с клиентов *ultra* больше. 

# <div class="alert alert-danger">
# <b>Комментарий ревьюера:</b>
# 
# <s>У нас не совсем верно проверена гипотеза. 
#     
# В нашем случае нам важно передавать все значения каждого месяца выручки у клиента, т.к. метод основан на усреднении показателей.
#     
# На текущий момент мы 2 раза усредняем наши значения, что является не совсем корректным.
#     
# Давай также поправим этот момент.
#     
# </div>

# ### Сравнение выручки пользователей из Москвы и других регионов
# 
# Проверим следующую гипотезу: средняя выручка пользователей из Москвы отличается от выручки пользователей из других регионов. 
# 
# Нулевая гипотеза: средняя выручка с обоих регеонов одинаковая. 
# Альтернативная гипотеза: средняя выручка отличается.

# <div class="alert alert-success">
# <b>Комментарий ревьюера:</b>
# 
# Гипотезы сформулированы верно.
#     
#     
#     
# </div>

# In[24]:


Moscow_query = all_costs.query('city == "Москва"')
another_city_query = all_costs.query('city != "Москва"')

def city_m(city_query):
    city_query = city_query.reset_index(drop=True)
    city_mean = []
    for i in col:
        for j in range(0, city_query.shape[0]):
            if city_query[i][j] != 0:
                city_mean.append(city_query[i][j])
    return city_mean

Moscow_mean = city_m(Moscow_query)
another_city_mean = city_m(another_city_query)

Moscow_var = np.var(Moscow_mean)
another_city_var = np.var(another_city_mean)

if (Moscow_var == another_city_var) :
    print('использовать equal_val = True')
else:
    print('использовать equal_val = False')


# In[25]:


results = st.ttest_ind(Moscow_mean, another_city_mean, equal_var = False)
print('p-значение: ', results.pvalue)


# Полученное p-значение позволяет отвергнуть нулевую гипотезу о равенстве прибыли с городов России и Москвы.
# 
# Получение гистограммы распределения частот

# In[65]:


value_list = []
frequency_list = []

for i in range(0, len(another_city_mean)):
    if another_city_mean[i] in value_list:
        cnt = value_list.index(another_city_mean[i])
        frequency_list[cnt] += 1
    else :
        value_list.append(another_city_mean[i])
        frequency_list.append(1)

df_smart_plot = pd.DataFrame(columns = ['value', 'frequency'])
df_smart_plot['value'] = value_list
df_smart_plot['frequency'] = frequency_list
df_smart_plot= df_smart_plot.sort_values(by='frequency')
df_smart_plot = df_smart_plot.set_index('value')
df_smart_plot.hist('frequency', bins=100, range=(-50,50))


# ## Общий вывод
# 
# Проведенный анализ показал, что люди в основном не превышают лимиты по различным параметрам в тарифе *ultra*, чего не скажешь о тарифе *smart*. Однако даже перерасход тарифа *smart* и его значительно превышающее коичество пользователей не обеспечивает той прибыли, что дает *ultra*. Также немаловажным является тот факт, что выручка с пользователей города Москвы выше, чем во всех остальных городах. 
# 
# Таким образом можно сделать вывод, что в Москве и остальных крупных городах лучше всего привлекать больше пользователей к тарифу *ultra*, а вот в региональных городах наоборот рекламировать тариф *smart*, который своей дешевизной будет привлекать клиентов в разы больше чем *ultra*, а завышенные цены на дополнительные услуги будут компенсировать ту выручку, которую можно было бы получить, если бы пользователь использовал бы тариф *ultima*.

# <div class="alert alert-success">
# <b>Комментарий ревьюера:</b>
# 
# 
#     
# Достаточно детально проделанная работа и это не может не радовать 😊
#     
# Давай поправим мои комментарии и будем двигаться дальше.
#     
# Если у тебя вдруг есчть какие–либо вопросы, то я с радостью отвечу на них 😊
#        
# 
# </div>

# <div class="alert alert-success">
# <b>Комментарий ревьюера (2):</b>
# 
# Выводы понятны и логичны, а самое главное подкреплены выявленными фактами.
#        
# В целом сам проект выполнен на хорошем уровне! На протяжении всей работы чувствуется глубина проработки задачи и это безусловный плюс для нас. Было использовано большое количество методов, которые будут помогать тебе в дальнейших проектах.
#        
# Рекомендую посмотреть в открытом доступе на ютубе например – курс по Алгоритмам и структурам данных, эта информация поможет нам в дальнейшем при работе с данными.
#     
# Поздравляю с успешным завершением проекта 😊👍
#     
# И желаю успехов в новых работах 😊
#     
# **[общий комментарий]** Ячейки **markdown** в том числе мы можем использовать как дополнительный способ стилизации нашего проекта. Оставил ниже ссылку, с примерами стилизации.
# 
# https://sqlbak.com/blog/jupyter-notebook-markdown-cheatsheet
#  
#     
# </div>

# # Чек-лист
# 
# - [x] Описыны выявленные в данных проблемы
# - [x] Подготовка данных к анализу
# - [x] Графики для распределений построены 
# - [x] Проинтерпретированы полученные графики
# - [x] Рассчитано стандартное отклонение и дисперсия
# - [x] Сформулированы альтернативные и нулевые гипотезы
# - [x] Проверены гипотезы
# - [x] Проинтерпретирован результат проверки гипотезы
# - [x] Выводы сделаны
# - [x] Комментарии к шагам оставлены
