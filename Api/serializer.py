from dataclasses import field
from rest_framework import serializers
from projects.models import project , Review ,Tag
from users.models import profile

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review 
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = profile
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    Tags = TagSerializer(many=True)
    review = serializers.SerializerMethodField()

    class Meta:
        model = project
        fields = '__all__'

    def get_review(self,obj):
        reviews = obj.review_set.all()
        serializers = ReviewSerializer(reviews,many=True)
        return serializers.data
