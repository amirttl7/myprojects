import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

# دیکشنری برای ذخیره لیست‌ها و آیتم‌هایشان
categories = {}

# افزودن لیست جدید
def add_category():
    category_name = category_entry.get()
    if category_name:
        categories[category_name] = []
        category_list.insert(tk.END, category_name)
        category_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("هشدار", "لطفاً نام لیست را وارد کنید!")

# انتخاب یک لیست
def on_category_select(event):
    selected_index = category_list.curselection()
    if selected_index:
        selected_category = category_list.get(selected_index)
        update_items_list(selected_category)

# افزودن آیتم به لیست انتخاب‌شده
def add_item():
    selected_index = category_list.curselection()
    if selected_index:
        selected_category = category_list.get(selected_index)
        name = name_entry.get()
        date = date_entry.get()
        price = price_entry.get()
        if name and date and price:
            item = {"name": name, "date": date, "price": price}
            categories[selected_category].append(item)
            update_items_list(selected_category)
            name_entry.delete(0, tk.END)
            date_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("هشدار", "لطفاً تمام فیلدها را پر کنید!")
    else:
        messagebox.showwarning("هشدار", "لطفاً یک لیست را انتخاب کنید!")

# به‌روزرسانی لیست آیتم‌ها
def update_items_list(category_name):
    items_list.delete(*items_list.get_children())
    for item in categories[category_name]:
        items_list.insert("", tk.END, values=(item["name"], item["date"], item["price"]))

# ذخیره اطلاعات به فایل
def save_to_file():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(categories, file, ensure_ascii=False, indent=4)  # ذخیره با کدگذاری UTF-8
            messagebox.showinfo("ذخیره شد", "اطلاعات با موفقیت ذخیره شد!")
        else:
            messagebox.showwarning("هشدار", "مسیر فایل انتخاب نشد.")
    except Exception as e:
        messagebox.showerror("خطا", f"مشکلی هنگام ذخیره رخ داد: {e}")

# بارگذاری اطلاعات از فایل
def load_from_file():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)  # بارگذاری اطلاعات از فایل
                if isinstance(data, dict):  # بررسی اینکه داده‌های بارگذاری شده یک دیکشنری هستند
                    categories.clear()
                    categories.update(data)
                    category_list.delete(0, tk.END)
                    for category in categories:
                        category_list.insert(tk.END, category)
                    messagebox.showinfo("بارگذاری شد", "اطلاعات با موفقیت بارگذاری شد!")
                else:
                    messagebox.showerror("خطا", "فرمت فایل JSON درست نیست!")
    except json.JSONDecodeError:
        messagebox.showerror("خطا", "فایل JSON نامعتبر است!")
    except Exception as e:
        messagebox.showerror("خطا", f"یک خطای غیرمنتظره رخ داد: {e}")

# رابط کاربری
root = tk.Tk()
root.title("PLM (purchase list manager)")

# رابط کاربری اصلی
ttk.Label(root, text="نام لیست جدید:").grid(row=0, column=0)
category_entry = ttk.Entry(root)
category_entry.grid(row=0, column=1)
add_category_button = ttk.Button(root, text="اضافه کردن لیست", command=add_category)
add_category_button.grid(row=0, column=2)

category_list = tk.Listbox(root, height=5)
category_list.grid(row=1, column=0, columnspan=3)
category_list.bind("<<ListboxSelect>>", on_category_select)

# تعریف آیتم‌ها
ttk.Label(root, text="نام آیتم:").grid(row=2, column=0)
name_entry = ttk.Entry(root)
name_entry.grid(row=2, column=1)

ttk.Label(root, text="تاریخ (yyyy-mm-dd):").grid(row=3, column=0)
date_entry = ttk.Entry(root)
date_entry.grid(row=3, column=1)

ttk.Label(root, text="مبلغ:").grid(row=4, column=0)
price_entry = ttk.Entry(root)
price_entry.grid(row=4, column=1)

add_item_button = ttk.Button(root, text="اضافه کردن آیتم", command=add_item)
add_item_button.grid(row=5, column=0, columnspan=2)

# نمایش آیتم‌های یک لیست
items_list = ttk.Treeview(root, columns=("name", "date", "price"), show="headings")
items_list.heading("name", text="نام آیتم")
items_list.heading("date", text="تاریخ")
items_list.heading("price", text="مبلغ")
items_list.grid(row=6, column=0, columnspan=3)

# افزودن دکمه‌های ذخیره و بارگذاری
save_button = ttk.Button(root, text="ذخیره به فایل", command=save_to_file)
save_button.grid(row=7, column=0, columnspan=1)

load_button = ttk.Button(root, text="بارگذاری فایل", command=load_from_file)
load_button.grid(row=7, column=1, columnspan=1)

root.mainloop()