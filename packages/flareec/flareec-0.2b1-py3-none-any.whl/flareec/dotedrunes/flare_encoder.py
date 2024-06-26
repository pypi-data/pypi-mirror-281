# flareec/dotedrunes/flare_encoder.py

class FlareEncoder:
    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.column_sizes = [8, 9, 9]  # Updated column sizes
        self.grid_sizes = [3, 3, 3]  # Each column has 3x3 grid
        self.numbers = "0123456789"
        self.special_chars = ".,-*/_=:"  # Added ':' as a special character
        self.number_mode_code = "3161"  # Updated code for number mode
        self.special_mode_code = "3161"  # Updated code for special character mode

    def encode_char(self, char):
        char = char.upper()
        if char in self.alphabet:
            index = self.alphabet.index(char)
            
            if index < 8:
                column = 1
                index_in_col = index
            elif index < 17:
                column = 2
                index_in_col = index - 8
            else:
                column = 3
                index_in_col = index - 17
            
            row = index_in_col // 3 + 1
            col_pos = index_in_col % 3 + 1
            code = f"{column}{row}{col_pos}{4 * (row - 1) + col_pos}"
            return code
        elif char in self.numbers:
            return self.number_mode_code + self.encode_morse(char)
        elif char in self.special_chars:
            return self.special_mode_code + char
        else:
            raise ValueError(f"Character {char} is not supported")

    def encode_morse(self, char):
        morse_code = {
            '0': '-----', '1': '.----', '2': '..---', '3': '...--', 
            '4': '....-', '5': '.....', '6': '-....', '7': '--...', 
            '8': '---..', '9': '----.'
        }
        return morse_code[char]

    def decode_char(self, code):
        if code.startswith(self.number_mode_code):
            morse_code = code[len(self.number_mode_code):]
            return self.decode_morse(morse_code)
        elif code.startswith(self.special_mode_code):
            return code[len(self.special_mode_code):]
        else:
            column = int(code[0])
            row = int(code[1]) - 1
            col_pos = int(code[2]) - 1
            
            if column == 1:
                index = row * 3 + col_pos
            elif column == 2:
                index = 8 + row * 3 + col_pos
            else:
                index = 17 + row * 3 + col_pos
                
            return self.alphabet[index]

    def decode_morse(self, morse):
        morse_code = {
            '-----': '0', '.----': '1', '..---': '2', '...--': '3', 
            '....-': '4', '.....': '5', '-....': '6', '--...': '7', 
            '---..': '8', '----.': '9'
        }
        return morse_code[morse]

class DotedRunes:
    @staticmethod
    def encode(text):
        encoder = FlareEncoder()
        return ",".join(encoder.encode_char(c) for c in text)

    @staticmethod
    def crack(text):
        encoder = FlareEncoder()
        return "".join(encoder.decode_char(c) for c in text.split(","))

# Main class to interact with the package
class FlareEC:
    dotedrunes = DotedRunes()
