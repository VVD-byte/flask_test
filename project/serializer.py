class Serialize:
    @staticmethod
    def post_serialize(data) -> list:
        return [{'id': i.id, 'author_id': i.author_id, 'title': i.title, 'content': i.content,
                 'publication_datetime': i.publication_datetime} for i in data]

    @staticmethod
    def comment_serialize(data) -> list:
        return [{'id': i.id, 'post_id': i.post_id, 'author_id': i.author_id, 'title': i.title, 'content': i.content,
                 'publication_datetime': i.publication_datetime} for i in data]
