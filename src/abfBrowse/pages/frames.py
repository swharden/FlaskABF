"""
The viewer is just a frameset that loads a menu and a folder.
"""

def generateHtml(pathUrl):
    html = f"""<html>
<head><title>ABF Browser</title></head>
<frameset cols='300px,100%' border='5'>
    <frame name='menu' src='/ABFmenu/{pathUrl}' frameborder='0' />
    <frame name='content' src='/ABFexperiment/{pathUrl}' frameborder='0' />
</frameset>
</html>"""
    return html