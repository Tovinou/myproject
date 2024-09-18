from abc import ABC, abstractmethod

# Klass Item som grundklass (abstrakt klass)
class Item(ABC):
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        self.is_borrowed = False

    @abstractmethod
    def display_info(self):
        pass

# Subklass Book som ärver från Item
class Book(Item):
    def __init__(self, title, author, year, pages):
        super().__init__(title, author, year)
        self.pages = pages

    def display_info(self):
        print(f"Book: {self.title}, Author: {self.author}, Year: {self.year}, Pages: {self.pages}, Borrowed: {self.is_borrowed}")

# Subklass Magazine som ärver från Item
class Magazine(Item):
    def __init__(self, title, author, year, issue):
        super().__init__(title, author, year)
        self.issue = issue

    def display_info(self):
        print(f"Magazine: {self.title}, Author: {self.author}, Year: {self.year}, Issue: {self.issue}, Borrowed: {self.is_borrowed}")

# Klass LibraryUser för låntagare
class LibraryUser:
    def __init__(self, name):
        self.name = name
        self.borrowed_items = []

    def borrow(self, item):
        if not item.is_borrowed:
            self.borrowed_items.append(item)
            item.is_borrowed = True
            print(f"{self.name} borrowed '{item.title}'")
        else:
            print(f"Item '{item.title}' is already borrowed by someone else.")

    def return_item(self, item):
        if item in self.borrowed_items:
            self.borrowed_items.remove(item)
            item.is_borrowed = False
            print(f"{self.name} returned '{item.title}'")
        else:
            print(f"{self.name} does not have the item '{item.title}'")

    def list_borrowed_items(self):
        if self.borrowed_items:
            print(f"{self.name} has borrowed the following items:")
            for item in self.borrowed_items:
                item.display_info()
        else:
            print(f"{self.name} has no borrowed items.")

# Klass Library för biblioteket
class Library:
    def __init__(self):
        self.items = []
        self.users = []

    def add_item(self, item):
        self.items.append(item)
        print(f"Added '{item.title}' to the library collection.")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Removed '{item.title}' from the library collection.")
        else:
            print(f"Item '{item.title}' is not in the library collection.")

    def register_user(self, user):
        self.users.append(user)
        print(f"Registered user '{user.name}'.")

    def borrow_item(self, user, item):
        if item in self.items and not item.is_borrowed:
            user.borrow(item)
        elif item.is_borrowed:
            print(f"Item '{item.title}' is already borrowed.")
        else:
            print(f"Item '{item.title}' is not available in the library.")

    def return_item(self, user, item):
        if item in self.items and item.is_borrowed:
            user.return_item(item)
        else:
            print(f"Item '{item.title}' is not currently borrowed.")

    def list_items(self):
        if self.items:
            print("Library collection:")
            for item in self.items:
                item.display_info()
        else:
            print("The library has no items.")

    def list_available_items(self):
        available_items = [item for item in self.items if not item.is_borrowed]
        if available_items:
            print("Available items in the library:")
            for item in available_items:
                item.display_info()
        else:
            print("No items are available at the moment.")

    def borrowed_summary(self):
        print("Summary of borrowed items:")
        for user in self.users:
            if user.borrowed_items:
                user.list_borrowed_items()

# Huvudprogrammet
def main():
    # Skapa bibliotek
    library = Library()

    # Skapa några objekt (böcker och tidskrifter)
    book1 = Book("1984", "George Orwell", 1949, 328)
    book2 = Book("The Catcher in the Rye", "J.D. Salinger", 1951, 277)
    magazine1 = Magazine("National Geographic", "Various", 2023, 12)

    # Lägg till objekt till biblioteket
    library.add_item(book1)
    library.add_item(book2)
    library.add_item(magazine1)

    # Skapa låntagare
    user1 = LibraryUser("Alice")
    user2 = LibraryUser("Bob")

    # Registrera låntagare
    library.register_user(user1)
    library.register_user(user2)

    # Alice lånar en bok
    library.borrow_item(user1, book1)

    # Bob försöker låna samma bok
    library.borrow_item(user2, book1)

    # Bob lånar en annan bok
    library.borrow_item(user2, book2)

    # Visa alla tillgängliga objekt
    library.list_available_items()

    # Visa sammanfattning av lånade objekt
    library.borrowed_summary()

    # Alice returnerar en bok
    library.return_item(user1, book1)

    # Visa tillgängliga objekt igen
    library.list_available_items()

if __name__ == "__main__":
    main()
