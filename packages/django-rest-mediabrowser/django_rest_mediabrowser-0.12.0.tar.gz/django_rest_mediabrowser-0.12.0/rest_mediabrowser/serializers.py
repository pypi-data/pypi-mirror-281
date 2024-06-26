import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from rest_mediabrowser.appconfig import MB_IMAGE_EXTENSIONS
from rest_mediabrowser.models import (
    Collection,
    Media,
    MediaFile,
    MediaImage,
    MediaTypeChoices,
    Node,
    NodePermission,
)

logger = logging.getLogger(__name__)
USER_MODEL = get_user_model()


class FlatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ("id", "username", "first_name", "last_name")


class FlatNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ("slug", "name")


class NodePermissionSerializer(serializers.ModelSerializer):
    node_data = FlatNodeSerializer(source="node", read_only=True)
    user_data = FlatUserSerializer(source="user", read_only=True)

    class Meta:
        model = NodePermission
        fields = "__all__"
        extra_kwargs = {
            "node": {"write_only": True},
            "user": {"write_only": True},
        }


class FlatNodePermissionSerializer(serializers.ModelSerializer):
    node = FlatNodeSerializer(read_only=True)
    user = FlatUserSerializer(read_only=True)

    class Meta:
        model = NodePermission
        fields = (
            "node",
            "user",
        )


class CollectionSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    parent = FlatNodeSerializer(read_only=True)
    shared_with = FlatNodePermissionSerializer(
        source="nodes_through", many=True, read_only=True
    )
    type = serializers.CharField(source="media_type", read_only=True)

    class Meta:
        model = Collection
        fields = ("slug", "owner", "name", "shared_with", "parent", "type")


class FlatCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ("slug", "name")


class SharedCollectionSerializer(serializers.ModelSerializer):
    owner = FlatUserSerializer(read_only=True)

    class Meta:
        model = Collection
        fields = (
            "slug",
            "owner",
            "name",
        )


