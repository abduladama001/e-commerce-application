# 🛒 Shoppy — Mock E-Commerce Application


A fully functional console-based e-commerce application built entirely in Python. Shoppy lets users sign up, log in, search over **3,700+ products**, manage a shopping cart, fund a wallet, and checkout securely — all from the terminal.


Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Project Structure](#project-structure)
- [Data Files](#data-files)
- [Setup & Installation](#setup--installation)
- [How to Run](#how-to-run)
- [How to Use](#how-to-use)
- [Group Members](#group-members)

---

About the Project

This project was built as part of the Python Beginners Cohort 32 group assignment. The goal was to design and implement a mock e-commerce application using only Python, with no graphical interface — just the terminal.

The program loads product inventory from a set of warehouse text files, manages user accounts stored in a plain text file, and provides a complete shopping experience including search, cart management, wallet funding, and secure checkout.

 Features

| Feature | Description |
|---|---|
| **Sign Up** | Create an account with a unique username, email, and a strong password |
| **Sign In** | Log in securely using your username or email |
| **Password Rules** | Passwords must be 16+ characters with uppercase, lowercase, digit, and symbol |
| **Auto Password** | The program can generate a secure password for you automatically |
| **Fund Wallet** | Add NGN 10,000 / 20,000 / 50,000 / 100,000 to your wallet |
| **Product Search** | Case-insensitive, multi-word search across 3,700+ products |
| **Shopping Cart** | Add, remove, and clear items with live inventory syncing |
| **Checkout** | Automatic balance check, payment processing, and receipt confirmation |
| **Manage Account** | Change username, email, password, view balance, reset, or delete account |
| **Data Persistence** | All account changes are saved immediately to `accounts.txt` |

---

Project Structure

```
Group-7/
│
├── ecommerce.py          # Main Python application
├── README.md             # This file
├── .gitignore            # Tells Git to ignore system files
│
└── data/
    ├── warehouse1.txt    # Product inventory files
    ├── warehouse2.txt
    ├── warehouse3.txt
    ├── warehouse4.txt
    ├── warehouse5.txt
    ├── warehouse6.txt
    ├── warehouse7.txt
    ├── warehouse8.txt
    ├── warehouse9.txt
    ├── warehouse10.txt
    ├── warehouse11.txt
    ├── warehouse12.txt
    ├── warehouse13.txt
    ├── warehouse14.txt
    └── accounts.txt      # Created automatically on first run
```

---

Data Files

The `data/` folder contains the warehouse inventory files that the program reads on startup. Each file holds hundreds of products in this format:

```
ProductName: Price;ProductName: Price;ProductName: Price
```

For example:
```
Rice (50kg): 115000;Garri (yellow 50kg): 28000;Beans (Oloyin 50kg): 65000
```

The program parses all 14 warehouse files on startup and loads every product into memory. In total, **3,782 products** are available across all files, covering categories like food, electronics, furniture, clothing, household items, and more. Prices are in Nigerian Naira (NGN).

The `accounts.txt` file is **not included** in this repository — it is created automatically the first time you run the program. It stores user account information in this format:

```
username,email,password,balance


Setup & Installation

Requirements

- Python 3.x — download from [python.org](https://www.python.org/downloads/)
- No third-party libraries needed — the program uses only Python's built-in modules

Step 1 — Clone the Repository

bash
git clone https://github.com/yourusername/Group-7.git


Or download the ZIP from GitHub and extract it.

Step 2 — Verify the Data Folder

Make sure the `data/` folder exists inside the project folder and contains all 14 warehouse `.txt` files. The folder structure should match exactly what is shown in the [Project Structure](#project-structure) section above.

Step 3 — Run the Program

bash
cd Group-7
python ecommerce.py
```

On first run, the program will automatically create `accounts.txt` inside the `data/` folder. You do not need to create it manually.

---

How to Run

Navigate to the project folder in your terminal and run:

```bash
python ecommerce.py
```

If that does not work, try:

```bash
python3 ecommerce.py
```

You should see this on startup:

```
============================================================
   Welcome to SHOPPY - Your Mock E-Commerce Store
============================================================
[INFO] Loaded 3,782 products from 14 warehouse file(s).
```

---

How to Use

Login Screen
When the program starts you will see three options:
- **1. Sign In** — for returning users
- **2. Sign Up** — to create a new account
- **3. Exit** — to close the program

Main Menu (after login)
- **1. Fund Wallet** — choose an amount to add to your balance
- **2. Make a Purchase** — search for products and shop
- **3. Manage Account** — update your account details
- **4. Exit** — log out and close the program

Searching for Products
Type any product name or brand in the search box. The search is case-insensitive and supports multiple words. For example, searching `samsung tv` will return all products that contain both `samsung` AND `tv` in their name.

Password Requirements
When creating or changing a password, it must meet all of these rules:
- At least **16 characters** long
- At least one **uppercase** letter (A–Z)
- At least one **lowercase** letter (a–z)
- At least one **number** (0–9)
- At least one **special character** (!@#$%^&* etc.)