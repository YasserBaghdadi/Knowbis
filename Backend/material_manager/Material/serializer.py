from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from Knowbis.serializers_methods import validate_field
from material_manager.Rate.model import AudienceRateMaterial
from material_manager.Material.model import Material
from category_manager.Category.serializer import CategorySerializer
from material_manager.EnrolledToMaterial.model import EnrolledToMaterial
from users_manager import Provider
from users_manager.Provider.serializer import RetrieveProviderSerializer


class MaterialSerializer(ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'title', 'category', 'provider', 'description', 'brief_description', 'image', 'status',
                  'requirements', 'what_will_learn', 'duration']


class RetrieveMaterialSerializer(MaterialSerializer):
    category = CategorySerializer()
    provider = RetrieveProviderSerializer()
    enrolled_students = serializers.SerializerMethodField()

    rating = serializers.SerializerMethodField()

    def get_rating(self, material):
        ratings = AudienceRateMaterial.objects.filter(material_id=material.id)
        like = ratings.filter(rating=True).count()
        dislike = ratings.filter(rating=False).count()
        total_ratings = like + dislike
        if total_ratings:
            return like / (like + dislike) * 100
        return 0.0

    def get_enrolled_students(self, material: Material):
        return EnrolledToMaterial.objects.filter(material=material).count()

    class Meta(MaterialSerializer.Meta):
        fields = MaterialSerializer.Meta.fields.copy()
        fields.extend(['enrolled_students', 'rating', 'last_update'])


class BriefRetrieveMaterialSerializer(RetrieveMaterialSerializer):
    class Meta(RetrieveMaterialSerializer.Meta):
        fields = RetrieveMaterialSerializer.Meta.fields.copy()
        for i in ['requirements', 'what_will_learn', 'description']:
            fields.remove(i)


class AddUpdateMaterialSerializer(MaterialSerializer):
    # fields = RetrieveMaterialSerializer.Meta.fields.copy()
    # fields.remove('provider')  # The value of the 'provider' will be auto

    """
    Special serializer, it differs from MaterialSerializer that it does not overwrite the id, and category fields.
    Used for creating and updating material.
    The programmer thinks that there is no need to have two classes (AddMaterialSerializer, UpdateMaterialSerializer)
    """

    def validate_title(self, value: str):
        validate_field(value)
        return value


class AddMaterialSerializer(AddUpdateMaterialSerializer):
    def save(self, **kwargs):
        user_id = self.context['user_id']
        provider = Provider.objects.get(user_id=user_id)
        material = Material.objects.create(provider=provider, **self.validated_data)
        return material
        # return provider

    def validate_title(self, value: str):
        validate_field(value)  # Validate if the title follows the standards of titles in our system
        return value
