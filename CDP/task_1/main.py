import tkinter as tk  # Импорт библиотеки tkinter для создания компонентов GUI
from tkinter import ttk  # Импорт ttk для использования стилизованных виджетов
from tkinter.messagebox import showinfo, askyesno  # Импорт функций для создания диалоговых окон
import psutil  # Импорт библиотеки psutil для взаимодействия с системными процессами и получения информации о ресурсах
import matplotlib.pyplot as plt  # Импорт matplotlib для построения графиков
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Импорт FigureCanvasTkAgg для встраивания графиков matplotlib в Tkinter
from matplotlib.figure import Figure  # Импорт Figure для создания объектов графиков
import threading  # Импорт threading для работы с потоками в фоновом режиме
import time  # Импорт time для работы с задержками


class App(tk.Tk):  # Определение главного класса приложения, наследующего класс Tk
    def __init__(self):
        super().__init__()  # Инициализация базового класса Tk
        self.title("Диспетчер задач")  # Установка заголовка окна
        self.geometry("1200x715")  # Установка размера окна

        self._setup_ui()  # Настройка компонентов пользовательского интерфейса
        self.update_graphs()  # Запуск обновления графиков с использованием системных данных
        
    def _setup_ui(self):
        # Настройка фреймов для графиков
        self._setup_graph_frames()  # Создание фреймов для графиков использования ресурсов

        # Настройка полосы прокрутки
        self.scrollbar = ttk.Scrollbar(self, orient="vertical")  # Создание вертикальной полосы прокрутки
        self.scrollbar.grid(row=2, column=2, sticky="ns")  # Размещение полосы прокрутки на сетке

        # Настройка таблицы Treeview
        self.tree = self._create_treeview()  # Создание таблицы для отображения информации о процессах
        self.scrollbar.config(command=self.tree.yview)  # Связывание полосы прокрутки с таблицей

        # Поле для ввода текста поиска
        self.search_entry = ttk.Entry(self, width=10)  # Создание виджета для ввода поиска
        self.search_entry.grid(row=3, column=0, padx=10, pady=10, sticky="ew")  # Размещение поля ввода

        # Кнопки управления
        self.delete_button = ttk.Button(self, text="Удалить", command=self.click)  # Создание кнопки для удаления процесса
        self.delete_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")  # Размещение кнопки удаления

        self.refresh_button = ttk.Button(self, text="Обновить", command=self.refresh)  # Создание кнопки для обновления списка процессов
        self.refresh_button.grid(row=3, column=2, padx=10, pady=10, sticky="w")  # Размещение кнопки обновления

        self.search_button = ttk.Button(self, text="Поиск", command=self.search)  # Создание кнопки для поиска процесса
        self.search_button.grid(row=3, column=1, padx=10, pady=10, sticky="e")  # Размещение кнопки поиска

        # Настройка веса строк и столбцов
        self.grid_rowconfigure(2, weight=1)  # Настройка веса для строки, чтобы она могла растягиваться
        self.grid_columnconfigure(0, weight=1)  # Настройка веса для столбца, чтобы он мог растягиваться

    def _create_treeview(self):
        # Создание таблицы для отображения информации о процессах
        tree = ttk.Treeview(self, columns=("Pid", "Name", "Status", "CPU", "Memory", "Username"),
                            yscrollcommand=self.scrollbar.set, show="headings")
        tree.grid(row=2, column=0, columnspan=2, sticky="nsew")  # Размещение таблицы на сетке

        # Настройка заголовков столбцов
        headings = ["Pid", "Name", "Status", "CPU", "Memory", "Username"]
        for idx, heading in enumerate(headings):
            tree.heading(heading, text=heading, command=lambda c=idx: self.sorting(c, False))  # Добавление сортировки по столбцам
            tree.column(heading, width=150 if idx != 3 and idx != 4 else 50)  # Настройка ширины столбцов

        # Заполнение таблицы информацией о процессах
        for proc in psutil.process_iter(['pid', 'name', 'status', 'username']):
            try:
                tree.insert("", tk.END, values=(
                    proc.info['pid'], proc.info['name'], proc.info['status'], proc.cpu_percent(interval=0.1),
                    proc.memory_percent(), proc.info['username']))  # Добавление строки с информацией о процессе
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue  # Обработка ошибок доступа к процессам

        return tree

    def _setup_graph_frames(self):
        # Создание фреймов для отображения графиков использования ресурсов
        frames = ["cpu", "memory", "disk", "network"]
        for idx, frame in enumerate(frames):
            frame_obj = ttk.Frame(self)  # Создание фрейма
            frame_obj.grid(row=0, column=idx, sticky="nsew")  # Размещение фрейма на сетке
            setattr(self, f"{frame}_frame", frame_obj)  # Сохранение ссылки на фрейм

            fig = Figure(figsize=(3, 2), tight_layout=True)  # Создание объекта Figure для графика
            ax = fig.add_subplot(111)  # Добавление подграфика
            canvas = FigureCanvasTkAgg(fig, master=frame_obj)  # Создание виджета для отображения графика
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Размещение виджета в фрейме

            setattr(self, f"{frame}_fig", fig)  # Сохранение ссылки на объект Figure
            setattr(self, f"{frame}_ax", ax)  # Сохранение ссылки на подграфик
            setattr(self, f"{frame}_canvas", canvas)  # Сохранение ссылки на виджет графика

    def update_graphs(self):
        # Обновление графиков для системных ресурсов
        self._update_cpu_graph()  # Обновление графика использования процессора
        self._update_memory_graph()  # Обновление графика использования оперативной памяти
        self._update_disk_graph()  # Обновление графика использования дискового пространства
        self._update_network_graph()  # Обновление графика использования сети

        # Обновление графиков каждую секунду
        self.after(1000, self.update_graphs)  # Установка таймера для обновления графиков

    def _update_cpu_graph(self):
        # Обновление графика использования процессора
        cpu_percent = psutil.cpu_percent(interval=None)  # Получение процента загрузки процессора
        self.cpu_ax.clear()  # Очистка предыдущего графика
        self.cpu_ax.set_title("CPU Usage")  # Установка заголовка графика
        self.cpu_ax.set_ylabel("Percentage")  # Установка подписи оси y
        self.cpu_ax.bar(["CPU"], [cpu_percent], color="blue")  # Построение столбчатого графика
        self.cpu_ax.set_ylim(0, 100)  # Установка пределов оси y
        self.cpu_canvas.draw()  # Отрисовка графика

    def _update_memory_graph(self):
        # Обновление графика использования оперативной памяти
        memory_percent = psutil.virtual_memory().percent  # Получение процента использования памяти
        self.memory_ax.clear()  # Очистка предыдущего графика
        self.memory_ax.set_title("Memory Usage")  # Установка заголовка графика
        self.memory_ax.set_ylabel("Percentage")  # Установка подписи оси y
        self.memory_ax.bar(["Memory"], [memory_percent], color="green")  # Построение столбчатого графика
        self.memory_ax.set_ylim(0, 100)  # Установка пределов оси y
        self.memory_canvas.draw()  # Отрисовка графика

    def _update_disk_graph(self):
        # Обновление графика использования дискового пространства
        disk_percent = psutil.disk_usage('/').percent  # Получение процента использования диска
        self.disk_ax.clear()  # Очистка предыдущего графика
        self.disk_ax.set_title("Disk Usage")  # Установка заголовка графика
        self.disk_ax.set_ylabel("Percentage")  # Установка подписи оси y
        self.disk_ax.bar(["Disk"], [disk_percent], color="orange")  # Построение столбчатого графика
        self.disk_ax.set_ylim(0, 100)  # Установка пределов оси y
        self.disk_canvas.draw()  # Отрисовка графика

    def _update_network_graph(self):
        # Обновление графика использования сети
        network_stats = psutil.net_io_counters()  # Получение сетевой статистики
        upload_speed = network_stats.bytes_sent  # Получение количества отправленных байтов
        download_speed = network_stats.bytes_recv  # Получение количества полученных байтов
        self.network_ax.clear()  # Очистка предыдущего графика
        self.network_ax.set_title("Network Usage")  # Установка заголовка графика
        self.network_ax.set_ylabel("Bytes")  # Установка подписи оси y
        self.network_ax.bar(["Upload", "Download"], [upload_speed, download_speed], color=["purple", "red"])  # Построение столбчатого графика
        self.network_canvas.draw()  # Отрисовка графика

    def sorting(self, col, reverse):
        # Сортировка таблицы по выбранному столбцу
        try:
            l = [(float(self.tree.set(k, col)), k) if col in ["CPU", "Memory"] else (self.tree.set(k, col), k) for k in self.tree.get_children("")]  # Сортировка по числовым или строковым значениям
        except ValueError:
            l = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]  # Обработка исключения для строковых значений
        l.sort(reverse=reverse)  # Сортировка в обратном порядке, если указано
        for index, (_, k) in enumerate(l):
            self.tree.move(k, "", index)  # Перемещение элементов в отсортированном порядке
        self.tree.heading(col, command=lambda: self.sorting(col, not reverse))  # Обновление заголовка для возможности повторной сортировки

    def refresh(self):
        # Обновление списка процессов
        for j in self.tree.get_children():
            self.tree.delete(j)  # Удаление всех записей из таблицы
        for i in psutil.process_iter(['pid', 'name', 'status', 'username']):
            try:
                self.tree.insert("", tk.END, values=(
                    i.info['pid'], i.info['name'], i.info['status'], i.cpu_percent(interval=0.1), i.memory_percent(),
                    i.info['username']))  # Добавление обновлённых данных о процессах
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue  # Обработка ошибок доступа к процессам

    def search(self):
        # Поиск процессов по имени
        query = self.search_entry.get().lower()  # Получение строки запроса в нижнем регистре
        filtered_processes = []
        for p in psutil.process_iter(['pid', 'name', 'status', 'username']):
            try:
                if query in p.info['name'].lower():
                    filtered_processes.append(p)  # Добавление процесса, если имя совпадает с запросом
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue  # Обработка ошибок доступа к процессам
        self.update_table(filtered_processes)  # Обновление таблицы результатами поиска

    def update_table(self, processes):
        # Обновление таблицы с процессами
        for j in self.tree.get_children():
            self.tree.delete(j)  # Удаление всех записей из таблицы
        for process in processes:
            try:
                self.tree.insert("", tk.END, values=(
                    process.info['pid'], process.info['name'], process.info['status'], process.cpu_percent(interval=0.1),
                    process.memory_percent(), process.info['username']))  # Добавление процесса в таблицу
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue  # Обработка ошибок доступа к процессам
        self.tree.update_idletasks()  # Обновление отображения таблицы

    def click(self):
        # Обработка нажатия кнопки удаления
        result = askyesno(title="Подтвержение операции",
                          message="Удаление данного процесса может вызвать непредвиденные ошибки. Вы уверены что хотите удалить его?")  # Подтверждение удаления процесса
        if result:
            self.delete_item()  # Удаление выбранного процесса
            showinfo("Результат", "Процесс удалён")  # Показ сообщения об успешном удалении
        else:
            showinfo("Результат", "Операция отменена")  # Показ сообщения об отмене операции

    def delete_item(self):
        # Удаление выбранного процесса
        selected_items = self.tree.selection()  # Получение выбранных элементов таблицы
        for item in selected_items:
            pid = self.tree.item(item, 'values')[0]  # Получение PID выбранного процесса
            try:
                proc = psutil.Process(int(pid))
                proc.terminate()  # Завершение процесса по PID
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue  # Обработка ошибок доступа к процессу
            self.tree.delete(item)  # Удаление элемента из таблицы


if __name__ == "__main__":
    app = App()  # Создание экземпляра класса приложения
    app.mainloop()  # Запуск основного цикла обработки событий
