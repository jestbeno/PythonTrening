# LINK DO SEZNAMA VSEH KOD METAPODATKOV FOTOGRAFIJE!
# https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif.html

#####################################################################
################## SET WATERMARK TO IMAGES ###################
#####################################################################

from PIL import Image, ImageDraw, ImageFont
import os
# img = '1300_20180724_02.jpg'
img = '1100_20180724_01.jpg'

draw = Image.open(img)

datetime = (Image.open(img)._getexif()[36867])
PixelXDimension = (Image.open(img)._getexif()[40962])
PixelYDimension = (Image.open(img)._getexif()[40963])
monthTaken = datetime[5:7]

print(datetime)
print(PixelXDimension)
print(PixelYDimension)
# print (f"slika je bila posneta v {monthTaken}. mesecu")

imageText = datetime[8:10] + '. ' + datetime[5:7] + \
    '. ' + datetime[:4] + ' ' + datetime[:4]

# if PixelXDimension>PixelYDimension:
pos = (PixelXDimension - 1250, PixelYDimension - 200)
drawing = ImageDraw.Draw(draw)
black = (3, 8, 12)
font = ImageFont.truetype("arial.ttf", 130)
drawing.text(pos, imageText, fill=black, font=font)
draw.show()
draw.save('test.jpg')

# try:
#
# #if image is opened!
# except IOError:
# 	pass
