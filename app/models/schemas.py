from marshmallow import ValidationError 
from marshmallow_sqlalchemy.fields import Nested
# Custom validator
def must_not_be_blank(data):
    if not data or str(data).isspace():
        raise ValidationError("Data not provided.")
    
class SmartNested(Nested):
    def serialize(self, attr, obj, accessor=None):
        if attr not in obj.__dict__:
            return {"id": int(getattr(obj, attr + "_id"))}
        return super(SmartNested, self).serialize(attr, obj, accessor)