from rest_framework import serializers
from .models import Book
from user_auth.models import CustomUser


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=CustomUser.objects.none(),
        slug_field='author_pseudonym'
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'description',
                  'author', 'cover_image', 'price']
        read_only_fields = ['id']

    def __init__(self, *args, **kwargs):
        context = kwargs['context']
        self.logged_in_user = context.pop('logged_in_user', None)
        super().__init__(*args, **kwargs)

    def get_fields(self):
        fields = super().get_fields()
        if self.logged_in_user:
            fields['author'].queryset = CustomUser.objects.filter(
                username=self.logged_in_user)
        return fields

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['request'].user.is_superuser:
            data['author'] = {
                'id': instance.author.id,
                'username': instance.author.username
            }
        else:
            data.pop('author')
        return data
