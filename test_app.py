import pytest
import json
from app import app, db, Task

@pytest.fixture
def client():
    """Setup test client with a fresh database for each test."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_tasks.db'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def sample_task(client):
    """Create a sample task for tests that need existing data"""

    response = client.post(
        '/tasks',
        data=json.dumps({'title': 'Sample Task'}),
        content_type='application/json'
    )

    return json.loads(response.data)

class TestHealth:
    def test_health_check(self, client):
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
class TestCreateTask:
    def test_create_task_success(self, client):

        response = client.post(
            '/tasks',
            data=json.dumps({'title': 'Test Task'}),
            content_type='application/json'
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == 'Test Task'
        assert data['completed'] == False
        assert 'id' in data
        assert 'created_at' in data
    
    def test_create_task_no_title(self, client):
    
        response = client.post(
            '/tasks',
            data=json.dumps({}),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_task_empty_title(self, client):

        response = client.post(
            '/tasks',
            data=json.dumps({'title': ''}),
            content_type='application/json'
        )

        assert response.status_code == 400
    
    def test_create_task_title_too_long(self, client):
        response = client.post(
            '/tasks',
            data=json.dumps({'title': 'x' * 201}),
            content_type='application/json',
        )

        assert response.status_code == 400
    
    def test_create_task_no_body(self, client):
        response = client.post(
            '/tasks',
            content_type='application/json'
        )
        assert response.status_code == 400

class TestGetTasks:
    def test_get_all_tasks_empty(self, client):
        response = client.get('tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['tasks'] == []
        assert data['count'] == 0
    
    def test_get_all_tasks_with_data(self, client, sample_task):
        response = client.get('/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 1
        assert len(data['tasks']) == 1
    
    def test_get_single_task(self, client, sample_task):
        task_id = sample_task['id']
        response = client.get(f'/tasks/{task_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == task_id
    
    def test_get_nonexistent_task(self, client):
        response = client.get('/tasks/999')
        assert response.status_code == 404
    
class TestUpdateTask:
    def test_update_task_title(self, client, sample_task):
        task_id = sample_task['id']
        response = client.put(
            f'/tasks/{task_id}',
            data=json.dumps({'title': 'Updated Title'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Updated Title'
    
    def test_update_task_completed(self, client, sample_task):
        task_id = sample_task['id']
        response = client.put(
            f'/tasks/{task_id}',
            data=json.dumps({'completed': True}),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['completed'] == True
    
    def test_update_nonexistent_task(self, client):
        response = client.put(
            '/tasks/999',
            data=json.dumps({'title': 'Updated'}),
            content_type='application/json'
        )

        assert response.status_code == 404
    
    def test_updated_task_invalid_completed(self, client, sample_task):
        task_id = sample_task['id']
        response = client.put(
            f'/tasks/{task_id}',
            data=json.dumps({'completed': 'yes'}),
            content_type='application/json'
        )

        assert response.status_code == 400
    
class TestDeleteTask:
    def test_delete_task(self, client, sample_task):
        task_id = sample_task['id']
        response = client.delete(f'/tasks/{task_id}')
        assert response.status_code == 200

        get_response = client.get(f'/tasks/{task_id}')
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_task(self, client):
        response = client.delete('/tasks/999')
        assert response.status_code == 404





