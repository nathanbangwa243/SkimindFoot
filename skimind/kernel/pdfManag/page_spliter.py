# importing the required modules 
import PyPDF2

# global config
from . import skiconfig

# config
from . import config

# system tools
import os


SPLIT_PAGES = [1, 2]

def PDFsplit(pdf, splits=None): 
	# clean temp folder
	for filename in os.listdir(config.TEMPS_PDF_FOLDER):
		os.remove(filename)
    	
	if not splits:
		splits = SPLIT_PAGES

	# creating input pdf file object 
	pdfFileObj = open(pdf, 'rb') 
	
	# creating pdf reader object 
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
	
	# starting index of first slice 
	start = 0
	
	# starting index of last slice 
	end = splits[0]

	files_splited = list()
	
	
	for num_page in range(len(splits)): 
		# creating pdf writer object for (num_page+1)th split 
		pdfWriter = PyPDF2.PdfFileWriter() 
		
		# output pdf file name 
		outputpdf = os.path.join(config.TEMPS_PDF_FOLDER, f"{num_page}.pdf")
		
		try:
			# adding pages to pdf writer object 
			for page in range(start,end): 
				pdfWriter.addPage(pdfReader.getPage(page)) 
			
			# writing split pdf pages to pdf file 
			with open(outputpdf, "wb") as fp: 
				pdfWriter.write(fp) 
		except Exception as error:
			print(error)
		
		else:
			files_splited.append(outputpdf)

		# interchanging page split start position for next split 
		start = end 

		try: 
			# setting split end positon for next split 
			end = splits[num_page+1] 
		except IndexError: 
			# setting split end position for last split 
			end = pdfReader.numPages 
		
	# closing the input pdf file object 
	pdfFileObj.close()

	return files_splited
