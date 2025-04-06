from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os, sys
from datetime import datetime, timedelta
from PIL import Image as PilImage, ImageTk

from utils.domain_checker import DomainChecker
from utils.rkn_data import ParserClient


class UserInterface:
    def __init__(self):
        self.root = Tk()
        self.root.title('RKN Check')
        self.root.geometry("850x450+400+200")
        self.root.iconbitmap(default="utils/static/icon.ico")
        self.root.attributes("-alpha", 0.96)
        self.root.minsize(800,450)
        self.path_icon_q = "utils/static/icon_q.png"
        self.question_photo = ImageTk.PhotoImage(PilImage.open(self.path_icon_q).
                                                 resize((20, 20), PilImage.LANCZOS))
        self.name_file_rkn = ParserClient().file_name

    def set_frame_1(self):
        frame_1 = Frame(self.root)
        frame_1.pack(fill='x', padx=15)
        self.btn_update_rkn = ttk.Button(frame_1, command=self._update_rkn, text="Обновить")
        self.btn_update_rkn.pack(side='right', padx=10, pady=10)
        date, color = self._get_file_creation_date(self.name_file_rkn)
        foreground = "black" if color else "red"
        self.label_last_update_rkn = ttk.Label(frame_1, text=f"Последнее обновление заблокированных доменов : {date}", foreground=foreground)
        self.label_last_update_rkn.pack(side='left', padx=10, pady=10)
        question_mark = ttk.Label(frame_1, image=self.question_photo, cursor="hand2")
        question_mark.pack(side='right', padx=5)
        # Привязка события нажатия на знак вопроса
        question_mark.bind("<Button-1>", lambda e: self._show_info())

    @staticmethod
    def _get_file_creation_date(file_path):
        if os.path.isfile(file_path):
            creation_time = os.path.getctime(file_path)
            formatted_time = datetime.fromtimestamp(creation_time).strftime('%H:%M:%S, %d %b %Y')
            is_recent = (datetime.now() - datetime.fromtimestamp(creation_time)) < timedelta(days=1)
            return formatted_time, is_recent
        else:
            return None, False

    def _update_rkn(self):
        parser_client = ParserClient()
        session = parser_client.open_session()
        parser_client.get_response(session, timeout=30)
        self.btn_update_rkn.config(text="Обновлено", state="disabled")
        date, color = self._get_file_creation_date(self.name_file_rkn)
        foreground = "black" if color else "red"
        self.label_last_update_rkn.config(
            text=f"Последнее обновление заблокированных ресурсов : {date}",
            foreground=foreground
        )

    @staticmethod
    def _show_info():
        messagebox.showinfo("Справка", "Программа получает данные от ресурса rknweb.ru о сайтах и (или) "
                                "страницах сайтов сети «Интернет» в отношении которых приняты меры по ограничению "
                                "доступа в рамках исполнения требований статей 15.1–15.6-1, 15.8 Федерального закона "
                                "от 27.07.2006 года\n№ 149-ФЗ «Об информации, информационных технологиях и защите "
                                "информации».\n\nДанные на сайте обновляются один раз в день.")

    def set_frame_2(self):
        frame_2 = Frame(self.root)
        frame_2.pack(fill='x', padx=15)
        style = ttk.Style()
        style.configure('TButton', padding=6)
        style.configure('TEntry', padding=5)
        self.entry = ttk.Entry(frame_2, width=50)
        self.entry.pack(side='left', padx=10, pady=10)
        self.entry.bind("<FocusIn>", self._on_entry_click)
        self.entry.bind("<FocusOut>", self._on_focusout)
        self.label_placeholder = ttk.Label(self.entry, text="Путь к файлу", style='TLabel')
        self.label_placeholder.place(relx=0.02, rely=0.5, anchor='w')
        button_browse = ttk.Button(frame_2, text="Выбрать файл", command=self._choose_file)
        button_browse.pack(side='right', padx=10, pady=10)
        question_mark = ttk.Label(frame_2, image=self.question_photo, cursor="hand2")
        question_mark.pack(side='right', padx=5)
        question_mark.bind("<Button-1>", lambda e: self._show_help())

    def _on_entry_click(self, event):
        if self.entry.get() == "путь к файлу":
            self.entry.delete(0, END)
            self.label_placeholder.place_forget()

    def _on_focusout(self, event):
        if self.entry.get() == "":
            self.entry.insert(0, "Путь к файлу")  # Восстанавливаем подсказку
            self.label_placeholder.place(relx=0.02, rely=0.5, anchor='w')  # Показываем подсказку

    def _choose_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsm;*.xlsx")])
        if file_path:
            self.entry.delete(0, END)
            self.entry.insert(0, file_path)
            self.label_placeholder.place_forget()

    @staticmethod
    def _show_help():
        messagebox.showinfo("Помощь","Для корректной работы программы требуется таблица Excel "
                                     "(.xlsm;.xlsx), в которой проверяемые домены должны быть записаны построчно "
                                     "в первой колонке.")

    def set_frame_3(self):
        frame_3 = ttk.Frame(self.root)
        frame_3.pack(fill='both', expand=True, padx=15, pady=15)
        button_process = ttk.Button(frame_3, text="Обработать данные", command=self._process_data)
        button_process.pack(side=RIGHT, pady=10)

    def set_frame_4(self):
        frame_4 = ttk.Frame(self.root)
        frame_4.pack(fill='both', expand=True, padx=15, pady=15)
        self.output_text = Text(frame_4, wrap=WORD, bg="#f0f0f0", fg="#333333")
        self.output_text.pack(side=LEFT, fill='both', expand=True)
        scrollbar = ttk.Scrollbar(frame_4, command=self.output_text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.output_text.config(yscrollcommand=scrollbar.set)

    def _process_data(self):
        file_path = self.entry.get()
        if file_path:
            dc = DomainChecker(file_path)
            results = dc.find_intersections()
            if len(results) == 0:
                self.output_text.insert(END, f'Совпадений не найдено. Убедитесь, что вы правильно '
                                             f'подготовили файл для проверки. Справку можно найти рядом с кнопкой '
                                             f'"Выбрать файл"')
            else:
                self.output_text.insert(END, f"Найдено {len(results)} пересечений. "
                                             f"Результаты записаны в файл '{dc.result_file}'.\n\n")
                for i in results:
                    self.output_text.insert(END, f"{i}\n")
        else:
            raise "Указан неверный путь к пользовательскому файлу."

    def mainloop(self):
        self.root.protocol("WM_DELETE_WINDOW", self._finish)
        self.root.mainloop()

    def _finish(self):
        self.root.destroy()

    def report_callback_exception(self):
        self.root.report_callback_exception = self._exception_handler

    @staticmethod
    def _exception_handler(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        messagebox.showerror("Ошибка", str(exc_value))
