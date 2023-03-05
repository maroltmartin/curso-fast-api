from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token

app = FastAPI()
app.title = "Mi app con FastAPI"
app.version = "0.0.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail= "Credenciales son invalidas")
        
class User(BaseModel):
    email:str
    password:str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_Lenght= 5, max_Lenght= 15) #Solo puedo ingresar peliculas hasta 15 digitos
    overview: str = Field(min_Length= 5, max_Length= 50) 
    year: int = Field(Le= 2022) #le significa qu no puede exceder a 2022
    rating: float = Field(ge= 1, Le= 10)
    category: str = Field(min_Length= 1, max_Length= 15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Mi descripcion",
                "year": 2022,
                "rating": 9.8,
                "category": "No data"
            }
        }

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': 'Descripcion Avatar',
        'year': 2009,
        'rating': 7.8,
        'category': 'Accion'
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': 'Descripcion Avatar',
        'year': 2010,
        'rating': 7.8,
        'category': 'Accion'
    }
]

@app.post('/login', tags= ['auth'])
def login(user: User):
    token:str = ""
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
    return JSONResponse(status_code= 200, content= token)

# Metodo GET

@app.get('/movies', tags= ['movies'], response_model= List[Movie],
         status_code= 200, dependencies= [Depends(JWTBearer)])
def get_movie() -> List[Movie]:
    return JSONResponse(status_code= 200, content=movies)

@app.get('/movies/{id}', tags= ['movies'], response_model= Movie)
def get_movie(id: int = Path(ge=1, Le= 1000)) -> Movie:
    for item in movies:
        if item['id'] == id:
            return JSONResponse(content=item)
    return JSONResponse(content=[])

@app.get('/movies/', tags= ['movies'], response_model= List[Movie])
def get_movies_by_category(
    category: str = Query(min_Lenght= 5, max_Lenght= 15)
    ) -> List[Movie]:

    for item in movies:
        if item['category'].lower() == category.lower():
            return JSONResponse(status_code= 200,
                        content=item)

    return JSONResponse(status_code= 404, content= [])

# Metodo POST, usando pydantic

@app.post('/movies/', tags= ['movies'], response_model= dict,
          status_code= 201)
def create_movies(movie: Movie) -> dict:

    movies.append(movie)
    return JSONResponse(status_code= 201, content=
                {'message': "Se ha registrado la pelicula"})

# Metodo PUT, usando pydantic

@app.put('/movies/{id}', tags= ['movies'], response_model= dict,
    status_code= 200)
def update_movie(
    id: int , movie: Movie) -> dict:

    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            
    return JSONResponse(status_code= 200, content=
        {'message': "Se ha modificado la pelicula"})

# Metodo DELETE

@app.delete('/movies/{id}', tags= ['movies'], response_model= dict,
                status_code= 200)
def delete_movie(id: int ) -> dict:

    for item in movies:
        if item['id'] == id:
            movies.remove(item)
        
    return JSONResponse(status_code= 200, content=
        {'message': "Se ha eliminado la pelicula"})
