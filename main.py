#PYTHON
from typing import Optional
from enum import Enum

#pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import  FastAPI
from fastapi import Body,Query,Path

app = FastAPI()

#Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"
    
class Location(BaseModel):
    city: str
    state: str
    country: str
    
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "city": "Cali",
    #             "state": "Valle del cauca",
    #             "country": "Colombia"
    #         }
    #     }
    
class Person(BaseModel):
    first_name:str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Andres"
        )
    last_name:str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Quintero"
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=25
    )
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None)
    
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Andres",
    #             "last_name": "Quintero",
    #             "age": 32, 
    #             "hair_color": "blonde",
    #             "is_married": False
    #         }
    #     }


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

#validaciones: request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title ="Person ID",
        description ="This is the person Id",
        gt = 0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    
    return results
