from pydantic import BaseModel, model_validator, field_validator


class TestBase(BaseModel):
    test_id: int


class Test(TestBase):
    type: str
    question: str
    answers: list[str]
    correct_answer: str

    @model_validator(mode="after")
    def validate_correct_answer_in_answers(self):
        if self.correct_answer not in self.answers:
            raise ValueError(f"'{self.correct_answer}' is not in answers list: {self.answers}")
        return self


class TestResponse(TestBase):
    user_id: int
    score: float

    @field_validator('score', mode="before")
    @classmethod
    def validate_score_field(cls, v):
        if not (isinstance(v, float) or isinstance(v, int)):
            raise ValueError(f"score score must be float or int: {v}")
        if v < 0 or v > 100:
            raise ValueError(f"score score must be between 0 and 100: {v}")

        return v

    @field_validator('user_id', mode='before')
    @classmethod
    def check_user_id(cls, v):
        if not isinstance(v, int):
            raise ValueError(f"user_id field must be int: {v}")
        if v < 1:
            raise ValueError("user_id must be a positive integer (>= 1)")
        return v

    @field_validator('test_id', mode='before')
    @classmethod
    def check_test_id(cls, v):
        if not isinstance(v, int):
            raise ValueError(f"test_id field must be int: {v}")
        return v
