from datetime import datetime

import pytest

from src.forecast.energy import _integrate_power_over_time


@pytest.mark.parametrize(
    "t, p, t_start, t_end, expected_energy",
    [
        # Test Case 1: Full interval coverage
        (
            [
                datetime(2021, 1, 1, 10, 0),
                datetime(2021, 1, 1, 11, 0),
                datetime(2021, 1, 1, 12, 0),
            ],
            [1000.0, 2000.0, 3000.0],
            datetime(2021, 1, 1, 9, 0),
            datetime(2021, 1, 1, 12, 0),
            6000.0,
        ),
        # Test Case 2: Partial interval coverage
        (
            [
                datetime(2021, 1, 1, 10, 0),
                datetime(2021, 1, 1, 11, 0),
                datetime(2021, 1, 1, 12, 0),
            ],
            [1000.0, 2000.0, 3000.0],
            datetime(2021, 1, 1, 10, 30),
            datetime(2021, 1, 1, 11, 30),
            2500.0,
        ),
        # Test Case 3: Start and end range between intervals
        (
            [
                datetime(2021, 1, 1, 10, 0),
                datetime(2021, 1, 1, 10, 30),
                datetime(2021, 1, 1, 11, 0),
            ],
            [1000.0, 1500.0, 2000.0],
            datetime(2021, 1, 1, 10, 15),
            datetime(2021, 1, 1, 10, 45),
            (1500 + 2000) / 4,
        ),
        # Test Case 4: Start before and end after intervals
        (
            [datetime(2021, 1, 1, 10, 0), datetime(2021, 1, 1, 11, 0)],
            [1000.0, 2000.0],
            datetime(2021, 1, 1, 9, 45),
            datetime(2021, 1, 1, 11, 15),
            2250.0,
        ),
        # Test Case 5: Start and end within the same interval
        (
            [datetime(2021, 1, 1, 10, 0), datetime(2021, 1, 1, 11, 0)],
            [1500.0, 2000.0],
            datetime(2021, 1, 1, 10, 15),
            datetime(2021, 1, 1, 10, 45),
            1000.0,
        ),
        # Additional test cases can be added as needed
    ],
)
def test_integrate_power_over_time(t, p, t_start, t_end, expected_energy):
    assert _integrate_power_over_time(t, p, t_start, t_end) == pytest.approx(
        expected_energy
    )
