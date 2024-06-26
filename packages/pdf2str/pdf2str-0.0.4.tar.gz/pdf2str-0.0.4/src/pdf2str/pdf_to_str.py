import PyPDF2

def pdf_to_str(file_path, page_start=0, early_finish=0, progress=True):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        num_pages = len(reader.pages)

        text = ''
        for page_num in range(page_start, num_pages-early_finish):
            page = reader.pages[page_num]
            text += page.extract_text() + '\n'

            if progress == True:
                print(page_num)
        return text