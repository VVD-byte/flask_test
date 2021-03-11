from project import api
from project.views import RegisterView, PostsView, CommentView

# Регистрация url api.add_resource(class_object, 'url')
api.add_resource(RegisterView, '/register/')
api.add_resource(PostsView, '/post/')
api.add_resource(CommentView, '/comment/')
