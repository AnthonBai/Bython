import requests
import re
#根据av ID和起始部分编号下载b站视频


headers = {'Host': 'www.bilibili.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Connection': 'keep-alive',
           }

av_id = int(input('请输入AV编号:'))
start_no = int(input('请输入要下载视频系列起始编号：'))
end_no = int(input('请输入要下载视频终止编号：'))

for i in range(start_no, end_no):
    
    url = 'https://www.bilibili.com/video/av%d/?p=%d' %(av_id,i)
    #print(url)

    res = requests.get(url=url, headers=headers).text

    vid = re.compile(r'"url":"http(.+?)","backup_url":.+?')
    vid_url = 'https'+re.findall(vid, res)[0]
    print('正在下载%d，总进度：%d/%d' %(i,i-start_no+1,end_no-start_no))
    vid_headers = {
        'Origin':'https://www.bilibili.com',
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    
        }
    print(vid_url)
    #video = requests.get(url=vid_url, headers=vid_headers).content 
    video = requests.get(url=vid_url, headers=vid_headers, stream = True) #启用stream，每次只下载一部分，减轻内存负担
# 视频保存在与py文件同级的video文件夹下
    with open('video/'+str(i)+'.mp4', 'wb+') as f:
        for chunk in video.iter_content(chunk_size = 512):#边下载边实时写入文件，
            if chunk:#
                f.write(chunk)


