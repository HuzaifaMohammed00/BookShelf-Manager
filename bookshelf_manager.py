import dataclasses
import sqlite3
import datetime


@dataclasses.dataclass
class Book:
    id: int | None
    title: str
    author: str
    price: float
    amount: int

    @property
    def available(self):
        return self.amount > 0


class BookRepository:
    def __init__(self, db_path="book.db"):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.conn.execute(
            "create table if not exists author (id integer not null primary key autoincrement ,name text)"
        )
        self.conn.execute(
            "create table if not exists Book (id integer not null primary key autoincrement ,title text not null,author_id integer,price float,amount integer)"
        )
        self.conn.commit()

    def close_table(self):
        self.conn.close()

    def add(self, book):
        self.cur.execute("select id from author where name = ?", (book.author,))
        row = self.cur.fetchone()
        if row:
            author_id = row[0]
        else:
            self.cur.execute("insert into author (name) values (?)", (book.author,))
            author_id = self.cur.lastrowid

        self.cur.execute(
            "insert into Book (title,author_id,price,amount) values(?,?,?,?)",
            (book.title, author_id, book.price, book.amount),
        )
        self.conn.commit()
        return self.cur.lastrowid

    def get_all(self):
        self.cur.execute(
            "select Book.id,Book.title,author.name,Book.price,Book.amount from Book join author on Book.author_id = author.id"
        )
        rows = self.cur.fetchall()
        return [Book(*row) for row in rows]

    def find_by_title(self, title):
        self.cur.execute(
            "select Book.id,Book.title,author.name,Book.price,Book.amount from Book join author on Book.author_id = author.id where Book.title = ?",
            (title,),
        )
        rows = self.cur.fetchall()
        return [Book(*row) for row in rows]

    def find_by_name(self, name):
        self.cur.execute(
            "select Book.id,Book.title,author.name,Book.price,Book.amount from Book join author on Book.author_id = author.id where author.name = ?",
            (name,),
        )
        rows = self.cur.fetchall()
        return [Book(*row) for row in rows]

    def update(self, book):
        self.cur.execute(
            "update Book set price = ? ,amount = ? where id = ?",
            (book.price, book.amount, book.id),
        )
        self.conn.commit()


class Inventory:
    def __init__(self, repo) -> None:
        self.repo = repo

    def add_book(self, book):
        if not book.title.strip() or not book.author.strip():
            raise ValueError("the title and author are required")
        if book.price < 0 or book.amount < 0:
            raise ValueError("the price or amount should not be negative")
        return self.repo.add(book)

    def list_books(self):
        return self.repo.get_all()

    def find_by_title(self, title):
        return self.repo.find_by_title(title)

    def find_by_author(self, author):
        return self.repo.find_by_name(author)

    def update_book(self, title, price=None, amount=None):
        books = self.repo.find_by_title(title)
        if not books:
            raise ValueError("the book not found")
        if price is None and amount is None:
            raise ValueError("you should enter price or amount")
        book = books[0]
        if price is not None:
            if price < 0:
                raise ValueError("the price should be positive")
            book.price = price
        if amount is not None:
            if amount < 0:
                raise ValueError("the amount should be positive")
            book.amount = amount
        self.repo.update(book)
        return book

    def restock(self, title, quantity):
        books = self.repo.find_by_title(title)
        if not books:
            raise ValueError("the book not found")
        if quantity <= 0:
            raise ValueError("quantity should be positive")
        book = books[0]
        book.amount += quantity
        self.repo.update(book)
        return book

    def sell_book(self, title, quantity):
        books = self.repo.find_by_title(title)
        if not books:
            raise ValueError("the book not found")
        if quantity <= 0:
            raise ValueError("quantity should be positive")
        book = books[0]
        if book.amount < quantity:
            raise ValueError("not enough stock")
        book.amount -= quantity
        self.repo.update(book)
        return book.price * quantity

    def report(self):
        books = self.repo.get_all()
        return {
            "total_books": len(books),
            "total_value": sum(b.price * b.amount for b in books),
            "free_books": sum(1 for b in books if b.price == 0),
            "low_stock": [b for b in books if b.amount < 5],
        }

    def save_report(self):
        data = self.report()
        with open(f"report_{datetime.date.today()}.txt", "a", encoding="utf-8") as file:
            file.write(
                f"""
========== Report ==========
Total Books            : {data['total_books']}
Total Inventory Value  : {data['total_value']}$
Free Books             : {data['free_books']}
------- Low Stock -------
"""
            )
            for b in data["low_stock"]:
                file.write(f"{b.title}: {b.amount} copies\n")


