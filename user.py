from pathlib import Path

from admin import display_books, find_book, load_library, save_library


def books_in_category(
    books,
    category
):
    category = category.strip().casefold()
    return [
        book_id for book_id, book in books.items()
        if book["category"].strip().casefold() == category
    ]


def search_by_title(
    books,
    search_text
):
    search_text = search_text.strip().casefold()
    return [
        book_id for book_id, book in books.items()
        if search_text in book["title"].casefold()
    ]


def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    book_id = find_book(books, search_text)
    if book_id is None:
        return "BOOK_NOT_FOUND"
    borrower = borrower.strip()
    if not borrower:
        return "EMPTY_NAME"
    if not books[book_id]["available"] or any(loan["book_id"] == book_id for loan in loans):
        return "NOT_AVAILABLE"
    books[book_id]["available"] = False
    loans.append({"book_id": book_id, "borrower": borrower})
    return "OK"


def return_book(
    books,
    loans,
    book_title,
    borrower
):
    book_id = find_book(books, book_title)
    if book_id is None:
        return "BOOK_NOT_FOUND"
    borrower = borrower.strip()
    if not borrower:
        return "EMPTY_NAME"
    for index, loan in enumerate(loans):
        if loan["book_id"] == book_id and loan["borrower"].strip().casefold() == borrower.casefold():
            loans.pop(index)
            books[book_id]["available"] = not any(
                remaining["book_id"] == book_id for remaining in loans
            )
            return "OK"
    return "NOT_ON_LOAN"


def main():
    filename = Path(__file__).with_name("library.json")
    data = load_library(filename)
    books = data["books"]
    loans = data["loans"]
    messages = {
        "BOOK_NOT_FOUND": "Book not found.",
        "EMPTY_NAME": "Please enter a borrower name.",
        "NOT_AVAILABLE": "This book is not available.",
        "NOT_ON_LOAN": "No matching loan was found for this borrower."
    }
    print("LIBRARY USER SYSTEM")
    while True:
        print("\n1. Search by title")
        print("2. Search by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            matches = search_by_title(books, input("Title or part of title: "))
            display_books({book_id: books[book_id] for book_id in matches})
        elif choice == "2":
            print(f"Categories: {', '.join(data['categories'])}")
            matches = books_in_category(books, input("Category: "))
            display_books({book_id: books[book_id] for book_id in matches})
        elif choice in ("3", "4"):
            search_text = input("Book ID, full title, or author: ")
            borrower = input("Borrower name: ")
            if choice == "3":
                result = borrow_book(books, loans, search_text, borrower)
                success = "Book borrowed successfully."
            else:
                result = return_book(books, loans, search_text, borrower)
                success = "Book returned successfully."
            print(success if result == "OK" else messages[result])
        elif choice == "5":
            save_library(data, filename)
            print("Library saved. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose 1 to 5.")


if __name__ == "__main__":
    main()
  