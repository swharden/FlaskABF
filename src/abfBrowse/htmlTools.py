import os
import glob

import abfBrowse

PATH_HERE = os.path.dirname(__file__)

copyCount = 0


def copyButton(label, text):
    """Return HTML for a small clipboard copy button"""
    global copyCount
    copyCount += 1
    id = "copyId%05d" % (copyCount)
    html = f"<span style='display: none;' id='{id}'>{text}</span>"
    html += f"<button class='smallButton' onclick=\"copyToClipboard('{id}')\">{label}</button> "
    return html


def refreshButton():
    html = "<FORM style='display: inline;'>"
    html += "<INPUT class='smallButton' TYPE='button' onClick='history.go(0)' VALUE='Refresh'>"
    html += "</FORM>"
    return html


def htmlPageWrap(htmlContent):
    with open(PATH_HERE+"/style.css") as f:
        cssContent = f.read()
    html = """
<html>
<head>
<style>
%s
</style>

<script>
    function copyToClipboard(elementId) {
    var input = document.createElement("input");
    document.body.appendChild(input);
    input.value=document.getElementById(elementId).innerText;
    input.select();
    document.execCommand("copy");
    document.body.removeChild(input);
    }
</script>

</head>
<body>
%s
</body>
</html>
    """ % (cssContent, htmlContent)
    return html.strip()
