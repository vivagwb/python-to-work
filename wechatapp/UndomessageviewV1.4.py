# coding:utf-8
#v1.1添加保存聊天记录在本地
#v1.2 添加将撤回消息记录发给登录账号的文件助手或者好友的功能以及设置界面
#v1.3 解决由于程序运行太长GUI卡死的情况
#v1.4 加入退出登录按钮，增加按钮执行后失效后功能，防止多次点击创建多个线程
import itchat
from itchat.content import TEXT
from itchat.content import *
import time
import re
import os
import wx
from threading import Thread
from wx.lib.pubsub import pub



class TestThread(Thread):
    """Test Worker Thread Class."""

    #----------------------------------------------------------------------
    def __init__(self):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.start()    # start the thread
    # itchat.auto_login(hotReload=True)
    # itchat.get_friends(update=False)
    # itchat.get_chatrooms(update=True)
    def run(self):
        global ToUsername,error_msg,notice
        ToUsername='filehelper'
        error_msg=''
        notice="请扫码或手机确认登录"
        wx.CallAfter(pub.sendMessage,'update',re_msg=notice)
        itchat.auto_login(hotReload=True)
        notice="登录成功"
        wx.CallAfter(pub.sendMessage,'update',re_msg=notice)
        itchat.get_friends(update=False)
        itchat.get_chatrooms(update=True)
        if nickname.GetValue() != "":
           searchfrined=itchat.search_friends(nickname.GetValue())
           try:
              if searchfrined !=[]:
                ToUsername=searchfrined[0]["UserName"]
                print(ToUsername,'\n')
                #contents.AppendText("设置接收人为："+nickname.GetValue()+'\n\n')
                error_msg="设置接收人为："+nickname.GetValue()+'\n\n'
              else:
                print("搜索不到联系人，请重新设置或默认发送到文件助手\n")
                # contents.AppendText("搜索不到联系人，请重新设置或默认发送到文件助手\n\n")
                error_msg="搜索不到联系人，请重新设置或默认发送到文件助手"+'\n\n'
           except:
              print("其他错误，请退出重试\n")
              #contents.AppendText("其他错误，请退出重试\n\n")
              error_msg="其他错误，请退出重试\n\n"
        else:
            print("未设置发送人，默认发送到文件助手\n")
            #contents.AppendText("未设置发送人，默认发送到文件助手\n\n")
            error_msg="未设置发送人，默认发送到文件助手\n"
        wx.CallAfter(pub.sendMessage,'update',re_msg=error_msg)
        #获取微信消息并进行记录
        #print("开始记录")
        @itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT,VIDEO],isFriendChat=True,isGroupChat=True, isMpChat=True)
        def handle_receive_msg(msg):
            #print("记录消息")
            global face_bug,msg_id,msg_time,msg_content,msg_from,msg_from_user,msg_type,msg_information
            msg_information = {}
            face_bug=None

            msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())   #接受消息的时间
   #判断消息是群消息还是好友消息
            if msg["FromUserName"][0:2] =="@@":
                msg_f=itchat.search_chatrooms(userName=msg['FromUserName'])
                msg_from = msg_f['NickName']
                if msg["ActualNickName"] is not None:
                    msg_from_user=msg["ActualNickName"]

                else:
                    msg_from_user="个人消息"

            else:
                if itchat.search_friends(userName=msg['FromUserName']) is not None:
                    msg_f=itchat.search_friends(userName=msg['FromUserName'])
                    msg_from = msg_f['NickName']
                    msg_from_user='个人消息'

                else:
                    msg_from=msg['FromUserName']
                    msg_from_user='个人消息'

            print(msg_from,'\n',msg_from_user)

            #contents.AppendText(msg_from+'\n'+msg_from_user+'\n')

            msg_t = time.localtime(msg['CreateTime'])    #信息发送的时间时间戳转换为时间数组
            msg_time=time.strftime("%Y-%m-%d %H:%M:%S",msg_t)
            msg_id = msg['MsgId']    #每条信息的id
            msg_content = ''      #储存信息的内容
            msg_share_url = ''    #储存分享的链接，比如分享的文章和音乐
            msg_type=msg['Type']
            print(msg_type,'\n',msg_time)
            #contents.AppendText(msg_type+'\n'+msg_time+'\n')



            #如果发送的消息是文本或者好友推荐
            if msg['Type'] == 'Text' or msg['Type'] == 'Friends':
                msg_content = msg['Text']
                print(msg_content,'\n')

            #如果发送的消息是附件、视屏、图片、语音
            elif msg['Type'] == "Attachment" or msg['Type'] == "Video" \
                    or msg['Type'] == 'Picture' \
                    or msg['Type'] == 'Recording':
                msg_content = msg['FileName']    #内容就是他们的文件名
                msg['Text'](str(msg_content))    #下载文件
                print(msg_content,'\n')
                # print msg_content
            elif msg['Type'] == 'Card':    #如果消息是推荐的名片
                msg_content = msg['RecommendInfo']['NickName'] + '的名片'    #内容就是推荐人的昵称和性别
                if msg['RecommendInfo']['Sex'] == 1:
                    msg_content += '性别为男'
                else:
                    msg_content += '性别为女'

                print(msg_content,'\n')
            elif msg['Type'] == 'Map':    #如果消息为分享的位置信息
                x, y, location = re.search(
                    "<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
                if location is None:
                    msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()     #内容为详细的地址
                else:
                    msg_content = r"" + location
                print(msg_content,'\n')

            elif msg['Type'] == 'Sharing':     #如果消息为分享的音乐或者文章，详细的内容为文章的标题或者是分享的名字
                msg_content = msg['Text']
                msg_share_url = msg['Url']       #记录分享的url
                print(msg_share_url,'\n')
            face_bug=msg_content
            #contents.AppendText(msg_content+'\n\n')
            ##将信息存储在字典中，每一个msg_id对应一条信息
            msg_information.update(
                {
                    msg_id: {
                        "msg_from": msg_from, "msg_actual_from": msg_from_user,"msg_time": msg_time, "msg_time_rec": msg_time_rec,
                        "msg_type": msg_type,
                        "msg_content": msg_content, "msg_share_url": msg_share_url
                    }
                }
            )

            #组装获取的msg
            wechatmsg=msg_from+'\n'+msg_from_user+'\n'+msg_time+'\n'+msg_type+'\n'+msg_content+'\n\n'
            with open('%s chatrecord.txt'% time.strftime("%Y-%m-%d %H", time.localtime()) ,'a',encoding="utf8") as chatfile:
                  chatfile.write(wechatmsg)


            wx.CallAfter(pub.sendMessage,'update',re_msg=wechatmsg)

        #监测撤回消息
        @itchat.msg_register(NOTE,isFriendChat=True,isGroupChat=True, isMpChat=True)
        def information(msg):
            global msg_body
            msg_body=''

            #这里如果这里的msg['Content']中包含消息撤回和id，就执行下面的语句
            if '撤回了一条消息' in msg['Content']:
                old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)   #在返回的content查找撤回的消息的id
                old_msg = msg_information.get(old_msg_id)    #得到消息
                print(old_msg)
                #if len(old_msg_id)<11:  #如果发送的是表情包
                    #itchat.send_file(face_bug,toUserName='filehelper')
                #else:  #发送撤回的提示给文件助手
                if old_msg.get('msg_actual_from') != '':
                    msg_body = "【"\
                               + old_msg.get('msg_from')+"】\n" +old_msg.get('msg_actual_from')+ "  撤回了 \n"\
                               + old_msg.get("msg_type") + " 消息：" + "\n" \
                               + old_msg.get('msg_time_rec') + "\n" \
                                +r""+ old_msg.get('msg_content')
                else:
                    msg_body = "【" \
                               + old_msg.get('msg_from') + "】" + "  撤回了 \n" \
                               + old_msg.get("msg_type") + " 消息：" + "\n" \
                               + old_msg.get('msg_time_rec') + "\n" \
                               + r"" + old_msg.get('msg_content')
                    #如果是分享的文件被撤回了，那么就将分享的url加在msg_body中发送给文件助手
                itchat.send_msg(msg_body, toUserName=ToUsername)
                print(msg_body,'\n')
                #contents.AppendText(msg_body+'\n\n')
                wx.CallAfter(pub.sendMessage,'update',re_msg=msg_body)

                if old_msg['msg_type'] == "Sharing":
                    #msg_body += "\n就是这个链接➣ " + old_msg.get('msg_share_url')
                    itchat.send(old_msg.get('msg_share_url'),toUserName=ToUsername)
                    print(old_msg.get('msg_share_url'))


                    # 有文件的话也要将文件发送回去
                elif old_msg["msg_type"] == "Picture" \
                            or old_msg["msg_type"] == "Recording" \
                            or old_msg["msg_type"] == "Video" \
                            or old_msg["msg_type"] == "Attachment":
                        file = '@fil@%s' % (old_msg['msg_content'])
                        itchat.send(msg=file, toUserName=ToUsername)
                        os.remove(old_msg['msg_content'])

                    # 删除字典旧消息
                msg_information.pop(old_msg_id)

                #将撤回消息写入文件
                with open('%s undomsg.txt'% time.strftime("%Y-%m-%d %H", time.localtime()) ,'a',encoding="utf8") as undomsg:
                     undomsg.write(msg_body+'\n\n')
        itchat.run()



