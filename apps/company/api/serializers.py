from rest_framework import serializers
from apps.accounts.models import Owner, UserAccount
from apps.company.models import Company


class CompanySerailizer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'industry', 'address', 'phone',
                  'email', 'website', 'established_date']
        model = Company


class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'


class OwnerSerializer(serializers.ModelSerializer):
    user = UserSerilizer(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        fields = ['inn', 'user', 'is_active']
        model = Owner

    def create(self, validated_data):
        user = self.context['request'].user
        print(validated_data)
        owner = Owner.objects.create(user=user, is_active=False, **validated_data)
        return owner
