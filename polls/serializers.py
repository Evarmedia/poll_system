# polls/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Poll, Option

class UserSerializer(serializers.ModelSerializer):
    # We no longer need 'username' because we will use 'email'
    class Meta:
        model = User
        fields = ('email', 'password')  # Use email and password instead of username and password
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only
        }

    def create(self, validated_data):
        # Ensure that email is unique
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({'email': 'Email is already in use.'})

        # Create a new user with the validated email and password
        user = User.objects.create_user(
            username=validated_data['email'],  # Use email as username for internal consistency
            email=validated_data['email'],     # Store email as the user's email
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'text')

class VoteSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()

class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('id', 'title', 'description', 'created_at', 'expires_at', 'options')

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        poll = Poll.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(poll=poll, **option_data)
        return poll

    def update(self, instance, validated_data):
        # Update the Poll fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.expires_at = validated_data.get('expires_at', instance.expires_at)

        # Handle the nested options update
        options_data = validated_data.get('options', None)
        if options_data is not None:
            # Update existing options or create new ones if necessary
            for option_data in options_data:
                option_id = option_data.get('id')
                if option_id:
                    # If option ID is provided, update the existing option
                    try:
                        option = instance.options.get(id=option_id)
                        option.text = option_data.get('text', option.text)  # Update only the 'text' field
                        option.save()
                    except Option.DoesNotExist:
                        # If the option doesn't exist, create a new one
                        Option.objects.create(poll=instance, **option_data)
                else:
                    # If no ID is provided, create a new option
                    Option.objects.create(poll=instance, **option_data)

        instance.save()
        return instance

