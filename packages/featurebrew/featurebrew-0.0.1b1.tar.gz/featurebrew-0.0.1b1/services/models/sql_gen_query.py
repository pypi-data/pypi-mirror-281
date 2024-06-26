from pydantic import BaseModel


class SQLGenQueryInput(BaseModel):
    db_id: str
    text: str


class SQLGenQueryOutput(BaseModel):
    input: str
    explanation: str
    output: str
    # intermediate_steps: list[str]
