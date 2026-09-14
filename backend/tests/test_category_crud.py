import pytest
from sqlite3 import IntegrityError as SQLiteIntegrityError
from sqlalchemy.exc import IntegrityError
from src.core.crud.sqlmodel_crud import SQLModelCRUD
from src.documentation.models import Category, Language
from src.documentation.models.category import CategoryCreate, CategoryUpdate
from src.documentation.models.language import LanguageCreate


@pytest.fixture
def category_crud():
    return SQLModelCRUD(model=Category)


@pytest.fixture
def language_crud():
    return SQLModelCRUD(model=Language)


def test_create_category_success(session, category_crud):
    payload = CategoryCreate(
        name="Algorithmique",
        description="Notions de base",
        lft=1,
        rgt=2,
    )
    category = category_crud.create(session, payload)

    assert category.id is not None
    assert category.name == "Algorithmique"
    assert category.lft == 1
    assert category.rgt == 2
    assert category.parent_id is None


def test_create_category_duplicate_name_raises_error(session, category_crud):
    payload = CategoryCreate(name="Architecture")
    category_crud.create(session, payload)

    # name est unique -> doit lever une exception d'intégrité
    with pytest.raises(IntegrityError):
        category_crud.create(session, CategoryCreate(name="Architecture"))


def test_create_category_with_parent_and_language(
    session, category_crud, language_crud
):
    # Setup de la langue parente
    lang = language_crud.create(
        session, LanguageCreate(name="Python", abbr="py")
    )

    # Setup de la catégorie parente
    parent_cat = category_crud.create(
        session, CategoryCreate(name="Backend", lft=1,
                                rgt=4, language_id=lang.id)
    )

    # Création de la catégorie enfant
    child_payload = CategoryCreate(
        name="FastAPI",
        lft=2,
        rgt=3,
        parent_id=parent_cat.id,
        language_id=lang.id,
    )
    child_cat = category_crud.create(session, child_payload)

    assert child_cat.parent_id == parent_cat.id
    assert child_cat.language_id == lang.id

    # Validation du chargement de l'auto-relation en ORM
    session.refresh(parent_cat)
    assert len(parent_cat.children) == 1
    assert parent_cat.children[0].id == child_cat.id


def test_update_category_bounds(session, category_crud):
    cat = category_crud.create(
        session, CategoryCreate(name="Bases de données", lft=1, rgt=2)
    )

    # Mise à jour des bornes de l'arbre (lft/rgt)
    update_payload = CategoryUpdate(lft=1, rgt=4)
    updated_cat = category_crud.update(session, cat.id, update_payload)

    assert updated_cat.lft == 1
    assert updated_cat.rgt == 4
    assert updated_cat.name == "Bases de données"  # Inchangé


def test_delete_category(session, category_crud):
    cat = category_crud.create(session, CategoryCreate(name="DevOps"))

    deleted = category_crud.destroy(session, cat.id)
    assert deleted is True
    assert category_crud.get_one(session, cat.id) is None
