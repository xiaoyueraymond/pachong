from pytube import YouTube
URL="https://www.youtube.com/watch?v=EbB7BVe81Fc"
path=r'D:/upload'
yt=YouTube(URL)
yt.streams.filter(progressive=True)
stream = yt.streams.get_by_itag(22)
stream.download(path)
