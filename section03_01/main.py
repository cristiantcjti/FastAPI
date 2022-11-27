from typing import Any, List, Optional, Dict

from fastapi.responses import JSONResponse
from fastapi import FastAPI, Header, Query
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from fastapi import Path
from fastapi import Depends

from time import sleep

from models import Curso
from models import cursos


def fake_db():
    try:
        print("Abrindo conexão com banco de dados...")
        sleep(1)
    finally:
        print("Fechando conexão com banco de dados")
        sleep(1)


app = FastAPI(
    title='Api course',
    version='0.0.1',
    description='API for studies of FastAPI',
    )

# cursos = {
#     1: {
#         "titulo": "Programação inicial",
#         "aulas": 122,
#         "horas": 58
#     },
#     2: {
#         "titulo": "Algoritimos e logica de programacao",
#         "aulas": 87,
#         "horas": 67
#     }
# }


@app.get(
    '/cursos', 
    description =' Retorna todos os cursos ou uma lista vazia', 
    summary =' Retorna todos os cursos', 
    response_model = List[Curso],
    response_description='Cursos encontrados com succeso'
    )
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos


@app.get('/cursos/{curso_id}')    
async def get_curso(curso_id: int = Path(default=None, title="ID do curso", description="Deve ser entre 1 e 2", gt=0, lt=3), db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Curso nao encontrado'
            )


@app.post('/cursos', status_code=status.HTTP_201_CREATED, response_model=Curso)
async def post_curso(curso: Curso):
    next_id: int = len(cursos) +1
    curso.id = next_id
    cursos.append(curso)
    return curso


@app.put('/cursos/{curso_id}')    
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id
        return curso
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Curso com ID {curso_id} nao encontrado'
            )

@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id]
        #return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Curso com ID {curso_id} nao encontrado'
            )


@app.get('/calculadora')
async def calculadora(
    a: int = Query(default=None, gt=5), 
    b: int = Query(default=None, gt=5), 
    c: Optional[int]=None, 
    x_geek: str = Header(default=None)
    ):

    soma: int = a + b
    if c:
        soma += c

    print("x_geek:", {x_geek})        

    return {"resultado": soma}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True, reload=True)