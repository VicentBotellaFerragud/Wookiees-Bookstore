from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('author_pseudonym', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['author_pseudonym'],
            author_pseudonym=validated_data['author_pseudonym'],
            password=validated_data['password']
        )

        return user
