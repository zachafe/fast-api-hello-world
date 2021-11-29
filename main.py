#PYTHON
from typing import Optional

#pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import  FastAPI
from fastapi import Body,Query,Path

app = FastAPI()

#Models

class Person(BaseModel):
    first_name:str
    last_name:str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


@app.get("/")
def home():
    return {"hello": "world"}

# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validations : Query parameters
@app.get("/person/detail")
def show_person (
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name, it,s between 1 and 50 charters"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age, it's requeri"
        )
):
    return {name:age}

# validaciones: path  parameters
# Query(None, regex="^[a-z]{5}$")
@app.get("/person/detail/{person_id}")
def show_person (
    person_id: int = Path (...,gt=0)
):
    return {person_id:"existe"}
