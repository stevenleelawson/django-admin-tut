from rest_framework import serializers
from .models import User, Permission, Role

class PermissionsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Permission
		fields = '__all__'

class PermissionRelatedField(serializers.StringRelatedField):
	# get the roles
	def to_representation(self, value):
		return PermissionsSerializer(value).data

	# store the roles
	def to_internal_value(self, data):
		return data


class RoleSerializer(serializers.ModelSerializer):
	permissions = PermissionRelatedField(many=True)
	class Meta:
		model = Role
		fields = '__all__'
	
	def create(self, validated_data):
		print('VALIDATEDATTTTTA', validated_data)
		permissions = validated_data.pop('permissions', None)
		print('PERRRMMMMMMY', permissions)
		instance = self.Meta.model(**validated_data)
		instance.save()
		instance.permissions.add(*permissions)
		instance.save()
		return instance


class  RoleRelatedField(serializers.RelatedField):
	def to_representation(self, instance):
		return RoleSerializer(instance).data

	def to_internal_value(self, data):
		return self.queryset.get(pk=data)


class UserSerializer(serializers.ModelSerializer):
	role = RoleRelatedField(many=False, queryset=Role.objects.all()) 

	class Meta:
		model = User
		fields = ['id', 'first_name', 'last_name', 'email', 'password', 'role']
		extra_kwargs = {
			'password': {'write_only': True}
		}

	def create(self, validated_data):
		password = validated_data.pop('password', None)
		# the two stars below are coz we a returning a dict aka obj
		instance = self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)

		instance.save()
		return instance

	def update(self, instance, validated_data):
		password = validated_data.pop('password', None)
		if password is not None:
			instance.set_password(password)

		instance.save()
		return instance