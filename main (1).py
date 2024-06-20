import json
import os
import tkinter as tk
from tkinter import messagebox

import bcrypt

# Sample recipes data
recipes = {
    "Kartupeļi ar dilli": {
        "Sastāvdaļas": {
            "Kartupeļi": "500g",
            "Dilles": "1 bunte",
            "Sāls": "pēc garšas",
        },
        "Kā pagatavot": [
            "1. Nomazgājiet un nomizojiet kartupeļus.",
            "2. Sagrieziet kartupeļus uz pusēt un lieciet vārīties uz 40.min.",
            "3. Pēc tam sagrieziet dilles.",
            "4. Kad kartupeļi gatavi, nokāsiet tos un uzberiet virsū dilles.",
            "5. Uzberiet šķipsniņu sāls un pasniedziet.",
        ]
    },
    "Makaroni ar sieru": {
        "Sastāvdaļas": {
            "Makaroni": "200g",
            "Siers": "200g",
        },
        "Kā pagatavot": [
            "1. Katlā uzvāriet makaronus.",
            "2. Sarīvējiet sieru.",
            "2. Kad gatavi makaroni nokāsiet un pievienojiet sarīvēto sieru",
            "3. Pasniedzat siltus.",
        ]
    },
    "Gurķu un tomātu salāti": {
        "Sastāvdaļas": {
            "Tomāti": "200g",
            "Gurķis": "200g",
            "Skābais krējums": "50g",
            "Sāls": "pēc garšas",
        },
        "Kā pagatavot": [
            "1. Sgriež gurķi un tomātu pus kumosa gabaliņos.",
            "2. Sliek vienā bļodā.",
            "3. Pieliek krējumu un sāli.",
            "4. Samaisa un pasniedz.",
        ]
    },
    "Katupeļu biezputra": {
        "Sastāvdaļas": {
            "Kartupeļi": "500g",
            "Saldais krējums": "100ml",
            "Sāls": "pēc garšas",
        },
        "Kā pagatavot": [
            "1.Nomizo un izvāra kartupeļus.",
            "2.Nokāš un pieliek saldo krējumu un sāli.",
            "3.Saspaida un maisa līdz izveidojas viendabīga konsistence.",
            "4.Pasniedz siltu.",
        ]

        
    }
}

# Path to the JSON file
users_file = 'users.json'

# Check if the users.json file exists, if not create it
if not os.path.exists(users_file):
    with open(users_file, 'w') as file:
        json.dump({"users": []}, file)

def load_users():
    with open(users_file, 'r') as file:
        return json.load(file)

def save_users(users_data):
    with open(users_file, 'w') as file:
        json.dump(users_data, file)

def register_user(username, password):
    users_data = load_users()
    for user in users_data["users"]:
        if user["username"] == username:
            return False  # Lietotājs jau eksistē
    hashed_password = (
        bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        .decode('utf-8')
    )
    users_data["users"].append({"username": username, "password": hashed_password})
    save_users(users_data)
    return True

def login_user(username, password):
    users_data = load_users()
    for user in users_data["users"]:
        if user["username"] == username and \
        bcrypt.checkpw(password.encode('utf-8'),
                       user["password"].encode('utf-8')):
            return True
    return False

def show_login_window():
    login_window = tk.Toplevel(root)
    login_window.title("Pieslēgties")
    login_window.configure(bg="wheat")

    tk.Label(login_window, text="Lietotājvārds", bg="wheat").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Parole", bg="wheat").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        if login_user(username, password):
            messagebox.showinfo("Success", "Pieslēgšanās veiksmīga!")
            login_window.destroy()
            show_main_application(username)
        else:
            messagebox.showerror("Error", "Nepareizs lietotājvārds vai parole")

    tk.Button(
        login_window,
        text="Pieslēgties",
        command=handle_login,
        bg="wheat"
    ).pack(pady=20)

def show_register_window():
    register_window = tk.Toplevel(root)
    register_window.title("Reģistrēties")
    register_window.configure(bg="wheat")

    tk.Label(register_window, text="Lietotājvārds", bg="wheat").pack(pady=5)
    username_entry = tk.Entry(register_window)
    username_entry.pack(pady=5)

    tk.Label(register_window, text="Parole", bg="wheat").pack(pady=5)
    password_entry = tk.Entry(register_window, show="*")
    password_entry.pack(pady=5)

    def handle_register():
        username = username_entry.get()
        password = password_entry.get()
        if register_user(username, password):
            messagebox.showinfo("Success", "Reģistrācija veiksmīga!")
            register_window.destroy()
        else:
            messagebox.showerror("Error", "Lietotājvārds jau eksistē")

    tk.Button(register_window, text="Reģistrēties",
              command=handle_register, bg="wheat").pack(pady=20)

def custom_messagebox(title, message, bg_color="wheat"):
    popup = tk.Toplevel()
    popup.title(title)
    popup.configure(bg=bg_color)

    label = tk.Label(popup, text=message, bg=bg_color, font=("Arial", 12))
    label.pack(pady=10, padx=10)

    button = tk.Button(popup, text="OK", command=popup.destroy, bg="wheat")
    button.pack(pady=5)

    popup.transient(root)  
    popup.grab_set()  
    root.wait_window(popup)  
    popup.grab_release()  

