import os
import time
from database import Database

class Application:
    def __init__(self):
        self.db = Database()
        self.user_id = None

    def authentication_menu(self):
        while True:
            os.system('cls')
            print("1. Register")
            print("2. Login")
            print("3. Exit")

            choice = input("\nEnter your choice: ")

            if choice == '1':
                name = input("Enter your name: ")
                email = input("Enter your email: ")
                password = input("Enter your password: ")

                result = self.db.createUser(name, email, password)
                print(result)
                input("Press Enter to continue...")
            elif choice == '2':
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                print("Logging in...")
                time.sleep(1)
                user = self.db.login(email, password)
                if user:
                    self.user_id = user[0]
                    self.main_menu()
                else:
                    print("Login failed. Invalid email or password.")
                    input("Press Enter to continue...")
            elif choice == '3':
                break
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")

    def main_menu(self):
        while True:
            os.system('cls')
            print("1. Notes")
            print("2. Groups")
            print("3. Categories")
            print("4. Logout")

            choice = input("\nEnter your choice: ")

            if choice == '1':
                self.notes_menu()
            elif choice == '2':
                self.groups_menu()
            elif choice == '3':
                self.categories_menu()
            elif choice == '4':
                self.user_id = None
                break
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")

    def notes_menu(self):
        while True:
            os.system('cls')
            print("1. Create Note")
            print("2. Update Note")
            print("3. Delete Note")
            print("4. Search Note by Title")
            print("5. Filter Notes by Date")
            print("6. View All Notes")
            print("7. Back")

            choice = input("\nEnter your choice: ")

            if choice == '1':
                os.system('cls')
                title = input("Enter note title: ")
                content = input("Enter note content: ")
                category_ids = input("Enter category IDs (comma-separated): ").split(',')

                result = self.db.createNote(title, content, self.user_id, category_ids)
                print(result)
                input("Press Enter to continue...")
            elif choice == '2':
                os.system('cls')
                note_id = int(input("Enter note ID: "))
                title = input("Enter updated title (leave blank to skip): ")
                content = input("Enter updated content (leave blank to skip): ")
                category_ids = input("Enter updated category IDs (comma-separated, leave blank to skip): ").split(',')

                result = self.db.updateNote(note_id, title, content, category_ids)
                print(result)
                input("Press Enter to continue...")
            elif choice == '3':
                os.system('cls')
                note_id = int(input("Enter note ID: "))

                result = self.db.deleteNote(note_id)
                print(result)
                input("Press Enter to continue...")
            elif choice == '4':
                os.system('cls')
                title = input("Enter note title: ")

                notes = self.db.searchNoteByTitle(title, self.user_id)
                if notes:
                    os.system('cls')
                    print("Note ID\tTitle\t\tContent\t\tCategories")
                    print("-----------------------------------------------")
                    for note in notes:
                        note_id = note[0]
                        title = note[1]
                        content = note[2]
                        categories = self.db.getNoteCategories(note_id)
                        categories_str = ', '.join(categories) if categories else "N/A"
                        print(f"{note_id}\t{title}\t\t{content}\t\t{categories_str}")
                else:
                    print("No notes found.")
                input("Press Enter to continue...")
            elif choice == '5':
                os.system('cls')
                start_date = input("Enter start date (YYYY-MM-DD): ")
                end_date = input("Enter end date (YYYY-MM-DD): ")

                notes = self.db.filterNotesByDate(start_date, end_date)
                if notes:
                    os.system('cls')
                    print("Note ID\tTitle\t\tContent\t\tCategories")
                    print("-----------------------------------------------")
                    for note in notes:
                        note_id = note[0]
                        title = note[1]
                        content = note[2]
                        categories = self.db.getNoteCategories(note_id)
                        categories_str = ', '.join(categories) if categories else "N/A"
                        print(f"{note_id}\t{title}\t\t{content}\t\t{categories_str}")
                else:
                    print("No notes found.")
                input("Press Enter to continue...")
            elif choice == '6':
                os.system('cls')
                notes = self.db.getAllNotes(self.user_id)
                if notes:
                    os.system('cls')
                    print("Note ID\tTitle\t\tContent\t\tCategories")
                    print("-----------------------------------------------")
                    for note in notes:
                        note_id = note[0]
                        title = note[1]
                        content = note[2]
                        categories = self.db.getNoteCategories(note_id)
                        categories_str = ', '.join(categories) if categories else "N/A"
                        print(f"{note_id}\t{title}\t\t{content}\t\t{categories_str}")
                else:
                    print("No notes found.")
                input("Press Enter to continue...")
            elif choice == '7':
                os.system('cls')
                break
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")

    def groups_menu(self):
        while True:
            os.system('cls')
            print("1. Create Group")
            print("2. Delete Group")
            print("3. Add Note to Group")
            print("4. View All Groups and Notes")
            print("5. Back")

            choice = input("\nEnter your choice: ")

            if choice == '1':
                name = input("Enter group name: ")

                result = self.db.createGroup(name)
                print(result)
                input("Press Enter to continue...")
            elif choice == '2':
                group_id = int(input("Enter group ID: "))

                result = self.db.deleteGroup(group_id)
                print(result)
                input("Press Enter to continue...")
            elif choice == '3':
                note_id = int(input("Enter note ID: "))
                group_id = int(input("Enter group ID: "))

                result = self.db.addNoteToGroup(note_id, group_id)
                print(result)
                input("Press Enter to continue...")
            elif choice == '4':
                groups = self.db.getAllGroups()
                if groups:
                    os.system('cls')
                    print("Group ID\tName")
                    print("------------------------")
                    for group in groups:
                        group_id = group[0]
                        name = group[1]
                        print(f"{group_id}\t\t{name}")
                        notes = self.db.getNotesInGroup(group_id)
                        if notes:
                            print("Notes:")
                            for note in notes:
                                note_id = note[0]
                                title = note[1]
                                content = note[2]
                                print(f"Note ID: {note_id}")
                                print(f"Title: {title}")
                                print(f"Content: {content}")
                                print("---------------------")
                        else:
                            print("No notes in this group.")
                        print("---------------------")
                else:
                    print("No groups found.")
                input("Press Enter to continue...")
            elif choice == '5':
                break
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")

    def categories_menu(self):
        while True:
            os.system('cls')
            print("1. Create Category")
            print("2. Delete Category")
            print("3. Assign Category to Note")
            print("4. Back")

            choice = input("\nEnter your choice: ")

            if choice == '1':
                name = input("Enter category name: ")

                result = self.db.createCategory(name)
                print(result)
                input("Press Enter to continue...")
            elif choice == '2':
                category_id = int(input("Enter category ID: "))

                result = self.db.deleteCategory(category_id)
                print(result)
                input("Press Enter to continue...")
            elif choice == '3':
                note_id = int(input("Enter note ID: "))
                category_id = int(input("Enter category ID: "))

                result = self.db.assignCategoryToNote(note_id, category_id)
                print(result)
                input("Press Enter to continue...")
            elif choice == '4':
                break
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")

app = Application()
app.authentication_menu()
