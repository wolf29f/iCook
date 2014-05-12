import sqlite3
#tools to correct db errors

conn = sqlite3.connect("recipeBDD",detect_types= sqlite3.PARSE_COLNAMES)
c=conn.cursor()
c.execute("""SELECT pictureLocation FROM onlineRecipe""")
result = c.fetchall()
for i in result:
    print(i[0][:i[0].rfind(".")]+".gif",i[0])
    c.execute("""update onlineRecipe set pictureLocation = ? where pictureLocation = ?""",[i[0][:i[0].rfind(".")]+".gif",i[0]])
conn.commit()
c.close()
