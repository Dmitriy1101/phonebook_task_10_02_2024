from unittest import TestCase
from pathlib import Path
from core.phonebook_dataclass import (
    Phonebook,
    PhonebookField,
)
from core.phonebook_core import PhonebookCore
from core.phonebook_manager import PhonebookManager


PBF = PhonebookField
PB = Phonebook
CORE = PhonebookCore
MANAGER = PhonebookManager
TEST_FILE = str(Path(Path(__file__).resolve().parent, "test.txt"))
print(TEST_FILE)
TEST_DATA: dict[str, str] = {
    "name": "Иван",
    "surname": "Рюриковичь",
    "patrionymic": "Васильевичь",
    "organization": "Москва",
    "work_phone": "11-11",
    "personal_phone": "+7 999 999 99 99",
}


class TestPhonebookCore(TestCase):
    """Тест обработчика БД"""

    def test_init(self):
        """
        Тестируем инициализацию объекта.
        """
        obj = CORE
        self.assertIsNotNone(obj(TEST_FILE))
        self.assertRaises(NameError, lambda: obj(".txt"))
        self.assertRaises(NameError, lambda: obj(".json"))
        self.assertRaises(NameError, lambda: obj(".t"))

    def test_ping(self):
        """Тест запроса на состояние файла."""
        obj = CORE(TEST_FILE)
        self.assertTrue(obj.ping())

    def test_inp_data_work(self):
        """
        Тестируем связанные функции оюработки данных:
        1) get_obj_fom_dict,
        2) set_manager_input_list
        """
        obj = CORE(TEST_FILE)
        data: dict[str, str] = TEST_DATA

        self.assertIsInstance(obj.get_obj_fom_dict(data.copy()), PBF)
        self.assertFalse(obj.set_manager_input_list([]))
        self.assertTrue(
            obj.set_manager_input_list(
                [
                    data.copy(),
                ]
            )
        )

    def test_text_work(self):
        """
        Тестируем функции обрабртки текста:
        1) get_is_fields_list
        """
        obj = CORE(TEST_FILE)
        test_list: list[str] = ["Имя", "Фамилия", " Имя Фамилия Жопа"]
        for d in test_list:
            self.assertNotEqual(len(obj.get_is_fields_list(d)), 0)
        invalid_test_list: list[str] = ["апв", "рпар", "fgh fgh"]
        for d in invalid_test_list:
            self.assertEqual(len(obj.get_is_fields_list(d)), 0)

    def test_file_work(self):
        """
        Тестируем работу с файлом:
        1)set_manager_input_list
        2)get_line_from_field
        3)get_data_from_file
        4)heal_manager_data

        """
        obj = CORE(TEST_FILE)
        data: dict[str, str] = TEST_DATA
        self.assertTrue(
            obj.set_manager_input_list(
                [
                    data.copy(),
                ]
            )
        )
        self.assertTrue(obj.put_data())
        field = obj.manager.fields[0]
        self.assertIsInstance(obj.get_line_from_field(field), str)
        self.assertTrue(obj.get_data_from_file())
        self.assertTrue(obj.heal_manager_data())


    def test_print(self):
        """Тестируем печать."""

        obj = CORE(TEST_FILE)
        self.assertTrue(obj.get_data_from_file())
        self.assertTrue(obj.print_data())

    def test_delete_data(self):
        """Тестируем удаление данных."""
        obj = CORE(TEST_FILE)
        data: dict[str, str] = TEST_DATA
        self.assertTrue(
            obj.set_manager_input_list(
                [
                    data.copy(),
                ]
            )
        )
        self.assertIsInstance(obj.get_obj_fom_dict(data), PBF)
        self.assertTrue(obj.put_data())
        self.assertTrue(obj.get_data_from_file())
        self.assertTrue(obj.manager.fields[0]==obj.get_obj_fom_dict(data.copy()))
        self.assertTrue(obj.del_manager_data())
