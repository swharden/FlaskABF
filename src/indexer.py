import os

def folder(localFolder):
    assert isinstance(localFolder, str)
    localFolder = os.path.abspath(localFolder)

    path, subdirs, files = next(os.walk(localFolder))
    urlRoot = path.split(":", 1)[1].replace("\\", "/")

    html = ""
    html += f"<code>{path}</code>"
    html += f"<br><br><a href='{os.path.dirname(urlRoot)}'>up one folder</a>"
    html += "<h1>Folders</h1>"
    for fname in subdirs:
        html += f"<a href='{urlRoot}/{fname}'>{fname}</a><br>"
    html += "<h1>Files</h1>"
    for fname in files:
        html += f"<a href='{urlRoot}/{fname}'>{fname}</a><br>"
    return html
