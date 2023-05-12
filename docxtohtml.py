from docx import Document
from docx.shared import RGBColor

# Open the .docx file
doc = Document('example.docx')

# Define the HTML template
html_template = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            {style}
        </style>
    </head>
    <body>
        {body}
    </body>
</html>
'''

# Define the CSS styles to use in the HTML
styles = ''
for paragraph_format in doc.styles:
    if paragraph_format.base_style is not None:
        continue
    style = f'''
        .{paragraph_format.name} {{
            font-size: {paragraph_format.font.size/2}pt;
            font-family: {paragraph_format.font.name};
            color: {RGBColor(paragraph_format.font.color.rgb).hex};
            { 'font-weight: bold;' if paragraph_format.font.bold else '' }
            { 'font-style: italic;' if paragraph_format.font.italic else '' }
            { 'text-decoration: underline;' if paragraph_format.font.underline else '' }
        }}
    '''
    styles += style

# Define the HTML body
body = ''
for paragraph in doc.paragraphs:
    body += f'<p class="{paragraph.style.name}">{paragraph.text}</p>'
    for run in paragraph.runs:
        if run.bold:
            body = body.replace(run.text, f'<strong>{run.text}</strong>')
        if run.italic:
            body = body.replace(run.text, f'<em>{run.text}</em>')
        if run.underline:
            body = body.replace(run.text, f'<u>{run.text}</u>')
    if paragraph._element.getchildren():
        tbl = paragraph._element.xpath('.//w:tbl')[0]
        body += f'<table>'
        for row in tbl.xpath('.//w:tr'):
            body += '<tr>'
            for cell in row.xpath('.//w:tc'):
                body += f'<td>{cell.xpath(".//w:t")[0].text}</td>'
            body += '</tr>'
        body += '</table>'

# Combine the HTML template, CSS styles, and HTML body to create the final HTML
html = html_template.format(title='Example Document', style=styles, body=body)

# Write the HTML to a file
with open('example.html', 'w') as f:
    f.write(html)
