from rest_framework import serializers
from .models import Challenge, Hint


class ChallengeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Challenge
        fields = ('id', 'title', 'score', 'category')


class ChallengeDetailSerializer(serializers.ModelSerializer):
    hints = serializers.StringRelatedField(many=True)

    class Meta:
        model = Challenge
        fields = ('id', 'title', 'description', 'category', 'hints', 'score')


class SubmitFlagSerializer(serializers.Serializer):
    flag = serializers.CharField(required=True)


class HintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hint
        fields = ['description']


class ChallengeSerializer(serializers.ModelSerializer):
    hints = HintSerializer(many=True, required=False)

    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description',
                  'score', 'category', 'flag', 'hints']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'score': {'required': True},
            'category': {'required': True},
            'flag': {'required': True},
        }

    def create(self, validated_data):
        hints_data = validated_data.pop('hints', [])
        challenge = Challenge.objects.create(**validated_data)

        for hint_data in hints_data:
            Hint.objects.create(challenge=challenge, **hint_data)

        return challenge
