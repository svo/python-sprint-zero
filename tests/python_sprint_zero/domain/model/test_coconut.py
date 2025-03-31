import uuid

from assertpy import assert_that

from python_sprint_zero.domain.model.coconut import Person


def test_should_have_id():
    id = uuid.uuid4()

    assert_that(Person(id=id).id).is_equal_to(id)
