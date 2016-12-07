import socket
import sys
from termcolor import colored
from xml.parsers.expat import *
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.exceptions import *


class wp_analysis(object):

    source = None

    target = None

    def __init__(self, url='', username='', password = ''):
        """
        :param config:
        """

        self.wp = Client(url, username, password)



    def error(self, _type, _error):

        """
        WP Post Error
        :param _type string
        :param _error string
        """
        print colored(str.format('{}: {}', _type, _error), 'red')

source = {
    'url': 'http://192.168.33.33/xmlrpc.php',
    'username': 'pbeltran',
    'password': 'LBA8510*%!)LBA'
}

post_id = int(sys.argv[1])

if post_id == 0:
    raise Exception('Expected post id.\n $python posts.py :id')

analytics = wp_analysis(source['url'], source['username'], source['password'])

try:

    post = analytics.wp.call(posts.GetPost(post_id))

    sql = "INSERT INTO `wp_posts`(`post_author`\n, `post_content`\n, `post_title`\n, `post_status`\n, `comment_status`\n,"
    sql += " `ping_status`\n, `post_name`\n, `post_parent`\n, `guid`\n, `menu_order`\n, `post_type`)\n "
    sql += " VALUES \n('{}'\n, '{}'\n, '{}'\n, '{}'\n, '{}'\n, '{}'\n, '{}'\n, '{}'\n, '{}'\n, '{}'\n, '{}'\n )"\
        .format(
            post.user, post.content, post.title, post.post_status,
            post.comment_status, post.ping_status, post.title,
            str(post.parent_id), post.guid, str(post.menu_order), str(post.post_type))

    print(colored(sql, 'blue'))

except ExpatError as e:
    # Invalid XML
    analytics.error('XML Error', e)
except ServerConnectionError as e:
    # Unexpected or invalid response
    analytics.error('Server ERROR', e.message)
except socket.gaierror as e:
    # Unreachable host
    analytics.error('Server ERROR', e)
except AttributeError as e:
    # Unreachable host
    analytics.error('Attribute ERROR', e)



