import PyPDF2
import os
    
def pdf_to_txt(file_path, txt_name = None, page_start=0, early_finish=0, progress=True):
    if txt_name == None:
        txt_name = os.path.splitext(os.path.basename(file_path))[0]
    
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        num_pages = len(reader.pages)

        text = ''
        for page_num in range(page_start, num_pages-early_finish):
            page = reader.pages[page_num]
            text += page.extract_text() + '\n'

            if progress == True:
                print(page_num)
    
    with open(txt_name + ".txt", "w", encoding="utf-8") as file:
        file.write(text)