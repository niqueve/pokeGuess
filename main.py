import customtkinter as ctk
import io
import urllib.request
import random
from PIL import Image
from game_request import Game_Request

class PokemonGame(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Welcome to PokeGuess")
        self.geometry("500x500")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.pokemon = None
        self.score = 0
        self.lives = 3
        self.choice_buttons = []

        self.menu_frame = None
        self.next_button = None
        self.pokemon_info_label = None

        self.home_screen()

    def home_screen(self):
        self.clear_screen()

        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.pack(pady=20)

        bulbasaur = ctk.CTkImage(light_image=Image.open("img/bulbasaur.png"), size=(100, 100))
        charmander = ctk.CTkImage(light_image=Image.open("img/charmander.png"), size=(100, 100))
        squirtle = ctk.CTkImage(light_image=Image.open("img/squirtle.png"), size=(100, 100))

        ctk.CTkLabel(self.menu_frame, image=bulbasaur, text="").pack(side="left", padx=5)
        ctk.CTkLabel(self.menu_frame, image=charmander, text="").pack(side="left", padx=5)
        ctk.CTkLabel(self.menu_frame, image=squirtle, text="").pack(side="left", padx=5)

        ctk.CTkLabel(self, text="Escolha um modo de jogo", font=("Arial", 18, "bold")).pack(pady=10)

        ctk.CTkButton(self, text="Modo Digitação", command=self.start_typing_mode).pack(pady=5)
        ctk.CTkButton(self, text="Modo Múltipla Escolha", command=self.start_multiple_choice_mode).pack(pady=5)

    def get_pokemon(self):
        pokemon_id = random.randint(1, 151)
        game_request = Game_Request(pokemon_id)
        return game_request.response()

    def random_choices(self):
        choice1 = self.get_pokemon().name
        choice2 = self.get_pokemon().name
        choice3 = self.get_pokemon().name

        choices = [choice1, choice2, choice3, self.pokemon.name]
        random.shuffle(choices)
        return choices

    def process_image(self):
        image_stream = io.BytesIO(urllib.request.urlopen(self.pokemon.photo).read())
        pil_image = Image.open(image_stream).convert("RGBA")

        pixels = pil_image.getdata()
        new_pixels = []
        for pixel in pixels:
            r, g, b, a = pixel
            if a > 0:
                new_pixels.append((0, 0, 0, a))
            else:
                new_pixels.append(pixel)

        black_image = Image.new("RGBA", pil_image.size)
        black_image.putdata(new_pixels)

        return pil_image, black_image

    def start_typing_mode(self):
        self.clear_screen()
        self.pokemon = self.get_pokemon()
        self.lives = 3
        self.score = 0

        ctk.CTkLabel(self, text="Quem é esse Pokémon?", font=("Arial", 18, "bold")).pack(pady=10)

        self.pil_image, self.black_image = self.process_image()

        self.pokemon_image = ctk.CTkImage(light_image=self.black_image, size=(150, 150))
        self.image_label = ctk.CTkLabel(self, image=self.pokemon_image, text="")
        self.image_label.pack(pady=10)

        self.entry = ctk.CTkEntry(self, placeholder_text="Digite o nome do Pokémon")
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.check_answer)

        ctk.CTkButton(self, text="Verificar", command=self.check_answer).pack(pady=5)

        self.lives_label = ctk.CTkLabel(self, text=f"Vidas: {self.lives}")
        self.lives_label.pack(pady=5)

        self.score_label = ctk.CTkLabel(self, text=f"Pontos: {self.score}")
        self.score_label.pack(pady=5)

        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack(pady=5)

    def start_multiple_choice_mode(self):
        self.clear_screen()
        self.pokemon = self.get_pokemon()
        self.lives = 3
        self.score = 0

        ctk.CTkLabel(self, text="Quem é esse Pokémon?", font=("Arial", 18, "bold")).pack(pady=10)

        self.pil_image, self.black_image = self.process_image()

        self.pokemon_image = ctk.CTkImage(light_image=self.black_image, size=(150, 150))
        self.image_label = ctk.CTkLabel(self, image=self.pokemon_image, text="")
        self.image_label.pack(pady=10)

        choices = self.random_choices()
        self.choice_buttons = []

        for choice in choices:
            btn = ctk.CTkButton(self, text=choice, command=lambda c=choice: self.check_multiple_choice(c))
            btn.pack(pady=5)
            self.choice_buttons.append(btn)

        self.lives_label = ctk.CTkLabel(self, text=f"Vidas: {self.lives}")
        self.lives_label.pack(pady=5)

        self.score_label = ctk.CTkLabel(self, text=f"Pontos: {self.score}")
        self.score_label.pack(pady=5)

        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack(pady=5)

    def check_answer(self, event=None):
        user_input = self.entry.get().lower()
        if user_input == self.pokemon.name:
            self.score += 10
            self.result_label.configure(text="✅ Correto!", text_color="green")
            self.score_label.configure(text=f"Pontos: {self.score}")
            self.image_label.configure(image=ctk.CTkImage(light_image=self.pil_image, size=(150, 150)))
            self.show_next_button()
        else:
            self.lives -= 1
            self.result_label.configure(text= "❌ Errado! Tente novamente.", text_color="red")
            self.lives_label.configure(text=f"Vidas: {self.lives}")
            if self.lives == 0:
                self.game_over()
            else:
                self.show_next_button()

    def check_multiple_choice(self, choice):
        for btn in self.choice_buttons:
            btn.pack_forget()

        if choice == self.pokemon.name:
            self.score += 10
            self.result_label.configure(text="✅ Correto!", text_color="green")
            self.score_label.configure(text=f"Pontos: {self.score}")
            self.image_label.configure(image=ctk.CTkImage(light_image=self.pil_image, size=(150, 150)))
            self.show_pokemon_info()
            self.show_next_button()
        else:
            self.lives -= 1
            self.image_label.configure(image=ctk.CTkImage(light_image=self.pil_image, size=(150, 150)))
            text_label = "❌ Errado! resposta correta: " + self.pokemon.name
            self.result_label.configure(text= text_label, text_color="red")
            self.lives_label.configure(text=f"Vidas: {self.lives}")
            if self.lives == 0:
                self.game_over()
            else:
                self.show_next_button()

    def show_pokemon_info(self):
        if self.pokemon_info_label:
            self.pokemon_info_label.pack_forget()

        self.pokemon_info_label = ctk.CTkLabel(self, text=str(self.pokemon), font=("Arial", 14))
        self.pokemon_info_label.pack(pady=5)

    def show_next_button(self):
        if self.next_button:
            self.next_button.pack_forget()

        self.next_button = ctk.CTkButton(self, text="Next", command=self.next_round)
        self.next_button.pack(pady=10)

    def next_round(self):
        self.result_label.configure(text= "", text_color="red")
        self.next_button.pack_forget()
        if self.pokemon_info_label:
            self.pokemon_info_label.pack_forget()

        self.pokemon = self.get_pokemon()
        self.pil_image, self.black_image = self.process_image()
        self.pokemon_image = ctk.CTkImage(light_image=self.black_image, size=(150, 150))
        self.image_label.configure(image=self.pokemon_image)

        if hasattr(self, 'entry'):
            self.entry.delete(0, "end")
        elif self.choice_buttons:
            choices = self.random_choices()
            for choice in choices:
                btn = ctk.CTkButton(self, text=choice, command=lambda c=choice: self.check_multiple_choice(c))
                btn.pack(pady=5)
                self.choice_buttons.append(btn)

    def game_over(self):
        self.clear_screen()
        ctk.CTkLabel(self, text=f"Fim de jogo! Pontuação final: {self.score}", font=("Arial", 18, "bold")).pack(pady=10)
        ctk.CTkLabel(self, text="Deseja jogar novamente?", font=("Arial", 14)).pack(pady=10)

        ctk.CTkButton(self, text="Home", command=self.home_screen).pack(pady=5)
        ctk.CTkButton(self, text="Sair", command=self.end_game).pack(pady=5)

    def end_game(self):
        self.clear_screen()

        ctk.CTkLabel(self, text=f"Fim de jogo! Pontuação final: {self.score}", font=("Arial", 18, "bold")).pack(pady=10)
        ctk.CTkLabel(self, text="Obrigada e até a próxima", font=("Arial", 14)).pack(pady=10)


    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = PokemonGame()
    app.mainloop()
