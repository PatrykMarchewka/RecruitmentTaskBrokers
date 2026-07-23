from rest_framework import serializers

from recruitmenttaskbrokers.main.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for Contact model converting object to dictionary
    """
    city = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ["ID", "name", "lastName", "city", "status", "createdAt"]

    def get_city(self, obj):
        return obj.city.name

    def get_status(self, obj):
        return obj.status.name
