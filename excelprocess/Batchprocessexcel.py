
import wx
from threading import Thread
from wx.lib.pubsub import pub
import xlwings as  xw
import time
import win32com
import win32com.client

#set the file filter
wildcard1 = "All files (*.*)|*.*|" \
            "Python source (*.py; *.pyc)|*.py;*.pyc"
wildcard2 = "Python source (*.py; *.pyc)|*.py;*.pyc|" \
            "All files (*.*)|*.*"


class Threadmodify(Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self):
        """Init Worker Thread Class."""
        #global filename,paths,cellname
        Thread.__init__(self)
        self.start()    # start the thread
    def run(self):
       global filename,paths,cellname
       # exlapp=xw.App(visible=False,add_book=False)
       # exlapp.display_alerts=False
       # exlapp.screen_updating=False
       print(paths)
       modifycellname=cellname.GetValue()
       print(modifycellname)

       modifycontent=filename.GetValue()

       print(modifycontent)
       wc=win32com.client.constants
       excel=win32com.client.gencache.EnsureDispatch('excel.application')
       for path in paths:
          exlapp=xw.App(visible=False,add_book=False)
          exlapp.display_alerts=False
          exlapp.screen_updating=False
          wb=exlapp.books.open(path)
          wb.sheets['1.开具增值税发票登记表'].range(modifycellname).value=modifycontent
          print(wb.sheets('1.开具增值税发票登记表').range('A1'))
          wb.save()
          wb.close()
          exlapp.quit()

          wx.CallAfter(pub.sendMessage,'update',re_msg=path+'修改成功')#利用PubSub实现wxPython应用程序与其他线程进行通讯
       wx.CallAfter(pub.sendMessage,'update',re_msg='修改完毕')

       #exlapp.quit()
class MyForm(wx.Frame):

    #-------------------------------------------------------------------
    #set the window layout
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "excel批量修改程序", size =(600,335))
        global filename,cellname,contents,paths

        bkg=wx.Panel(self,wx.ID_ANY)

        loadButton=wx.Button(bkg,label='选择文件')
        loadButton.Bind(wx.EVT_BUTTON,self.choose)

        modifyButton=wx.Button(bkg,label="修改")
        modifyButton.Bind(wx.EVT_BUTTON,self.modify)



        filename=wx.TextCtrl(bkg)
        filename.SetValue("请输入修改的内容,如'Hello'")
        cellname=wx.TextCtrl(bkg)
        cellname.SetValue("请输入修改的单元格,如'A1'")
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

        pub.subscribe(self.updatedispaly,'update')

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
       # global modifycontent
       # modifycontent=filename.GetValue()
       Threadmodify()


    def updatedispaly(self,re_msg):
        displaymessage=re_msg
        contents.AppendText(displaymessage+'\n\n')











if __name__ == "__main__":

    app = wx.App(False)

    frame = MyForm()

    frame.Show()
    app.MainLoop()





