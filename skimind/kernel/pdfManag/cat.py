import data_extractor

import os

cwd = os.getcwd()

filename = os.path.join(cwd, "samples")
filename = os.path.join(filename, "long-list.pdf")
#C:\Users\RMB PC\Downloads\AI\skimind_site\skimind\kernel\pdfManag\samples\long-list.pdf
print(os.path.exists(filename))

datas = data_extractor.pdf_process(filename)

print(len(datas))