from ninja import Schema


class IntakeFormSchema(Schema):
    name: str
    email: str
    phone: str
    message: str
    scheduled_date: str
