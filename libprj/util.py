def obr_sql( sql ):
    lst = sql.split('\n')
    lst = [s.strip() for s in lst]
    s = ' '.join(lst)
    return s

def ymd2dmy( d ):
    if d.find('.') >= 0:
        lst = d.split('.')[::-1]
    elif d.find('-') >= 0:
        lst = d.split('-')[::-1]
    else:
        lst = d.split('/')[::-1]
    return '.'.join(lst)

def dmy2ymd( self, sd ):
    if sd.find('.') >= 0:
        lst = sd.split('.')[::-1]
    elif sd.find('-') >= 0:
        lst = sd.split('-')[::-1]
    else:
        lst = sd.split('/')[::-1]
    return '.'.join(lst)


if __name__ == '__main__':
    sql = 'SELECT *\n                  FROM electro\n                  WHERE date = (SELECT MAX(date) FROM electro) AND address_id=1'
    print( obr_sql( sql ) )