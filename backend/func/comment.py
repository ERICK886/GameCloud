import datetime

from backend.func.config import get_config


def get_reply_list(comments, comment):
    """
    获取评论回复
    :param comments:
    :param comment:
    :return:
    """
    reply_list = []
    get_reply(comments, comment, reply_list)
    return reply_list


def get_reply(comments, comment, reply_list):
    site_url = get_config('SITE_URL')
    comms = comments.filter(reply=comment).all()
    for comm in comms:
        reply_list.append({
            'id': comm.id,
            'content': comm.content,
            'user': {
                'id': comm.user.id,
                'nickname': comm.user.nickname,
                'avatar': site_url + '/uploads' + comm.user.avatar.url
            },
            'is_check': comm.is_check,
            'create_time': datetime.datetime.strftime(comm.create_time, '%Y-%m-%d %H:%M'),
            'to': {
                'id': comment.id,
                'content': comment.content,
                'user': {
                    'id': comment.user.id,
                    'nickname': comment.user.nickname,
                    'avatar': site_url + '/uploads' + comment.user.avatar.url
                },
                'is_check': comment.is_check,
                'create_time': datetime.datetime.strftime(comm.create_time, '%Y-%m-%d %H:%M')
            }
        })
        get_reply(comments, comm, reply_list)
    return reply_list
