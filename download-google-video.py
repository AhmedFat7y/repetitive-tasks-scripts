import urllib2
import sys
file_url ='http://redirector.googlevideo.com/videoplayback?id=73e3b86291403a5f&itag=35&source=picasa&cmo=sensitive_content=yes&ip=0.0.0.0&ipbits=0&expire=1404735946&sparams=id,itag,source,ip,ipbits,expire&signature=13B6C78BE3C9F01CE8C2AB6FDF389F3D19B3C0B5.5170DDB8BDA6BFC3769131DCAAC86ABFF1A9B469&key=lh1'
if len(sys.argv) > 1:
  file_url = sys.argv[1]
# file to be written to
file_name = "death-note_episode-001."

response = urllib2.urlopen(file_url)
file_name += response.info().getsubtype()[-3:]
print '[Info -----] Downloading', file_name
# You can also use the with statement:
with open(file_name, 'wb') as f:
  f.write(response.read())
print '[Info -----] Done'