"""
create_admin.py — creates an admin account. This is the ONLY way to get
an admin account on this platform; public registration deliberately
rejects role=admin (see app/schemas/user.py).

Usage:
    python -m scripts.create_admin --name "Jane Admin" --email admin@example.com --password "SomeStrongPassword123"

Or interactively (omit flags to be prompted):
    python -m scripts.create_admin
"""
import argparse
import getpass
import sys

from app.core.database import SessionLocal
from app.core.exceptions import AppError
from app.services.admin_service import create_admin_user


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an admin account for AI Recruiter.")
    parser.add_argument("--name", help="Admin's full name")
    parser.add_argument("--email", help="Admin's email address")
    parser.add_argument("--password", help="Admin's password (min 8 characters). Omit to be prompted securely.")
    args = parser.parse_args()

    name = args.name or input("Admin name: ").strip()
    email = args.email or input("Admin email: ").strip()
    password = args.password or getpass.getpass("Admin password: ")

    if len(password) < 8:
        print("Error: password must be at least 8 characters.", file=sys.stderr)
        sys.exit(1)

    db = SessionLocal()
    try:
        admin = create_admin_user(db, name=name, email=email, password=password)
        print(f"Admin account created: {admin.email} (id={admin.id})")
    except AppError as exc:
        print(f"Error: {exc.message}", file=sys.stderr)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
