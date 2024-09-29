# DES Algorithm Simulation in Streamlit

This project simulates the Data Encryption Standard (DES) algorithm using Python and Streamlit. The app allows users to input a plaintext and key, both in hexadecimal format, and observe the various stages of the DES encryption process step-by-step.

Install the required packages using pip:
```sh
pip install streamlit
```

## How to Run the App
1. Clone the repository:
2. Run the Streamlit app:
```sh
streamlit run main.py
```
3. The app will open in your default web browser. You can input a plaintext and key, both in **16-character hexadecimal format**, and explore the DES encryption process.

## Usage
### Sidebar Inputs
- **Plaintext hex string**: Input your plaintext in hexadecimal format. Default is `0123456789ABCDEF`.
- **Key hex string**: Input your 64-bit key in hexadecimal format. Default is `133457799BBCDFF1`.
### Available Outputs
- **Final Permutation (FP)**: View the ciphertext after encryption.
- **Initial Permutation (IP)**: View the initial permutation output along with L(0) and R(0) values.
- **Key Generation**: View the PC-1 output and key generation details for each round.
- **Round Iterations**: Select any of the 16 rounds to view intermediate results, including expansion, XOR output, S-box output, and the final permuted output.