def save_selections():
    # Get selected items
    selected_items = [listbox.get(i) for i in listbox.curselection()]

    if selected_items:
        # Find matching recipes
        matching_recipes = find_recipes(selected_items)
        if matching_recipes:
            custom_messagebox(
                "Izvēlētās sastāvdaļas",
                "Jūs esat izvēlējušies: " + ", ".join(selected_items),
                bg_color="oldlace"
            )
            for recipe_name in matching_recipes:
                show_recipe_details(recipe_name)
        else:
            custom_messagebox(
                "Pieejamās receptes",
                "Nav pieejamu recepšu ar izvēlētajām sastāvdaļām.",
                bg_color="oldlace"
            )
    else:
        custom_messagebox(
            "Nēesat izvelejies sastāvdaļu",
            "Lūdzu atzīmējiet vismaz vienu produktu.",
            bg_color="oldlace"
        )

def find_recipes(selected_items):
    matching_recipes = []
    for recipe, details in recipes.items():
        # Check if all selected items are in the recipe's ingredients
        if all(item in details["Sastāvdaļas"] for item in selected_items):
            matching_recipes.append(recipe)
    return matching_recipes

def show_recipe_details(recipe_name):
    # Create a new window for displaying recipe details
    recipe_window = tk.Toplevel()
    recipe_window.title(recipe_name)
    recipe_window.configure(bg="wheat") 

    # Display recipe name
    recipe_name_label = tk.Label(
        recipe_window,
        text=recipe_name,
        font=("Arial", 14, "bold"),
        anchor='w',
        bg="wheat"
    )
    recipe_name_label.pack(pady=10)

    # Display ingredients
    ingredients_label = tk.Label(
        recipe_window,
        text="Sastāvdaļas:",
        font=("Arial", 12, "underline"),
        anchor='w',
        bg="wheat")
    ingredients_label.pack(
        anchor='w',
        padx=20
    )
    ingredients_text = "\n".join(
        [
            f"{ingredient}: {quantity}"
            for ingredient, quantity in recipes[recipe_name]["Sastāvdaļas"].items()
        ])
    ingredients_label_details = tk.Label(
        recipe_window,
        text=ingredients_text,
        anchor='w',
        justify='left',
        bg="wheat"
    )
    ingredients_label_details.pack(
        anchor='w',
        padx=20
    )

    # Display preparation steps
    steps_label = tk.Label(
        recipe_window,
        text="Kā pagatavot:",
        font=("Arial", 12, "underline"),
        anchor='w',
        bg="wheat"
    )
    steps_label.pack(
        anchor='w',
        padx=20
    )
    steps_text = "\n".join(recipes[recipe_name]["Kā pagatavot"])
    steps_label_details = tk.Label(
        recipe_window,
        text=steps_text,
        anchor='w',
        justify='left',
        bg="wheat"
    )
    steps_label_details.pack(
        anchor='w',
        padx=20
    )

def show_main_application(username):
    main_app = tk.Toplevel()
    main_app.title("Viedā recepšu grāmata")
    main_app.configure(bg="oldlace")

    main_app.geometry("600x400") 

    # Ingredient selection section
    tk.Label(
        main_app,
        text="Izvēlieties sastāvdaļas:",
        font=("Arial", 14),
        bg="wheat"
    ).pack(pady=10)
    global listbox
    listbox = tk.Listbox(
        main_app, selectmode=tk.MULTIPLE,
        bg="wheat"
    )
    ingredients = [
        "Kartupeļi",
        "Dilles",
        "Sāls",
        "Makaroni",
        "Siers",
        "Saldais krējums",
        "Tomāti",
        "Gurķis",
        "Skābais krējums"
    ]

    for ingredient in ingredients:
        listbox.insert(tk.END, ingredient)
    listbox.pack(pady=10)

    # Display the username
    tk.Label(
        main_app,
        text=f"Sveiki, {username}!",
        font=("Arial", 12),
        bg="wheat"
    ).pack(pady=5)

    def handle_save_selections():
        save_selections()

    tk.Button(
        main_app,
        text="Saglabāt izvēli un iegūt recepti",
        command=handle_save_selections,
        bg="wheat"
    ).pack(pady=20)

# Main application window
root = tk.Tk()
root.title("Reģistrācija/Pieslēgšanās")
root.configure(bg="oldlace")

tk.Label(
    root,
    text="Viedā recepšu grāmata",
    font=("Arial", 18, "bold"),
    bg="oldlace"
).pack(pady=20)
tk.Button(
    root, text="Reģistrēties",
    command=show_register_window,
    bg="wheat"
).pack(pady=10)
tk.Button(
    root,
    text="Pieslēgties",
    command=show_login_window,
    bg="wheat"
).pack(pady=10)

root.mainloop()
