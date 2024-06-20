# Password Manager

A password manager is a software application designed to store and manage online credentials. Typically, these credentials include usernames and passwords. Password managers securely store passwords in an encrypted database and allow users to access them with a single master password. They help users generate, retrieve, and manage complex passwords for various accounts and applications, ensuring enhanced security and convenience.

🔒 Features :
- Unique Encryption Algorithm: Encrypts data using a user-provided password, ensuring that without this password, decryption is impossible.
- Custom Encryption Patterns: Generates its own encryption pattern based on the encryption key, avoiding the use of specific hashes.
- Secure Deletion: Requires the encryption key for deletion, preventing unauthorized password removal.

🧠 Basic Concepts Used:
- Data Encryption and Decryption: Ensured data security through advanced encryption methods.
- Key-Based Authentication: Implemented key-based access for encryption, decryption, and deletion.
- Local Storage Security: Focused on secure local storage to maintain user privacy.


## Why Use a Password Manager?

In today's digital age, managing multiple passwords for various online services can be challenging. Password managers are essential tools that help users securely store and manage their passwords. They enable users to use strong, unique passwords for each service without the need to remember them all, thus enhancing online security and protecting against unauthorized access.

## Features

- Store and manage passwords securely.
- Easy-to-use graphical user interface.
- Cross-platform compatibility.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/WathsalaDewmina/Password-Manager.git
   cd Password-Manager
   ```

2. Install the required packages:

   ```sh
   pip3 install customtkinter
   pip3 install tkinter
   ```

## Usage

Run the main script using Python:

```sh
python3 main.py
```

## Converting to an Executable

You can convert the Python script to an executable file using PyInstaller. Follow these steps:

1. Install PyInstaller:

   ```sh
   pip3 install pyinstaller
   ```

2. Convert the script to an executable:

   ```sh
   pyinstaller --noconsole main.py
   ```

   This will generate the executable file in the `dist` directory.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
