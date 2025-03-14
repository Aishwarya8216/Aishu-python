import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def connect_db():
    try:
        # Connecting to your MySQL database
        return mysql.connector.connect(host="localhost", user="root", password="root", database="footwearshopdb")  # Changed database name
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

def fetch_footwear():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT brand, model, price FROM footwear")  # Changed table name from `icecreams` to `footwear`
        footwear_items = cursor.fetchall()
        conn.close()
        return footwear_items
    return []

def add_footwear():
    brand = brand_entry.get()
    model = model_entry.get()
    price = price_entry.get()
    if brand.lower() == "exit":
        root.quit()
    elif brand and model and price:
        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid price.")
            return
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO footwear (brand, model, price) VALUES (%s, %s, %s)", (brand, model, price))  # Changed table and column names
            conn.commit()
            conn.close()
        footwear_table.insert("", tk.END, values=(brand, model, f"${price:.2f}"))
        brand_entry.delete(0, tk.END)
        model_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)

def add_to_cart():
    selected = footwear_table.selection()
    for item in selected:
        cart_table.insert("", tk.END, values=footwear_table.item(item, "values"))
    calculate_total()

def remove_from_cart():
    for item in cart_table.selection():
        cart_table.delete(item)
    calculate_total()

def calculate_total():
    total = sum(float(cart_table.item(item, "values")[2][1:]) for item in cart_table.get_children())
    total_label.config(text=f"Total: ${total:.2f}")

def checkout():
    if cart_table.get_children():
        messagebox.showinfo("Success", "Purchase Successful!")
        cart_table.delete(*cart_table.get_children())
        total_label.config(text="Total: $0.00")

root = tk.Tk()
root.configure(bg="#f0f8ff")  # Background color changed to a light blue for a fresh look
root.title("Footwear Shop")
root.geometry("600x500")

# Title Label with customized font
title_label = tk.Label(root, text="Welcome to Footwear Shop", font=("Helvetica", 20, "bold"), fg="#2196F3", bg="#f0f8ff")
title_label.pack(pady=20)

# Footwear List Label
footwear_label = tk.Label(root, text="Footwear Available", font=("Arial", 16), fg="black", bg="#f0f8ff")
footwear_label.pack()

# Footwear Table with customized style
footwear_table = ttk.Treeview(root, columns=("Brand", "Model", "Price"), show="headings", height=5)
footwear_table.heading("Brand", text="Brand")
footwear_table.heading("Model", text="Model")
footwear_table.heading("Price", text="Price")
footwear_table.column("Brand", anchor="center")
footwear_table.column("Model", anchor="center")
footwear_table.column("Price", anchor="center")
footwear_table.pack(pady=10)

# Sample Footwear Data
sample_footwear = [
    ("Nike", "Air Max", 120),
    ("Adidas", "Ultraboost", 150),
    ("Puma", "Suede Classic", 80),
    ("Reebok", "Classic Leather", 90),
    ("New Balance", "574", 110)
]

for footwear in sample_footwear:
    footwear_table.insert("", tk.END, values=(footwear[0], footwear[1], f"${footwear[2]:.2f}"))

# Add to Cart Button with customized style
add_cart_button = tk.Button(root, text="Add to Cart", command=add_to_cart, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=3)
add_cart_button.pack(pady=10)

# New Footwear Form Section
new_footwear_label = tk.Label(root, text="Add a New Footwear", font=("Arial", 14, "bold"), fg="black", bg="#f0f8ff")
new_footwear_label.pack(pady=10)

# New Footwear Fields
brand_entry = tk.Entry(root, font=("Arial", 12), bd=2, relief="solid", width=25)
brand_entry.pack(pady=5)

model_entry = tk.Entry(root, font=("Arial", 12), bd=2, relief="solid", width=25)
model_entry.pack(pady=5)

price_entry = tk.Entry(root, font=("Arial", 12), bd=2, relief="solid", width=25)
price_entry.pack(pady=5)

# Add Footwear Button with customized style
add_footwear_button = tk.Button(root, text="Add Footwear", command=add_footwear, bg="#FF9800", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=3)
add_footwear_button.pack(pady=10)

# Cart Section
cart_label = tk.Label(root, text="Cart", font=("Arial", 16), fg="black", bg="#f0f8ff")
cart_label.pack(pady=10)

cart_table = ttk.Treeview(root, columns=("Brand", "Model", "Price"), show="headings", height=5)
cart_table.heading("Brand", text="Brand")
cart_table.heading("Model", text="Model")
cart_table.heading("Price", text="Price")
cart_table.column("Brand", anchor="center")
cart_table.column("Model", anchor="center")
cart_table.column("Price", anchor="center")
cart_table.pack(pady=10)

# Remove Footwear from Cart Button
remove_cart_button = tk.Button(root, text="Remove from Cart", command=remove_from_cart, bg="#F44336", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=3)
remove_cart_button.pack(pady=10)

# Total Price Label
total_label = tk.Label(root, text="Total: $0.00", font=("Arial", 14), fg="#4CAF50", bg="#f0f8ff")
total_label.pack(pady=10)

# Checkout Button
checkout_button = tk.Button(root, text="Checkout", command=checkout, bg="#2196F3", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=3)
checkout_button.pack(pady=20)

root.mainloop()


