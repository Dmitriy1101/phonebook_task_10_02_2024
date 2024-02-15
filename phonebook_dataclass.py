"""
Скоро!
"""
import datetime
from typing import Callable
from uuid import uuid4
from typing_extensions import Annotated
from pydantic import BaseModel, StringConstraints, Field
from pydantic.dataclasses import dataclass

NAMES_PATTERN = r"(^[А-Я][а-яё]*$)|(^[A-Z][a-z]*$)"
ORGANIZATION_PATTERN = r"(^[А-Я][а-яё]*[0-9]*$)|(^[A-Z][a-z]*[0-9]*$)"
WORK_PHONE_PATTERN = r"(^\d{2}[ -]?\d{2}$)"
PERSONAL_PHONE_PATTERN = r"(^[+][7]([ -]?\d{3}){2}([ -]?\d{2}){2}$)"
DATE_PATTERN = r"(^0[1-9]|^[1-2][0-9]|^3[0-1])\.(0[1-9]|1[1-2])\.(20\d\d$)"


@dataclass(unsafe_hash=True)
class PhonebookField:
    """Класс набора данных в еденичной записи(строки) из БД"""

    id: str = Field(
        default_factory=lambda: uuid4().hex,
        repr=False,
        serialization_alias="Идентификатор",
        title="Идентификатор",
        frozen=True,
    )
    name: Annotated[
        str,
        StringConstraints(
            min_length=2,
            max_length=20,
            pattern=NAMES_PATTERN,
        ),
    ] = Field(
        default="Not entered",
        repr=True,
        serialization_alias="Имя",
        title="Имя",
    )
    surname: Annotated[
        str,
        StringConstraints(
            min_length=2,
            max_length=20,
            pattern=NAMES_PATTERN,
        ),
    ] = Field(
        default="Not entered",
        repr=True,
        serialization_alias="Фамилия",
        title="Фамилия",
    )
    patrionymic: Annotated[
        str,
        StringConstraints(
            min_length=2,
            max_length=20,
            pattern=NAMES_PATTERN,
        ),
    ] = Field(
        default="Not entered",
        repr=True,
        serialization_alias="Отчество",
        title="Отчество",
    )
    organization: Annotated[
        str,
        StringConstraints(
            min_length=4,
            max_length=20,
            pattern=ORGANIZATION_PATTERN,
        ),
    ] = Field(
        default="Not entered",
        repr=True,
        serialization_alias="Организация",
        title="Организация",
    )
    work_phone: Annotated[
        str,
        StringConstraints(
            min_length=4,
            max_length=5,
            strip_whitespace=True,
            pattern=WORK_PHONE_PATTERN,
        ),
    ] = Field(
        default="Not entered",
        repr=True,
        serialization_alias="Рабочий_телефон",
        title="Рабочий_телефон",
    )
    personal_phone: Annotated[
        str,
        StringConstraints(
            min_length=12,
            max_length=16,
            strip_whitespace=True,
            pattern=PERSONAL_PHONE_PATTERN,
        ),
    ] = Field(
        default="Not entered",
        repr=True,
        serialization_alias="Личный_телефон",
        title="Личный_телефон",
    )
    recording_date: Annotated[
        str,
        StringConstraints(
            min_length=10,
            max_length=10,
            pattern=DATE_PATTERN,
        ),
    ] = Field(
        default_factory=lambda: datetime.datetime.now().strftime("%d.%m.%Y"),
        repr=False,
        serialization_alias="Дата_записи",
        title="Дата_записи",
        frozen=True,
    )
    modified: bool = Field(
        default=False,
        repr=False,
        serialization_alias="Изменялся",
        title="Изменялся",
    )

    def __eq__(self, __value: object) -> bool:
        if (
            self.name == __value.name
            and self.surname == __value.surname
            and self.patrionymic == __value.patrionymic
            and self.personal_phone == __value.personal_phone
            and self.work_phone == __value.work_phone
        ):
            return True
        return False


class Phonebook(BaseModel):
    """Класс хранящий список записей(строк) из БД"""

    fields: list[PhonebookField] = []


@dataclass
class PhonebookManagerFunctions:
    """Класс для описания функций менеджера."""

    action_name: str
    description: str
    function: Callable


class PhonebookManagerActions(BaseModel):
    """Действия менеджера сопоставленные с описаниемю"""

    find: PhonebookManagerFunctions
    update: PhonebookManagerFunctions
    print: PhonebookManagerFunctions
    add: PhonebookManagerFunctions
    inp: PhonebookManagerFunctions
    rem: PhonebookManagerFunctions
    exit: PhonebookManagerFunctions
    logs: PhonebookManagerFunctions
    clean_logs: PhonebookManagerFunctions
    check: PhonebookManagerFunctions
    commands: PhonebookManagerFunctions
