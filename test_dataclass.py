import random
import string
import datetime
from unittest import TestCase
from pydantic import ValidationError
from phonebook_dataclass import (
    Phonebook,
    PhonebookField,
)


PBF = PhonebookField
PHONEBOOK = Phonebook


def get_random_name(s: str, lenght: int = 1) -> str:
    """Набор строчных символов длинны len"""
    return "".join(random.choices(s, k=lenght))


class TestPhonebookField(TestCase):
    def test_name_positive(self):
        """Позитивный тест поля имя"""

        positive_data: list[str] = [
            get_random_name(
                string.ascii_lowercase, random.randrange(2, 10)
            ).capitalize()
            for i in range(20)
        ]

        obj = PBF
        for data in positive_data:
            self.assertIsInstance(obj(name=data), PBF)

    def test_name_negative(self):
        """Негативный тест поля имя"""

        negative_data: list[str] = ["И", "N", "6666, '+"]
        for i in range(5):
            negative_data.append(get_random_name(string.printable, lenght=10))
            negative_data.append("f" + get_random_name(string.ascii_letters, lenght=10))

        obj = PBF
        for data in negative_data:
            self.assertRaises(ValidationError, lambda: obj(name=data))

    def test_surname_positive(self):
        """Позитивный тест поля фамилия"""

        positive_data: list[str] = [
            get_random_name(
                string.ascii_lowercase, random.randrange(2, 10)
            ).capitalize()
            for i in range(20)
        ]

        obj = PBF
        for d in positive_data:
            self.assertIsInstance(obj(surname=d), PBF)

    def test_surname_negative(self):
        """Негативный тест поля фамилия"""

        negative_data: list[str] = ["И", "N", "6, '+", "h"]
        for i in range(5):
            negative_data.append(get_random_name(string.printable, lenght=10))
            negative_data.append(get_random_name(string.ascii_letters, lenght=10))

        obj = PBF
        for data in negative_data:
            self.assertRaises(ValidationError, lambda: obj(surname=data))

    def test_patrionymic_positive(self):
        """Позитивный тест поля отчечтво"""

        positive_data: list[str] = [
            get_random_name(
                string.ascii_lowercase, random.randrange(2, 10)
            ).capitalize()
            for i in range(20)
        ]

        obj = PBF
        for d in positive_data:
            self.assertIsInstance(obj(patrionymic=d), PBF)

    def test_patrionymic_negative(self):
        """Негативный тест поля отчечтво"""

        negative_data: list[str] = ["И", "N", "6, '+", "h"]
        for i in range(5):
            negative_data.append(get_random_name(string.printable, lenght=10))
            negative_data.append(get_random_name(string.ascii_letters, lenght=10))

        obj = PBF
        for d in negative_data:
            self.assertRaises(ValidationError, lambda: obj(patrionymic=d))

    def test_organization_positive(self):
        """Позитивный тест поля Организация"""

        positive_data: list[str] = []
        for i in range(5):
            positive_data.append(
                get_random_name(
                    string.ascii_lowercase, random.randrange(4, 10)
                ).capitalize()
            )
            positive_data.append(
                get_random_name(
                    string.ascii_lowercase, random.randrange(4, 10)
                ).capitalize()
                + str(random.randrange(2 + i, 10 + i))
            )

        obj = PBF
        for data in positive_data:
            self.assertIsInstance(obj(organization=data), PBF)

    def test_organization_negative(self):
        """Негативный тест поля Организация"""

        negative_data: list[str] = ["И", "N", "6, '+", "h"]
        for i in range(5):
            negative_data.append(get_random_name(string.printable, lenght=10))
            negative_data.append(get_random_name(string.ascii_letters, lenght=10))

        obj = PBF
        for d in negative_data:
            self.assertRaises(ValidationError, lambda: obj(organization=d))

    def test_work_phone_positive(self):
        """Позитивный тест поля Рабочий_телефон"""

        positive_data: list[str] = ["4444", "0000", "9999", "44-44", "55-55"]

        obj = PBF
        for data in positive_data:
            self.assertIsInstance(obj(work_phone=data), PBF)

    def test_work_phone_negative(self):
        """Негативный тест поля Рабочий_телефон"""

        negative_data: list[str] = ["И", 00.00, "6", 2222, "33+33", "h", "222", "22222"]
        for i in range(5):
            negative_data.append(
                get_random_name(string.printable + string.digits, lenght=10)
            )
            negative_data.append(get_random_name(string.ascii_letters, lenght=10))
            negative_data.append(
                get_random_name(string.digits, lenght=random.randrange(5, 10))
            )

        obj = PBF
        for data in negative_data:
            self.assertRaises(ValidationError, lambda: obj(work_phone=data))

    def test_personal_phone_positive(self):
        """Позитивный тест поля Личный_телефон"""

        positive_data: list[str] = [
            "+71112223344",
            "+7 000 000 00 00",
            "+7-999-999-99-99",
        ]

        obj = PBF
        for data in positive_data:
            self.assertIsInstance(obj(personal_phone=data), PBF)

    def test_personal_phone_negative(self):
        """Негативный тест поля Личный_телефон"""

        negative_data: list[str] = ["И", 00.00, "6", 2222, "33+33", "h", "222", "22222"]
        not_plus: list[str] = list(string.punctuation)
        not_plus.remove("+")
        not_seven: list[str] = list(string.digits)
        not_seven.remove("7")

        for i in range(5):
            perf = random.choice(not_plus) + random.choice(not_seven)
            negative_data.append(get_random_name(string.printable, lenght=12))
            negative_data.append(get_random_name(string.ascii_letters, lenght=12))
            negative_data.append(perf + get_random_name(string.digits, lenght=12))

        plus_seven: list[str] = ["+7", "000", "000", "00", "00"]

        punct_data = list(string.punctuation)
        punct_data.remove("-")
        negative_data = negative_data + [perf.join(plus_seven) for perf in punct_data]

        obj = PBF
        for data in negative_data:
            self.assertRaises(ValidationError, lambda: obj(personal_phone=data))

    def test_recording_date_positive(self):
        """Позитивный тест поля Дата_записи"""
        positive_data: list[str] = [
            datetime.datetime.now().strftime("%d.%m.%Y") for i in range(7)
        ]
        obj = PBF
        for d in positive_data:
            self.assertIsInstance(obj(recording_date=d), PBF)
        self.assertIsInstance(obj(), PBF)

    def test_recording_date_negative(self):
        """Негативный тест поля Дата_записи"""

        negative_data: list[str] = [
            datetime.datetime.now(),
            datetime.datetime.now().strftime("%d-%m-%Y"),
        ]

        obj = PBF
        for data in negative_data:
            self.assertRaises(ValidationError, lambda: obj(recording_date=data))

    def test_modified_field_positive(self):
        """Позитивный тест поля Изменялся"""
        obj = PBF
        d: PBF = obj()
        self.assertIsInstance(d, PBF)
        self.assertIsInstance(obj(modified="False"), PBF)
        self.assertFalse(d.modified)
        d.modified = True
        self.assertTrue(d.modified)
        setattr(d, "modified", False)
        self.assertFalse(d.modified)

    def test_modified_field_negative(self):
        """Негативный тест поля Изменялся"""

        obj = PBF
        self.assertRaises(ValidationError, lambda: obj(modified="ok"))
        self.assertRaises(ValidationError, lambda: obj(modified="3"))


class TestPhonebook(TestCase):
    """Тест Модели БД"""

    def test_all(self):
        obj: PHONEBOOK = PHONEBOOK
        obj_field: PBF = PBF
        self.assertIsInstance(obj(), PHONEBOOK)
        self.assertIsInstance(obj_field(), PBF)
        data: PHONEBOOK = obj()
        field: PBF = obj_field()
        data.fields.append(field)
        self.assertEqual(field, data.fields[0])
        data.fields.remove(field)
        self.assertEqual(0, len(data.fields))
