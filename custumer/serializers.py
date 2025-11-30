# api/serializers.py
from rest_framework import serializers

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserLogoutSerializer(serializers.Serializer):
    pass

# api/serializers.py
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'adresse', 'district', 'region', 'departement', 'sous_prefecture', 'commune','profile_image','is_agent','is_recenseur','is_entreprise','entreprise','is_lanfia')
        extra_kwargs ={
            'password':{'write_only':True}
        }
    def create(self,validated_data):
        password=validated_data.pop('password',None)
        instance =self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class UserSerializer1(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['entreprise']
