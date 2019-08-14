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

def ignoreButton(localPath):
    html = f"<button class='smallButton' onclick=\"ignoreAbf('{os.path.basename(localPath)}')\">ignore</button> "
    return html

def refreshButton():
    html = "<FORM style='display: inline;'>"
    html += "<INPUT class='smallButton' TYPE='button' onClick='history.go(0)' VALUE='Refresh'>"
    html += "</FORM>"
    return html

def autoRefresh(seconds = 5):
    return f"<meta http-equiv='refresh' content='{seconds}' />"

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

<script>
	function setClicked(id) {
		elems = document.getElementsByClassName('abflink');
		for (i = 0; i < elems.length; i++) {
			elems[i].style.fontWeight="normal";
			if (elems[i].id==id) {
				elems[i].style.fontWeight="bold";
			}
		}
		elems = document.getElementsByClassName('abftick');
		for (i = 0; i < elems.length; i++) {
			elems[i].style.visibility="hidden";
			if (elems[i].id==id) {
				elems[i].style.visibility="visible";
			}
		}
	}

    function ignoreAbf(baseName){
        if (confirm(`Are you sure you want to ignore ${baseName}?`) == true) {
            window.location.href = "?ignoreABF=" + baseName;
        }
    }
</script>

</head>
<body>
%s
</body>
</html>
    """ % (cssContent, htmlContent)
    return html.strip()
