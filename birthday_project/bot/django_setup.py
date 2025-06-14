import os
import sys

# Переходим в корень проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../../../../Desktop/site_bot-main/birthday_project')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "birthday_project.settings")

import django
django.setup()
