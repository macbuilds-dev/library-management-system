import json
import os
from datetime import datetime

# Node classes for Queue and Stack
class QueueNode:
    def __init__(self, book_id, user_name):
        self.book_id = book_id
        self.user_name = user_name
        self.next = None

class StackNode:
    def __init__(self, book_id, return_date):
        self.book_id = book_id
        self.return_date = return_date
        self.next = None

# Queue for book requests
class RequestQueue:
    def __init__(self):
        self.front = None
        self.rear = None
    
    def enqueue(self, book_id, user_name):
        new_node = QueueNode(book_id, user_name)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
    
    def dequeue(self):
        if self.front is None:
            return None
        temp = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return temp
    
    def is_empty(self):
        return self.front is None
    
    def display(self):
        if self.is_empty():
            return []
        requests = []
        current = self.front
        while current:
            requests.append({'book_id': current.book_id, 'user': current.user_name})
            current = current.next
        return requests
    
    def to_list(self):
        """Convert queue to list for saving"""
        result = []
        current = self.front
        while current:
            result.append({'book_id': current.book_id, 'user_name': current.user_name})
            current = current.next
        return result
    
    def from_list(self, data):
        """Load queue from list"""
        for item in data:
            self.enqueue(item['book_id'], item['user_name'])

# Stack for returned books
class ReturnStack:
    def __init__(self):
        self.top = None
    
    def push(self, book_id, return_date):
        new_node = StackNode(book_id, return_date)
        new_node.next = self.top
        self.top = new_node
    
    def pop(self):
        if self.top is None:
            return None
        temp = self.top
        self.top = self.top.next
        return temp
    
    def is_empty(self):
        return self.top is None
    
    def display(self):
        if self.is_empty():
            return []
        returns = []
        current = self.top
        while current:
            returns.append({'book_id': current.book_id, 'return_date': current.return_date})
            current = current.next
        return returns
    
    def to_list(self):
        """Convert stack to list for saving"""
        result = []
        current = self.top
        while current:
            result.append({'book_id': current.book_id, 'return_date': current.return_date})
            current = current.next
        return result
    
    def from_list(self, data):
        """Load stack from list (reverse order to maintain stack)"""
        for item in reversed(data):
            self.push(item['book_id'], item['return_date'])

