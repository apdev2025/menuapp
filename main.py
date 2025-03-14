import csv
import random
import os
from collections import Counter

def load_dishes_from_csv(filepath):
    """Loads dishes and their ingredients from a user-provided CSV file.

    Args:
        filepath: The path to provided CSV file.

    Returns:
        A dictionary where keys are dish names and values are lists of ingredients.
        Returns None if the file doesn't exist or is empty or wrong format.
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return None

    dishes = {}
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None)  # Skip header row if it exists
            if header is None or len(header) < 2:
                print(f"Error: file is empty or wrong format.")
                return None
            for row in reader:
                if len(row) >= 2:
                    dish_name = row[0].strip()
                    ingredients = [item.strip() for item in row[1:] if item.strip()]
                    dishes[dish_name] = ingredients
                else:
                    print(f"Warning: Skipping row due to insufficient data: {row}")

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

    if not dishes:
        print(f"Error: no dish found in the file.")
        return None

    return dishes


def generate_random_menu(dishes, num_days=5):
    """Generates random menu for a specified number of days without duplicates.

    Args:
        dishes: A dictionary of dishes and their ingredients.
        num_days: The number of days to generate a menu for.

    Returns:
        A list of dishes (one for each day) without duplicates, or None if not enough unique dishes.
    """
    all_dishes = list(dishes.keys())
    if len(all_dishes) < num_days:
        print(f"Error: Not enough unique dishes available to generate a menu for {num_days} days.")
        return None

    menu = random.sample(all_dishes, k=num_days)  # Use sample to avoid duplicates
    return menu


def get_shopping_list(menu, dishes):
    """Generates a shopping list from a given menu with ingredient counts.

    Args:
        menu: A list of dishes.
        dishes: A dictionary of dishes and their ingredients.

    Returns:
        A list of tuples: (ingredient, count).
    """
    all_ingredients = []
    for dish in menu:
        if dish in dishes:
            all_ingredients.extend(dishes[dish])

    ingredient_counts = Counter(all_ingredients)
    return sorted(ingredient_counts.items())

def display_menu(menu, dishes):
    """Displays the menu and the required shopping list.
      Args:
          menu: A list of dishes.
          dishes: A dictionary of dishes and their ingredients.
    """
    print("\n--- Your Menu ---")
    for i, dish in enumerate(menu):
        print(f"Day {i + 1}: {dish}")
        if dish in dishes:
            print(f"  Ingredients: {', '.join(dishes[dish])}")
        else:
            print("  Ingredients: Not found")

    shopping_list_with_counts = get_shopping_list(menu, dishes)
    print("\n--- Shopping List ---")
    for item, count in shopping_list_with_counts:
        if count > 1:
            print(f"- {item} (multiple)")
        else:
            print(f"- {item}")
    print("\n")


def main():
    """Main function to run the menu generator."""
    csv_filepath = 'dishes.csv'  # Replace with your CSV file path

    dishes = load_dishes_from_csv(csv_filepath)

    if dishes is None:
        return

    while True:
        answer = input("Do you want to generate a new menu? (y/n): ").lower()
        if answer == 'y':
            menu = generate_random_menu(dishes, 5)
            if menu:
                display_menu(menu, dishes)
        elif answer == 'n':
            print("Exiting program.")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


if __name__ == "__main__":
    main()