#界面

class MyForm(wx.Frame):

    #-------------------------------------------------------------------
    #set the window layout
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "微信撤回消息查看", size =(410,335))
        global nickname,contents,setButton,logoutButton
        bkg=wx.Panel(self,wx.ID_ANY)
        #bkg.SetBackgroundColour("Grey")

        setButton=wx.Button(bkg,label='设置发送人并登录')
        setButton.Bind(wx.EVT_BUTTON,self.set)

        logoutButton=wx.Button(bkg,label='退出登录')
        logoutButton.Disable()
        logoutButton.Bind(wx.EVT_BUTTON,self.logout)



        nickname=wx.TextCtrl(bkg)
        nickname.SetValue("请输入需要将撤回消息发送的好友，默认发送到登录账号的文件助手")
        contents=wx.TextCtrl(bkg,style=wx.TE_MULTILINE | wx.HSCROLL )
        #contents.SetStyle(410,335,wx.TextAttr("RED","YELLOW"))

        hbox=wx.BoxSizer()
        hbox.Add(nickname,1,wx.EXPAND)
        hbox.Add(setButton,0,wx.LEFT,5)
        hbox.Add(logoutButton,0,wx.LEFT,5)


        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox,0,wx.EXPAND | wx.ALL,5)
        vbox.Add(contents,1,wx.EXPAND | wx.LEFT |wx.BOTTOM | wx.RIGHT,5)

        bkg.SetSizer(vbox)

        #创建一个pub接收器
        pub.subscribe(self.updatedispaly,'update')
#设置消息发送的对象，默认为发送到登录微信的文件助手
    def set(self,event):
        TestThread()
        btn = event.GetEventObject()
        btn.Disable()
        logoutButton.Enable()
    #通过多行文本框显示提示和记录的信息
    def updatedispaly(self,re_msg):
        displaymessage=re_msg
        contents.AppendText(displaymessage+'\n\n')


    def logout(self,event):
        itchat.logout()
        print('请重新登录')
        contents.AppendText("请重新登录\n")
        logoutbtn=event.GetEventObject()
        logoutbtn.Disable()
        setButton.Enable()





# Main
if __name__ == "__main__":

    app = wx.App()

    frame = MyForm()

    frame.Show()


    app.MainLoop()













