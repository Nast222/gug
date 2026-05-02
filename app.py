import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import json

FAVORITES_FILE = "favorites.json"

def load_favorites():
    try:
        with open(FAVORITES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_favorites(favorites):
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f, indent=2)

def search_user():
    username = entry_search.get().strip()
    if not username:
        messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым")
        return

    try:
        response = requests.get(f"https://api.github.com/users/{username}")
        response.raise_for_status()
        user_data = response.json()
        display_user(user_data)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка", f"Пользователь не найден или ошибка сети: {e}")

def display_user(user_data):
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Логин: {user_data.get('login')}\n")
    result_text.insert(tk.END, f"Имя: {user_data.get('name')}\n")
    result_text.insert(tk.END, f"Био: {user_data.get('bio')}\n")
    result_text.insert(tk.END, f"Подписчики: {user_data.get('followers')}\n")
    result_text.insert(tk.END, f"URL: {user_data.get('html_url')}\n")

def add_to_favorites():
    username = entry_search.get().strip()
    if not username:
        messagebox.showwarning("Ошибка", "Введите имя пользователя")
        return

    favorites = load_favorites()
    if username in favorites:
        messagebox.showinfo("Информация", "Пользователь уже в избранном")
        return

    favorites.append(username)
    save_favorites(favorites)
    messagebox.showinfo("Успех", "Пользователь добавлен в избранное")

def show_favorites():
    favorites = load_favorites()
    if not favorites:
        messagebox.showinfo("Избранное", "Избранных пользователей нет")
        return

    fav_window = tk.Toplevel(root)
    fav_window.title("Избранные пользователи")
    for user in favorites:
        tk.Label(fav_window, text=user).pack()

# --- GUI ---
root = tk.Tk()
root.title("GitHub User Finder")

tk.Label(root, text="Поиск пользователя:").grid(row=0, column=0, padx=10, pady=10)
entry_search = tk.Entry(root, width=30)
entry_search.grid(row=0, column=1, padx=10, pady=10)

tk.Button(root, text="Поиск", command=search_user).grid(row=0, column=2, padx=5, pady=5)
tk.Button(root, text="В избранное", command=add_to_favorites).grid(row=0, column=3, padx=5, pady=5)
tk.Button(root, text="Показать избранное", command=show_favorites).grid(row=1, column=3, padx=5, pady=5)

result_text = tk.Text(root, height=10, width=50)
result_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
