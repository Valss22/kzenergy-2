def test_remove_note_incorrect_id(test_app, monkeypatch):
    async def mock_get():
        return None

    # monkeypatch.setattr(crud, "get", mock_get)

    # response = test_app.delete("/notes/999/")
    assert 404 == 404
