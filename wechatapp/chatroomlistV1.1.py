#用于向指定群发送消息

# coding:utf-8
#v1.1 支持获取群列表并选择需要保存的群列表写入本地文件中

import itchat
import wx
from threading import Thread
from wx.lib.pubsub import pub
import time
import os


class Threadacquire(Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.start()    # start the thread
    def run(self):
        global chatroomlist
        chatroomlist={}
        notice="请扫码或手机确认登录"
        wx.CallAfter(pub.sendMessage,'update',re_msg=notice)
        itchat.auto_login(hotReload=True)
        notice="登录成功"
        wx.CallAfter(pub.sendMessage,'update',re_msg=notice)
        chatlist=itchat.get_chatrooms(update=True)
        if chatlist != []:
           wx.CallAfter(pub.sendMessage,'update',re_msg="以下为群列表\n\n")
           time.sleep(1)
           for chatroom in chatlist:
                chatroomNickname=chatroom["NickName"]
                chatlistUsername=chatroom['UserName']
                chatdict={chatroomNickname: chatlistUsername}
                chatroomlist.update(chatdict)
                print(chatroomNickname)
                wx.CallAfter(pub.sendMessage,'update',re_msg=chatroomNickname)
        else:
            print("通讯录无群聊")
            wx.CallAfter(pub.sendMessage,'update',re_msg="通讯录无群聊")

        itchat.run()



#界面

class MyForm(wx.Frame):

    #-------------------------------------------------------------------
    #set the window layout
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "微信撤回消息查看", size =(500,410))
        global nickname,contents,acquireButton,saveButton
        bkg=wx.Panel(self,wx.ID_ANY)
        #bkg.SetBackgroundColour("Grey")

        acquireButton=wx.Button(bkg,label='获取群信息')
        acquireButton.Bind(wx.EVT_BUTTON,self.acquire)

        saveButton=wx.Button(bkg,label='保存需要群发的群列表')
        saveButton.Disable()
        saveButton.Bind(wx.EVT_BUTTON,self.save)



        #nickname=wx.TextCtrl(bkg)

        contents=wx.TextCtrl(bkg,style=wx.TE_MULTILINE | wx.HSCROLL )
        #contents.SetStyle(410,335,wx.TextAttr("RED","YELLOW"))


        hbox=wx.BoxSizer()
        #hbox.Add(nickname,1,wx.EXPAND)
        hbox.Add(acquireButton,0,wx.LEFT,5)
        hbox.Add(saveButton,0,wx.LEFT,5)


        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox,0,wx.EXPAND | wx.ALL,5)
        vbox.Add(contents,1,wx.EXPAND | wx.LEFT |wx.BOTTOM | wx.RIGHT,5)

        bkg.SetSizer(vbox)

        #创建一个pub接收器
        pub.subscribe(self.updatedispaly,'update')
#设置消息发送的对象，默认为发送到登录微信的文件助手

    def acquire(self,event):
         Threadacquire()
         acqbtn=event.GetEventObject()
         acqbtn.Disable()
         saveButton.Enable()

    #保存用户选择的群聊记录在本地文件中，保存信息包括群聊NickName和Username
    def save(self,event):
        savechatlist=[]
        linenum=contents.GetNumberOfLines()
        for i in range(1,linenum):
            chatassign=contents.GetLineText(i)
            if chatroomlist.get(chatassign) is not None:
                #savedict={chatassign:chatroomlist.get(chatassign)}
                savechatlist.append(chatassign)
        #将撤回消息写入文件
        with open(r'chatroomlist.txt' ,'w',encoding="utf8") as chatroomfile:
             chatroomfile.write(str(savechatlist))
        #os.getcwd()
        print("保存成功")
        contents.AppendText("保存成功\n保存目录为：%s \n" % os.getcwd())
        itchat.logout()
        contents.AppendText("已退出登录\n")
        saveButton.Disable()
        acquireButton.Enable()



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













