import uuid

from assertpy import assert_that

from python_sprint_zero.domain.model.person import Person
from python_sprint_zero.domain.model.relationship import Relationship


def test_should_have_from_person():
    from_person = Person(id=str(uuid.uuid4()))

    assert_that(
        Relationship(
            from_person=from_person,
            to_person=Person(id=str(uuid.uuid4())),
        ).from_person
    ).is_equal_to(from_person)


def test_should_have_to_person():
    to_person = Person(id=str(uuid.uuid4()))

    assert_that(
        Relationship(
            from_person=Person(id=str(uuid.uuid4())),
            to_person=to_person,
        ).to_person
    ).is_equal_to(to_person)
