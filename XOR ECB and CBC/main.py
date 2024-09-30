import streamlit as st

# Convert text to binary
def text_to_bin(text_value):
    return ''.join(format(ord(char), '08b') for char in text_value)

# Convert hex to binary
def hex_to_bin(hex_value):
    return bin(int(hex_value, 16))[2:].zfill(len(hex_value) * 4)

# Convert binary to text
def bin_to_text(bin_value):
    return ''.join(chr(int(bin_value[i:i+8], 2)) for i in range(0, len(bin_value), 8))

# Convert binary to hex
def bin_to_hex(bin_value):
    return hex(int(bin_value, 2))[2:].zfill(len(bin_value) // 4)

# Function to XOR plaintext and key
def xor_bin(bin_plaintext, bin_key):
    key_length = len(bin_plaintext)
    bin_key = (bin_key * (key_length // len(bin_key) + 1))[:key_length] 
    
    result = ''.join(format(int(b1) ^ int(b2), '01b') for b1, b2 in zip(bin_plaintext, bin_key))
    return result

# Encryption function for ECB
def encrypt_ecb(bin_plaintext, bin_key):
    return xor_bin(bin_plaintext, bin_key)

# Encryption function for CBC
def encrypt_cbc(bin_plaintext, bin_key, bin_iv):
    xor_iv = xor_bin(bin_plaintext, bin_iv)
    return xor_bin(xor_iv, bin_key)

# Streamlit UI
st.title("Encrypt XOR ECB and CBC")

# Selectbox for encryption mode
encryption_mode = st.selectbox("Choose encryption mode:", ["ECB", "CBC"])

plaintext_mode = st.selectbox("Choose plaintext mode:", ["Text", "Binary", "Hex"])
key_mode = st.selectbox("Choose key mode:", ["Text", "Binary", "Hex"])
if encryption_mode == "CBC":
    iv_mode = st.selectbox("Choose IV mode:", ["Text", "Binary", "Hex"])
else:
    iv_mode = None

# Input for plaintext, key, and IV
plaintext_input = st.text_area("Enter plaintext:")
key_input = st.text_input("Enter key:")
if encryption_mode == "CBC":
    iv_input = st.text_input("Enter IV:")

if st.button("Encrypt"):
    # Convert plaintext and key to binary
    if plaintext_mode == "Text":
        bin_plaintext = text_to_bin(plaintext_input)
    elif plaintext_mode == "Hex":
        bin_plaintext = hex_to_bin(plaintext_input)
    else:
        bin_plaintext = plaintext_input

    if key_mode == "Text":
        bin_key = text_to_bin(key_input)
    elif key_mode == "Hex":
        bin_key = hex_to_bin(key_input)
    else:
        bin_key = key_input

    if len(bin_plaintext) % 4 != 0 or len(bin_key) % 4 != 0:
        st.error("Plaintext and key must be in 4-bit binary.")
    else:
        if encryption_mode == "CBC":
            if iv_mode == "Text":
                bin_iv = text_to_bin(iv_input)
            elif iv_mode == "Hex":
                bin_iv = hex_to_bin(iv_input)
            else:
                bin_iv = iv_input

            if len(bin_iv) % 4 != 0:
                st.error("IV must be in 4-bit binary.")
            else:
                bin_ciphertext = encrypt_cbc(bin_plaintext, bin_key, bin_iv)
        else:
            bin_ciphertext = encrypt_ecb(bin_plaintext, bin_key)

        # Convert ciphertext to hex and text
        hex_ciphertext = bin_to_hex(bin_ciphertext)
        text_ciphertext = bin_to_text(bin_ciphertext)

        # # Output to streamlit
        st.text_area("Output (Binary):", value=bin_ciphertext, height=100)
        st.text_area("Output (Hexa):", value=hex_ciphertext, height=100)
        st.text_area("Output (Text):", value=text_ciphertext, height=100)
