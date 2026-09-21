def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_get_empty_notes(client):
    response = client.get('/api/notes')
    assert response.status_code == 200
    assert response.get_json()['notes'] == []


def test_create_note(client):
    response = client.post('/api/notes', json={
        'title': 'Test', 'content': 'Content'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test'
    assert 'id' in data


def test_create_note_missing_fields(client):
    response = client.post('/api/notes', json={'title': 'Only Title'})
    assert response.status_code == 400


def test_get_note_not_found(client):
    response = client.get('/api/notes/999')
    assert response.status_code == 404


def test_update_note(client):
    resp = client.post('/api/notes', json={'title': 'Old', 'content': 'X'})
    note_id = resp.get_json()['id']
    resp = client.put(f'/api/notes/{note_id}', json={'title': 'New'})
    assert resp.status_code == 200
    assert resp.get_json()['title'] == 'New'


def test_delete_note(client):
    resp = client.post('/api/notes', json={'title': 'To Delete', 'content': 'X'})
    note_id = resp.get_json()['id']
    resp = client.delete(f'/api/notes/{note_id}')
    assert resp.status_code == 200
    resp = client.get(f'/api/notes/{note_id}')
    assert resp.status_code == 404