from pydantic import BaseModel, constr, validator, Field

class UserRegistrationParams(BaseModel):
    username: str = Field(description="Username user", example="username", max_length=20, min_length=1)
    password1: str = Field(description="Password user", example="password", max_length=20, min_length=1)
    password2: str = Field(description="Password repeat", example="password", max_length=20, min_length=1)

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v
