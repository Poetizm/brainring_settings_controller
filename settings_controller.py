# ----------------------------------------------------------- #
# Данный файл является обработчиком настроек приложения       #
# ----------------------------------------------------------- #

# Импорт библиотек
import configparser
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from app.controllers.settings.save_dialog_controller import SaveDialog

''' Путь к файлу конфигурации settings.ini '''
settings_file = "app/assets/settings/settings.ini"


class Settings(QMainWindow):
    def __init__(self, parent)-> None:
        print("[+] Открыт экран Настройки")
        super().__init__(parent)
        self.parent().tabWidget.setCurrentWidget(self.parent().tabTimer)
        self.parent().pushbutton_back_from_settings.clicked.connect(self.press_back)
        self.parent().pushbutton_set_default.clicked.connect(self.press_set_default)
        self.parent().pushbutton_load.clicked.connect(self.press_load)
        self.parent().pushbutton_save.clicked.connect(self.press_save)
        self.parent().pushbutton_apply.clicked.connect(self.press_apply)
        # Загрузка текущих настроек из settings.ini раздела [CURRENT]
        # self.load_settings()

    def press_set_default(self):
        """
        Нажатие кнопки По умолчанию
        """
        print("[+] Нажата кнопка По умолчанию")
        box = QMessageBox()
        box.setIcon(QMessageBox.Icon.Question)
        box.setWindowTitle('Загрузка настроек по умолчанию')
        box.setText('Вы точно хотите установить настройки по умолчанию?')
        box.setStandardButtons(QMessageBox.StandardButton.Yes |
                               QMessageBox.StandardButton.No)
        btnYes = box.button(QMessageBox.StandardButton.Yes)
        btnYes.setText('Да')
        btnNo = box.button(QMessageBox.StandardButton.No)
        btnNo.setText('Нет')
        box.exec()

        if box.clickedButton() == btnYes:
             self.set_default_settings()

    def press_load(self):
        '''
        Нажатие кнопки Загрузить
        '''
        print("[+] Нажата кнопка Загрузить")
        pass

    def press_save(self):
        '''
        Нажатие кнопки Сохранить
        Открытие диалогового окна 'Сохранение пользовательских настроек'
        при сохранении набора настроек
        '''
        print("[+] Нажата кнопка Сохранить")

        self.save_dialog = SaveDialog(settings_window=self)
        # Вместо show() используется exec() для блокировки Главного окна
        self.save_dialog.exec()

    def press_back(self):
        """
        Нажатие кнопки Назад
        """
        print("[+] Нажата кнопка Назад")
        self.parent().stackedWidget.setCurrentIndex(0)

    def set_default_settings(self):
            """
            Установка настроек по умолчанию
            """
            print("[+] Устанавливаются значения настроек по умолчанию")
            self.parent().spinbox_answer_duration.setProperty("value", 60)
            self.parent().radiobutton_fixed_answer_time.setChecked(False)
            self.parent().radiobutton_remaining_answer_time.setChecked(True)
            self.parent().spinbox_fixed_answer_time_amount.setProperty("value", 20)
            self.parent().checkbox_timer_louder_when_round_time_runs_out.setChecked(True)

            self.parent().radiobutton_score_auto.setChecked(True)
            self.parent().checkbox_score_penalty_for_wrong_answer.setChecked(False)
            self.parent().checkbox_score_clear_each_round.setChecked(False)
            self.parent().radiobutton_score_not_recording.setChecked(False)
            self.parent().radiobutton_draw_manual.setChecked(True)
            self.parent().radiobutton_draw_auto.setChecked(False)
            self.parent().radiobutton_answer_price_always_one_point.setChecked(True)
            self.parent().radiobutton_answer_price_sum_unanswered.setChecked(False)
            self.parent().radiobutton_answer_price_custom.setChecked(False)
            self.parent().spinbox_custom_answer_price.setProperty("value", 1)
            self.parent().radiobutton_game_over_manual.setChecked(False)
            self.parent().radiobutton_game_over_score.setChecked(True)
            self.parent().spinbox_game_over_score.setProperty("value", 3)
            self.parent().radiobutton_game_over_answers.setChecked(False)
            self.parent().spinbox_game_over_answers.setProperty("value", 5)
            self.parent().checkbox_game_over_if_leader_unreachable.setChecked(False)

            self.parent().radiobutton_falsestart_off.setChecked(True)
            self.parent().radiobutton_falsestart_equal_wrong_answer.setChecked(False)
            self.parent().checkbox_ignore_time_button.setChecked(False)
            self.parent().spinbox_ignore_time_button_duration.setProperty("value", 5)
            self.parent().checkbox_ignore_last_team_falsestart.setChecked(False)
            self.parent().radiobutton_falsestart_block_team_button.setChecked(False)
            self.parent().checkbox_temporary_block_team_button.setChecked(False)
            self.parent().spinbox_block_team_button_duration.setProperty("value", 5)

            self.parent().checkbox_record_game_protocol.setChecked(True)

    def load_settings(self, set_name='CURRENT'):
        """
        Загрузка набора настроек для отображения в окне НАСТРОЙКИ
        (по умолчанию - из раздела CURRENT)
        """
        print(f"[+] Загружается набор настроек {set_name}")
        cfg = configparser.ConfigParser()

        with open(settings_file) as config:
            cfg.read_file(config)

        options = cfg.options(set_name)

        for option in options:
            value = cfg.get(set_name, option)
            if value.isdigit():
                complete = f'self.parent().{option}.setProperty("value", {int(value)})'
                eval(complete)
            elif value in ['True', 'False']:
                complete = f'self.parent().{option}.setChecked({value})'
                eval(complete)

    def save_settings(self, set_name='CURRENT'):
        """
        Сохранение настроек в заданный раздел
        (по умолчанию - CURRENT)
        """
        print(f"[+] Сохраняется набор настроек {set_name}")
        cfg = configparser.ConfigParser()

        with open(settings_file) as config:
            cfg.read_file(config)

        # Cписок всех опций (ключей) секции (раздела) [CURRENT]
        options = cfg.options('CURRENT')

        for option in options:
            if 'spinbox' in option:
                value = eval(f'self.parent().{option}.value()')
                cfg.set(set_name, option, str(value))
            else:
                value = eval(f'self.parent().{option}.isChecked()')
                cfg.set(set_name, option, str(value))

        with open(settings_file, 'w') as config:
            cfg.write(config)

    def press_apply(self):
        '''
        Нажатие кнопки Применить
        '''
        print(f"[+] Нажата кнопка Применить")
        box = QMessageBox()
        box.setIcon(QMessageBox.Icon.Question)
        box.setWindowTitle('Применение измененных настроек')
        # ! Формулировка ниже точная НЕ МЕНЯТЬ (СПРОСИ)
        # ? Почему не просто "Хотите применить новые настройки?"
        box.setText('Хотите сделать измененные настройки текущими?')
        box.setStandardButtons(QMessageBox.StandardButton.Yes |
                               QMessageBox.StandardButton.No)
        btnYes = box.button(QMessageBox.StandardButton.Yes)
        btnYes.setText('Да')
        btnNo = box.button(QMessageBox.StandardButton.No)
        btnNo.setText('Нет')
        box.exec()

        if box.clickedButton() == btnYes:
            self.save_settings()
            self.load_settings()
