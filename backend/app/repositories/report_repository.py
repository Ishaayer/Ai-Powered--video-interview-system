from sqlalchemy.orm import Session

from app.models.report import Report


class ReportRepository:

    def get_by_interview_id(
        self,
        db: Session,
        interview_id: int
    ):

        return (
            db.query(Report)
            .filter(
                Report.interview_id == interview_id
            )
            .first()
        )


    def create(
        self,
        db: Session,
        report: Report
    ):

        db.add(report)
        db.commit()
        db.refresh(report)

        return report