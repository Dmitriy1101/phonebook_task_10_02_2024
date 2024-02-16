"""
Это модуль управления БД отделённый от логики связанной 
пользователем, предназначеный для использования отдельно.
Термин менеджер означает сущность отвечающую за работу с файлом
и является объектом хранящим данные файла.
"""
import datetime
import os
import re
from pathlib import Path

from core.phonebook_dataclass import PhonebookField, Phonebook


class PhonebookCore:
    """
    БД телефонная книга:
    этот модуль отвечает за работу с файлом,
    операции с данными происходят в менеджере отдельно от файла.
    """

    err: list = []
    __invalid_str: list[str] = ["\n", "Not entered"]

    def __init__(self, file_name_path: str) -> None:
        """
        При инициализации надо передать путь с именем файла.txt
        где мы храним|будем_хранить данные.
        """
        self.manager = Phonebook()
        self.set_keys_names()
        if not self.set_path_file(file_name_path):
            raise ValueError(
                "Невозможно создать файл с таким именем по данному пути,\nубедитесь что путь существует"
            )

    def is_txt_file_name(self, file_name: str) -> bool:
        """Вернёт True если это имя txt файла, или выбросит ошибку"""

        if not file_name[-4:] == ".txt" or len(file_name) < 5:
            raise NameError(f"{file_name} <- Не имя txt файла")
        return True

    @property
    def get_keys_names(self) -> dict:
        """
        Словарь необходимый для сопоставления видимых полей и их читабельных версий.
        {'имя_поля_в_БД':'читаемое_пользователем_обозначение'}
        """
        return self._keys_names

    @property
    def manager_fields(self) -> list[PhonebookField]:
        """Вернём поля менеджера."""
        return self.manager.fields

    @property
    def get_fields(self) -> list:
        """Список имен полей включая скрытые"""
        return self._fields

    def set_keys_names(self) -> None:
        """
        Создаем словарь видимых полей состоящий из,
        сопоставленных имен_полей и их читабельных версий.
        {'name':'имя'}
        Также создаем список всех полей включая скрытые.
        ['id', 'name', ...]
        """
        keys_names: dict = {}
        fields_list: list = []
        for k, v in PhonebookField.__dataclass_fields__.items():
            if v.default.repr:
                keys_names.setdefault(k, v.default.title)
            fields_list.append(k)
        self._keys_names: dict = keys_names
        self._fields: list = fields_list

    def is_fields_name(self, names: list[str]) -> bool:
        """
        Проверяем имена в списке на соответствие читабельным_именам_полей,
        если все совпали то вернем True.
        """

        for name in names:
            if name not in self.get_keys_names.values():
                return False
        return True

    @property
    def get_path(self) -> Path:
        return self.file_name

    def add_log(self, text: str) -> None:
        """Добавление записи в лог."""

        self.err.append(text)

    def set_path_file(self, path_to_file: str) -> bool:
        """Путь к рабочему файлу"""

        self.is_txt_file_name(file_name=path_to_file)
        path: Path = Path(__file__).resolve().parent
        self.file_name: Path = Path(path, path_to_file)
        return self.ping()

    def ping(self) -> bool:
        """Проверка файла на существование и если не существует создаём"""

        is_file: bool = os.path.isfile(self.file_name)
        if is_file:
            with open(self.file_name, encoding="utf-8") as f:
                l: int = sum(1 for line in f)
            b = os.stat(self.file_name)
            self._id = l
            inf = f"Файл {self.file_name} существует, имеет {l} строк, занимает {b.st_size} байт.\n"
            self.add_log(inf)
        else:
            try:
                with open(self.file_name, "w+", encoding="utf-8") as f:
                    self._id = 0
                self.add_log(f"\nФайл {self.file_name} не обнаружен и был создан.")
            except OSError as e:
                self.add_log(f"\nФайл не был создан ошибка: {e}")
                return False
        return True

    def del_invalid_from_line(self, line: str) -> str:
        """Удаляем лишние символы из строки."""
        for item in self.__invalid_str:
            line = line.replace(item, "")
        return line

    def get_field_from_line(self, line: str) -> PhonebookField:
        """Преобразуем строку прочитаную из файла в объект PhonebookField."""

        line = self.del_invalid_from_line(line)
        line_list: list = line.split("|")
        try:
            line_dick: dict[str, str] = dict(zip(self.get_fields, line_list))
        except ValueError:
            self.add_log("Ошибка чтения из файла.")
            return False
        return self.get_obj_fom_dict(line_dick)

    def get_line_from_field(self, obj: PhonebookField) -> str:
        """Преобразует значения PhonebookField в строку, пригодную для записи в файл"""

        obj_list: list = [str(getattr(obj, item)) for item in self.get_fields]
        line: str = "|".join(obj_list)
        return f"{line}\n"

    @property
    def clear_manager(self) -> None:
        """Чистем поля Менеджера"""
        self.manager.fields.clear()

    def get_data_from_file(self) -> bool:
        """
        Извлекаем данные из файла.
        Заполняем список менеджера объектами данных.
        В случае успеха True
        """

        self.clear_manager
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                for l in f:
                    person: PhonebookField = self.get_field_from_line(l)
                    self.manager.fields.append(person)
                self.add_log("Менеджер обновлён.")
        except IOError as e:
            self.add_log(e)
            return False
        except Exception as e:
            self.add_log(e)
            return False
        return True

    def print_obj(self, obj: PhonebookField) -> None:
        """Печатаем одну строку данных на экран"""

        print(
            ",".join(
                [
                    f" {name} : {getattr(obj,field)}"
                    for field, name in self.get_keys_names.items()
                ]
            )
        )

    def print_data(self) -> bool:
        """
        Печатаем данные менеджера на экран.
        """

        if self.manager.fields:
            for data in self.manager.fields:
                self.print_obj(data)
            return True
        else:
            self.add_log("Печатать нечего.")
            return False

    def put_data(self, rem: bool = False) -> bool:
        """
        Это основной метод записи данных менеджера в БД!
        Используй heal_manager_data для обновления БД!
        Параметр rem является дополнительной подстраховкой,
        что бы при пустом менеджере не удалить данные файла.
        Эаппись данных менеджера в файл.
        Вернет True в случае успеха.
        """

        data: list[PhonebookField] = self.manager.fields
        if data or rem:
            try:
                with open(self.file_name, "w", encoding="utf-8") as f:
                    for obj in data:
                        f.write(self.get_line_from_field(obj))
            except IOError as e:
                self.add_log(e)
                return False
            self.get_data_from_file()
            return True
        else:
            self.add_log("Попытка пустой записи.")
            return False

    @property
    def is_not_date(self) -> bool:
        """Проверяем наличие данных в менеджере."""
        if self.manager.fields:
            return True
        return False

    def get_vilid_inp_dict(self, data: dict[str, str]) -> dict[str, str]:
        """Удаляем ключи с пустыми знапчениями"""

        return dict(filter(lambda x: x[1], data.items()))

    def get_obj_fom_dict(self, data: dict[str, str]) -> PhonebookField:
        """
        Получаем данные  для одной строки в нашей БД,
        валидируем и приобразуем в полноценную сущность пригодную к записи в БД.
        Вернет поле пригодныое к записи.
        """

        person: dict[str, str] = self.get_vilid_inp_dict(data)
        if not person:
            self.add_log("Введены пустые данные.")
            return False
        try:
            field = PhonebookField(**person)
            return field
        except Exception as e:
            self.add_log(e)
            return False

    def set_manager_input_list(self, inp_list: list[dict[str, str]]) -> bool:
        """
        Получаем список даныых считанных с клавиатуры,
        преобразуем в набор валидных данных,
        готовых к записи в БД.
        Передаем их в менеджер,
        возвращаем True при успехе,
        ошибки вернут False.
        """

        if not inp_list:
            self.add_log("Ввод пустого списка")
            return False
        self.clear_manager
        broken_data: list[dict[str, str]] = []
        for inp_person in inp_list:
            if person := self.get_obj_fom_dict(inp_person):
                if person not in self.manager.fields:
                    self.manager.fields.append(person)
            else:
                self.add_log(f"Некорректные данные:{inp_person}")
                broken_data.append(inp_person)
        if broken_data:
            return False
        return True

    def get_is_fields_list(self, choice: str) -> set:
        """
        На вход получаем строку с введенными через пробел полями,
        в которых необходимо произвести поиск.
        Создаем список полей и валидируем его для дальнейшего поиска
        """

        fields_set: set[str] = set()
        second: list[str] = re.split(" ", choice)
        second = [item.capitalize() for item in second]
        for field, name in self.get_keys_names.items():
            if name in second:
                fields_set.add(field)
                second.remove(name)
        if len(second) != 0:
            self.add_log(f"Некорректные поля Исключены: {second}")
        return fields_set

    def find_in_file(self, data_to_find: dict[str, str]) -> bool:
        """
        Поиск в данных, извлеченных из файла.
        На вход получаем словарь {'имя_поля':'что_ищем'},
        что нашли запишим в менеджер.
        При успехе поиска вернем True.
        """

        if not self.manager.fields:
            self.get_data_from_file()
        data: list[PhonebookField] = self.manager.fields
        correct_data = Phonebook()
        for obj in data:
            if self.find_in_field_data(field_data=obj, data_to_find=data_to_find):
                correct_data.fields.append(obj)

        if correct_data.fields:
            self.manager.fields = correct_data.fields
            return True
        return False

    def find_in_field_data(
        self, field_data: PhonebookField, data_to_find: dict[str, str]
    ) -> bool:
        """
        Принимаем запись из БД и словарь {валидные_поля_поиска:что_ищем}
        Tсли найдем хотябы одно совпадение вернём True, иначе False.
        """

        for field_name, data_find in data_to_find.items():
            field_value: str = getattr(field_data, field_name)
            if field_value.find(data_find) != -1:
                return True
        return False

    def del_manager_data(self) -> bool:
        """
        Удаляем объекты менеджера из БД, вернем при успехе True.
        """

        if not self.manager.fields:
            self.err.append("Менеджер пуст.")
            return False
        oper_data: list[PhonebookField] = self.manager.fields.copy()
        self.get_data_from_file()
        while oper_data:
            field: PhonebookField = oper_data.pop(0)
            if self.del_manager_field(field):
                self.add_log(f"Объект удалён: {field}")
        return self.put_data(rem=True)

    def del_manager_field(self, field: PhonebookField) -> bool:
        """
        Удаляем объект из менеджера, при успехе True.
        """

        try:
            self.manager.fields.remove(field)
            return True
        except ValueError as e:
            self.add_log(f"Невозможно удалить элемент {field} не найден, ошибка: {e}")
            return False

    def heal_manager_data(self) -> bool:
        """
        Основной метод дозаписи данных менеджера в БД!
        Записываем изменения данных в БД.
        При записи происходит проверка данных и удаление лишних данных.
        Вернём True при успехе.
        """

        if not self.manager.fields:
            self.add_log("Невозможно обработатка пустого Файла")
            return True
        update_data: list[PhonebookField] = self.manager.fields.copy()
        self.get_data_from_file()
        for field in update_data:
            self.manager.fields.append(field)
        self.group_manager_data()
        return self.put_data()

    def group_manager_data(self) -> bool:
        """Удаляем дубликаты из менеджера."""

        try:
            new_fields: list[PhonebookField] = []
            for field in self.manager.fields:
                if not new_fields:
                    new_fields.append(field)
                    continue
                new_fields = self.chek_list_field(new_fields, field)

            self.set_new_manager_fields(new_fields)
            return True
        except Exception as e:
            self.add_log(e)
            return False

    def chek_list_field(
        self, data: list[PhonebookField], field: PhonebookField
    ) -> list[PhonebookField]:
        """
        Ищем и оцениваем в список полей на соответствие полю:
        При оценке применяются элементы поля как id и дата создания,
        которые не учавствуют в сравнении полей.
        Если они равны или элемент в списке имеет приоритет то замены не будет,
        Если поле не в списке имеет отметку об изменении или позднею дату создания
        то заменем.
        Вернём обновлённый список.
        """

        index: int = -1
        for d in data:
            if d.id == field.id and d == field:
                return data
            elif d.id == field.id and d != field or d.id != field.id and d == field:
                if bool(d.modified) != bool(field.modified):
                    if bool(d.modified):
                        break
                    else:
                        index = data.index(d)
                        break
                else:
                    if self.get_date(d.recording_date) > self.get_date(
                        field.recording_date
                    ):
                        break
                    else:
                        index = data.index(d)
                        break
        if index != -1:
            data.insert(index, data)
        else:
            data.append(field)
        return data

    def set_new_manager_fields(self, fields_list: list[PhonebookField]) -> None:
        """Заменяем данные в менеджере полученными."""
        self.manager.fields = fields_list

    def get_date(self, date: str) -> datetime:
        """Дата из строки для сравнения."""
        try:
            return datetime.datetime.strptime(date, "%d.%m.%Y")
        except Exception as e:
            self.add_log(f"Jшибка работы с датой: {date} ->{e}")
            return False
