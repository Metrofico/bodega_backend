from datetime import datetime


class Date:

    @staticmethod
    def get_date():
        return datetime.now().strftime("%d/%m/%Y")
        pass

    @staticmethod
    def get_full_date():
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        pass
