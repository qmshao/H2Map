import dash_html_components as html
import dash_core_components as dcc
import re

def filterCell(content):
    content = re.sub(r'<div(.*?)</div>', '', content)
    link = re.search(r'"(http://.*?)"(.*?)>(.*?)<', content)
    if link:
        content = html.A(link.group(3), href=link.group(1))

    return content


def makeDashTable(data):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []

    for i in range(len(data)):
        el = html.Td(filterCell(data[i]))
        if i%2:
            html_row.append(el)
            table.append(html.Tr(html_row))
        else:
            html_row = [el]
        
    
    return html.Table(table)


def generateModal():
    return html.Div(
        id="markdown",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=dcc.Markdown(
                            children=(
                                """
                                    MODAL TEST!!!!!
                                """
                            )
                        ),
                    ),
                ],
            )
        ),
    )