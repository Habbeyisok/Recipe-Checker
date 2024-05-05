import pickle
import os

class Recipe:
    def __init__(self):
        self.name = input("\nName of meal:\n")
        self.ingredients = {}
        ingredient = add_ingredient()
        while ingredient.casefold() != "finished":
            self.ingredients[ingredient] = int_validator("How much? (Standard units = g, ml, pieces)\n")
            ingredient = add_ingredient()
        self.servings = int_validator("How many does it serve?\n")
    
    def print_recipe(self):
        print("\nRecipe:", self.name)
        print("Ingredients:")
        for num, ingredient in self.ingredients.items():
            print(f"{num}. {ingredient}")
        print("Serves", self.servings)

class Fridge:
    def __init__(self):
        self.ingredients = {}
        

    def print_fridge(self):
        print("Ingredients:")
        for num, ingredient in self.ingredients.items():
            print(f"{num}. {ingredient}")
            
if os.path.getsize('recipes.pkl') == 0:
    recipes = []
else:
    with open('recipes.pkl', 'rb') as f:
        recipes = pickle.load(f)

if os.path.getsize('fridge.pkl') == 0:
    fridge = Fridge()
else:
    with open('fridge.pkl', 'rb') as f:
        fridge = pickle.load(f)

def int_validator(question):
    user_input = input(question)
    while not user_input.isdigit():
        print("Invalid Input! Try again:")
        user_input= input(question)
            
    user_input = int(user_input)
    return user_input
        
def add_ingredient():
    ingredient = input("\nAdd an ingredient (In singular form).\nEnter 'finished' when done:\n")
    return ingredient_validator(ingredient)
    

def ingredient_validator(ingredient):
    
    if ingredient.casefold() == "finished":
        return ingredient
    else:
        with open("total_ingredients.txt", "r+") as f:
            # Check if the ingredient is already in the file
            if any(ingredient.casefold() == line.strip().casefold() for line in f):
                print("Found")
                return ingredient
            
            # If the ingredient is not in the file, ask the user if they want to add it
            print("That ingredient doesn't appear in the list of known ingredients! Make sure that you have spelled it correctly.")
            print("If you are sure you spelled the ingredient correctly and want to add it to the database, enter 'New'.\nOtherwise try to enter the ingredient again.")
            ingredient = input("")
            if ingredient.casefold() == "new":
                check = False
                while not check:
                    ingredient = input("Write again the new ingredient, ensuring it is spelled correctly:\n")
                    if input("You entered: '{}'. Is this correct? (Y/N)\n".format(ingredient)).casefold() == "y":
                        check = True
                f.seek(0, os.SEEK_END)  # Move the cursor to the end of the file
                f.write("\n" + ingredient)  # Write the new ingredient to the file
                return ingredient
            else:
                return ingredient_validator(ingredient)

        
def fridge_writer():
    with open('fridge.pkl', 'wb') as f:
        pickle.dump(fridge, f) 

def recipe_writer():
    with open('recipes.pkl', 'wb') as f:
        pickle.dump(recipes, f)
        
def add_fridge():
    
    if len(fridge.ingredients) == 0:
        print("\nFridge is empty :(")
    else:
        print("\nCurrent fridge inventory:\n")
        fridge.print_fridge()
        
    ingredient = add_ingredient()
    
    if ingredient.casefold() == "finished":
        fridge_writer()
    else:
        if ingredient in fridge.ingredients:
            quantity = int_validator("\nThere is already some of this ingredient in your fridge!\nHow much of this ingredient is there now? (Standard units = g, ml, pieces)\n")
            if quantity == 0:
                del fridge.ingredients[ingredient]
            else:
                fridge.ingredients[ingredient] = quantity
        else:
            quantity = int_validator("How much? (Standard units = g, ml, pieces)\n")
            if quantity != 0:
                fridge.ingredients[ingredient] = quantity                
        add_fridge()
    fridge_writer()
        
def recipe_checker():
    recipe_counter = 0
    for recipe in recipes:
        ingredient_proportions = []
        counter = 0
        for ingredient, quantity in recipe.ingredients.items():
            if ingredient in fridge.ingredients and fridge.ingredients[ingredient] >= quantity:
                counter += 1
                ingredient_proportions.append(fridge.ingredients[ingredient]/quantity)
            else:
                # If the ingredient is not in the fridge, break out of the loop
                counter = 0
                break
        if counter == len(recipe.ingredients):
            recipe_counter += 1
            minimum_serving = min(ingredient_proportions)
            recipe.print_recipe()
            print("You can make a maximum of " + str(int((minimum_serving*(recipe.servings)))) + " servings!")
    if recipe_counter == 0:
        print("\nYou don't have enough ingredients in your fridge to make any of the listed recipes.")
                
    
def print_recipes():
    
    if len(recipes) == 0:
        print("\nNo Recipes uploaded :(\n")
        return
    else:
        print("\nRecipes:")
        for recipe in recipes:
            recipe.print_recipe()
            print("")
        return

def add_recipe():
    
    recipe = Recipe()
    recipes.append(recipe)
    recipe.print_recipe()
    answer = ""
    while (answer.casefold() != "y") or (answer.casefold() != "n"):
        answer = input("Would you like to add another recipe? (y/n)\n")
        if answer.casefold() == "y":
            add_recipe()
        elif answer.casefold() == "n":
            recipe_writer()
            return
        else:
            print("Invalid Input!")

def remove_recipe():
    print_recipes()
    
    if len(recipes) == 0:
        return
    else:
        print("Enter the name of the recipe you would like to remove (enter 'finished' to stop):")
        answer = input("").strip().casefold()
        if answer == "finished":
            return
        else:
            found = False
            for recipe in recipes:
                if recipe.name.casefold().strip() == answer:
                    recipes.remove(recipe)
                    recipe_writer()  # Save the updated recipes list to the file
                    found = True
                    break  # Exit loop once the recipe is found and removed
            if not found:
                print("\nThat recipe does not exist in the list. Try again and ensure you spelled it correctly.")
            remove_recipe()  # Continue removing recipes until the user inputs "finished"


def menu():
    print("\n-------------------------------------------")
    user_input = int_validator("What would you like to do today?\n1. Find what recipes are available\n2. Update the fridge inventory\n3. Add a new recipe\n4. Remove a recipe\n5. View all recipes and fridge inventory\n6. End program\n-------------------------------------------\n")
    
    if user_input == 1:
        recipe_checker()
        menu()
    elif user_input == 2:      
        add_fridge()
        menu()
    elif user_input == 3:
        add_recipe()
        menu()
    elif user_input == 4:
        remove_recipe()
        menu()
    elif user_input == 5:
        print_recipes()
        if len(fridge.ingredients) == 0:
            print("Fridge is empty :(")
            menu()
        else:
            print("Fridge Inventory:\n")
            fridge.print_fridge()
            menu()
    elif user_input == 6:
        print("Closing program...")
        return
    else:
        print("Invalid input\n")
        menu()
    
menu()    
