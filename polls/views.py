from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from .models import Poll, Option  # Import Option model
from .serializers import UserSerializer, PollSerializer, LoginSerializer, OptionSerializer, VoteSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Call the parent class's create method to perform the usual registration
        response = super().create(request, *args, **kwargs)

        # Modify the response to return a custom success message
        return Response({"message": "Account created successfully, kindly log in."}, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.validated_data['email']).first()
            if user and user.check_password(serializer.validated_data['password']):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'email': serializer.validated_data['email'],
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                })
            return Response({"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PollListCreateView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class VoteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VoteSerializer  # Add this line to fix the schema generation issue

    def post(self, request, poll_id, option_id):
        poll = Poll.objects.get(id=poll_id)
        option = Option.objects.get(id=option_id, poll=poll)

        # Ensure user hasn't voted already
        if request.user in option.votes.all():
            return Response({"detail": "You have already voted for this option."}, status=status.HTTP_400_BAD_REQUEST)

        option.votes.add(request.user)  # Corrected to add the user to the votes ManyToMany field
        option.save()

        return Response({"detail": "Vote cast successfully!"})

class PollResultsView(APIView):
    def get(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
            options = poll.options.all()
            results = []
            for option in options:
                results.append({
                    'option': option.text,
                    'votes': option.votes.count()
                })
            return Response(results, status=status.HTTP_200_OK)
        except Poll.DoesNotExist:
            return Response({"detail": "Poll not found."}, status=status.HTTP_404_NOT_FOUND)

class PollUpdateView(generics.UpdateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        poll = self.get_object()
        
        # Retrieve and update only the fields that are passed in the request body
        data = request.data
        poll.title = data.get('title', poll.title)
        poll.description = data.get('description', poll.description)
        poll.expires_at = data.get('expires_at', poll.expires_at)

        poll.save()

        # Return response with updated poll
        return Response(PollSerializer(poll).data, status=status.HTTP_200_OK)

class OptionUpdateView(generics.UpdateAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        option = self.get_object()
        
        # Retrieve and update only the 'text' field for the option
        data = request.data
        option.text = data.get('text', option.text)
        
        option.save()

        # Return response with updated option
        return Response(OptionSerializer(option).data, status=status.HTTP_200_OK)

class OptionDeleteView(generics.DestroyAPIView):
    queryset = Option.objects.all()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        # Get the option object
        option = self.get_object()
        # Delete the option
        option.delete()
        # Return response indicating success
        return Response({"detail": "Option deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

class PollDeleteView(APIView):
    def delete(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
            poll.delete()  # Delete the poll
            return Response({"message": "Poll Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Poll.DoesNotExist:
            raise NotFound({"message": "Poll not found"})