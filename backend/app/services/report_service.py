from sqlalchemy.orm import Session

from app.repositories.report_repository import (
    ReportRepository
)


class ReportService:

    def __init__(self):
        self.repository = ReportRepository()


    def get_report(
        self,
        db: Session,
        interview_id: int
    ):

        return self.repository.get_by_interview_id(
            db,
            interview_id
        )