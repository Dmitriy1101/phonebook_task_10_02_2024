from core.phonebook_manager import PhonebookManager


def main() -> None:
    worker = PhonebookManager()
    worker.wellcome()


if __name__ == "__main__":
    main()
