from project.apps.lib.custom.custom_serializers import FlexFieldsModelSerializer
from .models import User
class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model=User
        exclude = ('password','groups','user_permissions')