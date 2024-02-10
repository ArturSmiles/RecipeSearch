import tkinter as tk
import customtkinter as ctk
from CTkListbox import *
from tkinter import ttk
import requests
import webbrowser


def callback1(meal):
    # Send the API request
    response = requests.get(
        f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal}")
    data = response.json()
    # If Meal has a Link - Open browser to Meal Link
    if data["meals"][0]["strSource"] != None:
        webbrowser.open(data["meals"][0]["strSource"])


def get_ingredients():
    # Send the API request
    response = requests.get(
        "https://www.themealdb.com/api/json/v1/1/list.php?i=list")
    data = response.json()

    # Collect and save all the Ingredients
    ingredients = [""]
    for i in data["meals"]:
        ingredients.append(i["strIngredient"])
    ingredient_combobox.configure(values=ingredients)


def get_recipes():
    # Get user input
    category = category_combobox.get()
    cuisine = cuisine_combobox.get()
    ingredient = ingredient_combobox.get()

    # Construct the API request URL
    base_url = "https://www.themealdb.com/api/json/v1/1/filter.php"
    params = {}
    if category:
        params["c"] = category
    if cuisine:
        params["a"] = cuisine
    if ingredient:
        params["i"] = ingredient

    # Send the API request
    response = requests.get(base_url, params=params)
    data = response.json()

    # Display the recipe recommendations
    recipe_listbox.delete(0, tk.END)
    if 'meals' in data:
        for meal in data['meals']:
            recipe_listbox.insert(tk.END, meal['strMeal'])


# Create the main window
root = ctk.CTk()
root.title("Recipe Search System")

# Create and place widgets
category_label = ctk.CTkLabel(root, text="Category:")
category_label.grid(row=0, column=0, padx=5, pady=5, sticky="E")

category_combobox = ctk.CTkComboBox(root, values=[
    "", "Beef", "Chicken", "Dessert", "Lamb", "Pasta", "Seafood", "Vegetarian"])
category_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="W")

cuisine_label = ctk.CTkLabel(root, text="Cuisine:")
cuisine_label.grid(row=1, column=0, padx=5, pady=5, sticky="E")

cuisine_combobox = ctk.CTkComboBox(root, values=[
    "", "American", "British", "Chinese", "Greek", "Indian", "Italian", "Mexican", "Spanish"])
cuisine_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="W")

ingredient_label = ctk.CTkLabel(root, text="Ingredient:")
ingredient_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")

ingredient_combobox = ctk.CTkComboBox(root, values=[""])
ingredient_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="W")

search_button = ctk.CTkButton(root, text="Get Recipes", command=get_recipes)
search_button.grid(row=3, columnspan=2, pady=10)

recipe_listbox = CTkListbox(
    root, width=300, height=10, text_color="black", command=callback1)
recipe_listbox.grid(row=4, columnspan=5, padx=5, pady=5)


# Run the application
get_ingredients()
root.mainloop()
