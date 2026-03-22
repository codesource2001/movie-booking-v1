from django.db.models import QuerySet
from typing import TypeVar, Generic, Type, Optional, List, Any
from django.contrib.auth.models import AbstractUser

ModelType = TypeVar('ModelType')


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
        self._queryset = None

    def get_queryset(self) -> QuerySet:
        if self._queryset is None:
            self._queryset = self.model.objects.all()
        return self._queryset

    def filter(self, **kwargs) -> QuerySet:
        return self.get_queryset().filter(**kwargs)

    def exclude(self, **kwargs) -> QuerySet:
        return self.get_queryset().exclude(**kwargs)

    def all(self) -> QuerySet:
        return self.get_queryset().all()

    def get(self, **kwargs) -> ModelType:
        return self.get_queryset().get(**kwargs)

    def get_or_none(self, **kwargs) -> Optional[ModelType]:
        return self.get_queryset().filter(**kwargs).first()

    def first(self) -> Optional[ModelType]:
        return self.get_queryset().first()

    def last(self) -> Optional[ModelType]:
        return self.get_queryset().last()

    def count(self) -> int:
        return self.get_queryset().count()

    def exists(self) -> bool:
        return self.get_queryset().exists()

    def order_by(self, *fields) -> QuerySet:
        return self.get_queryset().order_by(*fields)

    def distinct(self) -> QuerySet:
        return self.get_queryset().distinct()

    def values(self, *fields) -> QuerySet:
        return self.get_queryset().values(*fields)

    def values_list(self, *fields, flat=False) -> QuerySet:
        return self.get_queryset().values_list(*fields, flat=flat)

    def select_related(self, *fields) -> 'BaseRepository[ModelType]':
        repo = self.__class__(self.model)
        repo._queryset = self.get_queryset().select_related(*fields)
        return repo

    def prefetch_related(self, *fields) -> 'BaseRepository[ModelType]':
        repo = self.__class__(self.model)
        repo._queryset = self.get_queryset().prefetch_related(*fields)
        return repo

    def only(self, *fields) -> QuerySet:
        return self.get_queryset().only(*fields)

    def defer(self, *fields) -> QuerySet:
        return self.get_queryset().defer(*fields)


class CrudRepository(BaseRepository[ModelType]):
    def create(self, **kwargs) -> ModelType:
        return self.model.objects.create(**kwargs)

    def update(self, instance: ModelType, **kwargs) -> ModelType:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance: ModelType) -> None:
        instance.delete()

    def bulk_create(self, objects: List[ModelType], batch_size: int = None) -> List[ModelType]:
        return self.model.objects.bulk_create(objects, batch_size=batch_size)

    def bulk_update(self, objects: List[ModelType], fields: List[str], batch_size: int = None) -> None:
        self.model.objects.bulk_update(objects, fields, batch_size=batch_size)

    def get_or_create(self, defaults: dict = None, **kwargs) -> tuple[ModelType, bool]:
        return self.model.objects.get_or_create(defaults=defaults, **kwargs)

    def update_or_create(self, defaults: dict = None, **kwargs) -> ModelType:
        return self.model.objects.update_or_create(defaults=defaults, **kwargs)


class UserRepository(BaseRepository[AbstractUser]):
    def get_by_username(self, username: str) -> Optional[AbstractUser]:
        return self.get_or_none(username=username)

    def get_by_email(self, email: str) -> Optional[AbstractUser]:
        return self.get_or_none(email=email)

    def filter_by_role(self, role: str) -> QuerySet:
        return self.filter(role=role)

    def get_active_users(self) -> QuerySet:
        return self.filter(is_active=True)
