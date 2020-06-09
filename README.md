# arXiv Digest
I made the experience that I subscribed to probably way to many topics, and that I had a hard time to go through my daily subscription.
This script takes as a standard input a mail by arXiv, and only returns the titles per line. Additionally, the script can also filter for authors. I suggest only using last names for this filtering, increasing the false positives, but not having many false negatives either.

To run the code copy the settings.py.example to settings.py and edit to your liking. Then you should be able to call
`python3 arxiv-digest.py < mail.txt`
which should produce a digest at the location you set in the settings file. If you use an email client that allows for script execution upon events (such as evolution) this can also be done automatically, giving you a daily digest, saved automatically to your files.
