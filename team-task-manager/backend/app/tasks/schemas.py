"""
Tasks Schemas
Marshmallow schemas for request validation
"""
from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime


class TaskSchema(Schema):
    """Schema for task creation"""
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200),
        error_messages={'required': 'Title is required'}
    )
    description = fields.Str(
        allow_none=True,
        validate=validate.Length(max=1000)
    )
    project_id = fields.Int(
        required=True,
        error_messages={'required': 'Project ID is required'}
    )
    assigned_to = fields.Int(allow_none=True)
    due_date = fields.Str(allow_none=True)
    
    @validates('due_date')
    def validate_due_date(self, value):
        """Validate due_date format"""
        if value:
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValidationError('Invalid date format. Use YYYY-MM-DD or ISO format.')


class TaskUpdateSchema(Schema):
    """Schema for task update"""
    title = fields.Str(
        validate=validate.Length(min=1, max=200)
    )
    description = fields.Str(
        allow_none=True,
        validate=validate.Length(max=1000)
    )
    status = fields.Str(
        validate=validate.OneOf(['todo', 'in_progress', 'done'])
    )
    assigned_to = fields.Int(allow_none=True)
    due_date = fields.Str(allow_none=True)
    
    @validates('due_date')
    def validate_due_date(self, value):
        """Validate due_date format"""
        if value:
            try:
                datetime.fromisoformat(value)
            except ValueError:
                raise ValidationError('Invalid date format. Use YYYY-MM-DD or ISO format.')


class TaskDetailSchema(Schema):
    """Schema for task details response"""
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    status = fields.Str()
    due_date = fields.DateTime()
    project_id = fields.Int()
    assigned_to = fields.Int()
    assigned_user = fields.Dict()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
