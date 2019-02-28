#用于向指定群发送消息

# coding:utf-8
#v1.1 包含四个按钮，选择群聊列表、登录，发送文件，发送信息
#v1.2 优化报错搜索不到群聊的报错，群聊列表文件选错的报错
#v1.3 完善发送失败报错，并将发送失败的群列表保存在在本地文件中
import itchat
import wx
from threading import Thread
from wx.lib.pubsub import pub
import time
import ast
import filetype
import os




#创建一个文件对话框，用于选择文件，返回文件所在目录
def  choose(self):
        global tmp
        tmp=''
        wildcard1 = "All files (*.*)|*.*|" \
            "Python source (*.py; *.pyc)|*.py;*.pyc"
        dlg = wx.FileDialog(self,message="Choose a file",defaultFile="",wildcard=wildcard1,style=wx.FD_OPEN | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:

            #paths = dlg.GetPaths()
            paths = dlg.GetPaths()
            #print "You chose the following file(s):"
            #print(paths)
            #for path in paths:

                #tmp=tmp+path
            tmp=paths[0]
            #set the value of TextCtrl[filename]
            #filename.SetValue(tmp)
            #set the value to the TextCtrl[contents]
            #file=open(filename.GetValue())
            #file.close()
            #contents.SetValue("已选取图片")
        else:
            tmp=''
        dlg.Destroy()
        return tmp

#创建一个读取本地文件的函数，需以utf8编码方式读取，返回读取的文件内容
def get_file_content(filePath):
     with open(filePath, 'r',encoding="UTF-8") as fp:
           return fp.read()


#创建一个登录微信类，该类单独使用一个线程，防止因为发送时间过长导致GUI类MyFrom
class Threadlogin(Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.start()    # start the thread
    def run(self):
        notice="请扫码或手机确认登录"
        wx.CallAfter(pub.sendMessage,'update',re_msg=notice)#利用PubSub实现wxPython应用程序与其他线程进行通讯
        wx.CallAfter(pub.sendMessage,'update',re_msg="如果没有弹出二维码，请查看该应用所在目录是否生成登录二维码")
        itchat.auto_login(hotReload=True)
        notice="登录成功"
        wx.CallAfter(pub.sendMessage,'update',re_msg=notice+'\n'+'请选择需发送的文件或输入信息')
        itchat.run()




#创建一个发送信息的类，该类单独使用一个线程，防止因为发送时间过长导致GUI类MyFrom
class Threadsend(Thread):
    """Test Worker Thread Class."""
    #@sendre=<ItchatReturnValue: {'BaseResponse': {'Ret': 0, 'ErrMsg': '请求成功', 'RawMsg': '请求成功'}, 'MsgID': '7224254309590260193', 'LocalID': '15331388206320'}>
    #----------------------------------------------------------------------
    def __init__(self):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.start()    # start the thread
    def run(self):
        notice="准备群发消息"
        wx.CallAfter(pub.sendMessage,'update',re_msg=notice)
        # itchat.auto_login()
        # notice="登录成功"
        #wx.CallAfter(pub.sendMessage,'update',re_msg=notice)
        time.sleep(2)
        print(sendfiletype)

        sendfaillist=[] #用于保存发送失败的群列表
        searchfaillist=[] #用于保存搜索不到的群列表
        num=len(chatlist)
        #根据不同发送内容调用不同发送函数向微信群群发微信消息
        #如果发送的文件是文件类型
        if sendfiletype=='file'or sendfiletype=="archive" or sendfiletype=='font'or sendfiletype=='application':

            #print("1")
            print("向以下群聊发送文件：%s" % message)
            wx.CallAfter(pub.sendMessage,'update',re_msg="向以下群聊发送文件：%s" % message)
            i=0
            for chatroom in chatlist:
                # print("向以下群聊发送文件：%s" % message)
                # wx.CallAfter(pub.sendMessage,'update',re_msg="向以下群聊发送文件：%s" % message)

                if itchat.search_chatrooms(chatroom)!=[]:
                    chatroomusername=itchat.search_chatrooms(chatroom)[0]['UserName']
                    sendre=itchat.send_file(message,toUserName=chatroomusername)
                    if sendre['BaseResponse']['ErrMsg'] =="请求成功":
                        print("%s：发送成功"% chatroom)
                        wx.CallAfter(pub.sendMessage,'update',re_msg="%s：发送成功"% chatroom)
                    else:
                        print("%s：发送失败"% chatroom)
                        wx.CallAfter(pub.sendMessage,'update',re_msg="%s：发送失败"% chatroom)
                        sendfaillist.append(chatroom)
                else:
                    print("搜索不到群聊")
                    wx.CallAfter(pub.sendMessage,'update',re_msg="%s：搜索失败"% chatroom)
                    searchfaillist.append(chatroom)
                time.sleep(1)
                i+=1
                if i == num:
                    print("执行完毕")
                    wx.CallAfter(pub.sendMessage,'update',re_msg="执行完毕")

        #如果发送的文件是图片类型
        elif sendfiletype=='image':
            #print('2')
            print("向以下群聊发送图片：%s" %message)
            wx.CallAfter(pub.sendMessage,'update',re_msg="向以下群聊发送图片：%s" % message)
            i=0
            for chatroom in chatlist:
                # print("向以下群聊发送图片：%s" %message)
                # wx.CallAfter(pub.sendMessage,'update',re_msg="向以下群聊发送图片：%s" % message)
                # chatroomusername=itchat.search_chatrooms(chatroom)[0]['UserName']
                # sendre=itchat.send_image(message,toUserName=chatroomusername)
                # if sendre['BaseResponse']['ErrMsg'] =="请求成功":
                #     print("%s：发送成功"% chatroom)
                #     wx.CallAfter(pub.sendMessage,'update',re_msg="%s：发送成功"% chatroom)
                # else:
                #     print("%s：发送失败"% chatroom)
                #     wx.CallAfter(pub.sendMessage,'update',re_msg="%s：发送失败"% chatroom)
                if itchat.search_chatrooms(chatroom)!=[]:
                        chatroomusername=itchat.search_chatrooms(chatroom)[0]['UserName']#搜索群列表会返回一个群列表的类，混合列表和字典，需通过该方式获取群聊的UserName
                        sendre=itchat.send_image(message,toUserName=chatroomusername)
                        if sendre['BaseResponse']['ErrMsg'] =="请求成功":
                            print("%s：发送成功"% chatroom)
                            wx.CallAfter(pub.sendMessage,'update',re_msg="%s：发送成功"% chatroom)
                        else:
                            print("%s：发送失败"% chatroom)
                            wx.CallAfter(pub.sendMessage,'update',re_msg="%s：发送失败"% chatroom)
                            sendfaillist.append(chatroom)

                else:
                    print("搜索不到群聊")
                    wx.CallAfter(pub.sendMessage,'update',re_msg="%s：搜索失败"% chatroom)
                    searchfaillist.append(chatroom)

                time.sleep(1)
                i+=1
                if i == num:
                    print("执行完毕")
                    wx.CallAfter(pub.sendMessage,'update',re_msg="执行完毕")

        elif sendfiletype=="video" or sendfiletype=="audio":
            #print('3')
            print("向以下群聊发送视频：%s" % message)
            wx.CallAfter(pub.sendMessage,'update',re_msg="向以下群聊发送视频：%s" % message)
            i=0
            for chatroom in chatlist:
                # print("向以下群聊发送视频：%s" % message)
                # wx.CallAfter(pub.sendMessage,'update',re_msg="向以下群聊发送视频：%s" % message)
                 if itchat.search_chatrooms(chatroom)!=[]:
                    chatroomusername=itchat.search_chatrooms(chatroom)[0]['UserName']
                    sendre=itchat.send_video(message,toUserName=chatroomusername)
                    if sendre['BaseResponse']['ErrMsg'] =="请求成功":
                        print("%s：发送成功"% chatroom)
                        wx.CallAfter(pub.sendMessage,'update',re_msg="%s：发送成功"% chatroom)
                    else:
                        print("%s：发送失败"% chatroom)
                        wx.CallAfter(pub.sendMessage,'update',re_msg="%s：发送失败"% chatroom)
                        sendfaillist.append(chatroom)
                 else:
                        print("搜索不到群聊")
                        wx.CallAfter(pub.sendMessage,'update',re_msg="%s：搜索失败"% chatroom)
                        searchfaillist.append(chatroom)
                 time.sleep(1)
                 i+=1
                 if i == num:
                    print("执行完毕")
                    wx.CallAfter(pub.sendMessage,'update',re_msg="执行完毕")

        elif sendfiletype =="message":
            #print('4')
            print("向以下群聊发送信息：%s" % message)
            wx.CallAfter(pub.sendMessage,'update',re_msg="向以下群聊发信息：%s" % message)
            i=0
            for chatroom in chatlist:

                # wx.CallAfter(pub.sendMessage,'update',re_msg="向以下群聊发信息：%s" % message)
                if itchat.search_chatrooms(chatroom)!=[]:
                        chatroomusername=itchat.search_chatrooms(chatroom)[0]['UserName']
                        sendre=itchat.send(message,toUserName=chatroomusername)
                        if sendre['BaseResponse']['ErrMsg'] =="请求成功":
                            print("%s：发送成功"% chatroom)
                            wx.CallAfter(pub.sendMessage,'update',re_msg="%s：发送成功"% chatroom)
                        else:
                            print("%s：发送失败"% chatroom)
                            wx.CallAfter(pub.sendMessage,'update',re_msg="%s：发送失败"% chatroom)
                            sendfaillist.append(chatroom)

                else:
                    print("搜索不到群聊")
                    wx.CallAfter(pub.sendMessage,'update',re_msg="%s：搜索失败"% chatroom)
                    searchfaillist.append(chatroom)

                time.sleep(1)
                i+=1
                if i == num:
                    print("执行完毕")
                    wx.CallAfter(pub.sendMessage,'update',re_msg="执行完毕")

        else:
            #print('5')
            print("向以下群聊发送信息：%s" %message)
            wx.CallAfter(pub.sendMessage,'update',re_msg="向以下群聊发送信息：%s" % message)
            i=0
            for chatroom in chatlist:
                # print("向以下群聊发送信息：%s" %message)
                # wx.CallAfter(pub.sendMessage,'update',re_msg="向以下群聊发送信息：%s" % message)

                if itchat.search_chatrooms(chatroom)!=[]:
                        chatroomusername=itchat.search_chatrooms(chatroom)[0]['UserName']
                        sendre=itchat.send(message,toUserName=chatroomusername)
                        if sendre['BaseResponse']['ErrMsg'] =="请求成功":
                            print("%s：发送成功"% chatroom)
                            wx.CallAfter(pub.sendMessage,'update',re_msg="%s：发送成功"% chatroom)
                        else:
                            print("%s：发送失败"% chatroom)
                            wx.CallAfter(pub.sendMessage,'update',re_msg="%s：发送失败"% chatroom)
                            sendfaillist.append(chatroom)

                else:
                    print("搜索不到群聊")
                    wx.CallAfter(pub.sendMessage,'update',re_msg="%s：搜索失败"% chatroom)
                    searchfaillist.append(chatroom)

                time.sleep(1)
                i+=1
                if i == num:
                    print("执行完毕")
                    wx.CallAfter(pub.sendMessage,'update',re_msg="执行完毕")


            # print('发送完毕')
            # wx.CallAfter(pub.sendMessage,'update',re_msg="发送完毕\n")
        if sendfaillist!=[] and searchfaillist==[]:
            with open(r'sendfaillist.txt','w',encoding="UTF-8") as sendfaillistxt:
                sendfaillistxt.write(str(sendfaillist))
            print("将发送失败列表文件sendfaillist.txt保存在目：%s \n" % os.getcwd())
            wx.CallAfter(pub.sendMessage,'update',re_msg="将发送失败列表文件sendfaillist.txt保存在目：%s \n" % os.getcwd())
        elif searchfaillist!=[] and sendfaillist==[]:
            with open(r'searchfaillist.txt','w',encoding="UTF-8") as searchfaillistxt:
                searchfaillistxt.write(str(searchfaillist))
            print("将搜索失败列表文件searchfaillist.txt保存在目：%s \n" % os.getcwd())
            wx.CallAfter(pub.sendMessage,'update',re_msg="将搜索失败列表文件searchfaillist.txt保存在目：%s \n" % os.getcwd())
        elif sendfaillist!=[] and searchfaillist!=[]:
            with open(r'searchfaillist.txt','w',encoding="UTF-8") as searchfaillistxt:
                searchfaillistxt.write(str(searchfaillist))
            with open(r'sendfaillist.txt','w',encoding="UTF-8") as sendfaillistxt:
                sendfaillistxt.write(str(sendfaillist))

            print("将发送失败列表文件sendfaillist.txt保存在目：%s \n" % os.getcwd())
            print("将搜索失败列表文件searchfaillist.txt保存在目：%s \n" % os.getcwd())
            wx.CallAfter(pub.sendMessage,'update',re_msg="将发送失败列表文件sendfaillist.txt保存在目：%s \n" % os.getcwd())
            wx.CallAfter(pub.sendMessage,'update',re_msg="将搜索失败列表文件searchfaillist.txt保存在目：%s \n" % os.getcwd())
        else:
            print("%s个群全部发送成功" % num)
            wx.CallAfter(pub.sendMessage,'update',re_msg="%s个群全部发送成功" % num)

#创建一个GUI类，包含主界面和部分功能实现

class MyForm(wx.Frame):

    #创建主界面
    #set the window layout
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "微信群发消息（微信群）", size =(500,410))
        global filetext,contents,sendfiletype,filepath
        sendfiletype=''
        #chatlist=[]
        filepath=''
        bkg=wx.Panel(self,wx.ID_ANY)
        #bkg.SetBackgroundColour("Grey")

        #创建获取群群列表按钮
        acquirelistButton=wx.Button(bkg,label='选择群列表文件')
        acquirelistButton.Bind(wx.EVT_BUTTON,self.acquirelist)

        #创建选择并获取发送文件按钮
        acquirefileButton=wx.Button(bkg,label='选择发送文件')
        acquirefileButton.Bind(wx.EVT_BUTTON,self.acquirefile)


        #创建登录按钮
        loginButton=wx.Button(bkg,label='登录')
        loginButton.Bind(wx.EVT_BUTTON,self.login)

        #创建发送信息按钮
        sendButton=wx.Button(bkg,label='发送')
        sendButton.Bind(wx.EVT_BUTTON,self.send)

        #创建一个显示选择文件路径的文本框，还需能输入多行信息用于发送
        filetext=wx.TextCtrl(bkg,style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_RICH2 )

        contents=wx.TextCtrl(bkg,style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_RICH2 )
        #contents.SetStyle(410,335,wx.TextAttr("RED","YELLOW"))


        hbox=wx.BoxSizer()
        hbox.Add(filetext,1,wx.EXPAND)

        hbox.Add(acquirelistButton,0,wx.LEFT,5)
        hbox.Add(loginButton,0,wx.LEFT,5)
        hbox.Add(acquirefileButton,0,wx.LEFT,5)
        hbox.Add(sendButton,0,wx.LEFT,5)


        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox,0,wx.EXPAND | wx.ALL,5)
        vbox.Add(contents,1,wx.EXPAND | wx.LEFT |wx.BOTTOM | wx.RIGHT,5)

        bkg.SetSizer(vbox)

        #创建一个pub接收器
        pub.subscribe(self.updatedispaly,'update')


    #创建一个获取群发列表文件并读取内容的函数
    def acquirelist(self,event):
        global chatlist
        chatlist=[]
        chatlistfilepath=''
        chatlistfilepath=choose(self)
        if tmp != "":
           print(tmp)
           filetext.SetValue(chatlistfilepath)
           try:
               chatlist=ast.literal_eval(get_file_content(chatlistfilepath))
               print("以下为获取的群发列表\n\n")
               contents.AppendText("以下为获取的群发列表\n\n")
               print(chatlist)
               for index,chatroom in enumerate(chatlist):
                    contents.AppendText('%s : %s \n'%(index+1,chatroom))
               print("请点击登录微信\n\n")
               contents.AppendText("请点击登录微信\n\n")
           except:
               print("群聊列表文件不符合规范，请重新生成")
               contents.AppendText("群聊列表文件不符合规范，请重新生成\n")
        #for chatroom in chatlistdict.keys():

        else:
            print("请选择文件")
            contents.AppendText("请选择文件\n")

        #chatlistdict=ast.literal_eval(get_file_content(chatlistfilepath))


