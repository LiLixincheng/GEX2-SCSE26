import json
from pathlib import Path


def load_library(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def save_library(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def find_book(books, search_text):
    search_text = search_text.strip().casefold()
    if not search_text:
        return None
    for book_id in books:
        if book_id.casefold() == search_text:
            return book_id
    for book_id, book in books.items():
        if search_text in (book["title"].strip().casefold(), book["author"].strip().casefold()):
            return book_id
    return None


def display_books(books):
    print("\nBOOK CATALOGUE")
    print("-" * 60)
    for book_id, book in books.items():
        status = "AVAILABLE" if book["available"] else "ON LOAN"
        print(f"{book_id} | {book['title']} | {book['category']} | {status}")
    if not books:
        print("No books found.")


def display_loans(loans, books):
    print("\nCURRENT LOANS")
    print("-" * 60)
    for loan in loans:
        book_id = loan["book_id"]
        title = books.get(book_id, {}).get("title", "Unknown book")
        print(f"{book_id} | {title} | Borrower: {loan['borrower']}")
    if not loans:
        print("No current loans.")


def library_statistics(books):
    total = len(books)
    available = sum(1 for book in books.values() if book["available"])
    return total, available, total - available


def main():
    data = load_library(Path(__file__).with_name("library.json"))
    library = data["library"]
    print("LIBRARY ADMINISTRATION")
    print("=" * 60)
    print(f"Library: {library['name']}")
    print(f"Branch: {library['branch']}")
    print(f"Year: {library['year']}")
    print(f"Categories: {', '.join(data['categories'])}")
    display_books(data["books"])
    display_loans(data["loans"], data["books"])
    total, available, borrowed = library_statistics(data["books"])
    print("\nLIBRARY STATISTICS")
    print("-" * 60)
    print(f"Total books: {total}")
    print(f"Available: {available}")
    print(f"Borrowed: {borrowed}")


if __name__ == "__main__":
    main() 