class SharedMediaFileSerializer(TaggitSerializer, serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    type = serializers.CharField(source="media_type", read_only=True)

    def get_file_url(self, model):
        if not model.file:
            return ""
        return model.get_file_url()

    class Meta:
        model = MediaFile
        fields = ("slug", "file_url", "tags", "type")


class SharedMediaImageSerializer(TaggitSerializer, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    type = serializers.CharField(source="media_type", read_only=True)

    def get_image_url(self, model):
        if not model.image:
            return ""
        return model.get_image_url()

    class Meta:
        model = MediaImage
        fields = ("image_url", "alt_text", "height", "width", "tags", "type")


SHARED_MEDIA_SERIALIZERS = {
    "mediaimage": SharedMediaImageSerializer,
    "mediafile": SharedMediaFileSerializer,
}


class SharedMediaSerializer(TaggitSerializer, serializers.ModelSerializer):
    owner = FlatUserSerializer(read_only=True)
    tags = TagListSerializerField()
    media = serializers.SerializerMethodField()
    permission = serializers.SerializerMethodField()

    def get_media(self, model):
        media_type = model.media_type
        if media_type != MediaTypeChoices.UNDEFINED:
            data = SHARED_MEDIA_SERIALIZERS[media_type](
                model.media_data, context=self.context
            ).data
            return data
        return None

    def get_permission(self, model):
        try:
            return NodePermission.objects.get(
                user=self.context["request"].user, node=model
            ).permission
        except Exception:
            return ""

    class Meta:
        model = Media
        fields = (
            "slug",
            "name",
            "owner",
            "parent",
            "published",
            "tags",
            "permission",
            "media",
        )
        extra_kwargs = {"name": {"read_only": True}}


class SharedWithSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=USER_MODEL.objects.all()
    )
    permission = serializers.ChoiceField(
        choices=(("e", "Edit"), ("v", "View")), write_only=True
    )


class MediaImageSerializer(TaggitSerializer, serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    parent = FlatCollectionSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    image = serializers.ImageField(write_only=True, required=False)
    parent_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source="parent",
        required=False,
        queryset=Collection.objects.all(),
    )
    tags = TagListSerializerField(required=False)

    thumbnail = serializers.SerializerMethodField()
    published_path = serializers.ReadOnlyField()
    type = serializers.CharField(source="media_type", read_only=True)

    def get_thumbnail(self, model):
        if not model.thumbnail:
            return ""
        return model.get_thumbnail_url()

    def get_image_url(self, model):
        if not model.image:
            return ""
        return model.get_image_url()

    def validate(self, data):
        vdata = super().validate(data)
        parent_data = vdata.get("parent", None)
        if parent_data:
            if (
                parent_data.owner == vdata["owner"]
                or NodePermission.objects.filter(
                    user=vdata["owner"], parent=parent_data, permission="e"
                ).exists()
            ):
                return vdata
            else:
                raise serializers.ValidationError(
                    "Not enough permission for adding to this parent"
                )
        else:
            return vdata

    class Meta:
        model = MediaImage
        fields = (
            "owner",
            "parent",
            "parent_id",
            "image_url",
            "image",
            "alt_text",
            "thumbnail",
            "height",
            "width",
            # 'shared_with',
            "published",
            "published_path",
            "tags",
            "name",
            "type",
        )
        extra_kwargs = {
            "name": {"required": False},
            # "shared_with": {"write_only": True},
        }


class MediaFileSerializer(TaggitSerializer, serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file_url = serializers.SerializerMethodField()
    file = serializers.FileField(write_only=True, required=False)
    parent = FlatCollectionSerializer(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source="parent",
        required=False,
        queryset=Collection.objects.all(),
    )

    tags = TagListSerializerField(required=False)
    published_path = serializers.ReadOnlyField()
    type = serializers.CharField(source="media_type", read_only=True)

    def get_file_url(self, model):
        if not model.file:
            return ""
        return model.get_file_url()

    def validate(self, data):
        vdata = super().validate(data)
        parent_data = vdata.get("parent", None)
        if parent_data:
            if (
                parent_data.owner == vdata["owner"]
                or NodePermission.objects.filter(
                    user=vdata["owner"], parent=parent_data, permission="e"
                ).exists()
            ):
                return vdata
            else:
                raise serializers.ValidationError(
                    "Not enough permission for adding to this parent"
                )
        else:
            return vdata

    class Meta:
        model = MediaFile
        fields = (
            "owner",
            "parent",
            "parent_id",
            # 'shared_with',
            "file_url",
            "file",
            "published",
            "published_path",
            "tags",
            "name",
            "type",
        )
        extra_kwargs = {
            "name": {"required": False},
            "published": {"write_only": True},
            # "shared_with": {"write_only": True},
        }


NODE_SERIALIZERS = {
    "mediaimage": MediaImageSerializer,
    "mediafile": MediaFileSerializer,
    "collection": CollectionSerializer,
}
MEDIA_FIELD = (("mediaimage", "image"), ("mediafile", "file"), ("collection", None))


# Node
class NodeSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    media_file = serializers.FileField(write_only=True, required=False)
    media_object = serializers.DictField(write_only=True, required=False)
    media = serializers.SerializerMethodField()
    shared_user = FlatUserSerializer(many=True, source="shared_with", read_only=True)
    parent_id = serializers.UUIDField(write_only=True, required=False)

    def get_media(self, model):
        media_type = model.media_type
        if media_type != MediaTypeChoices.UNDEFINED:
            data = NODE_SERIALIZERS[media_type](
                model.media_data, context=self.context
            ).data
            return data
        return None

    class Meta:
        model = Node
        fields = (
            "slug",
            "name",
            "owner",
            "parent_id",
            "media_file",
            "media_object",
            "media",
            "media_type",
            "shared_user",
        )
        extra_kwargs = {
            "name": {"required": False},
            "media_type": {"read_only": True},
        }

    def media_field_name(self, file):
        if not file:
            return MEDIA_FIELD[2]
        extension = str(file).split(".")[-1].lower()
        if extension in MB_IMAGE_EXTENSIONS:
            return MEDIA_FIELD[0]
        else:
            return MEDIA_FIELD[1]

    def update(self, instance, validated_data):
        # extract all data
        validated_data.update(validated_data.get("media_object", {}))

        parent_id = validated_data.get("parent_id", None)
        if parent_id:
            parent = Collection.objects.get(slug=parent_id)
            validated_data["parent_id"] = parent.id

        # Prevent to upload file
        media_file = validated_data.pop("media_file", None)
        if media_file:
            raise Exception("You can't update file")

        serailizer = NODE_SERIALIZERS[instance.media_type]
        sobj = serailizer(
            instance.media_data, data=validated_data, context=self.context
        )
        validity = sobj.is_valid()
        logger.critical(f"{validity}---{sobj.errors}")
        m = sobj.save()
        return Media.objects.get(id=m.id)

    def create(self, validated_data):
        # extract all different  data
        validated_data.update(validated_data.get("media_object", {}))

        # add parent if necessary
        parent = validated_data.get("parent")
        if parent:
            validated_data["parent_id"] = parent.id

        # Get proper field and file
        media_file = validated_data.pop("media_file", None)
        media_type, field_name = self.media_field_name(media_file)
        if field_name:
            validated_data[field_name] = media_file
        validated_data["media_type"] = media_type

        # Serialize and save data
        serailizer = NODE_SERIALIZERS[media_type]
        sobj = serailizer(data=validated_data, context=self.context)
        validity = sobj.is_valid()
        logger.critical(f"{validity}---{sobj.errors}")
        m = sobj.save()

        return Media.objects.get(id=m.id)


class FlatMediaFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    published_path = serializers.ReadOnlyField()

    def get_file_url(self, model):
        if not model.file:
            return ""
        return model.get_file_url()

    class Meta:
        model = MediaFile
        fields = (
            "file_url",
            "published_path",
        )


class FlatMediaImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    published_path = serializers.ReadOnlyField()

    def get_thumbnail(self, model):
        if not model.thumbnail:
            return ""
        return model.get_thumbnail_url()

    def get_image_url(self, model):
        if not model.image:
            return ""
        return model.get_image_url()

    class Meta:
        model = MediaImage
        fields = (
            "image_url",
            "thumbnail",
            "published_path",
            "alt_text",
            "height",
            "width",
        )
        extra_kwargs = {
            "alt_text": {"read_only": True},
            "height": {"read_only": True},
            "width": {"read_only": True},
        }


FLAT_MEDIA_SERIALIZERS = {
    "mediaimage": FlatMediaImageSerializer,
    "mediafile": FlatMediaFileSerializer,
}


class FlatMediaSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField(read_only=True)
    media = serializers.SerializerMethodField()

    def get_media(self, model):
        media_type = model.media_type
        if media_type != MediaTypeChoices.UNDEFINED:
            data = FLAT_MEDIA_SERIALIZERS[media_type](
                model.media_data, context=self.context
            ).data
            return data
        return None

    class Meta:
        model = Media
        fields = (
            "slug",
            "name",
            "tags",
            "media_type",
            "media",
        )
        extra_kwargs = {
            "name": {"read_only": True},
            "media_type": {"read_only": True},
        }
