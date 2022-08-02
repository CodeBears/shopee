from app import db


class DBTool:
    @staticmethod
    def commit():
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def flush():
        try:
            db.session.flush()
        except Exception as e:
            db.session.rollback()
            raise e