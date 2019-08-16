from .models import User


class UserValidator:

    @staticmethod
    def check_exists_user_by_phone(phone: str) -> str:
        if User.objects.filter(phone=phone).exists():
            return 'This phone number is already in use'
        else:
            return 'The given phone number is available'
