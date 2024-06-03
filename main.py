import customtkinter as ctk
from tkinter import messagebox
import os


def generate_key_from_password(password):
    key = 0
    for char in password:
        key += ord(char)
    return key

def encrypt(text, password):
    key = generate_key_from_password(password)
    encrypted_text = ''.join(chr((ord(char) + key) % 256) for char in text)
    return encrypted_text

def decrypt(encrypted_text, password):
    key = generate_key_from_password(password)
    decrypted_text = ''.join(chr((ord(char) - key) % 256) for char in encrypted_text)
    return decrypted_text

class CustomInputDialog(ctk.CTkToplevel):
    def __init__(self, master, title, labels, exit_callback):
        super().__init__(master)
        self.iconbitmap('root.ico')
        self.title(title)
        self.geometry("400x350")

        self.entries = {}
        for i, label in enumerate(labels):
            ctk.CTkLabel(self, text=label).pack(pady=(20 if i == 0 else 10, 5))
            entry = ctk.CTkEntry(self, show='*' if 'Password' in label or 'Key' in label else None)
            entry.pack(pady=5)
            self.entries[label] = entry

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit)
        self.submit_button.pack(pady=20)

        self.exit_button = ctk.CTkButton(self, text="Exit", command=exit_callback)
        self.exit_button.pack(pady=10)

        self.result = None

        # Grab the focus for this window
        self.grab_set()

    def submit(self):
        self.result = {label: entry.get() for label, entry in self.entries.items()}
        if any(value == '' for value in self.result.values()):
            messagebox.showerror("Error", "All fields must be filled!")
        else:
            self.destroy()


class PasswordViewWindow(ctk.CTkToplevel):
    def __init__(self, master, title, data):
        super().__init__(master)
        self.iconbitmap('root.ico')
        self.title(title)
        self.geometry("600x400")

        # Header
        header = ctk.CTkLabel(self, text="Saved Information", font=("Arial", 18))
        header.pack(pady=20)

        # Create a frame for the table
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Add column headers
        headers = ["Website", "Username", "Password"]
        for i, header_text in enumerate(headers):
            label = ctk.CTkLabel(table_frame, text=header_text, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=10, pady=5)

        # Add data rows
        for row_num, entry in enumerate(data, start=1):
            website, username, password = entry.split(" | ")
            website = website.split(": ")[1]
            username = username.split(": ")[1]
            password = password.split(": ")[1]
            
            labels = [website, username, password]
            for col_num, text in enumerate(labels):
                label = ctk.CTkLabel(table_frame, text=text, font=("Arial", 12))
                label.grid(row=row_num, column=col_num, padx=10, pady=5)

        # Exit button
        self.exit_button = ctk.CTkButton(self, text="Exit", command=self.destroy)
        self.exit_button.pack(pady=20)


class PasswordManager:
    def __init__(self, master):
        self.master = master
        master.iconbitmap('root.ico')
        master.title("Password Manager")
        master.geometry("500x400")

        self.data_file = "passwords.txt"

        # UI Elements
        self.label = ctk.CTkLabel(master, text="Encryptix Password Manager", font=("Arial", 24))
        self.label.pack(pady=40)

        self.add_button = ctk.CTkButton(master, text="Add Password", command=self.add_password, width=200)
        self.add_button.pack(pady=10)

        self.view_button = ctk.CTkButton(master, text="View Passwords", command=self.view_passwords, width=200)
        self.view_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(master, text="Delete Password", command=self.delete_password, width=200)
        self.delete_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(master, text="Exit", command=self.exit_program, width=200)
        self.exit_button.pack(pady=10)

        self.copyright_label = ctk.CTkLabel(master, text="© 2024 Encryptix. All rights reserved.", font=("Arial", 12))
        self.copyright_label.pack(side="bottom", pady=10)

    def add_password(self):
        def exit_callback():
            dialog.destroy()

        dialog = CustomInputDialog(self.master, "Add Password", ["Encryption Key", "Website", "Username", "Password"], exit_callback)
        dialog.geometry("400x480")  # Adjust the geometry of the dialog window
        self.master.wait_window(dialog)
        result = dialog.result

        if result:
            key = result["Encryption Key"]
            website = result["Website"]
            username = result["Username"]
            password = result["Password"]

            entry = f"Website: {website} | Username: {username} | Password: {password}\n"
            encrypted_entry = encrypt(entry, key)

            with open(self.data_file, "ab") as f:
                f.write(encrypted_entry.encode('latin1'))

            messagebox.showinfo("Success", "Password added successfully!")

    def view_passwords(self):
        def exit_callback():
            dialog.destroy()

        if not os.path.exists(self.data_file):
            messagebox.showerror("Error", "No passwords found!")
            return

        dialog = CustomInputDialog(self.master, "View Passwords", ["Encryption Key"], exit_callback)
        dialog.geometry("400x350")  # Adjust the geometry of the dialog window
        self.master.wait_window(dialog)
        result = dialog.result

        if result:
            key = result["Encryption Key"]

            with open(self.data_file, "rb") as f:
                encrypted_data = f.read().decode('latin1')

            try:
                decrypted_data = decrypt(encrypted_data, key)
                entries = decrypted_data.strip().split('\n')
                PasswordViewWindow(self.master, "Saved Passwords", entries)
            except ValueError:
                messagebox.showerror("Error", "Invalid encryption key!")

    def delete_password(self):
        def exit_callback():
            dialog.destroy()

        dialog = CustomInputDialog(self.master, "Delete Password", ["Encryption Key", "Website"], exit_callback)
        dialog.geometry("400x350")  # Adjust the geometry of the dialog window
        self.master.wait_window(dialog)
        result = dialog.result

        if result:
            key = result["Encryption Key"]
            website = result["Website"]

            if not os.path.exists(self.data_file):
                messagebox.showerror("Error", "No passwords found!")
                return

            with open(self.data_file, "rb") as f:
                encrypted_data = f.read().decode('latin1')

            try:
                decrypted_data = decrypt(encrypted_data, key)
                lines = decrypted_data.split('\n')
                updated_lines = [line for line in lines if website not in line]

                if len(lines) == len(updated_lines):
                    messagebox.showinfo("Info", "Website not found!")
                else:
                    encrypted_lines = '\n'.join(encrypt(line, key) for line in updated_lines)
                    with open(self.data_file, "wb") as f:
                        f.write(encrypted_lines.encode('latin1'))
                    messagebox.showinfo("Success", "Password deleted successfully!")
            except ValueError:
                messagebox.showerror("Error", "Invalid encryption key!")

    def exit_program(self):
        self.master.destroy()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark") 
    ctk.set_default_color_theme("dark-blue") 
    root = ctk.CTk()
    password_manager = PasswordManager(root)
    root.mainloop()
