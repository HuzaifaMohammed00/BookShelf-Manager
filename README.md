# BookShelf Manager System

**Developer:** Huzaifa Mohammed

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Version History:
  v1.0 - 20/6/2026  : Basic structure and database design
  v2.0 - 21/6/2026  : Add, Search, and Show books
  v3.0 - 22/6/2026  : Update, Sell, and Report features
  v4.0 - 24/6/2026  : Final procedural version
  v5.0 - 15/11/2026 : Full OOP refactoring (4-layer architecture, restock, & report export)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

BookShelf Manager is a command-line inventory system built with Python and SQLite. It helps bookstore owners manage their library in a clean, organized, and maintainable way.

## What's New in v5.0 (Major Refactoring)

In **v5.0**, the project was completely rewritten from procedural functions into **Object-Oriented Programming (OOP)** with clear separation of responsibilities across four classes:

- **`Book` (`@dataclass`)**: Represents each book record with an `available` `@property`.
- **`BookRepository`**: Handles all SQLite database connections, `JOIN` queries, and updates.
- **`Inventory`**: Manages business rules, input validation (`ValueError`), restocking, selling, and report generation.
- **`BookShelfCLI`**: Provides the interactive command-line menu and handles user input cleanly.

## Features

- Add new books to the inventory (auto-creates or links authors)
- Search books by title or author
- View all books with live availability status
- Update book price and stock quantity
- Restock existing books and sell books with automatic stock checks
- Generate inventory reports and export them to daily `.txt` files (`report_YYYY-MM-DD.txt`)

## Technologies Used

- Python 3 (`dataclasses`, `sqlite3`, `datetime`)
- SQLite3 (relational database)

## What I Learned

- Object-Oriented Programming (OOP) & separation of concerns
- Using `@dataclass` and `@property` in Python
- Database design with relationships (Author & Book tables with `JOIN` queries)
- CRUD operations with parameterized SQL queries
- Error handling with `ValueError` and `try/except`
- Building a real-world, maintainable command-line application

---

This project was originally built as part of my *Python for Everybody* specialization on Coursera and refactored into OOP during my *Meta Back-End Developer* coursework.