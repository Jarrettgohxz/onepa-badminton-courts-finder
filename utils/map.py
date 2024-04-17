import webbrowser
import subprocess


def run_nodejs(file: str):

    PIPE = subprocess.PIPE

    p = subprocess.Popen(
        ['C:/Program Files/nodejs/node.exe', file], stdout=PIPE, stderr=PIPE)
    print(p.stdout.read())

    # data, err = p.communicate()
    # print(data)
    # print(err)


def open_url_on_browser(url: str):
    webbrowser.open(url, new=0, autoraise=True)
