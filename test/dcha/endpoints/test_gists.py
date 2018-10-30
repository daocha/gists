# Date: 30 Oct 2018
# Author: Ray LI
""" Test case for AES encryption """

from dcha.main import app, version
from unittest import mock, TestCase
from flask import Response


class TestGist(TestCase):

    @mock.patch('dcha.endpoints.github.call_github_gist_get')
    def test_get_gist_list(self, mock_call_github_gist_get):
        # mock github response
        mock_res = Response()
        mock_res.status_code = 200
        mock_res.text = "Testing"
        mock_call_github_gist_get.return_value = mock_res

        with app.test_client() as client:
            # test calling endpoint
            result = client.get('/' + version + '/gist')
            print(result.status_code)
            self.assertEqual(result.status_code, 200)

    @mock.patch('dcha.endpoints.github.call_github_gist_post')
    @mock.patch('dcha.endpoints.request.get_form_data')
    def test_create_gist(self, mock_get_form_data, mock_call_github_gist_post):
        # mock github response
        mock_res = Response()
        mock_res.status_code = 201
        mock_res.text = "Testing"
        mock_call_github_gist_post.return_value = mock_res

        # mock request data
        mock_get_form_data.return_value = {
            "gist_content": "Testing Content",
            "gist_description": "Testing Desc",
            "gist_filename": "Testing filename"
        }

        with app.test_client() as client:
            # test sending data as POST form to endpoint
            result = client.post('/' + version + '/gist')
            result_json = result.get_json(force=True)
            print(result_json.get('success'))
            self.assertEqual(result.status_code, 201)
            self.assertEqual(result_json.get('success'), True)

    @mock.patch('dcha.endpoints.github.call_github_gist_delete')
    def test_delete_gist(self, mock_call_github_gist_delete):
        # mock github response
        mock_res = Response()
        mock_res.status_code = 200
        mock_res.text = "Testing"
        mock_call_github_gist_delete.return_value = mock_res

        with app.test_client() as client:
            # test calling endpoint
            result = client.delete('/' + version + '/gist/gist-12345')
            print(result.status_code)
            self.assertEqual(result.status_code, 200)

    @mock.patch('dcha.endpoints.github.call_github_comment_get')
    def test_get_comments_list(self, mock_call_github_comment_get):
        # mock github response
        mock_res = Response()
        mock_res.status_code = 200
        mock_res.text = "Testing"
        mock_call_github_comment_get.return_value = mock_res

        with app.test_client() as client:
            # test calling endpoint
            result = client.get('/' + version + '/gist/gist-12345/comments')
            print(result.status_code)
            self.assertEqual(result.status_code, 200)

    @mock.patch('dcha.endpoints.github.call_github_comment_post')
    @mock.patch('dcha.endpoints.request.get_form_data')
    def test_create_comment(self, mock_get_form_data, mock_call_github_comment_post):
        # mock github response
        mock_res = Response()
        mock_res.status_code = 201
        mock_res.text = "Testing"
        mock_call_github_comment_post.return_value = mock_res

        # mock request data
        mock_get_form_data.return_value = {
            "gist_comment": "Testing Comment"
        }

        with app.test_client() as client:
            # test sending data as POST form to endpoint
            result = client.post('/' + version + '/gist/gist-123456/comments')
            result_json = result.get_json(force=True)
            print(result_json.get('success'))
            self.assertEqual(result.status_code, 201)
            self.assertEqual(result_json.get('success'), True)

    @mock.patch('dcha.endpoints.github.call_github_comment_delete')
    def test_delete_comment(self, mock_call_github_comment_delete):
        # mock github response
        mock_res = Response()
        mock_res.status_code = 200
        mock_res.text = "Testing"
        mock_call_github_comment_delete.return_value = mock_res

        with app.test_client() as client:
            # test calling endpoint
            result = client.delete(
                '/' + version + '/gist/gist-12345/comments/comment-12345')
            print(result.status_code)
            self.assertEqual(result.status_code, 200)
