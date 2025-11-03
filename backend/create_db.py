# backend/create_db_from_csv.py
import csv
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Index
from sqlalchemy.orm import sessionmaker, declarative_base

# Paths (adjust if your repo layout differs)
REPO_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = REPO_ROOT / "output" / "tabular" / "batter_agg.csv"
DB_PATH = REPO_ROOT / "backend" / "players.db"
SQLITE_URL = f"sqlite:///{DB_PATH}"

# SQLAlchemy setup
engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    runs = Column(Integer, nullable=False)

def load_csv_to_db():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV not found at {CSV_PATH}")

    # create tables
    Base.metadata.create_all(bind=engine)

    with CSV_PATH.open(newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        headers = reader.fieldnames or []
        if not headers:
            raise RuntimeError("CSV has no headers")

        name_col = "player"
        runs_col = "runs"

        # collect last-seen value for duplicate names
        mapping = {}
        total = skipped = 0
        for row in reader:
            total += 1
            raw_name = row.get(name_col, "")
            raw_runs = row.get(runs_col, "")
            if not raw_name:
                skipped += 1
                continue
            name = raw_name.strip()
            if not name:
                skipped += 1
                continue
            runs_str = str(raw_runs).strip().replace(",", "")
            try:
                runs_int = int(float(runs_str))
            except Exception:
                skipped += 1
                continue
            mapping[name] = runs_int

    # insert into DB (last-seen mapping)
    db = SessionLocal()
    try:
        for name, runs_int in mapping.items():
            # upsert-like behavior (simple): try update else insert
            existing = db.query(Player).filter(Player.name == name).first()
            if existing:
                existing.runs = runs_int
            else:
                db.add(Player(name=name, runs=runs_int))
        db.commit()
    finally:
        db.close()

    print(f"Finished: read rows={total}, unique_players={len(mapping)}, skipped={skipped}")
    print(f"DB written to: {DB_PATH}")

if __name__ == "__main__":
    load_csv_to_db()
