# coding: utf-8
__author__ = 'Jeremy'

import os.path

ROOT_DIR=os.path.dirname(__file__)

_DBUSER = "ctt"
_DBPASS = "ctt"
_DBNAME = "medicaldb"
_DBHOST = "localhost:3306"

ROOT_DIR=os.path.dirname(__file__)

#config
SECRET_KEY = 'flasksimplelaw'
SITE_TITLE = '易诊断'
SITE_URL = 'http://www.ezhenduan.com'
SITE_NAME = '易诊断'

#admin info
ADMIN_INFO = ''
ADMIN_EMAIL = 'admin@simplelaw.cn'
ADMIN_USERNAME = 'admin'


DEFAULT_FILE_STORAGE = 'filesystem'
UPLOADS_FOLDER = os.path.realpath('.') + '/static/'
FILE_SYSTEM_STORAGE_FILE_VIEW = 'static'

MAX_CONTENT_LENGTH = 256 * 1024 * 1024

# User
DEFAULT_IMAGE = '/static/assets/image/young-m.png'
DEFAULT_TITLE = '待定'

#command
WKHTMLTOPDF_COMMAND1 = 'xvfb-run'
WKHTMLTOPDF_COMMAND2 = '--server-args=-screen 0, 1280x1024x24'
WKHTMLTOPDF_COMMAND3 = 'wkhtmltopdf'
WKHTMLTOPDF_COMMAND4 = '--use-xserver'

#cdn
AVATAR_PREFIX = 'http://static.ezhenduan.com/static/'

class rec:
    pass

rec.database = 'mysql://%s:%s@%s/%s' % (_DBUSER, _DBPASS, _DBHOST, _DBNAME)
rec.description = u"易诊断"
rec.url = 'http://www.ezhenduan.com'
rec.paged = 8
rec.archive_paged = 20
rec.admin_username = 'admin'
rec.admin_email = 'admin@simplelaw.cn'
rec.admin_password = 'passw0rd'
rec.default_timezone = "Asia/Shanghai"

ALLOWED_PICTURE_EXTENSIONS = set(['doc', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'html', 'zip', 'rar'])

LOGIN_URL='/loginPage'
ERROR_URL='/error'
