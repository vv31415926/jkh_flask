

class Save2BD:
    def __init__(self, db, table_name):
        self.__db = db
        self.__cur = db.cursor()
        self.table_name = table_name