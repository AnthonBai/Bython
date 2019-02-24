import requests
import re
import os
#根据av ID和起始部分编号下载b站视频


#def down_bili():

headers = {'Host': 'www.bilibili.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Connection': 'keep-alive',
           }

url = input('请输入哔哩哔哩视频专辑网址:')#http://www.bilibili.com/av=
start_no = int(input('请输入要下载选集视频系列起始编号：'))
sub_no = int(input('请输入要下载选集起始视频的子段开始编号：'))
end_no = int(input('请输入要下载选集视频终止编号：'))
end_no = end_no+1#注意这里不是-1，因为range的第二个函数不含在内


for i in range(start_no, end_no):
    
    url1 = url+'?p=%d' %(i)
    

    res = requests.get(url=url1, headers=headers).text

    vid = re.compile(r'"url":"http(.+?)","backup_url":.+?')
    
    f_url = re.findall(vid, res)
    #print(len(f_url))
    #print(f_url)
    print('本部分共爬到%d条url'%(len(f_url)))
    if len(f_url)<1: #如果没有url，则查找baseUrl
        print('未找到，开始查找备用url')
        vid = re.compile(r'"baseUrl":"http(.+?)","backupUrl":.+?')
        f_url = re.findall(vid, res)
        print('共%d段，'%(len(f_url)),end='')
    sub_no1=sub_no-1#删除子视频列表指定索引的元素,列表索引从0开始，因此应在用户输入值基础上减1
    #print(sub_no)
    f_url2 = f_url[sub_no1:]
    #print('将要下载%d条url'%(f_url))
    print('将要下载%d段'%(len(f_url)))
    #print(f_url)

    for v_url in f_url:#如果视频为分段视频，则下载指定子视频起始编号以后的全部子视频，
    
      #vid_url = 'https'+f_url[0]
      vid_url = 'https'+v_url
      #print(vid_url)
      title = re.compile(r'"title":"(.+?)"')
      title = re.findall(title, res)[0]
      title = re.sub('[!#?:^&*\/<>|]','',title) #去掉特殊字符
      v_title = re.search('page":%d,"from":"vupload","part":"(.*?)","duration'%(i),res,re.S).group(1)#分段视频标题
      
      
      vid_headers = {
        'Origin':'https://www.bilibili.com',
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    
        }
    #print(vid_url)
    #video = requests.get(url=vid_url, headers=vid_headers).content
      try:
        video = requests.get(url=vid_url, headers=vid_headers, stream = True) #启用stream，每次只下载一部分，减轻内存负担
      except urllib.error.URLErroe as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
      if os.path.exists(title) == False:
        os.mkdir(title)
      n = f_url.index(v_url)+1 #子视频编号
      print("正在下载%s之%d第%d段%s，总进度：%d/%d" %(title,i,n,v_title,i-start_no+1,end_no-start_no)) 
      with open('%s/%s%d-%d.mp4'%(title,v_title,i,n), 'wb+') as f: 
        for chunk in video.iter_content(chunk_size = 512):#边下载边实时写入文件，
            if chunk:#
                f.write(chunk)


print('下载完成！')

