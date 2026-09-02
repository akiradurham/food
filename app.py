import streamlit as st
import json
import os

# recipe loader from file
def load_recipes():
    if not os.path.exists("recipes.json"):
        return []

    with open("recipes.json") as file:
        return json.load(file)

# save recipes to file
def save_recipe(recipes):
    with open("recipes.json", "w") as file:
        return json.dump(recipes, file, indent = 4)

# app
st.title("My Recipe App")

recipes = load_recipes()

st.sidebar.header("Menu")

st.divider()

page = st.sidebar.radio("Select a page", ["Recipes", "Add Recipe"])

# recipe page
if page == "Recipes":
    st.header("Recipes")

    search = st.text_input("Search recipes...")

    filtered_recipes = recipes
    if search:
        filtered_recipes = [recipe for recipe in recipes if search.lower() in recipe["name"].lower()]

    if not filtered_recipes:
        st.write("No saved recipes found")

    for recipe in filtered_recipes:
        with st.expander(recipe["name"]):

            st.write(f"**Cooking time:** {recipe["time"]}")

            st.subheader("Ingredients")
            for ingredient in recipe["ingredients"]:
                st.write(f"- {ingredient}")

            st.subheader("Instructions")
            for instruction in recipe["instructions"]:
                st.write(f"- {instruction}")

# add recipe page
elif page == "Add Recipe":
    st.header("Add a Recipe")
    with st.form("add_recipe_form"):
        name = st.text_input("Recipe Name")
        time = st.number_input("Cooking time in minutes", min_value=1)
        ingredients = st.text_area("Ingredients")
        instructions = st.text_area("Instructions")
        submitted = st.form_submit_button("Save Recipe")

    if submitted:
        if not name or not time or not ingredients or not instructions:
            st.error("Please fill out all fields")
        else:
            new_recipe = {
                "name": name,
                "time": time,
                "ingredients": ingredients.split("\n"),
                "instructions": instructions.split("\n")
            }
            recipes.append(new_recipe)
            save_recipe(recipes)
            st.rerun()
            st.success("Recipe saved!")
