class Pokemon:
    def __init__(self, id, name, types, species, weight, height, photo):
        self.id = id
        self.name = name
        self.types = types
        self.species = species
        self.weight = weight
        self.height = height
        self.photo = photo

    def __str__(self):
        return f'I´m {self.name.upper()}\nTypes: {self.types} \n Species: {self.species} \n Height: {self.height}m \n weight: {self.weight}kg'
    