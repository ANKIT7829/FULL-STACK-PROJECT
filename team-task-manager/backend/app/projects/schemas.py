"""
Projects Schemas
Marshmallow schemas for request validation
"""
from marshmallow import Schema, fields, validate


class ProjectSchema(Schema):
    """Schema for project creation"""
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200),
        error_messages={'required': 'Title is required'}
    )
    description = fields.Str(
        allow_none=True,
        validate=validate.Length(max=1000)
    )


class ProjectUpdateSchema(Schema):
    """Schema for project update"""
    title = fields.Str(
        validate=validate.Length(min=1, max=200)
    )
    description = fields.Str(
        allow_none=True,
        validate=validate.Length(max=1000)
    )


class ProjectDetailSchema(Schema):
    """Schema for project details response"""
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    created_by = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    members = fields.List(fields.Dict())
    tasks = fields.List(fields.Dict())
