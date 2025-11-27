from app.service.security_service import authentication, authorization, password_adhere
from app.service.mysql_service import (
    traversal_username_exist,
    insert_user,
    get_uuid_by_username,
    get_role,
    get_role_permission,
)
from app.common.enum import Role, Request, REQUEST_LABELS

def system_view():
    while True:
        print_unauth_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            uuid = login_flow()
            if uuid:
                main_menu(uuid)
        elif choice == "2":
            register_flow()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("❌ Invalid option.")

def print_unauth_menu():
    print("\n" + "=" * 40)
    print("          Welcome to justInvest")
    print("=" * 40)
    print("1. Login")
    print("2. Register")
    print("3. Exit")

def login_flow():
    print("\n=== Login ===")
    username = input("Username: ").strip().lower()
    password = input("Password: ").strip()

    if not authentication(username, password):
        print("❌ Incorrect username or password.")
        return None

    uuid = get_uuid_by_username(username)

    if not authorization(Request.AS, uuid):
        print("❌ Your role is not allowed to access the system.")
        return None

    print("✅ Login successful!")
    return uuid

def register_flow():
    print("\n=== Register ===")
    username = input("Enter username: ").strip().lower()

    if traversal_username_exist(username):
        print("❌ Username already exists.")
        return

    password = input("Enter password: ").strip()
    if not password_adhere(password, username):
        print("❌ Password does not meet required rules.")
        return

    name = input("Enter full name: ").strip()

    print("\nSelect role:")
    print("  C  - Client")
    print("  PC - Premium Client")
    print("  FA - Financial Advisor")
    print("  FP - Financial Planner")
    print("  T  - Teller")

    try:
        role_input = input("Enter role: ").strip().upper()
        role = Role(role_input)
    except ValueError:
        print("❌ Invalid role.")
        return

    insert_user(username, name, role, password)
    print("✅ Registration successful!")

def main_menu(uuid: str):
    from app.service.mysql_service import USER_INI_FILE
    import configparser
    cfg = configparser.ConfigParser()
    cfg.read(USER_INI_FILE)
    username = cfg[uuid]["username"]

    role = get_role(uuid)
    permissions = get_role_permission(role)

    while True:
        print(f"\n=== Welcome, {username} ({role.value}) ===")
        print("Select a request to perform (according to your permissions):\n")
        printable_requests = []
        for req in Request:
            flag = permissions[req.value]
            if flag in (1, 2):
                printable_requests.append(req)

        if not printable_requests:
            print("You have no permissions to perform operations.")
            print("Logging out...")
            return

        for req in printable_requests:
            print(f"{req.value}. {REQUEST_LABELS[req]}")

        print("X. Logout")

        choice = input("\nYour choice: ").strip().upper()

        if choice == "X":
            print("Logging out...")
            return

        if not choice.isdigit():
            print("❌ Invalid input.")
            continue

        selected_value = int(choice)
        if selected_value not in [r.value for r in printable_requests]:
            print("❌ You do not have this permission.")
            continue

        selected_request = Request(selected_value)

        if authorization(selected_request, uuid):
            print(f"➡️  Executing: {REQUEST_LABELS[selected_request]}")
        else:
            print("❌ Authorization denied.")
