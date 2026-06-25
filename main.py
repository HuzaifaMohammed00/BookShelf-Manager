import sqlite3

conn = sqlite3.connect("book.db")
cur = conn.cursor()


def add_book():
    title = input("enter the title ")
    name = input("enter the name ")
    price = int(input("enter the price "))
    amount = int(input("enter the amount "))
    available = "true" if amount > 0 else "false"
    cur.execute("select id from author where name = ?", (name,))
    row = cur.fetchone()
    if row:
        author_id = row[0]
    else:
        cur.execute("insert into author (name) values (?)", (name,))
        author_id = cur.lastrowid
    cur.execute(
        "insert into Book (title,author_id,price,amount,available) values (?,?,?,?,?)",
        (title, author_id, price, amount, available),
    )
    print("added done")
    conn.commit()


def search_book_author(author):
    cur.execute("select id from author where name = ?", (author,))
    row = cur.fetchone()
    if row:
        author_id = row[0]
        cur.execute("select * from Book where author_id  = ?", (author_id,))
        data = cur.fetchall()
        for row in data:
            print("title:", row[1])
            print("author:", author)
            print(
                "amount:", row[4], "and the price:", row[3], "$", "available:", row[5]
            )
    else:
        print("not found the author")


def search_book_title(title):
    cur.execute("select id from Book where title = ?", (title,))
    rows = cur.fetchone()
    if rows:
        cur.execute(
            "select title,author_id,price,amount,available from Book where title = ?",
            (title,),
        )
        row = cur.fetchall()

        autid = row[0][1]

        cur.execute("select name from author where id = ?", (autid,))
        author = cur.fetchone()[0]

        for data in row:
            print("the title:", title)
            print("the author:", author)
            print(
                "the price:", data[2], "and the amount", data[3], " available:", data[4]
            )

    else:
        print("the book not found.")


def update_quantity():
    title = input("enter the name of title to update: ")
    cur.execute("select id from Book where title = (?)", (title,))
    row = cur.fetchone()
    if row:
        choice = int(input("""
    1. Update the quantity
    2. Update the price 
    3. Update the quantity and price
    """))
        if choice == 1:
            new_quantity = int(input("enter the new quantity:"))
            cur.execute(
                "update Book set amount = ? where title = ?", (new_quantity, title)
            )
            print("updated done")
        elif choice == 2:
            new_price = int(input("enter the new price:"))
            cur.execute("update Book set price = ? where title = ?", (new_price, title))
            print("updated done")
        elif choice == 3:
            new_quantity = int(input("enter the new quantity:"))
            new_price = int(input("enter the new price:"))
            cur.execute(
                "update Book set price = ? ,amount  = ? where title = ?",
                (new_price, new_quantity, title),
            )
            print("updated done")
        else:
            print("please enter number from 1 to 3")
        conn.commit()
    else:
        print("the book not found")


def show_book():

    choice = int(input("do you want full show '1' or smplie show '2' "))
    if choice == 1:
        cur.execute("select * from Book ")
        rows = cur.fetchall()
        # print("ID. Title.   Author    Price   amount                  available")
        print("------------------------------------------------------------------")
        for row in rows:
            available = "true" if row[4] > 0 else "false"
            author_id = row[2]
            cur.execute("select name from author where id  = ?", (int(author_id),))
            author = cur.fetchone()[0]
            print(
                row[0],
                "||",
                row[1],
                "||",
                author,
                "||",
                row[3],
                "||",
                row[4],
                "||",
                available,
                "||",
            )
    elif choice == 2:
        cur.execute("select id , author_id , title from Book ")
        rows = cur.fetchall()
        if rows:
            print("ID. Title.   Author     ")
            print("----------------------")
            for row in rows:
                author_id = row[1]
                cur.execute("select name from author where id  = ?", (int(author_id),))
                author = cur.fetchone()[0]
                print(row[0], "  ||", row[2], "            ||", author)

        else:
            print("There is no book ")
    else:
        print("invalid input enter 1 or 2.")


def show_report():
    cur.execute("select count(*) from Book")
    books = cur.fetchone()[0]

    cur.execute("select sum(price * amount) from Book where price > 0")
    total_value = cur.fetchone()[0] or 0

    cur.execute("select count(*) from Book where price = 0")
    free_books = cur.fetchone()[0]

    cur.execute("select title, amount from Book where amount < 5")
    low_stock = cur.fetchall()

    print("========== Report ==========")
    print("Total Books            :", books)
    print("Total Inventory Value  :", total_value, "$")
    print("Free Books             :", free_books)
    print("------- Low Stock -------")
    if low_stock:
        for row in low_stock:
            print(" -", row[0], ":", row[1], "copies")
    else:
        print("All books are well stocked!")
    print("============================")


def sell_book():
    title = input("enter the title of the book: ")
    amount = int(input("how many copies do you want to sell:"))
    cur.execute("select price,amount from Book where title = ?", (title,))
    row = cur.fetchone()
    if row:
        price = row[0]
        real_amount = row[1]
        if real_amount < amount:
            print("not enough copies")
            print("--- the amount in database are:", real_amount)
            print("--- and the amount you want to sell are:", amount)
        else:
            cur.execute(
                "update Book set amount = amount - ? where title = ?",
                (int(amount), title),
            )
            total_price = price * amount
            print(
                "✅ Sold:",
                amount,
                "copies ×",
                price,
                "$ =",
                total_price,
                "$",
            )
            conn.commit()


print("----- Welcome in our system Bookshelf manger ------")
while True:
    print("""
    1. add book
    2. search about book
    3. show all the books
    4. update information about the books
    5. show report  
    6. sell book
    7. quit     
        
    """)
    user_choice = int(input())
    if user_choice == 1:
        add_book()
        print("-------------------------")
    elif user_choice == 2:
        choice = int(input("do you want search by title '1' or by author '2' "))
        if choice == 1:
            title = input("enter the title: ")
            search_book_title(title)
        elif choice == 2:
            author = input("enter the name of author: ")
            search_book_author(author)
        else:
            print("invalid input choose 1 or 2")
        print("-------------------------")
    elif user_choice == 3:
        show_book()
        print("-------------------------")
    elif user_choice == 4:
        update_quantity()
        print("-------------------------")
    elif user_choice == 5:
        show_report()
    elif user_choice == 6:
        sell_book()
        print("-------------------------")
    elif user_choice == 7:
        break
        print("-------------------------")
    else:
        print("invalid input choose from 1 to 6")
    conn.commit()
