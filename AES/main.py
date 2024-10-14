import streamlit as st
import numpy as np
import pandas as pd

# S-Box untuk substitusi
s_box = np.array([
    [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
    [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
    [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
    [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
    [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
    [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
    [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
    [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
    [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
    [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
    [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
    [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
    [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
    [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
    [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
    [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
])

# Fungsi substitusi menggunakan S-box
def sub_bytes(state):
    return np.array([[s_box[b >> 4][b & 0x0F] for b in row] for row in state])

# Fungsi ShiftRows
def shift_rows(state):
    state[1] = np.roll(state[1], -1)
    state[2] = np.roll(state[2], -2)
    state[3] = np.roll(state[3], -3)
    return state

# Fungsi Galois Field untuk perkalian dalam GF(2^8)
def galois_mult(a, b):
    p = 0
    hi_bit_set = 0
    for i in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        if hi_bit_set:
            a ^= 0x1B  # Modulo dengan polinomial AES: x^8 + x^4 + x^3 + x + 1
        b >>= 1
    return p % 256

# Fungsi MixColumns yang diperbarui
def mix_columns(state):
    for i in range(4):
        col = state[:, i]
        # Lakukan operasi perkalian Galois untuk setiap elemen dalam kolom
        temp = [
            galois_mult(col[0], 2) ^ galois_mult(col[1], 3) ^ col[2] ^ col[3],
            col[0] ^ galois_mult(col[1], 2) ^ galois_mult(col[2], 3) ^ col[3],
            col[0] ^ col[1] ^ galois_mult(col[2], 2) ^ galois_mult(col[3], 3),
            galois_mult(col[0], 3) ^ col[1] ^ col[2] ^ galois_mult(col[3], 2)
        ]
        state[:, i] = np.array(temp)
    return state

# Fungsi konversi dari hex ke array byte dalam format 4 kolom
def hex_to_bytes(hex_str):
    bytes_arr = np.array([int(hex_str[i:i + 2], 16) for i in range(0, len(hex_str), 2)], dtype=np.uint8)
    return bytes_arr.reshape(4, 4).T  # Mengubah bentuk menjadi 4 kolom dan 4 baris

# Fungsi konversi dari array byte ke hex dengan pemisahan setiap 8 byte
def bytes_to_hex(byte_array):
    hex_str = ''.join([f'{b:02x}' for col in byte_array.T for b in col])
    # Menambahkan spasi setiap 8 byte
    return ' '.join([hex_str[i:i + 8] for i in range(0, len(hex_str), 8)]).upper()

# Fungsi AddRoundKey
def add_round_key(state, round_key):
    return state ^ round_key

def key_expansion(key):
    round_keys = [key.copy()]  # Key awal sebagai round key pertama
    rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]  # Rcon values

    for i in range(1, 11):
        temp = round_keys[-1][:, 3].copy()  # Mengambil kolom terakhir dari key sebelumnya
        
        # Rotate word
        temp = np.roll(temp, -1)
        
        # Apply S-Box
        temp = np.array([s_box[b >> 4][b & 0x0F] for b in temp])
        
        # Apply Rcon ke byte pertama
        temp[0] ^= rcon[i - 1]
        
        new_key = round_keys[-1][:, 0] ^ temp  # Kolom pertama dari key baru
        new_round_key = new_key.reshape(4, 1)
        
        # Membuat 3 kolom berikutnya dengan XOR kolom sebelumnya
        for j in range(1, 4):
            new_key = round_keys[-1][:, j] ^ new_key
            new_round_key = np.hstack((new_round_key, new_key.reshape(4, 1)))
        
        round_keys.append(new_round_key)
    return round_keys

# Fungsi utama AES Encryption
def aes_encrypt(plaintext_hex, key_hex):
    state = hex_to_bytes(plaintext_hex)
    key = hex_to_bytes(key_hex)
    round_keys = key_expansion(key)

    steps = []
    key_steps = []

    # Initial AddRoundKey
    state = add_round_key(state, round_keys[0])
    steps.append({'Step': 'Add Round Key (Initial)', 'State': bytes_to_hex(state)})
    key_steps.append({'Step': 'Key (Initial)', 'Key': bytes_to_hex(round_keys[0])})

    # Main Rounds
    for round_num in range(1, 10):
        state = sub_bytes(state)
        steps.append({'Step': f'SubBytes (Round {round_num})', 'State': bytes_to_hex(state)})
        
        state = shift_rows(state)
        steps.append({'Step': f'ShiftRows (Round {round_num})', 'State': bytes_to_hex(state)})
        
        state = mix_columns(state)
        steps.append({'Step': f'MixColumns (Round {round_num})', 'State': bytes_to_hex(state)})
        
        state = add_round_key(state, round_keys[round_num])
        steps.append({'Step': f'Add Round Key (Round {round_num})', 'State': bytes_to_hex(state)})
        key_steps.append({'Step': f'Key (Round {round_num})', 'Key': bytes_to_hex(round_keys[round_num])})

    # Final Round
    state = sub_bytes(state)
    steps.append({'Step': 'SubBytes (Final Round)', 'State': bytes_to_hex(state)})
    
    state = shift_rows(state)
    steps.append({'Step': 'ShiftRows (Final Round)', 'State': bytes_to_hex(state)})

    state = add_round_key(state, round_keys[10])
    steps.append({'Step': 'Add Round Key (Final Round)', 'State': bytes_to_hex(state)})
    key_steps.append({'Step': 'Key (Final Round)', 'Key': bytes_to_hex(round_keys[10])})

    # Convert state to ciphertext hex
    ciphertext = bytes_to_hex(state)
    return steps, key_steps, ciphertext

# Streamlit App
st.title("AES 128-bit Encryption (Step by Step)")
plaintext_hex = st.text_input("Enter Plaintext (hex)", "00112233445566778899AABBCCDDEEFF")
key_hex = st.text_input("Enter Key (hex)", "FFEEDDCCBBAA99887766554433221100")

if st.button("Encrypt"):
    steps, key_steps, ciphertext = aes_encrypt(plaintext_hex, key_hex)
    
    st.write(f"Ciphertext: {ciphertext}")

    # Display key steps in a table
    key_df = pd.DataFrame(key_steps)
    st.subheader("Key Transformation Steps")
    st.table(key_df)
    
    # Display state steps in a table
    step_df = pd.DataFrame(steps)
    st.subheader("State Transformation Steps")
    st.table(step_df)

    
