def test_index_route(api):
    response = api.get("/profile")

    assert response.status == "200 OK"
    assert "Karlos" and "Hello! I'm a full stack developer that loves Python and React" in response.text
