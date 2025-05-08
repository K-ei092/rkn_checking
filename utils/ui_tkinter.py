from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os, sys
from datetime import datetime, timedelta
from PIL import Image as PilImage, ImageTk
from lexicon.lexicon import LEXICON_UI

from utils.domain_checker import DomainChecker
from utils.parser import ParserClient


class UserInterface:
    def __init__(self):
        self.root = Tk()
        self.root.title(LEXICON_UI["root.title"])
        self.root.geometry("850x450+400+200")
        self.root.iconbitmap(default="utils/static/icon.ico")
        self.root.attributes("-alpha", 0.96)
        screen_width = self.root.winfo_screenwidth() - 15
        screen_height = self.root.winfo_screenheight() - 90
        self.root.geometry(f"{screen_width}x{screen_height}+0+8")
        self.root.resizable(False, False)
        self.path_icon_q = "utils/static/icon_q.png"
        self.question_photo = ImageTk.PhotoImage(PilImage.open(self.path_icon_q).
                                                 resize((20, 20), PilImage.LANCZOS))
        self.name_file_rkn = ParserClient.file_name_rkn
        self.file_name_mnj = ParserClient.file_name_mnj

    def set_frame_1(self):
        frame_1 = Frame(self.root)
        frame_1.pack(fill='x', padx=15)
        self.btn_update_rkn = ttk.Button(frame_1, command=self._update_rkn, text=LEXICON_UI["btn_update"])
        self.btn_update_rkn.pack(side='right', padx=10, pady=10)
        date, color = self._get_file_creation_date(self.name_file_rkn, days=1)
        foreground = "black" if color else "red"
        self.label_last_update_rkn = ttk.Label(frame_1,
                                               text=LEXICON_UI["label_last_update_rkn"].format(date=date),
                                               foreground=foreground
                                               )
        self.label_last_update_rkn.pack(side='left', padx=10, pady=10)
        question_mark = ttk.Label(frame_1, image=self.question_photo, cursor="hand2")
        question_mark.pack(side='right', padx=5)
        # Привязка события нажатия на знак вопроса
        question_mark.bind("<Button-1>", lambda e: self._show_info(
            LEXICON_UI["showinfo.title.info"], LEXICON_UI["showinfo.title.msg.rkn"]
        )
                           )

    @staticmethod
    def _get_file_creation_date(file_path, days):
        if os.path.isfile(file_path):
            creation_time = os.path.getctime(file_path)
            formatted_time = datetime.fromtimestamp(creation_time).strftime('%H:%M:%S, %d %b %Y')
            is_recent = (datetime.now() - datetime.fromtimestamp(creation_time)) < timedelta(days=days)
            return formatted_time, is_recent
        else:
            return None, False

    def _update_rkn(self):
        parser_client = ParserClient(resource_rkn=True)
        session = parser_client.open_session()
        parser_client.get_response(session, timeout=30)
        self.btn_update_rkn.config(text=LEXICON_UI["btn_updated"], state="disabled")
        date, color = self._get_file_creation_date(self.name_file_rkn, days=1)
        foreground = "black" if color else "red"
        self.label_last_update_rkn.config(
            text=LEXICON_UI["label_last_update_rkn"].format(date=date),
            foreground=foreground
        )

    @staticmethod
    def _show_info(title, text):
        messagebox.showinfo(title, text)

    def set_frame_2(self):
        frame_2 = Frame(self.root)
        frame_2.pack(fill='x', padx=15)
        self.btn_update_mnj = ttk.Button(frame_2, command=self._update_mnj, text=LEXICON_UI["btn_update"])
        self.btn_update_mnj.pack(side='right', padx=10, pady=10)
        date, color = self._get_file_creation_date(self.file_name_mnj, days=3)
        foreground = "black" if color else "red"
        self.label_last_update_mnj = ttk.Label(frame_2,
                                               text=LEXICON_UI["label_last_update_mnj"].format(date=date),
                                               foreground=foreground
                                               )
        self.label_last_update_mnj.pack(side='left', padx=10, pady=10)
        question_mark = ttk.Label(frame_2, image=self.question_photo, cursor="hand2")
        question_mark.pack(side='right', padx=5)
        # Привязка события нажатия на знак вопроса
        question_mark.bind("<Button-1>", lambda e: self._show_info(
            LEXICON_UI["showinfo.title.info"],
            LEXICON_UI["showinfo.title.msg.mnj"]
        )
                           )

    def _update_mnj(self):
        parser_client = ParserClient(resource_rkn=False)
        session = parser_client.open_session()
        parser_client.get_response(session, timeout=30)
        self.btn_update_mnj.config(text=LEXICON_UI["btn_updated"], state="disabled")
        date, color = self._get_file_creation_date(self.file_name_mnj, days=3)
        foreground = "black" if color else "red"
        self.label_last_update_mnj.config(
            text=LEXICON_UI["label_last_update_mnj"].format(date=date),
            foreground=foreground
        )

    def set_frame_3(self):
        frame_3 = Frame(self.root)
        frame_3.pack(fill='x', padx=15)
        style = ttk.Style()
        style.configure('TButton', padding=6)
        style.configure('TEntry', padding=5)
        self.entry = ttk.Entry(frame_3, width=50)
        self.entry.pack(side='left', padx=10, pady=10)
        self.entry.bind("<FocusIn>", self._on_entry_click)
        self.entry.bind("<FocusOut>", self._on_focusout)
        self.label_placeholder = ttk.Label(self.entry, text=LEXICON_UI["File_path"], style='TLabel')
        self.label_placeholder.place(relx=0.02, rely=0.5, anchor='w')
        button_browse = ttk.Button(frame_3, text=LEXICON_UI["button_browse"], command=self._choose_file)
        button_browse.pack(side='right', padx=10, pady=10)
        question_mark = ttk.Label(frame_3, image=self.question_photo, cursor="hand2")
        question_mark.pack(side='right', padx=5)
        question_mark.bind("<Button-1>", lambda e: self._show_info(
            LEXICON_UI["showinfo.title.help"], LEXICON_UI["showinfo.title.msg.help"]
        )
                           )

    def _on_entry_click(self, event):
        if self.entry.get() == LEXICON_UI["File_path"]:
            self.entry.delete(0, END)
            self.label_placeholder.place_forget()

    def _on_focusout(self, event):
        if self.entry.get() == "":
            self.entry.insert(0, LEXICON_UI["File_path"])  # Восстанавливаем подсказку
            self.label_placeholder.place(relx=0.02, rely=0.5, anchor='w')  # Показываем подсказку

    def _choose_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsm;*.xlsx")])
        if file_path:
            self.entry.delete(0, END)
            self.entry.insert(0, file_path)
            self.label_placeholder.place_forget()

    def set_frame_4(self):
        frame_4 = ttk.Frame(self.root)
        frame_4.pack(fill='both', expand=True, padx=15, pady=15)
        button_process = ttk.Button(frame_4, text=LEXICON_UI["button_process"], command=self._process_data)
        button_process.pack(side=RIGHT, pady=10)

    def set_frame_5(self):
        frame_5 = ttk.Frame(self.root)
        frame_5.pack(fill='both', expand=True, padx=15, pady=15)
        self.output_text_rnk = Text(frame_5, wrap=WORD, bg="#f0f0f0", fg="#333333")
        self.output_text_rnk.pack(side=LEFT, fill='both', expand=True)
        scrollbar = ttk.Scrollbar(frame_5, command=self.output_text_rnk.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.output_text_rnk.config(yscrollcommand=scrollbar.set)

    def _process_data(self):
        file_path = self.entry.get()
        if file_path:
            dc = DomainChecker(file_path)
            results_rkn = dc.find_intersections_rkn()
            if len(results_rkn) == 0:
                self.output_text_rnk.insert(END, LEXICON_UI["output_text_rnk1"])
            else:
                self.output_text_rnk.insert(
                    END,
                    LEXICON_UI["output_text_rnk2"].format(
                        results_rkn=len(results_rkn), result_file_rkn=dc.result_file_rkn
                    )
                )
                for i in results_rkn:
                    self.output_text_rnk.insert(END, LEXICON_UI["output_text_rnk3"].format(i=i))

            results_mnj = dc.find_intersections_mnj()
            if len(results_mnj) == 0:
                self.output_text_mnj.insert(END, LEXICON_UI["output_text_mnj1"])
            else:
                self.output_text_mnj.insert(
                    END,
                    LEXICON_UI["output_text_mnj2"].format(
                        results_mnj=len(results_mnj), result_file_mnj=dc.result_file_mnj
                    )
                )
                for i in results_mnj:
                    self.output_text_mnj.insert(END, LEXICON_UI["output_text_mnj3"].format(i=i))

        else:
            raise Exception(LEXICON_UI["exception_path_file"])

    def set_frame_6(self):
        frame_6 = ttk.Frame(self.root)
        frame_6.pack(fill='both', expand=True, padx=15, pady=15)
        self.output_text_mnj = Text(frame_6, wrap=WORD, bg="#f0f0f0", fg="#333333")
        self.output_text_mnj.pack(side=LEFT, fill='both', expand=True)
        scrollbar = ttk.Scrollbar(frame_6, command=self.output_text_mnj.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.output_text_mnj.config(yscrollcommand=scrollbar.set)

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
        messagebox.showerror(LEXICON_UI["title.error"], str(exc_value))
