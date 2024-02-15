from unittest import TestCase
from phonebook_dataclass import (
    Phonebook,
    PhonebookField,
)
from phonebook_core import PhonebookCore
from phonebook_manager import PhonebookManager


PBF = PhonebookField
PB = Phonebook
CORE = PhonebookCore
MANAGER = PhonebookManager
TEST_FILE = "test.txt"
TEST_DATA: dict[str, str] = {
    "Имя": "Аапоао",
    "Фамилия": "Ирпорпо",
    "Отчество": "Арорпо",
    "Организация": "Прапо5",
    "Рабочий_телефон": "3333",
    "Личный_телефон": "+73332221111",
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
        obj = CORE(TEST_FILE)
        self.assertTrue(obj.ping())

    def test_inp_data_work(self):
        """
        Тестируем связанные функции оюработки данных:
        1) get_obj_fom_dict,
        2) set_manager_input_list
        """
        obj = CORE(TEST_FILE)
        self.assertTrue(obj.ping())
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
        1)get_field_index
        2)change_equal_field_or_add
        3)
        """
        obj = CORE(TEST_FILE)
        self.assertTrue(obj.ping())
        data: dict[str, str] = TEST_DATA
        self.assertTrue(
            obj.set_manager_input_list(
                [
                    data.copy(),
                ]
            )
        )
        obj.set_manager_input_list(
            [
                data.copy(),
            ]
        )
        field = obj.manager.fields[0]
        self.assertIsInstance(obj.get_line_from_field(field), str)
        self.assertTrue(obj.get_data_from_file())
        self.assertTrue(obj.heal_manager_data())
