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

def safe_int(value, default=0):
    """Safely convert a value to int, removing commas and handling errors."""
    if value is None or value == "":
        return default
    try:
        # Remove commas and convert to int
        cleaned = str(value).strip().replace(",", "")
        return int(float(cleaned))
    except (ValueError, TypeError):
        return default

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    runs = Column(Integer, nullable=False)
    country = Column(String, nullable=False)
    balls = Column(Integer, nullable=False)
    wickets = Column(Integer, nullable=False)
    sixes = Column(Integer, nullable=False)
    fours = Column(Integer, nullable=False)
    matches = Column(Integer, nullable=False)
    fifties = Column(Integer, nullable=False)
    centuries = Column(Integer, nullable=False)

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

        # collect last-seen value for duplicate names
        mapping = {}
        total = skipped = 0
        for row in reader:
            total += 1
            raw_name = row.get("player", "")
            if not raw_name:
                skipped += 1
                continue
            name = raw_name.strip()
            if not name:
                skipped += 1
                continue
            
            player_data = {
                "name": name,
                "runs": safe_int(row.get("runs")),
                "country": row.get("country", "").strip() or "Unknown",
                "balls": safe_int(row.get("balls")),
                "wickets": safe_int(row.get("wickets")),
                "sixes": safe_int(row.get("sixes")),
                "fours": safe_int(row.get("fours")),
                "matches": safe_int(row.get("matches")),
                "fifties": safe_int(row.get("fifties")),
                "centuries": safe_int(row.get("centuries"))
            }
            mapping[name] = player_data

    # insert into DB (last-seen mapping)
    db = SessionLocal()
    try:
        for name, player_data in mapping.items():
            # upsert-like behavior (simple): try update else insert
            existing = db.query(Player).filter(Player.name == name).first()
            if existing:
                existing.runs = player_data["runs"]
                existing.country = player_data["country"]
                existing.balls = player_data["balls"]
                existing.wickets = player_data["wickets"]
                existing.sixes = player_data["sixes"]
                existing.fours = player_data["fours"]
                existing.matches = player_data["matches"]
                existing.fifties = player_data["fifties"]
                existing.centuries = player_data["centuries"]
            else:
                db.add(Player(**player_data))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error during database operation: {e}")
        raise
    finally:
        db.close()

    print(f"Finished: read rows={total}, unique_players={len(mapping)}, skipped={skipped}")
    print(f"DB written to: {DB_PATH}")

if __name__ == "__main__":
    load_csv_to_db()
