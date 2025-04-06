import logging

from utils.ui_tkinter import UserInterface


logger = logging.getLogger(__name__)


def main():

    logging.basicConfig(
        level=logging.WARNING,                                 # настройка - DEBUG, production - WARNING
        filename="logs.log",                                   # добавляем логи в файл
        filemode='a',                                          # режим записи (a - добавить, w - переписать)
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting program')

    ui = UserInterface()
    ui.report_callback_exception()
    ui.set_frame_1()
    ui.set_frame_2()
    ui.set_frame_3()
    ui.set_frame_4()
    ui.mainloop()


if __name__ == "__main__":
    main()
