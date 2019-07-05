import os


def folder(localFolder):
    assert isinstance(localFolder, str)
    localFolder = os.path.abspath(localFolder)

    path, subdirs, files = next(os.walk(localFolder))
    urlRoot = "/C" + path.split(":", 1)[1].replace("\\", "/")
    urlRoot = "/" + urlRoot.strip("/")

    html = ""
    html += f"<code>{path}</code>"
    html += f"<br><br><a href='{os.path.dirname(urlRoot)}'>up one folder</a>"
    
    html += "<h1>Images</h1>"
    for fname in files:
        if fname.lower().endswith(".png"):
            html += f"<a href='{urlRoot}/{fname}'><img width='200' src='{urlRoot}/{fname}'></a> "

    html += "<h1>Folders</h1>"
    for fname in subdirs:
        html += f"<a href='{urlRoot}/{fname}'>{fname}</a><br>"
        
    html += "<h1>Files</h1>"
    for fname in files:
        html += f"<a href='{urlRoot}/{fname}'>{fname}</a><br>"
    return html
