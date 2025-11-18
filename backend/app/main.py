# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pathlib import Path
from prompt import db_schema, supported_charts
from schemas import PlayerRequest, PlayerResponse, NLAskRequest, NLAskResponse
from google import genai
import yaml

# Paths (adjust if needed)
REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / "players.db"
SQLITE_URL = f"sqlite:///{DB_PATH}"
creds = yaml.safe_load(open('./../../secrets.yml'))
GEMINI_KEY = creds['GEMINI_KEY']

# SQLAlchemy setup (local dev friendly)
engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Mirror of the Player table (ORM mapping used only to query)
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

# create tables if missing (safe; no-op if exists)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PlayerRuns API (SQLite)")

# CORS for local dev (Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/player_runs", response_model=PlayerResponse)
def get_player_runs(req: PlayerRequest, db: Session = Depends(get_db)):
    name = (req.name or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="empty name")
   
    player = db.query(Player).filter(Player.name == name).first()
    if not player:
        raise HTTPException(status_code=404, detail="player not found")
    # PlayerResponse will read from ORM object because orm_mode=True
    return player

@app.post("/api/ask", response_model=NLAskResponse)
def get_user_answer(req: NLAskRequest, db: Session = Depends(get_db)):
    query = req.query.strip()
    if not query:
        return HTTPException(status_code=400, detail="empty query")
    
    # text to sql
    # create client
    client = genai.Client(api_key=GEMINI_KEY)

    # create the prompt
    prompt = f"""given the data schema:
    {db_schema}

Convert this natural language query to SQL:
"{query}"

START YOUR RESPONSE WITH THE QUERY DIRECTLY, WITHOUT ANY CODE BLOCK DELIMITERS (e.g. sql)
you must ONLY return valid SQL SELECT statements, nothing else.
Use SQLite syntax.
IMPORTANT: Only return SELECT statement, never INSERT/UPDATE/DELETE/DROP.
    """
    # convert to sql
    sql_query = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    sql_query = sql_query.text.strip()
    # print(prompt, sql_query)
    
    # validate the sql
    sql_upper = sql_query.upper().strip()
    if not sql_upper.startswith("SELECT"):
        raise HTTPException(
            status_code=400, 
            detail="Only SELECT queries are allowed"
        )
    
    # Check for dangerous keywords
    dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "CREATE"]
    if any(keyword in sql_upper for keyword in dangerous_keywords):
        raise HTTPException(
            status_code=400,
            detail="Query contains forbidden operations"
        )
    
    # execute the sql
    try:
        result = db.execute(text(sql_query))
        rows = result.fetchall()
        
        # Convert to list of dicts
        columns = result.keys()
        results = [dict(zip(columns, row)) for row in rows][:10] # limit to a maximum of 10 rows
        
        # # Generate interpretation
        # interpretation_prompt = f"""The user asked: {query}
        # We executed this SQL: {sql_query}
        # We got following results: {results}

        # Provide a brief, natural language summary of what we found."""
        
        # interp_message = client.messages.create()
        
        # interpretation = interp_message.content[0].text.strip()

        # Generate Viz Hint
        # viz_prompt = f"""We have this sql query: {sql_query}
        
        # Select one from {supported_charts} as the most appropriate chart to represent data fetched from this query.
        # Only return the answer and NOTHING else. Return 'undecided' in case there is no clear answer."""
        
        # viz_hint = client.models.generate_content(
        #     model="gemini-2.5-flash",
        #     contents=viz_prompt)
        # viz_hint = viz_hint.text.strip()
        # # return NLAskResponse(
        # #     sql=sql_query,
        # #     results=results,
        # #     interpretation=interpretation
        # # )

        return NLAskResponse(
            columns=columns,
            rows=results,
            row_count=len(results),
            visualization_hint='bar plot',
            sql=sql_query
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"SQL execution error: {str(e)}"
        )
    # return the result