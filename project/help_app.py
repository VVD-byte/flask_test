from project import db_session
from .models import User, Posts, Comments


class CheckUser:
    @staticmethod
    def check_post(post_id, username) -> bool:
        if post_id is None or username is None:
            return False
        id_user = db_session.query(User).filter_by(username=username).first().id
        if db_session.query(Posts).filter_by(id=post_id).first().author_id == id_user:
            return True
        return False

    @staticmethod
    def check_comment(comment_id, username) -> bool:
        if comment_id is None or username is None:
            return False
        id_user = db_session.query(User).filter_by(username=username).first().id
        if db_session.query(Comments).filter_by(id=comment_id).first().author_id == id_user:
            return True
        return False
