from djoser.serializers import UserCreateSerializer as UCSBasic

class UserCreateSerializer(UCSBasic):
    class Meta(UCSBasic.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']