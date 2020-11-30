from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import tempfile
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def text_extract_from_pdf(pdf_file_path):
    with tempfile.TemporaryDirectory() as tmpdirname:
        # PDF_file = r'C:\Users\ElijahT\Google Drive\pdf_scan'  # Make this the name of the variable in the for loop.

        # Store all the pages of the PDF in a variable
        pages = convert_from_path(pdf_file_path, 500, poppler_path=r"C:\Program Files\poppler-0.68.0\bin")

        '''
        Converts the PDF to a JPEG. If it has multiple pages each individual page needs to be converted to its own
        individual JPEG
        '''

        # Counter to store images of each page of PDF to image
        image_counter = 1

        # Iterate through all the pages stored above
        for page in pages:
            # Declaring filename for each page of PDF as JPG
            # For each page, filename will be:
            # PDF page 1 -> page_1.jpg
            # PDF page 2 -> page_2.jpg
            # PDF page 3 -> page_3.jpg
            # ....
            # PDF page n -> page_n.jpg
            filename = "page_" + str(image_counter) + ".jpg"

            # Save the image of the page in system
            page.save(f'staging\\{filename}', 'JPEG')  # Can I use a tempfile instead of the staging area? I just want the
            # JPEG's deleted once the information is taken
            page.save(f'{tmpdirname}\\{filename}', 'JPEG')

            # Increment the counter to update filename
            image_counter = image_counter + 1

        ''' 
        Part #2 - Recognizing text from the images using OCR 
        '''

        # Variable to get count of total number of pages
        filelimit = image_counter - 1
        for i in range(1, filelimit + 1):
            # Set filename to recognize text from
            # Again, these files will be:
            # page_1.jpg
            # page_2.jpg
            # ....
            # page_n.jpg
            filename = "page_" + str(i) + ".jpg"

            # Recognize the text as string in image using pytesserct
            text = str(((pytesseract.image_to_string(Image.open(f'{tmpdirname}\\{filename}')))))

            # The recognized text is stored in variable text
            # Any string processing may be applied on text
            # Here, basic formatting has been done:
            # In many PDFs, at line ending, if a word can't
            # be written fully, a 'hyphen' is added.
            # The rest of the word is written in the next line
            # Eg: This is a sample text this word here GeeksF-
            # orGeeks is half on first line, remaining on next.
            # To remove this, we replace every '-\n' to ''.
            #text = text.replace('-\n', '')  # Took this out to see if I can get the program to work
            return text

