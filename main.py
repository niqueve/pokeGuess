import customtkinter as ctk
import io
import urllib.request
import random
from PIL import Image
from game_request import Game_Request



class PokemonGame(ctk.CTk):
    def __init__(self):
        super().__init__()

        #--------------------------------------------------------------criar janela

        self.title("PokeGuess")
        self.geometry("500x520")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        #----------------------------------------------------------fontes externas que serão utilizadas

        ctk.FontManager.load_font("fonts/Roboto/static/Roboto-BoldItalic.ttf")
        ctk.FontManager.load_font("fonts/Roboto/static/Roboto-Regular.ttf") 
        ctk.FontManager.load_font("fonts/Roboto/static/Roboto-Bold.ttf")
        ctk.FontManager.load_font("fonts/Roboto/static/Roboto-ExtraBold.ttf")


        #-------------------------------------------------------------------------fontes personalizada
        
        self.title_font = ctk.CTkFont(family="Roboto-ExtraBold", size=28)
        self.title2_font = ctk.CTkFont(family="Roboto-ExtraBold", size=18)
        self.standart_font = ctk.CTkFont(family="Roboto-Bold", size=16)
        self.credit_font = ctk.CTkFont(family="Roboto-Regular", size=14)

        #--------------------------------------------------------------------------atributos

        self.menu_frame = None
        self.score_frame = None
        self.button_frame = None
        
        self.pokemon = None
        self.pokemon_info_label = None
        self.next_button = None

        self.score = 0
        self.lives = 3
        self.choice_buttons = []
          
        #-----------------------------------------------------construir tela inicial
        self.home_screen()

    #---------------------------------------------------------------------------------- métodos da classe

    def home_screen(self):
        self.clear_screen()

        title_label = ctk.CTkLabel(self, text="Welcome to PokeGuess", font= self.title_font, bg_color="transparent")
        title_label.pack(pady=30)  


        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.pack(pady=20)

        bulbasaur = ctk.CTkImage(light_image=Image.open("img/bulbasaur.png"), size=(100, 100))
        charmander = ctk.CTkImage(light_image=Image.open("img/charmander.png"), size=(100, 100))
        squirtle = ctk.CTkImage(light_image=Image.open("img/squirtle.png"), size=(100, 100))

        ctk.CTkLabel(self.menu_frame, image=bulbasaur, text="").pack(side="left", padx=5)
        ctk.CTkLabel(self.menu_frame, image=charmander, text="").pack(side="left", padx=5)
        ctk.CTkLabel(self.menu_frame, image=squirtle, text="").pack(side="left", padx=5)

        ctk.CTkLabel(self, text="Escolha um modo de jogo", font=self.title2_font).pack(pady=10)

        ctk.CTkButton(self, text="Digite a Resposta", command=self.start_typing_mode, font=self.standart_font).pack(pady=10)
        ctk.CTkButton(self, text="Múltipla Escolha", command=self.start_multiple_choice_mode, font=self.standart_font).pack(pady=10)

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
    
    def random_buttons(self):
        choices = self.random_choices()
        choice_buttons = []

        for i, choice in enumerate(choices):  
            btn = ctk.CTkButton(self.button_frame, text=choice,  
                                command=lambda c=choice: self.check_multiple_choice(c))  

            # Organiza os botões em uma grade 2x2  
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)  
            choice_buttons.append(btn) 

        return choice_buttons 
    
    def update_multiple_choice_buttons(self):
        choices = self.random_choices()
        self.correct_choice = self.pokemon.name

        for i, btn in enumerate(self.choice_buttons):
            btn.configure(text=choices[i])
            btn.configure(command=lambda c=choices[i]: self.check_multiple_choice(c))

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

        ctk.CTkLabel(self, text="Quem é esse Pokémon?", font=self.standart_font).pack(pady=10)

        self.pil_image, self.black_image = self.process_image()

        self.pokemon_image = ctk.CTkImage(light_image=self.black_image, size=(150, 150))
        self.image_label = ctk.CTkLabel(self, image=self.pokemon_image, text="")
        self.image_label.pack(pady=10)

        self.entry = ctk.CTkEntry(self, placeholder_text="Digite o nome do Pokémon")
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.check_answer)

        ctk.CTkButton(self, text="Verificar", command=self.check_answer).pack(pady=5)

        self.lives_label = ctk.CTkLabel(self, text=f"Vidas: {self.lives}", font=self.standart_font)
        self.lives_label.pack(pady=5)

        self.score_label = ctk.CTkLabel(self, text=f"Pontos: {self.score}", font=self.standart_font)
        self.score_label.pack(pady=5)

        self.result_label = ctk.CTkLabel(self, text="", font=self.standart_font)
        self.result_label.pack(pady=5)

    def start_multiple_choice_mode(self):
        self.clear_screen()
        self.pokemon = self.get_pokemon()
        self.lives = 3
        self.score = 0

        ctk.CTkLabel(self, text="Quem é esse Pokémon?", font=self.standart_font).pack(pady=10)

        self.pil_image, self.black_image = self.process_image()
        self.pokemon_image = ctk.CTkImage(light_image=self.black_image, size=(150, 150))

        # Frame principal para imagem + pontuação
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=10)

        # Imagem do Pokémon
        self.image_label = ctk.CTkLabel(main_frame, image=self.pokemon_image, text="")
        self.image_label.grid(row=0, column=0, padx=10)

        # Frame de score e vidas ao lado da imagem
        self.score_frame = ctk.CTkFrame(main_frame)
        self.score_frame.grid(row=0, column=1, padx=10)

        self.lives_label = ctk.CTkLabel(self.score_frame, text=f"Vidas: {self.lives}", font=self.standart_font)
        self.lives_label.pack(pady=5)

        self.score_label = ctk.CTkLabel(self.score_frame, text=f"Pontos: {self.score}", font=self.standart_font)
        self.score_label.pack(pady=5)

        # Frame para os botões de múltipla escolha
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10)

        self.choice_buttons = []
        for i in range(4):
            btn = ctk.CTkButton(self.button_frame, text="", command=lambda c=i: self.check_multiple_choice(c))
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)
            self.choice_buttons.append(btn)

        self.update_multiple_choice_buttons()

        self.result_label = ctk.CTkLabel(self, text="", font=self.standart_font)
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
        if choice == self.correct_choice:
            self.score += 10
            self.result_label.configure(text="✅ Correto!", text_color="green")
            self.score_label.configure(text=f"Pontos: {self.score}")
            self.image_label.configure(image=ctk.CTkImage(light_image=self.pil_image, size=(150, 150)))
            self.show_pokemon_info()
            self.show_next_button()
        else:
            self.lives -= 1
            self.image_label.configure(image=ctk.CTkImage(light_image=self.pil_image, size=(150, 150)))
            text_label = "❌ Errado! Resposta correta: " + self.pokemon.name
            self.result_label.configure(text=text_label, text_color="red")
            self.lives_label.configure(text=f"Vidas: {self.lives}")
            if self.lives == 0:
                self.game_over()
            else:
                self.show_next_button()


    def show_pokemon_info(self):
        if self.pokemon_info_label:
            self.pokemon_info_label.pack_forget()

        self.pokemon_info_label = ctk.CTkLabel(self, text=str(self.pokemon), font=("Roboto-BoldItalic", 14))
        self.pokemon_info_label.pack(pady=5)

    def show_next_button(self):
        if self.next_button:
            self.next_button.pack_forget()

        self.next_button = ctk.CTkButton(self, text="Next", command=self.next_round)
        self.next_button.pack(pady=10)

    def next_round(self):
        self.result_label.configure(text="", text_color="red")
        if self.next_button:
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
            self.update_multiple_choice_buttons()


    def game_over(self):
        self.clear_screen()

        ctk.CTkLabel(self, text=f"Fim de jogo! Pontuação final: {self.score}", font=self.title_font).place(x = 50, y = 100)
        ctk.CTkLabel(self, text="Deseja jogar novamente?", font=self.title2_font).place(x = 150, y = 140)

        ctk.CTkButton(self, text="Home", command=self.home_screen, font=self.standart_font).place(x = 175, y = 230)
        ctk.CTkButton(self, text="Sair", command=self.end_game, font=self.standart_font).place(x = 175, y = 290)

    def end_game(self):
        self.clear_screen()

        ctk.CTkLabel(self, text=f"Fim de jogo! Pontuação final: {self.score}", font=self.title2_font).pack(pady=5)
        ctk.CTkLabel(self, text="Obrigada e até a próxima 👋", font= self.standart_font).pack(pady=5)
        

        self.textbox = ctk.CTkTextbox(master=self, width=320, height=310 ,corner_radius=0, font=self.credit_font, bg_color="yellow")
        self.textbox.pack(pady=10)
        self.textbox.insert("0.0", " \n\n\nTrabalho P2 \n Laboratório de Programação Orientada a Objetos \n"
                            " Professor: Marcio Fuchshuber \n"
                            " Aluna: Monique E R Gomes \n\n"
                            " Dados dos pokemons retirados de:\n https://pokeapi.co/ \n"
                            " Código completo no repositório: \n https://github.com/niqueve/pokeGuess \n")



    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = PokemonGame()
    app.mainloop()
