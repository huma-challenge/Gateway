from rest_framework import serializers


class UserProtoSerializer(serializers.Serializer):

    id = serializers.IntegerField(label="ID", read_only=True)
    username = serializers.CharField(
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        max_length=150,
    )
    password = serializers.CharField(max_length=128)
    first_name = serializers.CharField(allow_blank=True, max_length=150, required=False)
    last_name = serializers.CharField(allow_blank=True, max_length=150, required=False)
    email = serializers.EmailField(
        allow_blank=True, label="Email address", max_length=254, required=False
    )
    is_active = serializers.BooleanField(
        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
        label="Active",
        required=False,
    )
    is_staff = serializers.BooleanField(
        help_text="Designates whether the user can log into this admin site.",
        label="Staff status",
        required=False,
    )
    is_superuser = serializers.BooleanField(
        help_text="Designates that this user has all permissions without explicitly assigning them.",
        label="Superuser status",
        required=False,
    )
    groups = serializers.PrimaryKeyRelatedField(
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        many=True,
        required=False,
        read_only=True,
    )

    class Meta:
        model = None
        fields = "__all__"


