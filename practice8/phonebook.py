# phonebook.py

import csv
from connect import get_connection


# инсерт ссв
def insert_from_csv(file_path):
    conn = get_connection()
    cur = conn.cursor()

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                cur.execute(
                    "INSERT INTO phonebook (second_name, first_name, phone) VALUES (%s, %s, %s)",
                    (row['second_name'], row['first_name'], row['phone'])
                )
            except Exception as e:
                print("Error inserting:", row, e)

    conn.commit()
    cur.close()
    conn.close()
    print("CSV data inserted!")


# инсерт консол
def insert_from_console():
    surname = input("Enter surname: ")
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO phonebook (second_name, first_name, phone) VALUES (%s, %s, %s)",
            (surname, name, phone)
        )
        conn.commit()
        print("Contact added!")
    except Exception as e:
        print("Error:", e)

    cur.close()
    conn.close()



def update_contact():
    name = input("Enter existing name: ")
    new_surname = input("New surname (or press enter to skip): ")
    new_name = input("New name (or press enter to skip): ")
    new_phone = input("New phone (or press enter to skip): ")

    conn = get_connection()
    cur = conn.cursor()

    if new_surname:
        cur.execute(
            "UPDATE phonebook SET second_name=%s WHERE second_name=%s",
            (new_surname, name)
        )


    if new_name:
        cur.execute(
            "UPDATE phonebook SET first_name=%s WHERE first_name=%s",
            (new_name, name)
        )

    if new_phone:
        cur.execute(
            "UPDATE phonebook SET phone=%s WHERE first_name=%s",
            (new_phone, name)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated!")



def query_contacts():
    print("1 - Search by surname")
    print("2 - Search by name")
    print("3 - Search by phone prefix")

    choice = input("Choose option: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter surname: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE second_name ILIKE %s",
            ('%' + name + '%',)
        )

    elif choice == "2":
        name = input("Enter name: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE first_name ILIKE %s",
            ('%' + name + '%',)
        )

    elif choice == "3":
        prefix = input("Enter phone  prefix: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE phone LIKE %s",
            (prefix + '%',)
        )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()



def delete_contact():
    print("1 - Delete by surname")
    print("2 - Delete by name")
    print("3 - Delete by phone")

    choice = input("Choose option: ")

    conn = get_connection()
    cur = conn.cursor()
    if choice == "1":
        id = input("Enter surname: ")
        cur.execute(
            "DELETE FROM phonebook WHERE second_name = %s",
            (name,)
        )
    elif choice == "2":
        name = input("Enter name: ")
        cur.execute(
            "DELETE FROM phonebook WHERE first_name=%s",
            (name,)
        )

    elif choice == "3":
        phone = input("Enter phone: ")
        cur.execute(
            "DELETE FROM phonebook WHERE phone=%s",
            (phone,)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted!")



def main():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Insert from CSV")
        print("2. Insert from console")
        print("3. Update contact")
        print("4. Query contacts")
        print("5. Delete contact")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()