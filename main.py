import pandas as pd

a = pd.read_csv("data.csv")

pd.options.mode.chained_assignment = None  # default='warn' for copy column

# создание колонки номера сессии
a['id'] = a.index
# вычисление разницы в секундах до предыдущей сессии каждого клиента
a['difference'] = a.groupby('customer_id')['timestamp'].diff(1)
# новый фрейм с выборкой начала сессий
sessions_start_df = a[(a['difference'].isnull()) | (a['difference'] > 180)]
# дублирование столбца
sessions_start_df["session_id"] = sessions_start_df['id']
# объединение фреймов с указанием id сессий
event_df = pd.merge_asof(a, sessions_start_df[['id', 'customer_id', 'session_id']], on='id', by='customer_id')
# добавление в изначальный фрейм столбца с id сессий
a['session_id'] = event_df['session_id']
a.drop('id', inplace=True, axis=1)
a.drop('difference', inplace=True, axis=1)
# показ всего фрейма
print(a)