# Book class
class Book:
    def __init__(self, book_id, title, author, total_copies, available_copies):
        self.id = book_id
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = available_copies
    
    def to_dict(self):
        """Convert book to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'total_copies': self.total_copies,
            'available_copies': self.available_copies
        }
    
    @staticmethod
    def from_dict(data):
        """Create book from dictionary"""
        return Book(
            data['id'],
            data['title'],
            data['author'],
            data['total_copies'],
            data['available_copies']
        )

# Library Management System
class Library:
    def __init__(self):
        self.books = []
        self.request_queue = RequestQueue()
        self.return_stack = ReturnStack()
        self.issued_books = {}  # {book_id: [user_names]}
        self.load_data()
    
    def load_data(self):
        """Load all data from files"""
        # Load books
        if os.path.exists('library_books.json'):
            try:
                with open('library_books.json', 'r') as f:
                    data = json.load(f)
                    self.books = [Book.from_dict(book) for book in data]
                    print(f"[DEBUG] Loaded {len(self.books)} books from file")
            except Exception as e:
                print(f"[ERROR] Failed to load books: {e}")
        
        # Load issued books
        if os.path.exists('issued_books.json'):
            try:
                with open('issued_books.json', 'r') as f:
                    self.issued_books = json.load(f)
                    print(f"[DEBUG] Loaded issued books data")
            except Exception as e:
                print(f"[ERROR] Failed to load issued books: {e}")
        
        # Load request queue
        if os.path.exists('request_queue.json'):
            try:
                with open('request_queue.json', 'r') as f:
                    data = json.load(f)
                    self.request_queue.from_list(data)
                    print(f"[DEBUG] Loaded request queue")
            except Exception as e:
                print(f"[ERROR] Failed to load request queue: {e}")
        
        # Load return stack
        if os.path.exists('return_stack.json'):
            try:
                with open('return_stack.json', 'r') as f:
                    data = json.load(f)
                    self.return_stack.from_list(data)
                    print(f"[DEBUG] Loaded return stack")
            except Exception as e:
                print(f"[ERROR] Failed to load return stack: {e}")
    
    def save_data(self):
        """Save all data to files"""
        try:
            # Save books
            with open('library_books.json', 'w') as f:
                books_data = [book.to_dict() for book in self.books]
                json.dump(books_data, f, indent=4)
            
            # Save issued books
            with open('issued_books.json', 'w') as f:
                json.dump(self.issued_books, f, indent=4)
            
            # Save request queue
            with open('request_queue.json', 'w') as f:
                json.dump(self.request_queue.to_list(), f, indent=4)
            
            # Save return stack
            with open('return_stack.json', 'w') as f:
                json.dump(self.return_stack.to_list(), f, indent=4)
            
            print("[DEBUG] Data saved successfully")
        except Exception as e:
            print(f"[ERROR] Failed to save data: {e}")
    
    def display_header(self, title):
        print(f"\n{'='*50}")
        print(f"{title.center(50)}")
        print('='*50)
    
    def add_book(self):
        self.display_header("ADD BOOK")
        try:
            book_id = int(input("Enter Book ID: "))
            if any(b.id == book_id for b in self.books):
                print("Book ID already exists!")
                return
            
            title = input("Enter Book Title: ")
            author = input("Enter Author Name: ")
            total_copies = int(input("Enter Total Copies: "))
            
            if total_copies < 0:
                print("Total copies cannot be negative!")
                return
            
            book = Book(book_id, title, author, total_copies, total_copies)
            self.books.append(book)
            self.save_data()
            print("Book added successfully!")
        except ValueError:
            print("Invalid input! Please enter valid numbers.")
        except Exception as e:
            print(f"Error adding book: {e}")
    
    def search_book(self):
        self.display_header("SEARCH BOOK")
        try:
            book_id = int(input("Enter Book ID to search: "))
            for book in self.books:
                if book.id == book_id:
                    print(f"\nID: {book.id}")
                    print(f"Title: {book.title}")
                    print(f"Author: {book.author}")
                    print(f"Total Copies: {book.total_copies}")
                    print(f"Available: {book.available_copies}")
                    return
            print("Book not found!")
        except ValueError:
            print("Invalid input! Please enter a valid Book ID.")
    
    def add_book_request(self):
        self.display_header("REQUEST BOOK")
        try:
            book_id = int(input("Enter Book ID: "))
            user_name = input("Enter Your Name: ")
            
            book = next((b for b in self.books if b.id == book_id), None)
            if not book:
                print("Book not found in library!")
                return
            
            self.request_queue.enqueue(book_id, user_name)
            self.save_data()
            position = len(self.request_queue.display())
            print(f"Request added for '{user_name}'. Position in queue: {position}")
        except ValueError:
            print("Invalid input!")
    
    def issue_book_from_queue(self):
        self.display_header("ISSUE BOOK FROM QUEUE")
        if self.request_queue.is_empty():
            print("No pending requests!")
            return
        
        request = self.request_queue.dequeue()
        book = next((b for b in self.books if b.id == request.book_id), None)
        
        if book and book.available_copies > 0:
            book.available_copies -= 1
            if str(book.id) not in self.issued_books:
                self.issued_books[str(book.id)] = []
            self.issued_books[str(book.id)].append(request.user_name)
            self.save_data()
            print(f"Book '{book.title}' issued to {request.user_name}")
        else:
            print("Book not available. Request cancelled.")
            self.save_data()
    
    def return_book(self):
        self.display_header("RETURN BOOK")
        try:
            book_id = int(input("Enter Book ID: "))
            user_name = input("Enter Your Name: ")
            
            book = next((b for b in self.books if b.id == book_id), None)
            if not book:
                print("Book not found!")
                return
            
            if str(book_id) in self.issued_books and user_name in self.issued_books[str(book_id)]:
                book.available_copies += 1
                self.issued_books[str(book_id)].remove(user_name)
                if not self.issued_books[str(book_id)]:
                    del self.issued_books[str(book_id)]
                
                return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.return_stack.push(book_id, return_date)
                self.save_data()
                print(f"Book '{book.title}' returned successfully on {return_date}")
            else:
                print("No record of this book issued to you!")
        except ValueError:
            print("Invalid input!")
    
    def check_rack_availability(self):
        self.display_header("RACK AVAILABILITY")
        total_racks = 100
        occupied = sum(b.total_copies for b in self.books)
        available = total_racks - occupied
        print(f"Total Rack Spaces: {total_racks}")
        print(f"Occupied: {occupied}")
        print(f"Available: {available}")
        
        if available < 0:
            print("\nWARNING: Rack capacity exceeded!")
    
    def display_inventory(self):
        self.display_header("LIBRARY INVENTORY")
        if not self.books:
            print("No books in library!")
            return
        print(f"{'ID':<8}{'Title':<25}{'Author':<20}{'Total':<8}{'Available':<10}")
        print('-'*70)
        for book in self.books:
            print(f"{book.id:<8}{book.title:<25}{book.author:<20}{book.total_copies:<8}{book.available_copies:<10}")
    
    def display_request_queue(self):
        self.display_header("PENDING REQUESTS")
        requests = self.request_queue.display()
        if not requests:
            print("No pending requests!")
            return
        print(f"{'Position':<10}{'Book ID':<10}{'User Name':<30}")
        print('-'*50)
        for i, req in enumerate(requests, 1):
            book = next((b for b in self.books if b.id == req['book_id']), None)
            book_title = book.title if book else "Unknown"
            print(f"{i:<10}{req['book_id']:<10}{req['user']:<30}")
    
    def display_return_history(self):
        self.display_header("RETURN HISTORY (Last 10)")
        returns = self.return_stack.display()
        if not returns:
            print("No return history!")
            return
        print(f"{'Book ID':<10}{'Book Title':<30}{'Return Date':<25}")
        print('-'*65)
        for ret in returns[:10]:
            book = next((b for b in self.books if b.id == ret['book_id']), None)
            book_title = book.title if book else "Unknown"
            print(f"{ret['book_id']:<10}{book_title:<30}{ret['return_date']:<25}")
    
    def delete_book(self):
        self.display_header("DELETE BOOK")
        try:
            book_id = int(input("Enter Book ID to delete: "))
            book = next((b for b in self.books if b.id == book_id), None)
            
            if not book:
                print("Book not found!")
                return
            
            # Check if book is issued
            if str(book_id) in self.issued_books and self.issued_books[str(book_id)]:
                print(f"Cannot delete! Book is currently issued to: {', '.join(self.issued_books[str(book_id)])}")
                return
            
            self.books = [b for b in self.books if b.id != book_id]
            self.save_data()
            print(f"Book '{book.title}' deleted successfully!")
        except ValueError:
            print("Invalid input!")
    
    def display_issued_books(self):
        self.display_header("CURRENTLY ISSUED BOOKS")
        if not self.issued_books:
            print("No books are currently issued!")
            return
        
        print(f"{'Book ID':<10}{'Book Title':<30}{'Issued To':<30}")
        print('-'*70)
        for book_id, users in self.issued_books.items():
            book = next((b for b in self.books if b.id == int(book_id)), None)
            book_title = book.title if book else "Unknown"
            for user in users:
                print(f"{book_id:<10}{book_title:<30}{user:<30}")

def authenticate():
    print("="*50)
    print("Library Management System".center(50))
    print("="*50)
    username = input("Username: ")
    password = input("Password: ")
    
    credentials = {
        'admin': 'admin123',
        'librarian': 'lib123',
        'student': 'student123'
    }
    
    return username if credentials.get(username) == password else None

def main():
    try:
        library = Library()
        role = authenticate()
        
        if not role:
            print("Invalid credentials!")
            input("Press Enter to exit...")
            return
    except Exception as e:
        print(f"Error initializing library: {e}")
        input("Press Enter to exit...")
        return
    
    while True:
        print(f"\n{'='*50}")
        print(f"Library Management System - {role.upper()}".center(50))
        print('='*50)
        
        if role == 'admin':
            print("1. Add Book")
            print("2. Delete Book")
            print("3. Search Book")
            print("4. View Request Queue")
            print("5. Issue Book from Queue")
            print("6. View Return History")
            print("7. Check Rack Availability")
            print("8. Display Inventory")
            print("9. View Issued Books")
            print("10. Exit")
        elif role == 'librarian':
            print("1. Search Book")
            print("2. View Request Queue")
            print("3. Issue Book from Queue")
            print("4. Return Book")
            print("5. View Return History")
            print("6. Display Inventory")
            print("7. View Issued Books")
            print("8. Exit")
        else:  # student
            print("1. Search Book")
            print("2. Request Book")
            print("3. Return Book")
            print("4. View Inventory")
            print("5. Exit")
        
        try:
            choice = int(input("\nEnter choice: "))
            
            if role == 'admin':
                if choice == 1: library.add_book()
                elif choice == 2: library.delete_book()
                elif choice == 3: library.search_book()
                elif choice == 4: library.display_request_queue()
                elif choice == 5: library.issue_book_from_queue()
                elif choice == 6: library.display_return_history()
                elif choice == 7: library.check_rack_availability()
                elif choice == 8: library.display_inventory()
                elif choice == 9: library.display_issued_books()
                elif choice == 10: break
                else: print("Invalid choice!")
            elif role == 'librarian':
                if choice == 1: library.search_book()
                elif choice == 2: library.display_request_queue()
                elif choice == 3: library.issue_book_from_queue()
                elif choice == 4: library.return_book()
                elif choice == 5: library.display_return_history()
                elif choice == 6: library.display_inventory()
                elif choice == 7: library.display_issued_books()
                elif choice == 8: break
                else: print("Invalid choice!")
            else:  # student
                if choice == 1: library.search_book()
                elif choice == 2: library.add_book_request()
                elif choice == 3: library.return_book()
                elif choice == 4: library.display_inventory()
                elif choice == 5: break
                else: print("Invalid choice!")
        except ValueError:
            print("Invalid input! Please enter a number.")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nThank you for using Library Management System!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        input("Press Enter to exit...")