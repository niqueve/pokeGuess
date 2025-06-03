import customtkinter as ctk
import io
import urllib.request
import random
from PIL import Image
from game_request import Game_Request

#--------------------------------------------------------------------------classe principal
class PokemonGame(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Quem é esse Pokémon??")
        self.geometry("500x500")
        ctk.set_appearance_mode("light")  # Define o tema claro para evidenciar contorno do pokemon
        ctk.set_default_color_theme("blue")  

        self.pokemon = self.get_pokemon()
        self.create_widgets()

    def get_pokemon(self):
        pokemon_id = random.randint(1,151) #restrito a primeira geração
        game_request = Game_Request(pokemon_id)
        pokemon = game_request.response()
        return pokemon

    def create_widgets(self):
        """Cria os elementos da interface"""

        # **Carregar imagem original**
        image_stream = io.BytesIO(urllib.request.urlopen(self.pokemon.photo).read())
        self.pil_image = Image.open(image_stream).convert("RGBA")  # Mantém transparência

        # **Converter apenas as cores internas para preto**
        pixels = self.pil_image.getdata()
        new_pixels = []
        for pixel in pixels:
            r, g, b, a = pixel  # Separando os canais de cor
            if a > 0:  # Mantém fundo transparente
                new_pixels.append((0, 0, 0, a))  # Define o Pokémon como preto
            else:
                new_pixels.append(pixel)

        # Criar nova imagem com os pixels modificados
        self.black_image = Image.new("RGBA", self.pil_image.size)
        self.black_image.putdata(new_pixels)

        # **Exibir imagem preta inicialmente**
        self.pokemon_image = ctk.CTkImage(light_image=self.black_image, size=(150, 150))

        self.image_label = ctk.CTkLabel(self, image=self.pokemon_image, text="")
        self.image_label.pack(pady=20)

        # Campo de entrada
        self.entry = ctk.CTkEntry(self, placeholder_text="Digite o nome do Pokémon")
        self.entry.pack(pady=10)

        # Botão de verificação
        self.button = ctk.CTkButton(self, text="Verificar", command=self.check_answer)
        self.button.pack(pady=10)

        # Label de resposta
        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack(pady=10)

    def check_answer(self):
        """Verifica se o nome digitado está correto e revela a imagem colorida"""
        user_input = self.entry.get().lower()
        if user_input == self.pokemon.name:
            self.result_label.configure(text="✅ Correto!", text_color="green")
            # **Trocar para imagem colorida**
            self.pokemon_image = ctk.CTkImage(light_image=self.pil_image, size=(150, 150))
            self.image_label.configure(image=self.pokemon_image)
        else:
            self.result_label.configure(text="❌ Errado! Tente novamente.", text_color="red")

# Executar o jogo
if __name__ == "__main__":
    app = PokemonGame()
    app.mainloop()