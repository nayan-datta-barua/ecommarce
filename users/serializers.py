# from chat.models import Contact
from rest_framework import serializers
from .models import CustomUser,CustomUserManager
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',     
            'first_name',
            'last_name',
            'street',
            'street_number',
            'zip_code',
            'city',
            'country',
            'phone',
            'current_address']
        extra_kwargs = {
                    'user': {'write_only': True},
                }

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],

            street=validated_data['street'],
            street_number=validated_data['street_number'],
            zip_code=validated_data['zip_code'],
            city=validated_data['city'],
           
            country=validated_data['country'],
            phone=validated_data['phone'],
            current_address=validated_data['current_address'],
        )

        # contact= Contact(user=user)
        # contact.save()
        
        return user
