# XOR ECB and CBC (Shift) Encryption

This project demonstrates a variant of XOR encryption using shift operations. Similar to the XOR ECB and CBC encryption, this version allows the encryption and decryption of text data but applies a shift to the key during the XOR operation.

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
- **ECB (Electronic Codebook) with Shift**:
In this mode, each block of plaintext is XORed with a shifted version of the key.

- **CBC (Cipher Block Chaining) with Shift**:
In CBC mode, each block of plaintext is XORed with the previous ciphertext block, and the key is shifted before each round of encryption. The first block is XORed with an initialization vector (IV).

### Available Outputs
- text
- binary
- hex