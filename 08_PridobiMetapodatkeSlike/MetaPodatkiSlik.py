# LINK DO SEZNAMA VSEH KOD METAPODATKOV FOTOGRAFIJE!
# https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif.html

#####################################################################
################## GET METADATA OF PICTURES ###################
#####################################################################

from PIL import Image
# def get_date_taken(path):
#     return Image.open(path)._getexif()[36867]

# img = '8500_20180718_04.jpg'
img = '9240_20130301_02.jpg'



datetime =  (Image.open(img)._getexif()[36867])
PixelXDimension = (Image.open(img)._getexif()[40962])
PixelYDimension = (Image.open(img)._getexif()[40963])
monthTaken = datetime[5:7]


print (datetime)
print (PixelXDimension)
print (PixelYDimension)
print (f"slika je bila posneta v {monthTaken}. mesecu")