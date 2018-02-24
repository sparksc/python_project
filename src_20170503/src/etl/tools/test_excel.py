#! coding:utf-8
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

data = [
    [u"吴盼磊", u"浙江湖州", '1'],
    [u"宋龙", u"师范学院", "2"]
]

for r in data:
    ws.append(r)

wb.save("test.xlsx")
