#!/usr/bin/env python

import codecs
import os
import re

from bs4 import BeautifulSoup


def parse_videos():
    """
    Prints the total number of video files inside the /videos foler.
    """
    if not os.path.exists('videos'):
        return

    _, __, filenames = os.walk('videos').next()
    print('Number of Videos: {}'.format(len(filenames)))


def parse_photos():
    """
    Traverses the contents of the /photos folder.

    Prints the total number of photos/comments, as well as your average
    comments per photo and the top 10 most frequent commenters.

    The actual photos are separated by album and have their own folders.
    There is a corresponding HTML file for each with metadata and the comments.
    """

    if not os.path.exists('photos'):
        return

    photo_count = 0
    photo_albums = []
    comment_counts = {}

    for i, (dirpath, dirnames, filenames) in enumerate(os.walk('photos')):
        if i == 0:
            # Retrieve top level file names
            photo_albums = filenames
        else:
            photo_count += len(filenames)

    photo_albums = [name for name in photo_albums if '.html' in name]
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
    f = codecs.open('photos/{}'.format(filename), 'r', 'utf-8')
    soup = BeautifulSoup(f.read(), 'lxml')

    for comment in soup.findAll('div', {'class': 'comment'}):
        user = comment.findAll('span', {'class': 'user'})[0].text
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
    f = codecs.open('html/friends.htm', 'r', 'utf-8')
    soup = BeautifulSoup(f.read(), 'lxml')

    friend_map = {}
    friends_list = soup.findAll('ul')[1]
    for friend in friends_list:
        year = get_year(friend.text)
        friend_map = increment_dict(friend_map, year)

    print('Friends Added By Year:')
    print_dict(friend_map)


def parse_timeline():
    """
    Traverses the contents of the timeline HTML file.

    Example comment format:
    <div class="meta">Friday, March 9, 2018 at 11:53pm UTC+11</div>
    <div class="comment">Some post, comment, song, or link shared</div>
    """
    f = codecs.open('html/timeline.htm', 'r', 'utf-8')
    soup = BeautifulSoup(f.read(), 'lxml')

    posts = 0
    songs = 0
    for comment in soup.findAll('div', {'class': 'comment'}):
        if 'a song by' in comment.text:
            songs += 1
        else:
            posts += 1

    metadata_map = {}
    for metadata in soup.findAll('div', {'class': 'meta'}):
        year = get_year(metadata.text)
        metadata_map = increment_dict(metadata_map, year)

    print('Number of Posts/Comments: {}'.format(posts))
    print('Songs Streamed: {}'.format(songs))
    print('Timeline Activity By Year:')
    print_dict(metadata_map)


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
    - Friday, January 7, 2011 at 4:25pm UTC+11
    """
    match = re.findall(r', [0-9]{4}', text)
    return match[0][2:] if match else '2018'


if __name__ == '__main__':
    parse_videos()
    parse_photos()
    parse_friends_list()
    parse_timeline()
