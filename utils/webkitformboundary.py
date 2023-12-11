import random
import string

from typing import List


def generate_webkitformboundary(fields: List[dict]):
    boundary = '----WebKitFormBoundary' \
        + ''.join(random.sample(string.ascii_letters + string.digits, 16))

    content_type = f'multipart/form-data; boundary={boundary}'

    data = ''

    for field in fields:

        name = list(field.keys())[0]
        value = list(field.values())[0]

        data += (('\n' if data != '' else '') +
                 f'{boundary}\nContent-Disposition: form-data; name="{name}"\n\n{value}')

    if data != '':
        data += f'\n{boundary}'

    return {
        'data': data,
        'content_type': content_type
    }
