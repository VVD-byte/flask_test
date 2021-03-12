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
    """
    :param username: имя пользователя
    :param password: пароль пользователя
    :return: есть такой пользователь или нет (bool)
    проверка авторизации пользователя (используется Basic Auth)
    """
    us = db_session.query(User).filter_by(username=username).first()
    if us and check_password_hash(us.password, password):
        return True
    return False


def error(func):
    """
    :param func: имя функции
    :return: результат работы функции или ошибку
    Декоратор для приметивной обработки ошибок (плохая реализация, доработать)
    """
    def warp(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return {'Unknown error': 'contact the administrator - vovavoronin1999@gmail.com'}
    return warp


class RegisterView(Resource):
    """
    Класс регистрации
    url - /register/
    Поддерживаемые методы - ['POST']
    """
    @error
    def post(self, *args, **kwargs):
        """
        :return: Ошибка или подтверждение о прохождении регистрации
        Метод регистрации пользователя
        """
        passwd = generate_password_hash(request.args.get('passwd', None))
        email, username = self.check_data()
        print(email, username, passwd)
        if None in [email, username]:
            return (email or username), 404
        u = User(email, username, passwd)
        db_session.add(u)
        db_session.commit()
        return {'register': 'True'}, 200

    def check_data(self, *args, **kwargs):
        """
        :return: Ошибку или готовые данные - майл и имя пользователя
        Проверяет валидность майла и имя пользователя
        """
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
    """
    Класс для работы с постами
    url - /post/
    Поддерживаемые методы - ['GET', 'POST', 'PUT', 'DELETE']
    """
    @error
    def get(self, *args, **kwargs):
        """
        :return: Все посты из БД
        """
        # добавить сортировку по юзеру
        return jsonify(self.post_serialize(db_session.query(Posts).all()))

    @error
    @auth.login_required
    def post(self, *args, **kwargs):
        """
        :return: Ошибку или подтверждение добавления поста
        QueryString параметры - title, content
        """
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
    def put(self, *args, **kwargs):
        """
        :return: ошибку или подтверждение изменения данных
        QueryString параметры - posts_id, title, content
        """
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
    def delete(self, *args, **kwargs):
        """
        :return: ошибку или подтверждение о удалении поста
        QueryString параметры - posts_id
        """
        posts_id = request.args.get('posts_id', None)
        if self.check_post(posts_id, auth.username()):
            data = db_session.query(Posts).filter_by(id=posts_id).first()
            db_session.delete(data)
            db_session.commit()
            return {'delete': 'True'}, 200
        return {'error': 'permission denied'}, 404


class CommentView(Resource, Serialize, CheckUser):
    @error
    def get(self, *args, **kwargs):
        """
        :return: Все комментарии
        """
        # добаить фильтрацию по посту или юзеру
        return jsonify(self.comment_serialize(db_session.query(Comments).all()))

    @error
    @auth.login_required
    def post(self, *args, **kwargs):
        """
        :return: ошибку или подтверждение создания комментария
        QueryString параметры - post_id, title, content
        """
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
    def put(self, *args, **kwargs):
        """
        :return: ошибку или подтверждение о изменении комментария
        QueryString параметры - comment_id, title, content
        """
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
    def delete(self, *args, **kwargs):
        """
        :return: ошибку или подтверждение о удалении комментария
        QueryString параметры - comment_id
        """
        comment_id = request.args.get('comment_id', None)
        if self.check_post(comment_id, auth.username()):
            data = db_session.query(Posts).filter_by(id=comment_id).first()
            db_session.delete(data)
            db_session.commit()
            return {'delete': 'True'}, 200
        return {'error': 'permission denied'}, 404
