from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import User as UserJWT
from .utils import EmailVerifier


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserJWT
        fields = ('id', 'email', 'phone', 'first_name', 'last_name',)


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        """
        :param obj:
        :return:
        """
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        """
        :param validated_data:
        :return:
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        email = validated_data.get('email', None)
        result = EmailVerifier.lookup(email)
        if result.get('status', 0):
            # Verify email if it exists
            instance.verified = True

        instance.save()
        return instance

    class Meta:
        model = UserJWT
        fields = ('id', 'email', 'phone', 'token', 'password', )

