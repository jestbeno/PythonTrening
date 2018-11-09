# APLIKACIJA SKOPIRA SLIKE IZ MAP IN PODMAP, KI SO NAVEDENA V EXCEL DATOTEKI

import openpyxl
import shutil
import os.path

src = "C:\\Users\\nucic\\Desktop\\SLIKE\IZBOR 2017\\"
dst = "C:\\Users\\nucic\\Desktop\\SLIKE\\2 TABLICE\\"
exFile = "Zvezek1.xlsx"

wb = openpyxl.load_workbook(exFile)
ws = wb.get_sheet_by_name('List1')

for row in ws.iter_rows(row_offset=0):
    try:
        fullFileName = os.path.join(src, row[0].value[:4], row[0].value)
        print(fullFileName)
        if (os.path.isfile(fullFileName)):
            shutil.copy(fullFileName, dst)
    except:
        print("napaka...")