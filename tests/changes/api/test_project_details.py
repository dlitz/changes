from changes.models import Project
from changes.testutils import APITestCase


class ProjectDetailsTest(APITestCase):
    def test_retrieve(self):
        path = '/api/0/projects/{0}/'.format(
            self.project.id.hex)

        resp = self.client.get(path)
        assert resp.status_code == 200
        data = self.unserialize(resp)
        assert data['id'] == self.project.id.hex

    def test_retrieve_by_slug(self):
        path = '/api/0/projects/{0}/'.format(
            self.project.slug)

        resp = self.client.get(path)
        assert resp.status_code == 200
        data = self.unserialize(resp)
        assert data['id'] == self.project.id.hex

    def test_update(self):
        path = '/api/0/projects/{0}/'.format(
            self.project.id.hex)

        resp = self.client.post(path, data={
            'name': 'details test project',
            'slug': 'details-test-project',
        })
        assert resp.status_code == 200

        project = Project.query.get(self.project.id)
        assert project.name == 'details test project'
        assert project.slug == 'details-test-project'

    def test_update_by_slug(self):
        path = '/api/0/projects/{0}/'.format(
            self.project.slug)

        resp = self.client.post(path, data={
            'name': 'details test project',
            'slug': 'details-test-project',
        })
        assert resp.status_code == 200
        assert resp.status_code == 200
        data = self.unserialize(resp)
        assert data['id'] == self.project.id.hex

        project = Project.query.get(self.project.id)
        assert project.name == 'details test project'
        assert project.slug == 'details-test-project'
