from rest_framework import serializers
from .models import Book
from user_auth.models import CustomUser


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=CustomUser.objects.none(),
        slug_field='username'
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
            user = CustomUser.objects.get(username=self.logged_in_user)

            if user.is_superuser:
                fields['author'].queryset = CustomUser.objects.all()
            else:
                fields['author'].queryset = CustomUser.objects.filter(
                    username=self.logged_in_user)

        return fields
