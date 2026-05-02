"""
Authentication Schemas
Marshmallow schemas for request validation
"""
from marshmallow import Schema, fields, validate, ValidationError


class UserRegistrationSchema(Schema):
    """Schema for user registration validation"""
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=120),
        error_messages={'required': 'Name is required'}
    )
    email = fields.Email(
        required=True,
        error_messages={'required': 'Email is required', 'invalid': 'Invalid email format'}
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, max=255),
        error_messages={'required': 'Password is required'}
    )


class UserLoginSchema(Schema):
    """Schema for user login validation"""
    email = fields.Email(
        required=True,
        error_messages={'required': 'Email is required', 'invalid': 'Invalid email format'}
    )
    password = fields.Str(
        required=True,
        error_messages={'required': 'Password is required'}
    )


class UserSchema(Schema):
    """Schema for user serialization"""
    id = fields.Int()
    name = fields.Str()
    email = fields.Email()
    role = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
