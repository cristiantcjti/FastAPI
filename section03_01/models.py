from typing import Optional

from pydantic import BaseModel, validator

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

    @validator('titulo')
    def validar_titulo(cls, value):
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError('O titulo deve conter mais que duas palavras')
        
        return value



cursos = [
    Curso(id=1, titulo='FastAPI in depth', aulas=55, horas=90),
    Curso(id=2, titulo='FastAPI the future', aulas=40, horas=65)
]
