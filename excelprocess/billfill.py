import xlwings as  xw
import os
import re


billpath=r'C:\Users\Administrator\Desktop\10月份对账单\存管P2P平台'
fillpath=r'C:\Users\Administrator\Desktop\10月份对账单\10月存管开票信息'

cellname_bill='G13:G18'
cellname_fill='C17'

sheet_bill='1'
sheet_fill='1.开具增值税发票登记表'



def  getbill(billpath,cellname_bill,sheetname):
    os.chdir(billpath)
    billfiles=os.listdir('.')
    global billdict
    billdict={}
    splitletter='10'
    #获取账单金额数据
    for  file in billfiles:
          exlapp=xw.App(visible=False,add_book=False)
          exlapp.display_alerts=False
          exlapp.screen_updating=False
          wb=exlapp.books.open(file)
          billlist=wb.sheets[sheetname].range(cellname_bill).value
          print("处理文件"+file+'\n')
          if '\\' in billlist:
              print(file+' 处理成功'+'\n')
              billindex=billlist.index('\\')
              billamount=round(billlist[billindex-1],2)
          else:
              print(file+' 未找到金额\n')
              billamount=0
          ma=re.split(splitletter,file)
          billdict[ma[0]]=billamount
          print(file+' 账单金额'+str(billamount))
          wb.save()
          wb.close()
          exlapp.quit()
    return billdict

getbill(billpath,cellname_bill,sheet_bill)

def  fillbill(fillpath,cellname_fill,sheetname):
    os.chdir(fillpath)
    fillfile=os.listdir('.')
    splitletter='开'
    for file in fillfile:
        exlapp=xw.App(visible=False,add_book=False)
        exlapp.display_alerts=False
        exlapp.screen_updating=False
        wb=exlapp.books.open(file)
        ma=re.split(splitletter,file)
        if billdict.get(ma[0]):
           wb.sheets[sheetname].range(cellname_fill).value=billdict[ma[0]]
           print(file+"修改完毕")
        else:
           wb.sheets[sheetname].range(cellname_fill).value='无'
           print(file+"未找到对应对账单")
        wb.save()
        wb.close()
        exlapp.quit()

fillbill(fillpath,cellname_fill,sheet_fill)
