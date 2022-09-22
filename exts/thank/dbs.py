import mysql.connector

def connect():
    return mysql.connector.connect(host='',
                               database='',
                               user='',
                               password='')

def getThanks(user):
    conn = connect()

    c = conn.cursor()

    c.execute(f"SELECT count,weeklyCount FROM thanks WHERE user='{user}'")

    res = c.fetchall()

    if res == []:
        c.execute(f"INSERT INTO thanks (user, count, weeklyCount, lastUsed) VALUES('{user}', 0, 0, '2000-1-1 0:0:0')")
        conn.commit()
        c.close()
        return getThanks(user)

    conn.commit()
    c.close()

    return (res [0][0], res [0][1])

def setThanks(user, total, week):
    conn = connect()

    c = conn.cursor()

    c.execute(f"SELECT count,weeklyCount FROM thanks WHERE user='{user}'")

    res = c.fetchall()

    if res == []:
        c.execute(f"INSERT INTO thanks (user, count, weeklyCount, lastUsed) VALUES('{user}', 0, 0, '2000-1-1 0:0:0')")
        conn.commit()
        c.close()
        return setThanks(user, total, week)

    c.execute(f"UPDATE thanks SET count={total}, weeklyCount={week} WHERE user='{user}'")

    conn.commit()
    c.close()

def getRank(user):
    conn = connect()

    c = conn.cursor()

    c.execute(f"SELECT count,weeklyCount FROM thanks WHERE user='{user}'")

    res = c.fetchall()

    if res == []:
        c.execute(f"INSERT INTO thanks (user, count, weeklyCount, lastUsed) VALUES('{user}', 0, 0, '2000-1-1 0:0:0')")
        conn.commit()
        c.close()
        return getThanks(user)

    c.execute(f"""SELECT temp.rank FROM (SELECT user,count, ROW_NUMBER() OVER (ORDER BY count DESC) rank FROM thanks )temp WHERE user='{user}'""")

    res = c.fetchall()

    conn.commit()
    c.close()

    return res [0][0]

def getTop():
    conn = connect()

    c = conn.cursor()


    c.execute(f"""SELECT temp.user,temp.count FROM (SELECT user,count, ROW_NUMBER() OVER (ORDER BY count DESC) rank FROM thanks )temp WHERE rank <= 11""")

    res = c.fetchall()

    conn.commit()
    c.close()

    return res



"""conn = connect()

c = conn.cursor()

c.execute("CREATE TABLE thanks (user text, count int, weeklyCount int, lastUsed text);")

conn.commit()
c.close()"""
