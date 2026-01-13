from sqlalchemy.orm import Session
from app.db import SessionLocal, engine, Base
from app.models import User

def main():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    names = ["Khalid", "Amina", "Sam", "Taylor"]
    users = []
    for n in names:
        u = db.query(User).filter(User.display_name == n).first()
        if not u:
            u = User(display_name=n)
            db.add(u)
            db.commit()
            db.refresh(u)
        users.append(u)

    print("\nDemo users:")
    for u in users:
        print(f"- id={u.id} name={u.display_name} api_key={u.api_key}")

    db.close()

if __name__ == "__main__":
    main()
