from pydantic import BaseModel,field_validator,model_validator
from rich import print

class User(BaseModel):
    email:str
    username:str
    password:str


    @field_validator("email",mode="after")
    def emil_checker(cls,v):
        if ("@" not in v):
            raise ValueError("email must inlcude '@'")
        return v
    @field_validator("password",mode="after")
    def check_pw_len(cls,v):
        if len(v) < 8:
            raise ValueError("password must be 8 chars long")
        return v
    @model_validator(mode="after")
    def pass_check(cls,model):
        if model.username in model.password:
            raise ValueError("username should not include in password")
        return model



from pydantic import BaseModel, field_validator, model_validator
from rich import print

class User(BaseModel):
    email: str
    username: str
    password: str

    @field_validator("email", mode="after")
    def email_checker(cls, v):
        if "@" not in v:
            raise ValueError("email must include '@'")
        return v

    @field_validator("password", mode="after")
    def check_pw_len(cls, v):
        if len(v) < 8:
            raise ValueError("password must be at least 8 chars long")
        return v

    @model_validator(mode="after")
    def pass_check(cls, model):
        if model.username in model.password:
            raise ValueError("password must not contain username")
        return model


# ✅ Test Cases

try:
    u = User(email="saraexample.com", username="sara", password="mypassword")
except Exception as e:
    print("[red]Email Error →", e)

try:
    u = User(email="sara@example.com", username="sara", password="short")
except Exception as e:
    print("[red]Password Length Error →", e)

try:
    u = User(email="sara@example.com", username="sara", password="sara12345")
except Exception as e:
    print("[red]Password-Username Error →", e)

# ✅ Correct data
u = User(email="sara@example.com", username="sara", password="strongpass123")
print("[green]Valid User →", u)
