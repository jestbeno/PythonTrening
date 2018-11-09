from lxml import etree

##################BRANJE XML DATOTEK#########################
file = '7060_2018_07_13 - Kopija.xml'

et = etree.parse(file)
ProcessedBy = et.xpath("Project/Site_Information/ProcessedBy/text()")[0]
# print(ProcessedBy)
Measurement_Date = et.xpath("Project/Site_Information/Measurement_Date/text()")[0]
# print(Measurement_Date)
River_Name = et.xpath("Project/Site_Information/River_Name/text()")[0]
# print (River_Name)
Number = et.xpath("Project/Site_Information/Number/text()")[0]

Name = et.xpath("Project/Site_Information/Name/text()")[0]
Remarks = et.xpath("Project/Site_Information/Remarks/text()")
# print(len(Remarks))
if len(Remarks) != 0:
    Remarks = et.xpath("Project/Site_Information/Remarks/text()")[0]
else:
    Remarks = ""
Outside_Gage_Height = format(float(et.xpath("Project/Site_Information/Outside_Gage_Height/text()")[0]) * 100, '.1f')
Water_Temperature = format(float(et.xpath("Project/Site_Information/Water_Temperature/text()")[0]), '.1f')

new_data = [Measurement_Date, ProcessedBy, Number, River_Name, Name, Outside_Gage_Height, Water_Temperature, Remarks]
datum = new_data[0]
print (datum)