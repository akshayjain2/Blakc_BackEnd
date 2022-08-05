from marshmallow import Serializer, fields


class UserSerializer(Serializer):
    class Meta:
        fields = ("id", "email")


class PostSerializer(Serializer):
    user = fields.Nested(UserSerializer)

    class Meta:
        fields = ("id", "title", "body", "user", "created_at")


class ToDoSerializer(Serializer):
    class Meta:
        fields = ("id", "text", "is_complete", "created_at", "status")


class ContactSerializer(Serializer):
    class Meta:
        fields = ("id", "first_name", "last_name", "text", "created_at", "is_selected")


class ProjectSerializer(Serializer):
    class Meta:
        fields = ("id", "name", "description", "user_id", "created_at")


class IssueSerializer(Serializer):
    class Meta:
        fields = (
            "id", "title", "description", "project_id", "created_at", "column_id", "tag_id", "milestone_id", "effort_id",
            "assigned_to_id")


class TagSerializer(Serializer):
    class Meta:
        fields = ("id", "name", "description", "color")


class MilestoneSerializer(Serializer):
    class Meta:
        fields = ("id", "name", "description", "due_date", "status")


class EffortSerializer(Serializer):
    class Meta:
        fields = ("id", "name", "description")


class ColumnSerializer(Serializer):
    tasks = fields.Nested(IssueSerializer, many=True)

    class Meta:
        fields = ("id", "name", "description", "tasks")