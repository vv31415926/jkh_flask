import sqlite3 as sq

class FDataBase:
    def __init__(self, db, table_name):
        self.__db = db
        self.__cur = db.cursor()
        self.table_name = table_name

    def getListAddress(self):
        sql = f'''SELECT * FROM address'''
        try:
            #print(f'{sql=}')
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []
    def get_item(self, id ):
        sql = f'''SELECT * FROM {self.table_name} WHERE id={id}'''
        try:
            print(f'get_item {sql=}')
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            # print( f'{type(res)=}')
            # print(f"{res=}")
            # print(f"{len(res)=}")
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []
    def get_end_date(self, bdid, mode=None ):
        if mode == 'character':
            sql = f'''SELECT *
                      FROM {self.table_name} 
                        JOIN character ON {self.table_name}.character_id = character.id
                      WHERE date = (SELECT MAX(date) FROM {self.table_name} WHERE {self.table_name}.address_id={bdid}) 
                            AND {self.table_name}.address_id={bdid} '''
        else:
            sql = f'''SELECT *
                      FROM {self.table_name}
                      WHERE date = (SELECT MAX(date) FROM {self.table_name} WHERE {self.table_name}.address_id={bdid})
                      AND address_id={bdid} '''


        sql = self.obr_sql( sql)
        try:
            print(f'get_end_date {sql=}')
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            #print( f'{type(res)=}')
            # print(f"{res=}")
            # print(f"{len(res)=}")
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []
    def add_record_water(self, adr_id, d, h,c ):
        try:
            lst = d.split('.')[::-1]
            d = '.'.join(lst)
            print('add_record_water ============', adr_id, d, h, c)

            self.__cur.execute( f"INSERT INTO {self.table_name} VALUES(NULL,?,?,?,?)", (adr_id, d, h,c) )
            self.__db.commit()
        except sq.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False
        return True

    def add_record_electro(self, adr_id, ch_id, date, pnight, pday, pall ):
        try:
            lst = date.split('.')[::-1]
            date = '.'.join(lst)
            print('add_record_water ========',adr_id, ch_id, date, pnight, pday, pall)
            self.__cur.execute( f"INSERT INTO {self.table_name} VALUES(NULL,?,?,?,?,?,?)",
                                                                (adr_id, ch_id, date, pnight, pday, pall) )
            self.__db.commit()
        except sq.Error as e:
            print("Ошибка добавления электро показаний  " + str(e))
            return False
        return True

    def get_history_electro(self, adr_id ):
        sql = f'''SELECT *
                  FROM electro 
                  JOIN character ON electro.character_id = character.id
                  WHERE  electro.address_id={adr_id}
                  ORDER BY date  DESC  '''
        sql = self.obr_sql(sql)
        try:
            #print(f'>>>>>>>>> {sql=}')
            self.__cur.execute( sql )
            res = self.__cur.fetchall()
            lst=[]
            for v in res:
                dic={}
                for k in v.keys():
                    if k == 'date':
                        z = self.ymd2dmy( v[k] )
                    else:
                        z = v[k]
                    #print( z, end=', ' )
                    dic[k]=z
                #print()
                lst.append( dic )
            return lst
        except:
            print("Ошибка чтения из БД")
        return []

    def get_history_water(self, adr_id ):
        sql = f'''SELECT *
                  FROM water 
                  WHERE  water.address_id={adr_id}
                  ORDER BY date  DESC  '''
        sql = self.obr_sql(sql)
        try:
            #print(f'>>>>>>>>> {sql=}')
            self.__cur.execute( sql )
            res = self.__cur.fetchall()
            lst=[]
            for v in res:
                dic={}
                for k in v.keys():
                    if k == 'date':
                        z = self.ymd2dmy( v[k] )
                    else:
                        z = v[k]
                    #print( z, end=', ' )
                    dic[k]=z
                #print()
                lst.append( dic )
            return lst
        except:
            print("Ошибка чтения из БД")
        return []

    def ymd2dmy( self, sd ):
        if sd.find('.') >= 0:
            lst = sd.split('.')[::-1]
        elif sd.find('-') >= 0:
            lst = sd.split('-')[::-1]
        else:
            lst = sd.split('/')[::-1]
        return '.'.join(lst)

    def dmy2ymd( self, sd ):
        if sd.find('.') >= 0:
            lst = sd.split('.')[::-1]
        elif sd.find('-') >= 0:
            lst = sd.split('-')[::-1]
        else:
            lst = sd.split('/')[::-1]
        return '.'.join(lst)


    def obr_sql(self,sql):
        lst = sql.split('\n')
        lst = [s.strip() for s in lst]
        s = ' '.join(lst)

        return s






