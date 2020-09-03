from tests.conftest import AuthActions


def test_get_index_should_return_200(client):
    actions = AuthActions(client)
    actions.register_and_login()
    rv = client.get("/")
    assert rv.status_code == 200
