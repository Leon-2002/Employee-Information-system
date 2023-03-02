import psycopg2

conn = psycopg2.connect("postgresql://postgres:admin321@localhost:5432/employee_db")

choice = int(input("Operations\n1 - Add Data\n2 - View All Data"))
cur = conn.cursor()

while True:
    if choice == 1:
        insertQuery = "INSERT INTO employee_tbl(lname,fname,email,address,number,position) VALUES (%s, %s, %s, %s, %s, %s)"
        values = ("ROoque", "Iven", "iven@gmail.com","Quezon", "123123123", "CEO" )
        cur.execute(insertQuery, values)
        print("Inserted Successfully")
        continue
    elif choice == 2:
        viewQuery = "SELECt * FROM employee_tbl"
        continue
        

conn.commit()
conn.close()