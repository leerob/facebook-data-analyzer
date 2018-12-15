# Facebook Data Analyzer

> Update December 2018: Unfortunately, Facebook has completed changed the format of their data export making this script no longer work. PRs are welcome if anyone would like to try and update it to match the new output format.

- "Which year was I the most active?"
- "Who has commented on my pictures the most?"
- "How many songs have I streamed?"

This Python script will analyze the contents of your Facebook [data export](https://www.facebook.com/help/131112897028467) locally. To use this script, place `facebook.py` in the same folder as your Facebook data dump. Then, open the Terminal and run:

```bash
$ pip install bs4 lxml
$ python facebook.py
```

Which will produce the following output:

```bash
Number of Videos: 175
Number of Photos: 292
Number of Comments: 90
Average Comments Per Photo: 0.31
Top 10 Commenters:
 - My Mom: 17
 - Another Person: 15
..
..
..
Friends Added By Year:
 - 2010: 293
 - 2009: 280
 - 2011: 243
 - 2016: 159
 - 2012: 140
 - 2008: 87
 - 2017: 73
 - 2013: 73
 - 2018: 33
 - 2015: 33
 - 2014: 20
 - 2007: 5
Number of Posts/Comments: 5917
Songs Streamed: 43511
Timeline Activity By Year:
 - 2016: 13903
 - 2015: 8599
 - 2017: 8146
 - 2013: 7615
 - 2014: 5048
 - 2012: 3492
 - 2010: 1664
 - 2011: 1304
 - 2009: 1126
 - 2008: 100
 - 2018: 54
 - 2007: 6
```

## About

For more information about how this was created, see my [blog post](https://www.leejamesrobinson.com/blog/analyzing-10-years-of-facebook-data/). Cheers! 🎉
