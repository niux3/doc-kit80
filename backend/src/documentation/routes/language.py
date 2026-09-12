from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session
from src.database import db
from src.documentation.models import (
    Language,
    LanguageRead,
    LanguageCreate,
    LanguageUpdate
)


language_router = APIRouter(tags=["language"], prefix="/language")


@language_router.get("/", response_model=List[LanguageRead])
def get_languages(db: Session = Depends(db.get_session)):
    """Récupèrer toutes les langues disponibles"""
    return db.query(Language).all()


@language_router.get("/{id}", response_model=LanguageRead)
def get_language(id: int, db: Session = Depends(db.get_session)):
    """Récupèrer une langue par son ID"""
    item = db.query(Language).get(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Language not found"
        )
    return item


@language_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy_language(id: int, db: Session = Depends(db.get_session)):
    """Supprimer une langue par son ID"""
    item = db.query(Language).get(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"item {id} not found"
        )
    db.delete(item)
    db.commit()
    return None


@language_router.post('/', response_model=LanguageRead, status_code=status.HTTP_201_CREATED)
def create_language(language: LanguageCreate, db: Session = Depends(db.get_session)):
    """Créer une nouvelle langue"""
    db_language = Language(**language.model_dump())
    db.add(db_language)
    db.commit()
    db.refresh(db_language)
    return db_language


@language_router.put('/{id}', response_model=LanguageRead)
def update_language(id: int, language: LanguageUpdate, db: Session = Depends(db.get_session)):
    """modifier une langue"""
    item = db.query(Language).get(id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"item {id} not found"
        )
    data = language.model_dump(exclude_unset=True)
    item.sqlmodel_update(data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
