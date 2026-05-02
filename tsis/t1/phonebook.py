import csv
import json
from connect import get_connection


# ---------- HELPERS ----------
def get_or_create_group(cur, name):
    cur.execute("SELECT id FROM groups WHERE name=%s", (name,))
    res = cur.fetchone()
    if res:
        return res[0]

    cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id", (name,))
    return cur.fetchone()[0]


# ---------- INSERT ----------
def add_contact():
    first = input("First name: ")
    last = input("Last name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")

    conn = get_connection()
    cur = conn.cursor()

    gid = get_or_create_group(cur, group)

    cur.execute("""
        INSERT INTO contacts(first_name, second_name, email, birthday, group_id)
        VALUES (%s,%s,%s,%s,%s) RETURNING id
    """, (first, last, email, birthday, gid))

    cid = cur.fetchone()[0]

    while True:
        phone = input("Phone (or empty to stop): ")
        if not phone:
            break
        ptype = input("Type (home/work/mobile): ")

        cur.execute(
            "INSERT INTO phones(contact_id, phone, type) VALUES (%s,%s,%s)",
            (cid, phone, ptype)
        )

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Contact added")


# ---------- SEARCH ----------
def search():
    query = input("Search: ")
    sort = input("Sort by (name/birthday/date): ")

    order = "c.first_name"
    if sort == "birthday":
        order = "c.birthday"
    elif sort == "date":
        order = "c.created_at"

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT c.first_name, c.second_name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE c.first_name ILIKE %s
           OR c.second_name ILIKE %s
           OR c.email ILIKE %s
        ORDER BY {order}
    """, (f"%{query}%", f"%{query}%", f"%{query}%"))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


# ---------- FILTER ----------
def filter_group():
    group = input("Group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.first_name, c.second_name
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name=%s
    """, (group,))

    for r in cur.fetchall():
        print(r)

    cur.close()
    conn.close()


# ---------- PAGINATION ----------
def paginate():
    limit = 3
    offset = 0

    conn = get_connection()
    cur = conn.cursor()

    while True:
        cur.execute("""
            SELECT first_name, second_name FROM contacts
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        print("\n--- PAGE ---")
        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        elif cmd == "quit":
            break

    cur.close()
    conn.close()


# ---------- EXPORT ----------
def export_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.first_name, c.second_name, c.email, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """)

    result = []

    for row in cur.fetchall():
        cid = row[0]

        cur.execute("SELECT phone, type FROM phones WHERE contact_id=%s", (cid,))
        phones = cur.fetchall()

        result.append({
            "first_name": row[1],
            "second_name": row[2],
            "email": row[3],
            "group": row[4],
            "phones": phones
        })

    with open("contacts.json", "w") as f:
        json.dump(result, f, indent=4)

    print("✅ Exported")


# ---------- IMPORT ----------
def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    for c in data:
        cur.execute("SELECT id FROM contacts WHERE first_name=%s", (c["first_name"],))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{c['first_name']} exists (skip/overwrite): ")
            if choice == "skip":
                continue
            else:
                cur.execute("DELETE FROM contacts WHERE id=%s", (exists[0],))

        gid = get_or_create_group(cur, c["group"])

        cur.execute("""
            INSERT INTO contacts(first_name, second_name, email, group_id)
            VALUES (%s,%s,%s,%s) RETURNING id
        """, (c["first_name"], c["second_name"], c["email"], gid))

        cid = cur.fetchone()[0]

        for p in c["phones"]:
            cur.execute(
                "INSERT INTO phones(contact_id, phone, type) VALUES (%s,%s,%s)",
                (cid, p[0], p[1])
            )

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Imported")


# ---------- MENU ----------
def main():
    while True:
        print("\n--- PHONEBOOK ---")
        print("1 Add contact")
        print("2 Search")
        print("3 Filter by group")
        print("4 Pagination")
        print("5 Export JSON")
        print("6 Import JSON")
        print("0 Exit")

        c = input("Choose: ")

        if c == "1":
            add_contact()
        elif c == "2":
            search()
        elif c == "3":
            filter_group()
        elif c == "4":
            paginate()
        elif c == "5":
            export_json()
        elif c == "6":
            import_json()
        elif c == "0":
            break


if __name__ == "__main__":
    main()