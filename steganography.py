# -*- coding: utf-8 -*-
"""Steganography.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tvvLKb-FX5Fg70aYGO-GqeRH3CelGzoW
"""

from matplotlib import pyplot as plt


def show_image(image, label=None):
    plt.imshow(image)
    plt.title(label)
    plt.xticks([])
    plt.yticks([])
    plt.show()


def string_to_bytes(message):
    bin_array = bytearray(message, "utf8")
    byte_list = list()
    for b in bin_array:
        to_bin = bin(b)[2:].zfill(8)
        byte_list.append(to_bin)
    return ''.join(byte_list)


def bytes_to_string(bytes_in):
    result = ""
    byte_list = list()
    for i in range(0, len(bytes_in), 8):
        bin_int = bytes_in[i:i+8]
        byte_list.append(bin_int)
    i = 0
    while int(byte_list[i], 2) != 0:
        if byte_list[i][0] == "0":
            char = int(byte_list[i], 2)
            result += chr(char)
        elif byte_list[i][0:3] == "110" and byte_list[i+1][0:2] == "10":
            char = int(byte_list[i][3:8] + byte_list[i+1][2:8], 2)
            result += chr(char)
            i += 1
        elif byte_list[i][0:4] == "1110" and byte_list[i+1][0:2] == "10" and byte_list[i+2][0:2] == "10":
            char = int(byte_list[i][4:8] + byte_list[i+1][2:8] + byte_list[i+2][2:8], 2)
            result += chr(char)
            i += 2
        else:
            char = int(byte_list[i][5:8] + byte_list[i+1][2:8] + byte_list[i+2][2:8] + byte_list[i+3][2:8], 2)
            result += chr(char)
            i += 3
        i += 1
    return result


def write_message_to_image(image, message):
    h, w = image[:, :, 2].shape
    blue_channel = image[:, :, 2]
    max_length = h*w // 16  # 8 * 2, since every latin-like character requires 2 bytes (8 bits)
    if len(message) + 1 > max_length:
        print("Error: message is too long. Max chars allowed for this pic: ", max_length)
        return None
    binary_message = string_to_bytes(message)
    binary_message += "00000000"  # add non printable character to the end of the message
    for i in range(h):
        for j in range(w):
            if i*w + j >= len(binary_message):
                return image
            pixel = blue_channel[i, j]
            to_bin = bin(pixel)[2:].zfill(8)
            to_bin = list(to_bin)
            to_bin[7] = binary_message[i*w + j]
            to_bin = ''.join(to_bin)
            blue_channel[i, j] = int(to_bin, 2)
    return image


def read_message_from_image(image):
    h, w = image[:, :, 2].shape
    blue_channel = image[:, :, 2]
    bits = list()
    count = 0  # count is used to keep track of the number of bits read till now
    for i in range(h):
        exit_loop = True  # Set this here so that the outer loop can read it at the end
        for j in range(w):
            pixel = blue_channel[i, j]
            to_bin = bin(pixel)[2:].zfill(8)
            bits.append(to_bin[7])
            count += 1
            if count % 8 == 0:  # if a number of full characters has been read...
                exit_loop = True
                for bit in bits[-8:]:  # check if the last one is 00000000 (termination character)
                    if bit != "0":
                        exit_loop = False
                if exit_loop:  # if it's the case break the inner loop because the whole message has been read
                    break
        if count % 8 == 0 and exit_loop:  # if the last full character is the termination one, then break the outer loop too
            break
    res_bytes = ''.join(bits)
    message = bytes_to_string(res_bytes)
    allowed_np_chars = ["\n"]  # put here escapes you want to be able to print
    for c in message:
        if not c.isprintable() and c not in allowed_np_chars:
            index = message.index(c)
            return message[0:index]
    return message


def format_out_filename(filename):
    filename = filename.replace(':', '-')
    filename = filename.replace(' ', '_')
    return filename
