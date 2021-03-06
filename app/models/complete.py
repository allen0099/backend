from datetime import datetime

from app import db


class Complete(db.Model):
    __tablename__: str = "complete"

    id: int = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )
    user_id: str = db.Column(
        db.String(30),
        db.ForeignKey("user.id"),
        nullable=False
    )
    practice_uuid: str = db.Column(
        db.String(64),
        db.ForeignKey("practice.uuid"),
        nullable=False
    )
    timestamp: datetime = db.Column(
        db.TIMESTAMP(),
        server_default=db.func.now()
    )

    def __init__(self,
                 user_id: str,
                 practice_uuid: str) -> None:
        self.user_id = user_id
        self.practice_uuid = practice_uuid

    def __repr__(self) -> str:
        return f"<Complete {self.id}>"

    @staticmethod
    def add(user_id: str, practice_uuid: str) -> None:
        db.session.add(Complete(user_id, practice_uuid))
        db.session.commit()

    @staticmethod
    def is_solved(user_id: str, practice_uuid: str) -> bool:
        complete: Complete = Complete.query \
            .filter_by(user_id=user_id) \
            .filter_by(practice_uuid=practice_uuid) \
            .first()
        if complete is not None:
            return True
        return False
