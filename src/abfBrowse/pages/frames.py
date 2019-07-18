"""
The viewer is just a frameset that loads a menu and a folder.
"""

def generateHtml(pathUrl):
    html = f"""<html>
<head><title>ABF Browser</title></head>
<frameset cols='300px,100%'>
    <frame name='menu' src='/ABFmenu/{pathUrl}' />
    <frame name='content' src='/ABFexperiment/{pathUrl}' />
</frameset>
</html>"""
    return html