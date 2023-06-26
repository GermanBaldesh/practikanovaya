import sqlite3
import tkinter as tk
from tkinter import ttk

# Подключение к базе данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создание графического интерфейса
root = tk.Tk()
root.geometry('800x600')
root.title('Access Log Viewer')

# Создание списка записей (Listbox)
listbox = tk.Listbox(root, width=100, height=30)
listbox.grid(row=0, column=0, padx=10, pady=10)

# Получение всех записей из базы данных
cursor.execute('SELECT * FROM access_log')
rows = cursor.fetchall()

# Добавление записей в список
for row in rows:
    listbox.insert(tk.END, f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]}')

# Создание полей ввода для фильтрации записей
ip_address_var = tk.StringVar()
ip_address_var.trace('w', lambda name, index, mode: apply_filter())
timestamp_var = tk.StringVar()
timestamp_var.trace('w', lambda name, index, mode: apply_filter())

label_ip_address = ttk.Label(root, text="IP Address:")
label_ip_address.grid(row=1, column=0, padx=10, pady=10, sticky='w')
ip_address_entry = ttk.Entry(root, textvariable=ip_address_var)
ip_address_entry.grid(row=1, column=0, padx=10, pady=10, sticky='w')

label_timestamp = ttk.Label(root, text="Timestamp:")
label_timestamp.grid(row=1, column=0, padx=10, pady=10, sticky='e')
timestamp_entry = ttk.Entry(root, textvariable=timestamp_var)
timestamp_entry.grid(row=1, column=0, padx=10, pady=10, sticky='e')

# Создание кнопок для поиска и сброса фильтра
search_btn = ttk.Button(root, text='Search', command=lambda: apply_filter())
search_btn.grid(row=2, column=0, padx=10, pady=10, sticky='w')

reset_btn = ttk.Button(root, text='Reset', command=lambda: reset_filter())
reset_btn.grid(row=2, column=0, padx=10, pady=10, sticky='e')

# Функция для применения фильтра
def apply_filter():
    # Получение значений фильтров
    ip_address = ip_address_var.get()
    timestamp = timestamp_var.get()

    # Выполнение запроса с учетом фильтров
    cursor.execute('SELECT * FROM access_log WHERE ip_address LIKE ? AND timestamp LIKE ?', ('%' + ip_address + '%', '%' + timestamp + '%'))
    rows = cursor.fetchall()

    # Обновление списка записей
    listbox.delete(0, tk.END)
    for row in rows:
        listbox.insert(tk.END, f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]}')

# Функция для сброса фильтра
def reset_filter():
    # Сброс значений фильтров
    ip_address_var.set('')
    timestamp_var.set('')

    # Получение всех записей из базы данных
    cursor.execute('SELECT * FROM access_log')
    rows = cursor.fetchall()

    # Обновление списка записей
    listbox.delete(0, tk.END)
    for row in rows:
        listbox.insert(tk.END, f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]}')

# Функция для отображения подробной информации
def show_details():
    # Получение выбранной записи
    selection = listbox.curselection()
    if selection:
        row_index = selection[0]
        row_id = listbox.get(row_index).split(' ')[0]

        # Выполнение запроса для получения дополнительной информации о записи
        cursor.execute('SELECT * FROM access_log WHERE id = ?', (row_id,))
        row = cursor.fetchone()

        # Отображение дополнительной информации
        details_window = tk.Toplevel(root)
        details_window.geometry('400x300')
        details_window.title(f'Details for Record {row_id}')

        details_text = tk.Text(details_window, width=50, height=20)
        details_text.grid(row=0, column=0, padx=10, pady=10)

        details_text.insert(tk.END, f'IP Address: {row[1]}\n')
        details_text.insert(tk.END, f'Timestamp: {row[2]}\n')
        details_text.insert(tk.END, f'Method: {row[3]}\n')
        details_text.insert(tk.END, f'Path: {row[4]}\n')
        details_text.insert(tk.END, f'Status: {row[5]}\n')
        details_text.insert(tk.END, f'Size: {row[6]}')

# Добавление возможности выбора записи из списка и отображения подробной информации
listbox.bind('<<ListboxSelect>>', lambda event: show_details())

# Запуск приложения
root.mainloop()

# Закрытие подключения к базе данных
conn.close()