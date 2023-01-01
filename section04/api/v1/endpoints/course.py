from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import CourseModel
from schemas.curso_schema import CourseSchema
from core.deps import get_session

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CourseSchema)
async def post_course(course: CourseSchema, db: AsyncSession = Depends(get_session)):
     new_course = CourseModel(
        title=course.title, 
        classes=course.classes, 
        hours=course.hours
        )
     
     db.add(new_course)
     await db.commit()

     return new_course


@router.get('/', response_model=List[CourseSchema])
async def get_courses(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel)
        result = await session.execute(query)
        courses: List[CourseModel] = result.scalars().all()

        return courses


@router.get('/{course_id}', response_model=CourseSchema, status_code=status.HTTP_200_OK )
async def get_course(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course = result.scalar_one_or_none()

        if course:
            return course
        else:
            raise HTTPException(
                detail='Course not found', 
                status_code=status.HTTP_404_NOT_FOUND
                )

@router.put('/{course_id}', response_model=CourseSchema, status_code=status.HTTP_200_OK)
async def put_course(course_id: int, curso: CourseSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course_obj = result.scalar_one_or_none()

        if course_obj:
            course_obj.title = curso.title
            course_obj.classes = curso.classes
            course_obj.hours = curso.hours

            await session.commit()
            return course_obj
        else:
            raise HTTPException(
                detail='Course not found', 
                status_code=status.HTTP_404_NOT_FOUND
                )                

@router.delete('/{course_id}', status_code=status.HTTP_204_NO_CONTENT )
async def delete_course(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course_obj = result.scalar_one_or_none()

        if course_obj:
            await session.delete(course_obj)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                detail='Course not found', 
                status_code=status.HTTP_404_NOT_FOUND
                )                