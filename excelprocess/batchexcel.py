import xlwings as  xw
import os


os.chdir(r'E:\新网工作\支付工作\支付收费对账单\10月份对账单\10月存管开票信息')
print(os.getcwd())
files=os.listdir(r'E:\新网工作\支付工作\支付收费对账单\10月份对账单\10月存管开票信息')

modifycellname='C18'
modifycontent='2018年10月充值服务费'

for  file in files:
          exlapp=xw.App(visible=False,add_book=False)
          exlapp.display_alerts=False
          exlapp.screen_updating=False
          wb=exlapp.books.open(file)
          wb.sheets['1.开具增值税发票登记表'].range(modifycellname).value=modifycontent
          print(file+'修改成功')
          wb.save()
          wb.close()
          exlapp.quit()