import re
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создание таблицы access_log
cursor.execute('''
    CREATE TABLE IF NOT EXISTS access_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT,
        timestamp TEXT,
        method TEXT,
        path TEXT,
        status INTEGER,
        size INTEGER
    )
''')

# Открытие файла и чтение его построчно
with open('access_logs.log', 'r') as f:
    lines = f.readlines()

# Преобразование данных и запись их в базу данных
for line in lines:
    # Извлечение данных из строки с помощью регулярных выражений
    pattern = '^(\S+) (\S+) (\S+) \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"$'
    match = re.search(pattern, line)
    if match:
        row = match.groups()

        # Преобразование даты и времени в формат для записи в базу данных
        timestamp = row[3].split()[0] + ' ' + row[3].split()[1][:-6]

        # Преобразование данных в формат для записи в базу данных и запись их в базу данных
        data = (row[0], timestamp, row[4].split()[0], row[4].split()[1], int(row[5]), int(row[6]))
        cursor.execute('INSERT INTO access_log(ip_address, timestamp, method, path, status, size) VALUES (?, ?, ?, ?, ?, ?)', data)

# Сохранение изменений и закрытие подключения
conn.commit()
conn.close()