#创建一个选择发送文件的函数并返回文件类型
    def acquirefile(self,event):
        #global filepath
        #filepath=''
        #sendfiletype=''
        global  sendfiletype
        filepath=choose(self)
        if tmp != "":
           filetext.SetValue(filepath)
           print("选取的文件为：%s \n\n" % filepath )
           contents.AppendText("选取的文件为：%s \n" % filepath )
           fileguess=filetype.guess_mime(filepath)

           if fileguess is None:
              sendfiletype="file"
              print("文件类型为：%s \n" % sendfiletype)
              contents.AppendText("文件类型为：%s \n" % sendfiletype)
           else:
              sendfiletype=fileguess.split('/')[0]
              print(sendfiletype)
              print("文件类型为：%s \n" % sendfiletype)
              contents.AppendText("文件类型为：%s \n" % sendfiletype)

        #Threadacquire()
#创建登录微信的函数
    def login(self,event):
        Threadlogin()


#信息发送函数
    def send(self,event):
        global message,sendfiletype
        tmppath=filetext.GetValue()
        message=tmppath
        #if sendfiletype !=''and not os.path.exists(tmppath):
        if not os.path.exists(tmppath):
           sendfiletype="message"

        if chatlist !=[] and sendfiletype !='' and message !='':
            getchatroom=itchat.get_chatrooms()
            if len(getchatroom) != 0:
                print(chatlist,sendfiletype)
                Threadsend()
            else:
                print("请点击登录按钮登录")
                contents.AppendText("请点击登录按钮登录\n")
        #elif chatlist==[] or sendfiletype==''or message=='':
        else:
            #print(chatlist,sendfiletype)
            print('未选择群发列表或未选择发送文件或未输入发送信息')
            contents.AppendText('未选择群发列表或未选择发送文件或未输入发送信息\n')




    #通过多行文本框显示提示和记录的信息
    def updatedispaly(self,re_msg):
        displaymessage=re_msg
        contents.AppendText(displaymessage+'\n\n')








# Main
if __name__ == "__main__":

    app = wx.App()
    frame = MyForm()
    frame.Show()
    app.MainLoop()













