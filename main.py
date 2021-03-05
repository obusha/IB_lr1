from matplotlib import pyplot as plt
import os
import tkinter as tk
import tkinter.filedialog as fd
from Blocks32Bit import Blocks32Bit


hash_values = ['6a09e667', 'bb67ae85', '3c6ef372', 'a54ff53a', '510e527f', '9b05688c', '1f83d9ab', '5be0cd19']
constants = ['428a2f98', '71374491', 'b5c0fbcf', 'e9b5dba5', '3956c25b', '59f111f1', '923f82a4', 'ab1c5ed5',
     'd807aa98', '12835b01', '243185be', '550c7dc3', '72be5d74', '80deb1fe', '9bdc06a7', 'c19bf174',
     'e49b69c1', 'efbe4786', '0fc19dc6', '240ca1cc', '2de92c6f', '4a7484aa', '5cb0a9dc', '76f988da',
     '983e5152', 'a831c66d', 'b00327c8', 'bf597fc7', 'c6e00bf3', 'd5a79147', '06ca6351', '14292967',
     '27b70a85', '2e1b2138', '4d2c6dfc', '53380d13', '650a7354', '766a0abb', '81c2c92e', '92722c85',
     'a2bfe8a1', 'a81a664b', 'c24b8b70', 'c76c51a3', 'd192e819', 'd6990624', 'f40e3585', '106aa070',
     '19a4c116', '1e376c08', '2748774c', '34b0bcb5', '391c0cb3', '4ed8aa4a', '5b9cca4f', '682e6ff3',
     '748f82ee', '78a5636f', '84c87814', '8cc70208', '90befffa', 'a4506ceb', 'bef9a3f7', 'c67178f2']


def get_from_file(path: str):
    """Считывание данных из файла
    """
    with open(path, 'r') as file:
        return file.readlines()


def to_binary(message):
    """ Перевод сообщения в двоичный код """
    b = format(int.from_bytes(message.encode(), 'big'), 'b')
    while len(b) % 8 != 0:
        b = '0' + b
    return b


# def to_binary(str):
#     return ''.join(format(ord(i), '08b') for i in str)
#     return ''.join(format(i, 'b') for i in bytearray(str, encoding ='utf-8'))


def edit_bit(message, number_bit):
    if message[number_bit] == '0':
        new_message = message[:number_bit] + '1' + message[number_bit + 1:]
    else:
        new_message = message[:number_bit] + '0' + message[number_bit + 1:]
    return new_message


def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def ch(x, y, z):
    return (x & y) ^ (~x & z)


def sha_256(binary_message):
    """ Алгоритм хэширования sha-256"""
    H = []
    for h in hash_values:
        H.append(Blocks32Bit(format(int(h, 16), '032b')))
    K = []
    for k in constants:
        K.append(Blocks32Bit(format(int(k, 16), '032b')))
    len_message = len(binary_message)
    binary_message += '1'
    while (len(binary_message) - 448) % 512 != 0:
        binary_message += '0'
    binary_message += format(len_message, '064b')
    blocks = []
    for i in range(0, len_message, 512):
        blocks.append(binary_message[i:i+512])
    if not blocks:
        blocks.append(binary_message)
    W = []
    H_preliminary = []
    for block in blocks:
        for i in range(64):
            if i <= 15:
                W.append(Blocks32Bit(block[i*32:(i+1)*32]))
            else:
                new_W = W[i - 2].s_1() + W[i - 7] + W[i - 15].s_0() + W[i - 16]
                W.append(new_W)
        a, b, c, d, e, f, g, h = H[0], H[1], H[2], H[3], H[4], H[5], H[6], H[7]
        for t in range(64):
            T1 = h + e.sigma_1() + ch(e, f, g) + K[t] + W[t]
            T2 = a.sigma_0() + maj(a, b, c)
            h = g
            g = f
            f = e
            e = d + T1
            d = c
            c = b
            b = a
            a = T1 + T2
            H_preliminary.append((a + H[0]).to_string() + (b + H[1]).to_string() + (c + H[2]).to_string() +
                                 (d + H[3]).to_string() + (e + H[4]).to_string() + (f + H[5]).to_string() +
                                 (g + H[6]).to_string() + (h + H[7]).to_string())
        H[0] = a + H[0]
        H[1] = b + H[1]
        H[2] = c + H[2]
        H[3] = d + H[3]
        H[4] = e + H[4]
        H[5] = f + H[5]
        H[6] = g + H[6]
        H[7] = h + H[7]
    return "".join(map(Blocks32Bit.to_string_hash, H)), H_preliminary


def char_by_char_string_comparison(first, second):
    count_different_bit = 0
    for elem_first, elem_second in zip(first, second):
        if elem_first != elem_second:
            count_different_bit += 1
    return count_different_bit


def graph_avalanche_effect(number_of_changed_bits):
    plt.plot(number_of_changed_bits)
    plt.show()


def avalanche_effect(binary_message, number_bit, hash_preliminary_value_original):
    binary_message = edit_bit(binary_message, 3)
    hash_message, hash_preliminary_value = sha_256(binary_message)
    number_of_changed_bits = []
    for i in range(len(hash_preliminary_value)):
        count_different_bit = 0
        count_different_bit += char_by_char_string_comparison(hash_preliminary_value[i], hash_preliminary_value_original[i])
        number_of_changed_bits.append(count_different_bit)
    graph_avalanche_effect(number_of_changed_bits)
    print(number_of_changed_bits)


def open_file():
    path = fd.askopenfilename(title='Открыть файл', filetypes=(("Text files", "*.txt"), ("Binary files", "*.bin")))
    return path

if __name__ == "__main__":
    window = tk.Tk()
    window.geometry('400x400')
    window.title("Добро пожаловать в приложение PythonRu")

    window.mainloop()

    # path = "input_data/test.bin"
    # file_path, file_ext = os.path.splitext(path)
    # if file_ext != '.txt' or file_ext != '.bin':
    #     print('Error')
    #     exit(0)
    # message = get_from_file(path)
    # message = ''.join(message)
    # if message and file_ext != '.bin':
    #     message = to_binary(message)
    # hash_message, hash_preliminary_value = sha_256(message)
    # print(hash_message)
    # if message and len(message) < 448:
    #     avalanche_effect(message, 3, hash_preliminary_value)