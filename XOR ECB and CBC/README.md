# XOR Encryption in ECB and CBC Modes

This project demonstrates the XOR encryption algorithm using both ECB (Electronic Codebook) and CBC (Cipher Block Chaining) modes. It allows the encryption and decryption of text data by applying the XOR operation between the plaintext and a key.

## How to Run the App
Run the Streamlit app:
```sh
streamlit run main.py
```

## Usage
### Input Format
- The plaintext can be provided in text, binary, and hex.
- The key can be entered as a text, binary, and hex.
- IV can be entered as a text, binary, and hex (CBC).

### Encryption Modes
- **ECB (Electronic Codebook)**:
In ECB mode, each block of plaintext is XORed independently with the key.

- **CBC (Cipher Block Chaining)**:
In CBC mode, each block of plaintext is XORed with the previous ciphertext block before encryption. The first block is XORed with an initialization vector (IV).

### Available Outputs
- text
- binary
- hex