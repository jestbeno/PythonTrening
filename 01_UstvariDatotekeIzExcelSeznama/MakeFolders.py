##############################################################################
# USTVARI DATOTEKE Z ŽELENIMI IMENI - IMENA PREBERE IZ EXCELOVE DATOTEKE!#####
##############################################################################
import openpyxl
import os

root_path = r'C:\Users\nucic\Desktop\PYTHON\Bliznjice\MakeFolders'
exFile = "Zvezek1.xlsx"
wb = openpyxl.load_workbook(exFile)
ws = wb.get_sheet_by_name('List1')

for row in ws.iter_rows(row_offset=1):
    try:
        os.mkdir(os.path.join(root_path, str(row[0].value)))
    except:
        print("Zadnja prenešena datoteka: "+ str(row[0].value) )