class BookShelfCLI:
    def __init__(self, inventory):
        self.inventory = inventory

    def show_books(self, books):
        if not books:
            print("No books found.")
            return
        for b in books:
            status = "Available" if b.available else "Out of stock"
            print(f"[{b.id}] {b.title} - {b.author} | {b.price}$ | Amount: {b.amount} ({status})")

    def run(self):
        while True:
            print("\n=== BookShelf Manager ===")
            print("1. Add Book")
            print("2. List All Books")
            print("3. Search by Title")
            print("4. Search by Author")
            print("5. Update Book")
            print("6. Restock Book")
            print("7. Sell Book")
            print("8. Show Report")
            print("9. Save Report")
            print("0. Exit")

            choice = input("Choose an option: ").strip()

            try:
                if choice == "1":
                    title = input("Title: ").strip()
                    author = input("Author: ").strip()
                    price = float(input("Price: "))
                    amount = int(input("Amount: "))
                    book_id = self.inventory.add_book(Book(None, title, author, price, amount))
                    print(f"Book added with ID {book_id}.")

                elif choice == "2":
                    self.show_books(self.inventory.list_books())

                elif choice == "3":
                    title = input("Enter title: ").strip()
                    self.show_books(self.inventory.find_by_title(title))

                elif choice == "4":
                    author = input("Enter author: ").strip()
                    self.show_books(self.inventory.find_by_author(author))

                elif choice == "5":
                    title = input("Enter book title to update: ").strip()
                    price_str = input("New price (leave empty to skip): ").strip()
                    amount_str = input("New amount (leave empty to skip): ").strip()
                    price = float(price_str) if price_str else None
                    amount = int(amount_str) if amount_str else None
                    book = self.inventory.update_book(title, price=price, amount=amount)
                    print(f"Updated: {book.title} | {book.price}$ | Amount: {book.amount}")

                elif choice == "6":
                    title = input("Enter book title: ").strip()
                    qty = int(input("Quantity to add: "))
                    book = self.inventory.restock(title, qty)
                    print(f"Restocked: {book.title} | New Amount: {book.amount}")

                elif choice == "7":
                    title = input("Enter book title: ").strip()
                    qty = int(input("Quantity to sell: "))
                    total = self.inventory.sell_book(title, qty)
                    print(f"Sold! Total price: {total}$")

                elif choice == "8":
                    data = self.inventory.report()
                    print("\n========== Report ==========")
                    print(f"Total Books           : {data['total_books']}")
                    print(f"Total Inventory Value : {data['total_value']}$")
                    print(f"Free Books            : {data['free_books']}")
                    print("Low Stock (< 5):")
                    for b in data["low_stock"]:
                        print(f"  - {b.title}: {b.amount} copies")

                elif choice == "9":
                    self.inventory.save_report()
                    print("Report saved to file.")

                elif choice == "0":
                    print("Goodbye!")
                    break

                else:
                    print("Invalid choice, please try again.")

            except ValueError as err:
                print(f"Error: {err}")


if __name__ == "__main__":
    repo = BookRepository("book.db")
    try:
        inventory = Inventory(repo)
        cli = BookShelfCLI(inventory)
        cli.run()
    finally:
        repo.close_table()