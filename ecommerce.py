import os
import re
import random
import string


# ===========================================================================
#  CONSTANTS
# ===========================================================================
DATA_FOLDER   = "data"
ACCOUNTS_FILE = os.path.join(DATA_FOLDER, "accounts.txt")

FUND_OPTIONS = {
    1: 10_000,
    2: 20_000,
    3: 50_000,
    4: 100_000,
}

# ===========================================================================
#  STORAGE SETUP
# ===========================================================================

def setup_storage():
    """Create the data folder and accounts.txt file if they don't exist."""
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
        print("[INFO] 'data' folder created.")

    if not os.path.exists(ACCOUNTS_FILE):
        open(ACCOUNTS_FILE, "w").close()
        print("[INFO] 'accounts.txt' file created.")


# ===========================================================================
#  INVENTORY LOADING
# ===========================================================================

def load_inventory():
    """
    Read all warehouse*.txt files from the data folder.
    Returns a dict:  { "Product Name": {"price": int, "quantity": int} }
    Quantity starts at 100 for every item (simulated stock).
    """
    inventory = {}

    if not os.path.exists(DATA_FOLDER):
        print("[ERROR] Data folder not found. Cannot load inventory.")
        return inventory

    warehouse_count = 0
    for filename in sorted(os.listdir(DATA_FOLDER)):
        if filename.startswith("warehouse") and filename.endswith(".txt"):
            warehouse_count += 1
            filepath = os.path.join(DATA_FOLDER, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                print(f"[WARNING] Could not read '{filename}': {e}")
                continue

            for raw_item in content.split(";"):
                item = raw_item.strip()
                if not item or ":" not in item:
                    continue
                idx = item.rfind(":")
                name      = item[:idx].strip()
                price_str = item[idx + 1:].strip()
                if not name:
                    continue
                try:
                    price = int(price_str)
                    inventory[name] = {"price": price, "quantity": 100}
                except ValueError:
                    pass

    print(f"[INFO] Loaded {len(inventory):,} products from {warehouse_count} warehouse file(s).\n")
    return inventory


# ===========================================================================
#  SEARCH  (adapted from the provided search.py)
# ===========================================================================

def search_inventory(query, inventory):
    """
    Case-insensitive, multi-word search through inventory keys.
    Returns a list of matching product name strings.
    """
    words   = query.split()
    patterns = [re.compile(re.escape(w), re.IGNORECASE) for w in words]
    results  = []
    for item_name in inventory:
        if all(p.search(item_name) for p in patterns):
            results.append(item_name)
    return results


# ===========================================================================
#  PASSWORD UTILITIES
# ===========================================================================

def is_valid_password(password):
    """
    Password rules:
      - At least 16 characters
      - At least one lowercase letter
      - At least one uppercase letter
      - At least one digit
      - At least one special character
    Returns (True, "") on success or (False, reason) on failure.
    """
    if len(password) < 16:
        return False, "Password must be at least 16 characters long."
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit."
    if not any(c in string.punctuation for c in password):
        return False, "Password must contain at least one special character (!@#$%^ etc.)."
    return True, ""


def generate_password(length=20):
    """Auto-generate a password that meets all the rules."""
    while True:
        chars = (
            random.choices(string.ascii_lowercase, k=4) +
            random.choices(string.ascii_uppercase, k=4) +
            random.choices(string.digits,          k=4) +
            random.choices(string.punctuation,     k=4) +
            random.choices(string.ascii_letters + string.digits + string.punctuation,
                           k=max(0, length - 16))
        )
        random.shuffle(chars)
        pwd = "".join(chars)
        ok, _ = is_valid_password(pwd)
        if ok:
            return pwd


# ===========================================================================
#  ACCOUNTS FILE  (read / write helpers)
# ===========================================================================

def read_all_accounts():
    """
    Read accounts.txt and return a list of dicts:
    [{ "username": .., "email": .., "password": .., "balance": float }, ...]
    """
    accounts = []
    if not os.path.exists(ACCOUNTS_FILE):
        return accounts
    with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 4:
                continue
            username, email, password, balance_str = parts
            try:
                balance = float(balance_str.strip())
            except ValueError:
                balance = 0.0
            accounts.append({
                "username": username.strip(),
                "email":    email.strip(),
                "password": password.strip(),
                "balance":  balance,
            })
    return accounts


def write_all_accounts(accounts):
    """Overwrite accounts.txt with the current list of account dicts."""
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        for acc in accounts:
            f.write(f"{acc['username']},{acc['email']},{acc['password']},{acc['balance']:.2f}\n")


def find_account(identifier):
    """
    Find an account by username OR email (case-insensitive).
    Returns the account dict or None.
    """
    for acc in read_all_accounts():
        if (acc["username"].lower() == identifier.lower() or
                acc["email"].lower() == identifier.lower()):
            return acc
    return None


def update_account(updated_acc):
    """Replace the matching account record in accounts.txt."""
    accounts = read_all_accounts()
    for i, acc in enumerate(accounts):
        if acc["username"].lower() == updated_acc["username"].lower():
            accounts[i] = updated_acc
            break
    write_all_accounts(accounts)


def delete_account_from_file(username):
    """Remove an account from accounts.txt by username."""
    accounts = [a for a in read_all_accounts()
                if a["username"].lower() != username.lower()]
    write_all_accounts(accounts)


# ===========================================================================
#  DISPLAY HELPERS
# ===========================================================================

def divider(char="=", width=60):
    print(char * width)


def header(title):
    divider()
    print(f"  {title}")
    divider()


def format_naira(amount):
    return f"NGN {amount:,.2f}"


def pause():
    input("\nPress Enter to continue...")


# ===========================================================================
#  LOGIN SECTION
# ===========================================================================

def sign_in():
    """
    Prompt for username/email + password.
    Returns the account dict on success, or None on failure.
    """
    header("SIGN IN")
    identifier = input("  Username or Email: ").strip()
    if not identifier:
        print("  [!] Input cannot be empty.")
        return None

    acc = find_account(identifier)
    if not acc:
        print("  [!] No account found with that username or email.")
        return None

    password = input("  Password: ").strip()
    if password != acc["password"]:
        print("  [!] Incorrect password.")
        return None

    print(f"\n  Welcome back, {acc['username']}!")
    return acc


def sign_up():
    """
    Guide a new user through account creation.
    Returns the newly created account dict, or None if cancelled.
    """
    header("SIGN UP")
    accounts = read_all_accounts()
    existing_usernames = {a["username"].lower() for a in accounts}
    existing_emails    = {a["email"].lower()    for a in accounts}

    # --- Username ---
    while True:
        username = input("  Choose a username: ").strip()
        if not username:
            print("  [!] Username cannot be empty.")
            continue
        if username.lower() in existing_usernames:
            print("  [!] That username is already taken. Try another.")
            continue
        break

    # --- Email ---
    while True:
        email = input("  Enter your email address: ").strip()
        if not email or "@" not in email:
            print("  [!] Please enter a valid email address.")
            continue
        if email.lower() in existing_emails:
            print("  [!] That email is already registered. Try another.")
            continue
        break

    # --- Password ---
    print("\n  How would you like to set your password?")
    print("  1. Enter it manually")
    print("  2. Auto-generate a secure password")
    while True:
        choice = input("  Choose (1/2): ").strip()
        if choice == "1":
            while True:
                password = input("  Enter password (min 16 chars, upper, lower, digit, symbol): ").strip()
                ok, reason = is_valid_password(password)
                if ok:
                    break
                print(f"  [!] {reason}")
            break
        elif choice == "2":
            password = generate_password()
            print(f"  Your generated password is: {password}")
            print("  IMPORTANT: Please save this password somewhere safe!")
            break
        else:
            print("  [!] Please enter 1 or 2.")

    new_account = {
        "username": username,
        "email":    email,
        "password": password,
        "balance":  0.0,
    }

    accounts.append(new_account)
    write_all_accounts(accounts)

    print(f"\n  Account created successfully! Welcome, {username}!")
    return new_account


def login_section():
    """
    Main login loop. Returns a logged-in account dict when successful,
    or None if the user chooses to exit.
    """
    while True:
        header("SHOPPY - Mock E-Commerce Store")
        print("  1. Sign In")
        print("  2. Sign Up")
        print("  3. Exit")
        divider("-")
        choice = input("  Choose an option: ").strip()

        if choice == "1":
            acc = sign_in()
            if acc:
                return acc
            pause()

        elif choice == "2":
            acc = sign_up()
            if acc:
                pause()
                return acc
            pause()

        elif choice == "3":
            print("\n  Thank you for visiting Shoppy. Goodbye!")
            return None

        else:
            print("  [!] Invalid option. Please choose 1, 2, or 3.")
            pause()


# ===========================================================================
#  FUND WALLET
# ===========================================================================

def fund_wallet(current_user):
    """Let the user add money to their wallet."""
    while True:
        header("FUND WALLET")
        print(f"  Current Balance: {format_naira(current_user['balance'])}\n")
        for num, amount in FUND_OPTIONS.items():
            print(f"  {num}. {format_naira(amount)}")
        print("  5. Back to Main Menu")
        divider("-")
        choice = input("  Select an amount to fund: ").strip()

        if choice == "5":
            break

        try:
            option = int(choice)
        except ValueError:
            print("  [!] Please enter a valid number.")
            pause()
            continue

        if option not in FUND_OPTIONS:
            print("  [!] Invalid option. Choose 1 to 4.")
            pause()
            continue

        amount = FUND_OPTIONS[option]
        current_user["balance"] += amount
        update_account(current_user)
        print(f"\n  ✓ {format_naira(amount)} has been added to your wallet.")
        print(f"  New Balance: {format_naira(current_user['balance'])}")

        again = input("\n  Fund again? (y/n): ").strip().lower()
        if again != "y":
            break


# ===========================================================================
#  PURCHASE SECTION
# ===========================================================================

def display_search_results(results):
    print()
    for i, name in enumerate(results, 1):
        print(f"  {i}. {name}")
    print()


def search_menu(current_user, inventory, cart):
    """Search for items and optionally add them to cart."""
    while True:
        header("SEARCH")
        query = input("  Search for an item: ").strip()

        if not query:
            print("  [!] Search query cannot be empty.")
            pause()
            continue

        results = search_inventory(query, inventory)

        if not results:
            print(f'\n  No items matched "{query}".')
        else:
            print(f"\n  Found {len(results)} result(s):\n")
            display_search_results(results)

        print("  1. Search Again")
        print("  2. Add Item to Cart")
        print("  3. Back to Purchase Menu")
        divider("-")
        choice = input("  Choose an option: ").strip()

        if choice == "1":
            continue

        elif choice == "2":
            if not results:
                print("  [!] No results to add. Please search first.")
                pause()
                continue

            display_search_results(results)
            while True:
                try:
                    item_num = int(input("  Enter item number to add to cart: ").strip())
                    if 1 <= item_num <= len(results):
                        break
                    print(f"  [!] Please enter a number between 1 and {len(results)}.")
                except ValueError:
                    print("  [!] Please enter a valid number.")

            chosen_name = results[item_num - 1]

            if inventory[chosen_name]["quantity"] <= 0:
                print(f"  [!] Sorry, '{chosen_name}' is out of stock.")
                pause()
                continue

            # Decrease inventory, increase cart
            inventory[chosen_name]["quantity"] -= 1
            if chosen_name in cart:
                cart[chosen_name]["quantity"] += 1
            else:
                cart[chosen_name] = {
                    "price":    inventory[chosen_name]["price"],
                    "quantity": 1,
                }
            print(f"  ✓ '{chosen_name}' added to cart.")
            pause()

        elif choice == "3":
            break

        else:
            print("  [!] Invalid option.")
            pause()


def view_cart(cart):
    """Display all items currently in the cart."""
    if not cart:
        print("\n  Your cart is empty.")
        return
    print()
    divider("-")
    print(f"  {'#':<4} {'Product':<42} {'Qty':<6} {'Price':<12} {'Subtotal'}")
    divider("-")
    total = 0
    for i, (name, info) in enumerate(cart.items(), 1):
        subtotal = info["price"] * info["quantity"]
        total   += subtotal
        print(f"  {i:<4} {name[:40]:<42} {info['quantity']:<6} "
              f"{format_naira(info['price']):<14} {format_naira(subtotal)}")
    divider("-")
    print(f"  {'TOTAL':<54} {format_naira(total)}")
    divider("-")
    print()


def manage_cart(current_user, inventory, cart):
    """Full cart management sub-menu."""
    while True:
        header("MANAGE CART")
        print("  1. View Items in Cart")
        print("  2. Add Items to Cart  (from inventory list)")
        print("  3. Remove Items from Cart")
        print("  4. Clear Cart")
        print("  5. Back to Purchase Menu")
        divider("-")
        choice = input("  Choose an option: ").strip()

        # ---- View ----
        if choice == "1":
            view_cart(cart)
            pause()

        # ---- Add ----
        elif choice == "2":
            query = input("  Search for an item to add: ").strip()
            if not query:
                print("  [!] Search query cannot be empty.")
                pause()
                continue
            results = search_inventory(query, inventory)
            if not results:
                print("  No matching items found.")
                pause()
                continue
            display_search_results(results)
            while True:
                try:
                    num = int(input("  Enter item number to add: ").strip())
                    if 1 <= num <= len(results):
                        break
                    print(f"  [!] Choose between 1 and {len(results)}.")
                except ValueError:
                    print("  [!] Enter a valid number.")
            chosen = results[num - 1]
            if inventory[chosen]["quantity"] <= 0:
                print(f"  [!] '{chosen}' is out of stock.")
            else:
                inventory[chosen]["quantity"] -= 1
                if chosen in cart:
                    cart[chosen]["quantity"] += 1
                else:
                    cart[chosen] = {"price": inventory[chosen]["price"], "quantity": 1}
                print(f"  ✓ '{chosen}' added to cart.")
            pause()

        # ---- Remove ----
        elif choice == "3":
            if not cart:
                print("  [!] Your cart is empty.")
                pause()
                continue
            view_cart(cart)
            cart_items = list(cart.keys())
            while True:
                try:
                    num = int(input("  Enter item number to remove (0 to cancel): ").strip())
                    if num == 0:
                        break
                    if 1 <= num <= len(cart_items):
                        break
                    print(f"  [!] Choose between 1 and {len(cart_items)}.")
                except ValueError:
                    print("  [!] Enter a valid number.")
            if num == 0:
                continue
            chosen = cart_items[num - 1]
            # Return one unit to inventory
            inventory[chosen]["quantity"] += 1
            cart[chosen]["quantity"] -= 1
            if cart[chosen]["quantity"] == 0:
                del cart[chosen]
            print(f"  ✓ One unit of '{chosen}' removed from cart.")
            pause()

        # ---- Clear ----
        elif choice == "4":
            if not cart:
                print("  [!] Your cart is already empty.")
                pause()
                continue
            confirm = input("  Are you sure you want to clear your entire cart? (y/n): ").strip().lower()
            if confirm == "y":
                for name, info in cart.items():
                    inventory[name]["quantity"] += info["quantity"]
                cart.clear()
                print("  ✓ Cart cleared.")
            pause()

        # ---- Exit ----
        elif choice == "5":
            break

        else:
            print("  [!] Invalid option.")
            pause()


def checkout(current_user, inventory, cart):
    """Process payment for all items in the cart."""
    header("CHECKOUT")

    if not cart:
        print("  [!] Your cart is empty. Nothing to checkout.")
        pause()
        return

    view_cart(cart)

    proceed = input("  Proceed to payment? (y/n): ").strip().lower()
    if proceed != "y":
        print("  Returning to Purchase Menu...")
        pause()
        return

    total = sum(info["price"] * info["quantity"] for info in cart.values())
    print(f"\n  Total Amount Due: {format_naira(total)}")
    confirm = input("  Confirm payment? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Payment cancelled.")
        pause()
        return

    if current_user["balance"] < total:
        print(f"\n  [!] Insufficient funds.")
        print(f"  Your Balance : {format_naira(current_user['balance'])}")
        print(f"  Amount Due   : {format_naira(total)}")
        print("  Please fund your wallet and try again.")
        pause()
        return

    # Debit the account
    current_user["balance"] -= total
    update_account(current_user)
    cart.clear()

    print("\n  ✓ Payment Successful!")
    print(f"  Amount Paid     : {format_naira(total)}")
    print(f"  Remaining Balance: {format_naira(current_user['balance'])}")
    pause()


def purchase_section(current_user, inventory, cart):
    """Purchase sub-menu."""
    while True:
        header("PURCHASE")
        print("  1. Search for Items")
        print("  2. Manage Cart")
        print("  3. Checkout")
        print("  4. Exit Purchase Menu")
        divider("-")
        choice = input("  Choose an option: ").strip()

        if choice == "1":
            search_menu(current_user, inventory, cart)
        elif choice == "2":
            manage_cart(current_user, inventory, cart)
        elif choice == "3":
            checkout(current_user, inventory, cart)
        elif choice == "4":
            break
        else:
            print("  [!] Invalid option.")
            pause()


# ===========================================================================
#  MANAGE ACCOUNT
# ===========================================================================

def verify_password(current_user):
    """Ask user for their password. Returns True if correct."""
    pwd = input("  Enter your current password to continue: ").strip()
    if pwd != current_user["password"]:
        print("  [!] Incorrect password. Access denied.")
        return False
    return True


def change_username(current_user):
    header("CHANGE USERNAME")
    if not verify_password(current_user):
        pause()
        return

    accounts = read_all_accounts()
    existing = {a["username"].lower() for a in accounts
                if a["username"].lower() != current_user["username"].lower()}

    while True:
        new_username = input("  Enter new username: ").strip()
        if not new_username:
            print("  [!] Username cannot be empty.")
            continue
        if new_username.lower() in existing:
            print("  [!] That username is already taken.")
            continue
        break

    current_user["username"] = new_username
    update_account(current_user)
    print(f"  ✓ Username changed to '{new_username}' successfully.")
    pause()


def change_email(current_user):
    header("CHANGE EMAIL")
    if not verify_password(current_user):
        pause()
        return

    accounts = read_all_accounts()
    existing = {a["email"].lower() for a in accounts
                if a["email"].lower() != current_user["email"].lower()}

    while True:
        new_email = input("  Enter new email address: ").strip()
        if not new_email or "@" not in new_email:
            print("  [!] Please enter a valid email address.")
            continue
        if new_email.lower() in existing:
            print("  [!] That email is already in use.")
            continue
        break

    current_user["email"] = new_email
    update_account(current_user)
    print(f"  ✓ Email changed to '{new_email}' successfully.")
    pause()


def change_password(current_user):
    header("CHANGE PASSWORD")
    if not verify_password(current_user):
        pause()
        return

    print("\n  1. Enter new password manually")
    print("  2. Auto-generate a new password")
    while True:
        choice = input("  Choose (1/2): ").strip()
        if choice == "1":
            while True:
                new_pwd = input("  New password: ").strip()
                ok, reason = is_valid_password(new_pwd)
                if ok:
                    break
                print(f"  [!] {reason}")
            break
        elif choice == "2":
            new_pwd = generate_password()
            print(f"  Generated password: {new_pwd}")
            print("  Please save this somewhere safe!")
            break
        else:
            print("  [!] Enter 1 or 2.")

    current_user["password"] = new_pwd
    update_account(current_user)
    print("  ✓ Password changed successfully.")
    pause()


def view_account_details(current_user):
    header("ACCOUNT DETAILS")
    if not verify_password(current_user):
        pause()
        return
    print()
    print(f"  Username : {current_user['username']}")
    print(f"  Email    : {current_user['email']}")
    print(f"  Balance  : {format_naira(current_user['balance'])}")
    pause()


def reset_balance(current_user):
    header("RESET BALANCE")
    if not verify_password(current_user):
        pause()
        return

    print(f"\n  Current Balance: {format_naira(current_user['balance'])}")
    confirm = input("  Are you sure you want to reset your balance to NGN 0.00? (y/n): ").strip().lower()
    if confirm == "y":
        current_user["balance"] = 0.0
        update_account(current_user)
        print("  ✓ Balance has been reset to NGN 0.00.")
    else:
        print("  Reset cancelled.")
    pause()


def delete_account(current_user):
    """Delete the account. Returns True if deleted so caller can redirect to login."""
    header("DELETE ACCOUNT")
    if not verify_password(current_user):
        pause()
        return False

    print("\n  WARNING: This action is permanent and cannot be undone!")
    confirm = input("  Type DELETE to confirm account deletion: ").strip()
    if confirm != "DELETE":
        print("  Deletion cancelled.")
        pause()
        return False

    delete_account_from_file(current_user["username"])
    print("  ✓ Your account has been permanently deleted.")
    pause()
    return True


def manage_account(current_user):
    """
    Account management sub-menu.
    Returns "logout" or "deleted" so the caller knows what to do next.
    """
    while True:
        header("MANAGE ACCOUNT")
        print(f"  Logged in as: {current_user['username']}\n")
        print("  1. Change Username")
        print("  2. Change Email")
        print("  3. Change Password")
        print("  4. View Account Balance / Details")
        print("  5. Reset Balance")
        print("  6. Delete Account")
        print("  7. Logout")
        print("  8. Exit Manage Account")
        divider("-")
        choice = input("  Choose an option: ").strip()

        if choice == "1":
            change_username(current_user)
        elif choice == "2":
            change_email(current_user)
        elif choice == "3":
            change_password(current_user)
        elif choice == "4":
            view_account_details(current_user)
        elif choice == "5":
            reset_balance(current_user)
        elif choice == "6":
            deleted = delete_account(current_user)
            if deleted:
                return "deleted"
        elif choice == "7":
            print(f"\n  {current_user['username']} has been logged out.")
            pause()
            return "logout"
        elif choice == "8":
            break
        else:
            print("  [!] Invalid option.")
            pause()

    return "continue"


# ===========================================================================
#  RUN SECTION  (main menu after login)
# ===========================================================================

def run_section(current_user, inventory):
    """
    Main application loop after the user logs in.
    Returns True to stay in the login loop, False to exit the program.
    """
    cart = {}  # Fresh cart per session

    while True:
        header(f"SHOPPY  |  Welcome, {current_user['username']}")
        print(f"  Balance: {format_naira(current_user['balance'])}\n")
        print("  1. Fund Wallet")
        print("  2. Make a Purchase")
        print("  3. Manage Account")
        print("  4. Exit")
        divider("-")
        choice = input("  Choose an option: ").strip()

        if choice == "1":
            fund_wallet(current_user)

        elif choice == "2":
            purchase_section(current_user, inventory, cart)

        elif choice == "3":
            result = manage_account(current_user)
            if result in ("logout", "deleted"):
                return True   # Go back to login screen

        elif choice == "4":
            print(f"\n  {current_user['username']} has been securely logged out.")
            print("  Thank you for shopping with Shoppy!")
            print("  We hope to see you again soon. Goodbye! 👋")
            return False      # Exit the entire program

        else:
            print("  [!] Invalid option. Please choose 1 to 4.")
            pause()


# ===========================================================================
#  ENTRY POINT
# ===========================================================================

def main():
    print("\n" + "=" * 60)
    print("   Welcome to SHOPPY - Your Mock E-Commerce Store")
    print("=" * 60)

    # 1. Set up folders and files
    setup_storage()

    # 2. Load all products into memory
    inventory = load_inventory()

    if not inventory:
        print("[ERROR] Inventory is empty. Please check your data folder.")
        return

    # 3. Login / run loop
    while True:
        user = login_section()

        if user is None:
            # User chose Exit from the login screen
            break

        keep_running = run_section(user, inventory)

        if not keep_running:
            # User chose Exit from the main menu
            break


if __name__ == "__main__":
    main()
