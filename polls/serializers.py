# polls/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Poll, Option


class UserSerializer(serializers.ModelSerializer):
    # We no longer need 'username' because we will use 'email'
    class Meta:
        model = User
        # Use email and password instead of username and password
        fields = ('email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only
        }

    def create(self, validated_data):
        # Ensure that email is unique
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError(
                {'email': 'Email is already in use.'})

        # Create a new user with the validated email and password
        user = User.objects.create_user(
            # Use email as username for internal consistency
            username=validated_data['email'],
            # Store email as the user's email
            email=validated_data['email'],
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
        ref_name = 'OptionSerializer'


class VoteSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()


class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)  # Include options in the Poll serializer

    class Meta:
        model = Poll
        fields = ['id', 'title', 'description', 'expires_at', 'options']
        ref_name = 'PollSerializer'

    def create(self, validated_data):
        # Pop the 'options' field from validated_data to handle it separately
        options_data = validated_data.pop('options')

        # Create the Poll instance
        poll = Poll.objects.create(**validated_data)

        # Create the associated Options
        for option_data in options_data:
            Option.objects.create(poll=poll, **option_data)  # Assign the created poll to the option

        return poll

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']
    
    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)
        
        # Check if we are in the context of the poll results view and add the votes field
        if self.context.get('include_votes', False):
            representation['votes'] = instance.votes.count()
        
        return representation

