from pydantic import BaseModel, model_validator

class ReportFilterDTO(BaseModel):
    genre: str | None = None
    director: str | None = None
    year_from: int | None = None
    year_to: int | None = None

    @model_validator(mode="after")
    def validate_years(self):
        if self.year_from and self.year_to:
            if self.year_from > self.year_to:
                raise ValueError("year_from no puede ser mayor que year_to")
        return self