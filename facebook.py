#!/usr/bin/env python

import codecs, os, re

from bs4 import BeautifulSoup

def find_fb_dir():
    for item in os.listdir():
        if item.startswith('facebook-') and not item.endswith('.zip'):
            return item
    if fb_dir is None:
        print('There was an error. Did you unzip your file?')

def parse_videos():
    """
    Prints the total number of video files inside the /photos_and_videos/videos folder
    uploaded directly to Facebook.
    """

    if not os.path.exists('{}/photos_and_videos'.format(fb_dir)):
        return
      
    _, __, filenames = next(os.walk('{}/photos_and_videos/videos'.format(fb_dir)))
    print('Number of Videos: {}'.format(len(filenames)))


def parse_photos():
    """
    Traverses the contents of the /photos_and_videos folder.

    Prints the total number of photos/comments, as well as your average
    comments per photo and the top 10 most frequent commenters.

    The actual photos are separated by album and have their own folders.
    There is an HTML file for each album in the /photos_and_videos/album 
    folder with metadata and the comments.
    """

    if not os.path.exists('{}/photos_and_videos'.format(fb_dir)):
        return

    photo_count = 0
    photo_albums = []
    comment_counts = {}

    for i, (dirpath, dirnames, filenames) in enumerate(os.walk('{}/photos_and_videos'.format(fb_dir))):
        if dirpath == '{}/photos_and_videos/album'.format(fb_dir):
            # Retrieve album filenames
            photo_albums = filenames
        elif i != 0 and dirpath != '{}/photos_and_videos/stickers_used'.format(fb_dir) and dirpath != '{}/photos_and_videos/videos'.format(fb_dir):
            # Skip the first iteration to ignore the html files in the
            # root photos_and_videos file, along with any stickers in
            # /stickers_used and videos in /videos
            photo_count += len(filenames)

    for filename in photo_albums:
        comment_counts = parse_photo_album(filename, comment_counts)

    total_comment_count = len(comment_counts)
    average_comments_per_photo = total_comment_count / float(photo_count)

    print('Number of Photos: {}'.format(photo_count))
    print('Number of Comments: {}'.format(total_comment_count))
    print('Average Comments Per Photo: {}'.format(average_comments_per_photo))
    print('Top 10 Commenters:')
    print_dict(comment_counts, end_index=10)


def parse_photo_album(filename, comment_counts):
    """
    Traverses the contents of a specific photo album HTML file.

    Example comment format:
    <div class="comment">
      <span class="user">Probably My Mom</span>Love this photo!
      <div class="meta">Wednesday, May 17, 2017 at 7:08am UTC+10</div>
    </div>
    """
    f = codecs.open('{}/photos_and_videos/album/{}'.format(fb_dir, filename), 'r', 'utf-8')
    soup = BeautifulSoup(f.read(), 'lxml')

    for comment in soup.findAll('div', {'class': 'uiBoxGray'}):
        user = comment.findAll('span')[0].text
        try:
            user = str(user)
            comment_counts = increment_dict(comment_counts, user)
        except:
            # There was a unicode error with the user name
            continue

    return comment_counts


def parse_friends_list():
    """
    Traverses the contents of the friends HTML file.
    """
    f = codecs.open('{}/friends/friends.html'.format(fb_dir), 'r', 'utf-8')
    soup = BeautifulSoup(f.read(), 'lxml')

    friend_map = {}
    friends_list = soup.findAll('div', {'class': 'uiBoxWhite'})
    for friend in friends_list:
        year = get_year(friend.text)
        friend_map = increment_dict(friend_map, year)

    print('Friends Added By Year:')
    print_dict(friend_map)


def parse_timeline():
    """
    Traverses the contents of the comments HTML file.

    Example comment format:
    <div class="pam _3-95 _2pi0 _2lej uiBoxWhite noborder">
        <div class="_3-96 _2pio _2lek _2lel">[Your name] commented on [another user's name] &#039;s [post, comment, song, video, or link]</div>
        <div class="_3-96 _2let">
            <div>
                <div class="_2pin">
                    <div>[Your comment]</div>
                </div>
            </div>
        </div>
        <div class="_3-94 _2lem">
            <a href=[Live URL]>Jan 16, 2019, 10:15 AM</a>
        </div>
    </div>
    """
    f = codecs.open('{}/comments/comments.html'.format(fb_dir), 'r', 'utf-8')
    comments_soup = BeautifulSoup(f.read(), 'lxml')
    comments_data = comments_soup.findAll('div', {'class': 'uiBoxWhite'})

    f = codecs.open('{}/posts/your_posts.html'.format(fb_dir), 'r', 'utf-8')
    posts_soup = BeautifulSoup(f.read(), 'lxml')
    posts_data = posts_soup.findAll('div', {'class': 'uiBoxWhite'})

    posts = 0
    songs = 0
    videos = 0
    comments = 0

    for post in posts_data:
        shared_media = define_media_link(post.text)

        if shared_media == 'song':
            songs += 1
        elif shared_media == 'video':
            videos += 1
        else:
            posts += 1

    for comment in comments_data:
        comments += 1

    metadata_map = {}
    for metadata in comments_data:
        year = get_year(metadata.text)
        metadata_map = increment_dict(metadata_map, year)
    for metadata in posts_data:
        year = get_year(metadata.text)
        metadata_map = increment_dict(metadata_map, year)

    print('Number of Posts: {}'.format(posts))
    print('Number of Comments: {}'.format(comments))
    print('Songs Shared: {}'.format(songs))
    print('Videos Shared: {}'.format(videos))
    print('Timeline Activity By Year:')
    print_dict(metadata_map)


def define_media_link(text):
    song_dict = {
        'spotify': 'https://open.spotify.com/track/',
        'soundcloud': 'https://soundcloud.com/'
    }

    video_dict = {
        'youtube': 'https://www.youtube.com/attribution_link?',
        'vimeo': 'https://vimeo.com/'
    }

    for val in song_dict.values():
        if val in text:
            return 'song'
    
    for val in video_dict.values():
        if val in text:
            return 'video'


def print_dict(dictionary, sort_index=1, end_index=100000):
    """
    Iterate over the dictionary items and print them as a key, value list.
    """
    sorted_dict = sorted(dictionary.items(),
                         key=lambda x: x[sort_index],
                         reverse=True)
    for k, v in sorted_dict[:end_index]:
        print(' - {}: {}'.format(k, v))


def increment_dict(dictionary, key):
    """
    Given a dict of str keys, increment the int count value.
    """
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1

    return dictionary


def get_year(text):
    """
    Given some text, parse out the year.

    Example formats:
    - May 19, 2007
    - Jan 7, 2011, 4:25 PM
    """
    match = re.findall(r', [0-9]{4}', text)
    return match[0][2:]


if __name__ == '__main__':
    fb_dir = find_fb_dir()
    parse_videos()
    parse_photos()
    parse_friends_list()
    parse_timeline()
