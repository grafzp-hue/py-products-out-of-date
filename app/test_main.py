import datetime
from typing import Any

import pytest
from _pytest.monkeypatch import MonkeyPatch

from app import main


@pytest.mark.parametrize(
    ("today", "products", "expected"),
    [
        (
            datetime.date(2022, 2, 2),
            [
                {
                    "name": "salmon",
                    "expiration_date": datetime.date(2022, 2, 10),
                    "price": 600,
                },
                {
                    "name": "chicken",
                    "expiration_date": datetime.date(2022, 2, 5),
                    "price": 120,
                },
                {
                    "name": "duck",
                    "expiration_date": datetime.date(2022, 2, 1),
                    "price": 160,
                },
            ],
            ["duck"],
        ),
        (
            datetime.date(2022, 2, 2),
            [
                {
                    "name": "yesterday",
                    "expiration_date": datetime.date(2022, 2, 1),
                },
                {
                    "name": "today",
                    "expiration_date": datetime.date(2022, 2, 2),
                },
                {
                    "name": "tomorrow",
                    "expiration_date": datetime.date(2022, 2, 3),
                },
            ],
            ["yesterday"],
        ),
        (
            datetime.date(2024, 1, 1),
            [
                {
                    "name": "first",
                    "expiration_date": datetime.date(2023, 12, 31),
                },
                {
                    "name": "second",
                    "expiration_date": datetime.date(2023, 12, 30),
                },
                {
                    "name": "fresh",
                    "expiration_date": datetime.date(2024, 1, 1),
                },
            ],
            ["first", "second"],
        ),
        (datetime.date(2022, 2, 2), [], []),
        (
            datetime.date(2022, 2, 2),
            [{"name": "fresh", "expiration_date": datetime.date(2022, 2, 3)}],
            [],
        ),
    ],
)
def test_outdated_products(
    monkeypatch: MonkeyPatch,
    today: datetime.date,
    products: list[dict[str, Any]],
    expected: list[str],
) -> None:
    class FrozenDate(datetime.date):
        @classmethod
        def today(cls) -> datetime.date:
            return today

    monkeypatch.setattr(main.datetime, "date", FrozenDate)

    assert main.outdated_products(products) == expected
