
import sys

sys.path.append("../../")
from utils.map import open_url_on_browser, run_nodejs  # NOQA

try:
    run_nodejs('server.js')
    open_url_on_browser('http://localhost:4000')


except KeyboardInterrupt:
    exit()
