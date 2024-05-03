import sys

recipies = {}

class Recipe:
    def __init__(self):
        self.name = input("Name of meal:\n")
        self.ingredients = {}
        no_ingredients = int_validator("How many ingredients are in the meal?\n")
        for i in range (1, (no_ingredients+1)):
            ingredient = input("Add an ingredient:\n")
            self.ingredients[ingredient] = int_validator("How much? (Standard units = g, ml, pieces)\n")
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

fridge = Fridge()

def int_validator(question):
    user_input = input(question)
    while user_input.isdigit() == False:
        print("Invalid Input! Try again:")
        user_input= input(question)
            
    user_input = int(user_input)
    return user_input

def recipe_checker():
    recipe_counter = 0
    for i in range(1, len(recipies) + 1):
        ingredient_proportions = []
        counter = 0
        for ingredient, quantity in recipies[i].ingredients.items():
            if ingredient in fridge.ingredients and fridge.ingredients[ingredient] >= quantity:
                counter += 1
            ingredient_proportions.append(fridge.ingredients[ingredient]/quantity)
        if counter == len(recipies[i].ingredients):
            recipe_counter += 1
            minimum_serving = min(ingredient_proportions)
            recipies[i].print_recipe()
            print("You can make a maximum of " + str(int((minimum_serving*(recipies[i].servings)))) + " servings!")
    if recipe_counter == 0:
        print("\nYou don't have enough ingredients in your fridge to make any of the listed recipies.")
                

def add_fridge():
    finished = False
    print("\nEnter 'Finished' as an ingredient to stop adding ingredients to the fridge.")
    while finished == False:
        ingredient = input("Add an ingredient:\n")
        if ingredient == "Finished" or ingredient == "finished":
            finished = True
        elif ingredient in fridge.ingredients:
            quantity = int_validator("\nThere is already some of this ingredient in your fridge!\nHow much of this ingredient is there now? (Standard units = g, ml, pieces)\n")
            if quantity == 0:
                del fridge.ingredients[ingredient]
            else:
                fridge.ingredients[ingredient] = quantity
        else:
            fridge.ingredients[ingredient] = int_validator("How much? (Standard units = g, ml, pieces)\n")
            
    
def print_recipies():
    
    if len(recipies) == 0:
        print("\nNo recipies uploaded :(")
        return
    else:
        print("\nRecipies:")
        for i in range (1, len(recipies)+1):
            recipies[i].print_recipe()
            print("")
        return

def add_recipe():

    key = 1
    no_recipies = int_validator("How many recipies would you like to add?\n")
    
    for i in range (1, (no_recipies+1)):
        recipe = Recipe()
        while key in recipies.keys():
            key +=1
        recipies[key] = recipe
        recipies[key].print_recipe()
    return

def user_interface():
    print("\n-------------------------------------------")
    user_input = int_validator("What would you like to do today?\n1. Find what recipies are available\n2. Update the fridge inventory\n3. Add a new recipe\n4. View all recipies and fridge inventory\n5. End program\n-------------------------------------------\n")
    
    if user_input == 1:
        recipe_checker()
        user_interface()
    elif user_input == 2:
        
        add_fridge()
        user_interface()
    elif user_input == 3:
        add_recipe()
        user_interface()
    elif user_input == 4:
        print_recipies()
        if len(fridge.ingredients) == 0:
            print("Fridge is empty :(")
            user_interface()
        else:
            print("Fridge Inventory:\n")
            fridge.print_fridge()
            user_interface()
    elif user_input == 5:
        print("Closing program...")
        sys.exit(0)
    else:
        print("Invalid input\n")
        user_interface()
        
        
user_interface()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    