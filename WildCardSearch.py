
@app.route('/api/search')
def search():
    query = request.args.get('query')
    pdf_dir = '/path/to/pdf/dir'
    results = []
    for filename in os.listdir(pdf_dir):
        if filename.endswith('.pdf'):
            with open(os.path.join(pdf_dir, filename), 'rb') as f:
                pdf = PyPDF2.PdfFileReader(f)
                for page in range(pdf.getNumPages()):
                    text = pdf.getPage(page).extractText()
                    if query in text:
                        results.append(filename)
                        break
    return jsonify(results)
