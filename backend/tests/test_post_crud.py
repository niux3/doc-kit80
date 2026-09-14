from datetime import datetime, timezone
import pytest
from sqlalchemy.exc import IntegrityError
from src.core.crud.sqlmodel_crud import SQLModelCRUD
from src.documentation.models import Category, Language, Post
from src.documentation.models.category import CategoryCreate
from src.documentation.models.language import LanguageCreate
from src.documentation.models.post import PostCreate, PostUpdate


@pytest.fixture
def post_crud():
    return SQLModelCRUD(model=Post)


@pytest.fixture
def category_crud():
    return SQLModelCRUD(model=Category)


@pytest.fixture
def language_crud():
    return SQLModelCRUD(model=Language)


def test_create_post_success(session, post_crud):
    payload = PostCreate(
        title="Installer Debian 12",
        slug="installer-debian-12",
        content="Guide d'installation pas à pas...",
        online=True,
    )
    post = post_crud.create(session, payload)

    assert post.id is not None
    assert post.title == "Installer Debian 12"
    assert post.slug == "installer-debian-12"
    assert post.content == "Guide d'installation pas à pas..."
    assert post.online is True
    assert isinstance(post.created_at, datetime)
    assert isinstance(post.updated_at, datetime)


def test_create_post_duplicate_title_or_slug_raises_error(session, post_crud):
    post_crud.create(
        session,
        PostCreate(
            title="Configuration i3wm",
            slug="config-i3wm",
            content="Configuration de base",
        ),
    )

    # Titre en double -> Doit lever une IntegrityError
    with pytest.raises(IntegrityError):
        post_crud.create(
            session,
            PostCreate(
                title="Configuration i3wm",
                slug="config-i3wm-v2",
                content="Autre contenu",
            ),
        )
    session.rollback()

    # Slug en double -> Doit lever une IntegrityError
    with pytest.raises(IntegrityError):
        post_crud.create(
            session,
            PostCreate(
                title="Autre titre",
                slug="config-i3wm",
                content="Autre contenu",
            ),
        )


def test_create_post_with_relations(
    session, post_crud, category_crud, language_crud
):
    lang = language_crud.create(
        session, LanguageCreate(name="Python", abbr="py")
    )
    cat = category_crud.create(
        session, CategoryCreate(name="Tutoriels", language_id=lang.id)
    )

    payload = PostCreate(
        title="FastAPI et SQLModel",
        slug="fastapi-and-sqlmodel",
        content="Utilisation de SQLModel avec FastAPI",
        category_id=cat.id,
        language_id=lang.id,
    )
    post = post_crud.create(session, payload)

    assert post.category_id == cat.id
    assert post.language_id == lang.id

    # Validation du chargement de la relation ORM
    session.refresh(cat)
    assert len(cat.posts) == 1
    assert cat.posts[0].id == post.id


def test_update_post_partial_and_timestamp(session, post_crud):
    post = post_crud.create(
        session,
        PostCreate(
            title="Bases de Vim",
            slug="bases-vim",
            content="Contenu initial",
            online=False,
        ),
    )

    # Mise à jour du statut et du contenu
    update_payload = PostUpdate(content="Contenu enrichi", online=True)
    updated_post = post_crud.update(session, post.id, update_payload)

    assert updated_post.content == "Contenu enrichi"
    assert updated_post.online is True
    assert updated_post.title == "Bases de Vim"  # Titre inchangé
    assert updated_post.slug == "bases-vim"  # Slug inchangé


def test_delete_post(session, post_crud):
    post = post_crud.create(
        session,
        PostCreate(
            title="Post à supprimer",
            slug="post-a-supprimer",
            content="Fichier temporaire",
        ),
    )

    deleted = post_crud.destroy(session, post.id)
    assert deleted is True
    assert post_crud.get_one(session, post.id) is None
