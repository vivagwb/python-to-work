
import wx

import xlwings as  xw


#set the file filter
wildcard1 = "All files (*.*)|*.*|" \
            "Python source (*.py; *.pyc)|*.py;*.pyc"
wildcard2 = "Python source (*.py; *.pyc)|*.py;*.pyc|" \
            "All files (*.*)|*.*"



class MyForm(wx.Frame):

    #-------------------------------------------------------------------
    #set the window layout
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "excel批量修改程序", size =(600,335))
        global filename,cellname,contents

        bkg=wx.Panel(self,wx.ID_ANY)

        loadButton=wx.Button(bkg,label='选择文件')
        loadButton.Bind(wx.EVT_BUTTON,self.choose)

        modifyButton=wx.Button(bkg,label="修改")
        modifyButton.Bind(wx.EVT_BUTTON,self.modify)



        filename=wx.TextCtrl(bkg)
        cellname=wx.TextCtrl(bkg)
        contents=wx.TextCtrl(bkg,style=wx.TE_MULTILINE | wx.HSCROLL)
        #contents.SetStyle(410,335,wx.TextAttr("RED","YELLOW"))

        hbox=wx.BoxSizer()
        fbox=wx.BoxSizer()
        hbox.Add(filename,1,wx.EXPAND)
        hbox.Add(loadButton,0,wx.LEFT,5)
        fbox.Add(cellname,1,wx.EXPAND)
        fbox.Add(modifyButton,0,wx.LEFT,5)

        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox,0,wx.EXPAND | wx.ALL,5)
        vbox.Add(fbox,0,wx.EXPAND| wx.ALL,5)
        vbox.Add(contents,1,wx.EXPAND | wx.LEFT |wx.BOTTOM | wx.RIGHT,5)

        bkg.SetSizer(vbox)



    def choose(self,event):
        dlg = wx.FileDialog(self,message="Choose a file",defaultFile="",wildcard=wildcard1,style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_MULTIPLE)
        global paths
        if dlg.ShowModal() == wx.ID_OK:
           paths = dlg.GetPaths()
           #type(paths)
           print(paths)
           print(len(paths))
           print(type(len(paths)))
           print("选取了"+str(len(paths))+'个文件\n')
           contents.AppendText("选取了"+str(len(paths))+'个文件\n')
           for path in paths:
               print(path)
               contents.AppendText(path+'\n')

        else:
            paths=''

        dlg.Destroy()


    def modify(self,event):
       global  paths
       print(paths)
       modifycellname=cellname.GetValue()
       print(modifycellname)

       modifycontent=filename.GetValue()

       print(modifycontent)
       # wc=win32com.client.constants
       # excel=win32com.client.gencache.EnsureDispatch('excel.application')
       for path in paths:
          exlapp=xw.App(visible=False,add_book=False)
          exlapp.display_alerts=False
          exlapp.screen_updating=False
          wb=exlapp.books.open(path)
          wb.sheets['sheet1'].range('A1').value='K'
          print(wb.sheets('sheet1').range('A1'))
          contents.AppendText('文件'+path+"修改完毕\n\n")
          wb.save()
          wb.close()
          exlapp.quit()













if __name__ == "__main__":

    app = wx.App(False)

    frame = MyForm()

    frame.Show()
    app.MainLoop()





