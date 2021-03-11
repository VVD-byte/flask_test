from flask_restful import Resource, request
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from validate_email import validate_email

from project import auth, db_session
from .models import User, Posts, Comments
from .serializer import Serialize
from .help_app import CheckUser


@auth.verify_password
def verify_password(username, password):
    us = db_session.query(User).filter_by(username=username).first()
    if us and check_password_hash(us.password, password):
        return True
    return False


def error(func):
    def warp(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return {'Unknown error': 'contact the administrator - vovavoronin1999@gmail.com'}
    return warp


class RegisterView(Resource):
    @error
    def get(self):
        passwd = generate_password_hash(request.args.get('passwd', None))
        email, username = self.check_data()
        print(email, username, passwd)
        if None in [email, username]:
            return (email or username), 404
        u = User(email, username, passwd)
        db_session.add(u)
        db_session.commit()
        return {'register': 'True'}, 200

    def check_data(self):
        email, us = request.args.get('email', None), request.args.get('username', None)
        if validate_email(email):
            if db_session.query(User).filter_by(email=email).first():
                return {'error': 'user with such mail is already registered'}, None
        else:
            return {'error': 'invalid email address'}, None
        if db_session.query(User).filter_by(username=us).first():
            return None, {'error': 'user with such username is already registered'}
        return email, us


class PostsView(Resource, Serialize, CheckUser):
    @error
    def get(self, *args, **kwargs):
        return jsonify(self.post_serialize(db_session.query(Posts).all()))

    @error
    @auth.login_required
    def post(self):
        author_id = db_session.query(User).filter_by(username=auth.username()).first().id
        title = request.args.get('title', None)
        content = request.args.get('content', None)
        if author_id is None:
            return {'error': 'authorisation error'}, 404
        if None in [title, content]:
            return {'error': 'title and content should not have null values'}, 404
        p = Posts(author_id, title, content)
        db_session.add(p)
        db_session.commit()
        return {'post_create': 'True'}, 200

    @error
    @auth.login_required
    def put(self):
        posts_id = request.args.get('posts_id', None)
        title = request.args.get('title', None)
        content = request.args.get('content', None)
        if self.check_post(posts_id, auth.username()) and None not in [title, content]:
            data = db_session.query(Posts).filter_by(id=posts_id).first()
            data.title = title
            data.content = content
            db_session.commit()
            return {'update_data': 'True'}, 200
        return {'error': 'permission denied'}, 404

    @error
    @auth.login_required
    def delete(self):
        posts_id = request.args.get('posts_id', None)
        if self.check_post(posts_id, auth.username()):
            data = db_session.query(Posts).filter_by(id=posts_id).first()
            db_session.delete(data)
            db_session.commit()
            return {'delete': 'True'}, 200
        return {'error': 'permission denied'}, 404


class CommentView(Resource, Serialize, CheckUser):
    @error
    def get(self):
        return jsonify(self.comment_serialize(db_session.query(Comments).all()))

    @error
    @auth.login_required
    def post(self):
        post_id = request.args.get('post_id', None)
        author_id = db_session.query(User).filter_by(username=auth.username()).first().id
        title = request.args.get('title', None)
        content = request.args.get('content', None)
        if post_id is None:
            return {'error': 'post not found'}, 404
        if author_id is None:
            return {'error': 'authorisation error'}, 404
        if None in [title, content]:
            return {'error': 'title and content should not have null values'}, 404
        p = Comments(post_id, author_id, title, content)
        db_session.add(p)
        db_session.commit()
        return {'comment_create': 'True'}, 200

    @error
    @auth.login_required
    def put(self):
        comment_id = request.args.get('comment_id', None)
        title = request.args.get('title', None)
        content = request.args.get('content', None)
        if self.check_post(comment_id, auth.username()) and None not in [title, content]:
            data = db_session.query(Comments).filter_by(id=comment_id).first()
            data.title = title
            data.content = content
            db_session.commit()
            return {'update_data': 'True'}, 200
        return {'error': 'permission denied'}, 404

    @error
    @auth.login_required
    def delete(self):
        comment_id = request.args.get('comment_id', None)
        if self.check_post(comment_id, auth.username()):
            data = db_session.query(Posts).filter_by(id=comment_id).first()
            db_session.delete(data)
            db_session.commit()
            return {'delete': 'True'}, 200
        return {'error': 'permission denied'}, 404
