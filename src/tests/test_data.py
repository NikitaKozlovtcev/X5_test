import pytest


@pytest.mark.parametrize(
    "number_rows, expected_code",
    [
        (0, 422),
        (1, 200),
        (2, 200),
        (3, 200),
    ]
)
def test_get_weather(test_app, number_rows, expected_code):
    test_request = f'/data?n={number_rows}'
    response = test_app.get(test_request)
    print('-----------------------------------------------------------')
    print(test_request)
    print(response.status_code)
    print(response.json())
    print('-----------------------------------------------------------')
    assert response.status_code == expected_code
