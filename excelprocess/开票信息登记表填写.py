import xlwings as  xw
import os







billpath=r'C:\Users\Administrator\Desktop\12月存管开票信息'
fillpath=r'C:\Users\Administrator\Desktop\12月存管开票信息\商户收费及开票登记-12月.xlsx'

sheet_bill='1.开具增值税发票登记表'
sheet_fill="开票登记"



cellname_bill_1='C11'
cellname_bill_2='C17'
cellname_bill_3='C6'
cellname_fill_1='A5'#填充发票类型
cellname_fill_2='E5'#填写商户名称
cellname_fill_3='F5'#填写商户开票金额


billdict={}



def  getbill(billpath,cellname_bill_1,cellname_bill_2,cellname_bill_3,sheetname):
    os.chdir(billpath)
    billfiles=os.listdir('.')
    # global billdict
    # billdict={}
    #获取账单金额数据
    for  file in billfiles:
          exlapp=xw.App(visible=False,add_book=False)
          exlapp.display_alerts=False
          exlapp.screen_updating=False
          wb=exlapp.books.open(file)
          billlistname=wb.sheets[sheet_bill].range(cellname_bill_1).value
          billlistnum=wb.sheets[sheet_bill].range(cellname_bill_2).value
          billlistype=wb.sheets[sheet_bill].range(cellname_bill_3).value
          print("处理文件"+file+'\n')
          if billlistnum[0] !='无':
              billdict[billlistname]=[billlistnum]
              if billlistype[0]!='R':
                  billdict[billlistname].append("增值税专用发票")
              else:
                  billdict[billlistname].append("增值税普通发票")
              print(billlistname+': '+str(billlistnum)+','+billdict[billlistname][1]+'\n')

          else:
              print(billlistname[0]+' 该商户无本月对账单\n')


          wb.save()
          wb.close()
          exlapp.quit()
    return billdict



getbill(billpath,cellname_bill_1,cellname_bill_2,cellname_bill_3,sheet_bill)



fillexl=xw.App(visible=False,add_book=False)
fillexl.display_alerts=False
fillexl.screen_updating=False
fillwb=fillexl.books.open(fillpath)
#向登记表中填写信息
for i,bill in enumerate(billdict):
    print(str(i)+bill+'\n')
    fillwb.sheets[sheet_fill].range(cellname_fill_1).value=billdict[bill][1]
    fillwb.sheets[sheet_fill].range(cellname_fill_2).value=bill
    fillwb.sheets[sheet_fill].range(cellname_fill_3).value=billdict[bill][0]
    cellname_fill_1=cellname_fill_1[0]+str(int(cellname_fill_1[1])+i+1)
    cellname_fill_2 = cellname_fill_2[0] + str(int(cellname_fill_2[1]) + i + 1)
    cellname_fill_3 = cellname_fill_3[0] + str(int(cellname_fill_3[1]) + i + 1)
    print(bill+"处理完毕")


fillwb.save()
fillwb.close()
fillexl.quit()