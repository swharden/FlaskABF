import time


def htmlAround(htmlCore, t1=False):
    if t1:
        renderTimeMs = (time.perf_counter() - t1)*1000.0
    else:
        renderTimeMs = 0
    html = """
<html>
    <head>
        <style>
            .msgBar {
                background-color: red; 
                color: white; 
                margin: 20px;
                padding: 20px;
            }
        </style>
    </head>
    <body>
        <div style=''>%s</div>
        <div class='msgBar'>render time: %.03f ms</div>
    </body>
</html>
    """ % (htmlCore, renderTimeMs)
    return html
