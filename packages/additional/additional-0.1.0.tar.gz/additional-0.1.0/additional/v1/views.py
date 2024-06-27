from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests

class GitHubRepoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        github_api_url = "https://api.github.com/user/repos"
        auth_token = request.user.social_auth.get(provider='github').extra_data['access_token']
        headers = {'Authorization': f'token {auth_token}'}
        response = requests.get(github_api_url, headers=headers)
        response_data = response.json()
        return Response(response_data)
