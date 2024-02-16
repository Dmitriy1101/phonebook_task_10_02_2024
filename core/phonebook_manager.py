"""
\t\tЗдравствуйте!\n
Телефонный справочник работающий через txt файл.
"""
from pdb import run
from typing import LiteralString, Any
from pathlib import Path
from pydantic.fields import FieldInfo
from core.phonebook_core import PhonebookCore
from core.phonebook_dataclass import (
    PhonebookField,
    PhonebookManagerActions,
    PhonebookManagerFunctions,
)


class PhonebookManager:
    file_name: Path = "phonebook.txt"

    def __init__(self) -> None:
        self.manager: PhonebookCore = self.get_manager
        self.worker: PhonebookManagerActions = self.get_worker
        self._set_actions()

    @property
    def get_manager(self) -> PhonebookCore:
        """
        Точка входа для начала работы.
        """

        q: str = f"Используем тестовый файл: {self.file_name}?"
        if self.is_yes(text=q):
            return PhonebookCore(file_name_path=self.file_name)
        else:
            answer: str = input("Введите путь с именем файла.txt:")
            return PhonebookCore(file_name_path=answer)

    @property
    def get_worker(self) -> PhonebookManagerActions:
        """
        Создаём объект управления worker.
        """
        return PhonebookManagerActions(
            find=PhonebookManagerFunctions(
                action_name="Поиск",
                description="Поиск элемента в данных.",
                function=self.find_data,
            ),
            update=PhonebookManagerFunctions(
                action_name="Изменить",
                description="Изменить данные в файле.",
                function=self.update_data,
            ),
            print=PhonebookManagerFunctions(
                action_name="Печать",
                description="Печать данных файла на экран.",
                function=self.print_data,
            ),
            add=PhonebookManagerFunctions(
                action_name="Оптимизировать",
                description="Удалить дубликаты из БД.",
                function=self.heal_data,
            ),
            inp=PhonebookManagerFunctions(
                action_name="Ввод",
                description="Ввести данные с клавиатуры в файл.",
                function=self.input_data,
            ),
            rem=PhonebookManagerFunctions(
                action_name="Удалить",
                description="Удалить объекты  из файла.",
                function=self.delete_data,
            ),
            exit=PhonebookManagerFunctions(
                action_name="Выход",
                description="Выход из программы.",
                function=self.end_it,
            ),
            logs=PhonebookManagerFunctions(
                action_name="Логи",
                description="Распечатка логов.",
                function=self.print_mamager_err_list,
            ),
            clean_logs=PhonebookManagerFunctions(
                action_name="Очистить логи",
                description="Очистить данные логов.",
                function=self.clean_logs,
            ),
            check=PhonebookManagerFunctions(
                action_name="Проверить файл",
                description="Проверить состояние и размер файла.",
                function=self.check,
            ),
            commands=PhonebookManagerFunctions(
                action_name="Команды",
                description="Вывести список команд.",
                function=self.commands,
            ),
        )

    def _set_actions(self):
        '''Создаём словарь {читаемое_имя:имя_данных}"'''

        data: dict[str, FieldInfo] = self.worker.model_fields
        self._actions: dict = {}
        for d in data:
            inf: PhonebookManagerFunctions = getattr(self.worker, d)
            self._actions.setdefault(inf.action_name, d)

    def is_yes(self, text: str | None = None) -> bool:
        """Спрашиваем да/нет"""

        answer: str = input(f"{text} [да/нет]:").lower()
        if answer == "да":
            return True
        elif answer == "нет":
            return False
        elif answer == "Home":
            return self.get_start()
        else:
            print(f'\n {answer}<- Будем считать как "нет"')
            return False

    def print_mamager_err_list(self):
        """Печаитаем ошибку записанную в менеджере"""
        if self.manager.err:
            for e in self.manager.err:
                print(f"\t-> {e}")
        else:
            print("Логи пусты.")
        return self.get_start()

    def print_data(self) -> None:
        """
        Печатаем данные менеджера на экран.
        """

        if not self.is_manager_fields():
            return self.get_start()
        if not self.manager.print_data():
            self.manager.add_log("Невозможно распечатать данные.")
        return self.get_start()

    def input_data(self):
        """Читаем данные с клавиатуры."""

        print(
            "Памятка:\n\t1) Имена начинаются с заглавной и пишутся на одном языке Русском или Фнглийском.\
            \n\t2) Название организации в дополнение к п.1 может заканчиваться на цифру.\
            \n\t3)Сотовый телефон начинается на +7 и имеет формат +7 000 000 00 00, может разделяться,\
            \n\t как пробелами или знаком '-', так и не иметь разделителей вообще\
            \n\t4)рабочий телефон состоит из 4 цифр и может разделяться пробелои или знаком '-'\n"
        )
        name_fields: dict = self.manager.get_keys_names
        data: list[dict[str, str]] = []
        choice = True
        while choice:
            person: dict[str, str] = {}
            for field, name in name_fields.items():
                person.setdefault(field, input(f"Введите значение {name}:"))
            data.append(person)
            choice = self.is_yes(text="Создать ещё запись.")
        if not self.manager.set_manager_input_list(data):
            print("Некоторрые данные содержат ошибку и не были записаны.")
        self.manager.heal_manager_data()
        return self.get_start()

    def end_it(self):
        """Так мы выйдем."""
        print("See you soon")

    def delete_data(self):
        """Удалить или отфильтровать иудалить  объекты менеджера из базы"""

        if not self.is_manager_fields():
            return self.get_start()
        if not self.is_yes("Удалим все данные[да], или отфильтруем[нет]?"):
            search = True
            while search:
                wishes: dict[str, str] = self.get_user_find_wishes()
                if not self.manager.find_in_file(wishes):
                    print("Ничего не нашли.")
                    return self.get_start()
                if len(self.manager.manager_fields) > 1:
                    search = self.is_yes("Фильтруем ещё раз?")
                else:
                    search = False

        if not self.is_yes("Подтвердите удаление данных!"):
            return self.get_start()

        if self.manager.del_manager_data():
            print("\nДанные удалены\n")
        else:
            print("Не получилось удалить все данные, отчет в логах.")
        return self.get_start()

    def get_filds_choice(self, fields_list: str) -> set:
        """Спрашиваем в каких полях искать"""

        p: str = ", ".join(fields_list)
        choice: str = input(f"Список полей: {p}\n Укажите через пробел выбраные имена:")
        return self.manager.get_is_fields_list(choice)

    def get_data_to_find(
        self, fields_set: set, fields_data: dict[str, str]
    ) -> dict[str, str]:
        """Спрашиваем что искать в поле."""

        wishes: dict = {}
        for field, name in fields_data.items():
            if field in fields_set:
                q: str = input(
                    f"Enter для поиска не введённого значения.\nЧто ищем в поле {name}: "
                )
                if q:
                    wishes.setdefault(field, q)
                else:
                    wishes.setdefault(field, "Not entered")
        return wishes

    def get_user_find_wishes(self) -> dict[str, str]:
        """Создаём словарь поиска для БД {'название_поля':'что_ищем'}"""

        field_list: dict[str, str] = self.manager.get_keys_names
        fields: set = self.get_filds_choice(field_list.values())
        if not fields:
            print("Правильных полей нет.")
            return self.get_start()

        wishes: dict[str, str] = self.get_data_to_find(fields, field_list)
        if not wishes:
            print("Нечего искать.")
            return self.get_start()
        return wishes

    def is_manager_fields(self) -> bool:
        """
        Если менеджер пуст заполнить его или вернуться.
        Заполнен  True.
        Файл пуст False.
        """
        if not self.manager.manager_fields:
            self.manager.get_data_from_file()
            if self.manager.manager_fields:
                self.manager.add_log("Читаем файл.")
                return True
            else:
                print("Файл пуст.")
                return False
        return True

    def find_data(self):
        """Поеск в данных менеджера."""

        if not self.is_manager_fields():
            return self.get_start()
        wishes: dict[str, str] = self.get_user_find_wishes()
        if not self.manager.find_in_file(wishes):
            print("Ничего не нашли.")
        else:
            print("Совпадения:\n")
            self.manager.print_data()
        return self.get_start()

    def get_new_line(self, field: PhonebookField) -> PhonebookField:
        """Изменяем запись в менеджере"""

        new_data = {}
        for k, v in self.manager.get_keys_names.items():
            field_atr = getattr(field, k)
            if m := input(
                f"Enter чтобы пропустить.\nПоле {v} содержит значение: {field_atr}, новое значение {v}:"
            ):
                new_data.setdefault(k, m)
            elif field_atr == "Not entered":
                new_data.setdefault(k, m)
            else:
                new_data.setdefault(k, field_atr)
        return self.manager.get_obj_fom_dict(new_data)

    def update_data(self):
        """Изменяем данные в менеджере"""

        if not self.is_manager_fields():
            return self.get_start()
        if not self.is_yes("Меняем все данные[да], или отфильтруем[нет]?"):
            wishes: dict[str, str] = self.get_user_find_wishes()
            if not self.manager.find_in_file(wishes):
                print("Ничего не нашли.")
                return self.get_start()

        new_fields: list[PhonebookField] = []
        for field in self.manager.manager_fields:
            self.manager.print_obj(field)
            if self.is_yes("Изменяем?"):
                if new_line := self.get_new_line(field):
                    new_line.modified = True
                    new_fields.append(new_line)
                else:
                    self.manager.add_log("Неудалось изменить поле.")
                    new_fields.append(field)
            else:
                new_fields.append(field)
        self.manager.set_new_manager_fields(new_fields)
        self.manager.put_data()
        return self.get_start()

    def check(self):
        """Проверяем наличие файла и его объём"""

        p: bool = self.manager.ping()
        if p:
            print(f"Отчет: {self.manager.err[-1]}")
        else:
            print(f"Ошибка: {self.manager.err[-1]}")
        return self.get_start()

    def heal_data(self) -> Any:
        """Удаляем дубликаты из БД"""

        print("Удаляем дубликаты из БД.")
        self.manager.get_data_from_file()
        if not self.manager.heal_manager_data():
            print("Возникла ошибка.")
        return self.get_start()

    def clean_logs(self) -> Any:
        """Чистим логи менеджера."""

        self.manager.err.clear()
        print("Очистка логов.")
        return self.get_start()

    def run_action(self, obj: str) -> Any:
        """По названию события ищем его и в случае успеха запускаем."""

        if obj in self._actions:
            act: PhonebookManagerFunctions = getattr(self.worker, self._actions[obj])
            return act.function()
        e = "Ошибка Ввода"
        self.manager.add_log(e)
        print(e)
        return self.get_start()

    def commands(self):
        """Печатаем список команд."""
        print(f"\nСписок комманд:\n|{'-'*21}|{'-'*39}|\n{self.get_methods()}")
        return self.get_start()

    def get_methods(self) -> LiteralString:
        """Создаем форму функционала"""

        s: list = [f'| {"Команда: ":<20}| {"Описание:":<38}|\n|{"-"*21}|{"-"*39}|']
        for v in self._actions.values():
            el: PhonebookManagerFunctions = getattr(self.worker, v)
            s.append(f"| {el.action_name:<20}| {el.description:<38}|")
        s.append(f'|{"-"*21}|{"-"*39}|')
        return "\n".join(s)

    def get_start(self) -> Any:
        """Точка входа в наш рабочий процесс. Тут мы выбираем действие."""

        while True:
            move = input("Выбор команды: ")
            move = move.capitalize()
            if move in self._actions:
                return self.run_action(move)

    def wellcome(self):
        """Приветственная функция входа, служит для разового предоставления информации."""

        print(__doc__)
        self.commands()
