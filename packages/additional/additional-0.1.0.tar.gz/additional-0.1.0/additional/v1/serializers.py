from rest_framework import serializers

class GitHubRepoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    full_name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1024, allow_blank=True, allow_null=True)

