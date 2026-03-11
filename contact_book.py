import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.contacts = []
        self.load_contacts()

        # GUI Elements
        self.listbox = tk.Listbox(root, width=50, height=15)
        self.listbox.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Contact", command=self.add_contact)
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.view_button = tk.Button(root, text="View Details", command=self.view_contact)
        self.view_button.pack(side=tk.LEFT, padx=10)

        self.search_button = tk.Button(root, text="Search Contact", command=self.search_contact)
        self.search_button.pack(side=tk.LEFT, padx=10)

        self.update_button = tk.Button(root, text="Update Contact", command=self.update_contact)
        self.update_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(root, text="Delete Contact", command=self.delete_contact)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.refresh_list()

    def load_contacts(self):
        if os.path.exists('contacts.json'):
            with open('contacts.json', 'r') as f:
                self.contacts = json.load(f)

    def save_contacts(self):
        with open('contacts.json', 'w') as f:
            json.dump(self.contacts, f, indent=4)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def add_contact(self):
        name = simpledialog.askstring("Add Contact", "Enter name:")
        if not name:
            return
        phone = simpledialog.askstring("Add Contact", "Enter phone number:")
        if not phone:
            return
        email = simpledialog.askstring("Add Contact", "Enter email:")
        address = simpledialog.askstring("Add Contact", "Enter address:")

        contact = {
            'name': name,
            'phone': phone,
            'email': email,
            'address': address
        }
        self.contacts.append(contact)
        self.save_contacts()
        self.refresh_list()
        messagebox.showinfo("Success", "Contact added successfully!")

    def view_contact(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to view.")
            return
        index = selected[0]
        contact = self.contacts[index]
        details = f"Name: {contact['name']}\nPhone: {contact['phone']}\nEmail: {contact['email']}\nAddress: {contact['address']}"
        messagebox.showinfo("Contact Details", details)

    def search_contact(self):
        query = simpledialog.askstring("Search Contact", "Enter name or phone number:")
        if not query:
            return
        results = [c for c in self.contacts if query.lower() in c['name'].lower() or query in c['phone']]
        if not results:
            messagebox.showinfo("Search Results", "No contacts found.")
            return
        result_text = "\n\n".join([f"Name: {c['name']}\nPhone: {c['phone']}\nEmail: {c['email']}\nAddress: {c['address']}" for c in results])
        messagebox.showinfo("Search Results", result_text)

    def update_contact(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to update.")
            return
        index = selected[0]
        contact = self.contacts[index]

        name = simpledialog.askstring("Update Contact", "Enter new name:", initialvalue=contact['name'])
        if name:
            contact['name'] = name
        phone = simpledialog.askstring("Update Contact", "Enter new phone:", initialvalue=contact['phone'])
        if phone:
            contact['phone'] = phone
        email = simpledialog.askstring("Update Contact", "Enter new email:", initialvalue=contact['email'])
        if email:
            contact['email'] = email
        address = simpledialog.askstring("Update Contact", "Enter new address:", initialvalue=contact['address'])
        if address:
            contact['address'] = address

        self.save_contacts()
        self.refresh_list()
        messagebox.showinfo("Success", "Contact updated successfully!")

    def delete_contact(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to delete.")
            return
        index = selected[0]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {self.contacts[index]['name']}?")
        if confirm:
            del self.contacts[index]
            self.save_contacts()
            self.refresh_list()
            messagebox.showinfo("Success", "Contact deleted successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()