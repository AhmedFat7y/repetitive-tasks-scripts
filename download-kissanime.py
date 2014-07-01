import argparse
import urllib2
import re
import urlparse
import math

def info(msg, *additional_args):
  msg = '[Info -----] %s' % msg
  if len(additional_args) == 0:
    print msg
  else:
    print msg % additional_args

def debug(msg):
  msg = '[Debug ----] %s' % msg
  print msg % additional_args

def error(msg):
  msg = '[Error ----] %s' % msg
  print msg % additional_args

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("input_link", help="link to anime's main page")
  args = parser.parse_args()
  info('Opening - %s. . .', args.input_link)
  return args

def open_html_file(input_link):
  data_accumlator = ''
  data_read = ''
  total_bytes = 0
  bytes_read = 0
  response = urllib2.urlopen(input_link)
  if 'content-length' in response.headers:
    total_bytes = ['content-length']
  info('Downloading the html file')
  while True:
    data_read = response.read(1024 * 4)
    if not data_read:
      break;
    data_accumlator += data_read
  info('Done')
  return data_accumlator

def get_episodes_urls(input_link, html_file):
  info('Parsing the file')
  pattern = re.compile('<td><a href="(?P<episode_url>.*?)".*?>(?P<episode_name>.*?)</a></td>')
  urls_and_names = pattern.findall(html_file)
  urls_and_names = [(urlparse.urljoin(input_link, url_and_name[0]), url_and_name[1]) for url_and_name in urls_and_names]
  return urls_and_names

def get_episode_videos_urls(html_file):
  p = re.compile('<a target="_blank" href="(?P<video_url>http://redirector.googlevideo.com/videoplayback?.*?)">(?P<quality>.*?)</a>')
  urls_and_names = p.findall(html_file)
  return urls_and_names

def download_video(file_name_prefix, file_url_and_name):
  file_url = file_url_and_name[0]
  quality_text = file_url_and_name[1] 
  response = urllib2.urlopen(file_url)
  file_name = file_name_prefix + "." + response.info().getsubtype()[-3:]
  info(file_name)
  info(str(math.ceil(int(response.headers['content-length'])/1024.0/1024.0)) + ' MB')
  # with open(file_name, 'wb') as f:
  #   f.write(response.read())

def main():
  args = parse_args()
  html_file = open_html_file(args.input_link)
  episodes_urls_and_names = get_episodes_urls(args.input_link, html_file)
  for episode_url_and_name in episodes_urls_and_names:
    episode_url = episode_url_and_name[0]
    episode_name = episode_url_and_name[1]
    html_file = open_html_file(episode_url)
    videos_urls_and_names = get_episode_videos_urls(html_file)
    download_video(episode_name, videos_urls_and_names[0])
    break

if __name__ == "__main__":
  main()