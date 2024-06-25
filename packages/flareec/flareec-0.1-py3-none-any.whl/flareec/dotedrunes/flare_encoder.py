# flareec/dotedrunes/flare_encoder.py

class FlareEncoder:
    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.column_sizes = [8, 8, 9]
        self.grid_sizes = [3, 3, 2]
        
    def encode_char(self, char):
        index = self.alphabet.index(char)
        
        if index < 8:
            column = 1
            row = index // 3
            col_pos = index % 3
        elif index < 16:
            column = 2
            index -= 8
            row = index // 3
            col_pos = index % 3
        else:
            column = 3
            index -= 16
            row = index // 3
            col_pos = index % 3
        
        code = f"{column}{row + 1}{col_pos + 1}{4 * row + col_pos + 1}"
        return code

    def decode_char(self, code):
        column = int(code[0])
        row = int(code[1]) - 1
        col_pos = int(code[2]) - 1
        
        if column == 1:
            index = row * 3 + col_pos
        elif column == 2:
            index = 8 + row * 3 + col_pos
        else:
            index = 16 + row * 3 + col_pos
            
        return self.alphabet[index]

    def encode(self, text):
        encoded_text = []
        for char in text.upper():
            encoded_text.append(self.encode_char(char))
        return ','.join(encoded_text)

    def decode(self, encoded_text):
        encoded_chars = encoded_text.split(',')
        decoded_text = []
        for code in encoded_chars:
            decoded_text.append(self.decode_char(code))
        return ''.join(decoded_text)
