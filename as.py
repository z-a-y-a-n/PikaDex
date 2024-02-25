import tkinter as tk
import requests
from PIL import ImageTk, Image
import io
from tkinter import messagebox

def fetch_pokemon_data():
    pokemon_name = pokemon_name_entry.get()
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        pokemon_name_label.config(text="Name: " + pokemon_data["name"].capitalize())
        pokemon_type_label.config(text="Type: " + ", ".join([t["type"]["name"].capitalize() for t in pokemon_data["types"]]))
        pokemon_hp_label.config(text="HP: " + str(pokemon_data["stats"][0]["base_stat"]))
        pokemon_weight_label.config(text="Weight: " + str(pokemon_data["weight"]) + " kg")
        pokemon_height_label.config(text="Height: " + str(pokemon_data["height"]) + " cm")
        pokemon_id_label.config(text="ID: " + str(pokemon_data["id"]))

        # Retrieve the image URL
        image_url = pokemon_data["sprites"]["front_default"]

        # Fetch the image data
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # Create an ImageTk object from the image data
            image_data = Image.open(io.BytesIO(image_response.content))
            image_data = image_data.resize((400, 400))  # Resize the image
            pokemon_image = ImageTk.PhotoImage(image_data)
            pokemon_image_label.config(image=pokemon_image)
            pokemon_image_label.image = pokemon_image  # Store a reference to avoid garbage collection
        else:
            messagebox.showerror("ERROR","Failed to retrieve pokemon data.")

        # Retrieve evolution chain information
        species_url = pokemon_data["species"]["url"]
        species_response = requests.get(species_url)
        if species_response.status_code == 200:
            species_data = species_response.json()
            evolution_chain_url = species_data["evolution_chain"]["url"]
            evolution_chain_response = requests.get(evolution_chain_url)
            if evolution_chain_response.status_code == 200:
                evolution_chain_data = evolution_chain_response.json()
                chain = evolution_chain_data["chain"]
                first_evolution = chain["species"]["name"].capitalize()
                last_evolution = None
                while "evolves_to" in chain and len(chain["evolves_to"]) > 0:
                    chain = chain["evolves_to"][0]
                    if "species" in chain:
                        last_evolution = chain["species"]["name"].capitalize()

                if first_evolution:
                    pokemon_first_evolution_label.config(text="First Evolution: " + first_evolution)
                if last_evolution:
                    pokemon_last_evolution_label.config(text="Last Evolution: " + last_evolution)

        # Retrieve ability information
        abilities = pokemon_data["abilities"]
        ability_names = [ability["ability"]["name"].capitalize() for ability in abilities]
        pokemon_ability_label.config(text="Ability: " + ", ".join(ability_names))
    else:
        messagebox.showerror("ERROR","Failed to retrieve pokemon data.")

# Create the Tkinter GUI
root = tk.Tk()
root.title("Pokédex")
root.geometry("400x600")
root.configure(bg="#F6F6F6")

# Create input fields and labels
pokemon_name_label = tk.Label(root, text="Name:", font=("Arial", 16, "bold"), bg="#F6F6F6")
pokemon_name_label.pack(pady=10)

pokemon_name_entry = tk.Entry(root, font=("Arial", 16))
pokemon_name_entry.pack()

fetch_button = tk.Button(root, text="Fetch", font=("Arial", 14), command=fetch_pokemon_data)
fetch_button.pack(pady=10)

# Create labels to display Pokémon information
pokemon_type_label = tk.Label(root, text="Type:", font=("Arial", 14), bg="#F6F6F6")
pokemon_type_label.pack()

pokemon_hp_label = tk.Label(root, text="HP:", font=("Arial", 14), bg="#F6F6F6")
pokemon_hp_label.pack()

pokemon_weight_label = tk.Label(root, text="Weight:", font=("Arial", 14), bg="#F6F6F6")
pokemon_weight_label.pack()

pokemon_height_label = tk.Label(root, text="Height:", font=("Arial", 14), bg="#F6F6F6")
pokemon_height_label.pack()

pokemon_id_label = tk.Label(root, text="ID:", font=("Arial", 14), bg="#F6F6F6")
pokemon_id_label.pack()

pokemon_first_evolution_label = tk.Label(root, text="First Evolution:", font=("Arial", 14), bg="#F6F6F6")
pokemon_first_evolution_label.pack()

pokemon_last_evolution_label = tk.Label(root, text="Last Evolution:", font=("Arial", 14), bg="#F6F6F6")
pokemon_last_evolution_label.pack()

pokemon_ability_label = tk.Label(root, text="Ability:", font=("Arial", 14), bg="#F6F6F6")
pokemon_ability_label.pack()

# Create a label to display the Pokémon image
pokemon_image_label = tk.Label(root, bg="#F6F6F6")
pokemon_image_label.pack(pady=20)

root.mainloop()

