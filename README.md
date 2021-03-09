# TikTokCommentsFetcher
Script to parse comments from TikTok

_Requires authentication via Google Account._

If you have problems, head to **Problems** section and to Issues.

### How to use
0. **Prerequisites.** This script works on Linux and Mac systems. Good work is not guaranteed for Windows. Create python virtual environment and install dependencies.
```bash
python3 -m venv/
source venv/bin/activate
python3 -m pip install -r requirements.txt
```
1. Open terminal and set environment variables EMAIL, PASSWORD, COMMENTS_LIMIT with gmail account email and password.
> COMMENTS_LIMIT is used to limit comment parsing for posts with lots of comments. For example, if COMMENTS_LIMIT = 100, than script will parse first 100 comments and then stop. If COMMENTS_LIMIT is too big, script will work for too long.

```bash
export EMAIL=<your_email@gmail.com> && \
export PASSWORD=<password_for_google_account> && \
export COMMENTS_LIMIT=<comment_limit>
```
2. Copy-paste link to video you want to parse into the `input.txt`.
```
echo "https://www.tiktok.com/?lang=en&is_copy_url=1&is_from_webapp=v3&item_id=6906436719541767425#/@youneszarou/video/6906436719541767425" >input.txt
```
3. Run python script `tiktok.py`.
```
python3 tiktok.py <input.txt
```


### Result
CSV file with columns: `id`, `nickname`, `link_to_profile`, `text`, `like_count`. No headers!
TODO: comment's answers.

### Parsing speed
Grows in non-linear way:

|Comment amt | Time              |
|------------|-------------------|
|100         | ~ 0               |
|2000        | ~1min             |
|5000        | ~10min            |

Speed is limited not only to language, technologies and parsing technique, but also to TikTok limitations. TikTok is against parsing and it will cause as many problems to parse as possible. For example:

* Comments are loaded in batches of 20 comments each.
* Next batch of comments can be loaded _only_ after previous one was done. No way to make process parallel.
* After parsing of about 1000 comments TikTok starts to make delays for about 1sec per batch. Further it will become 5sec and so on...

So we can't make this process parallel, but we can try to make this process use several accounts. Comments for different users are mixed.

### Technologies
Python, selenium


### How it works
1. Login in TikTok via Google Auth
2. Open the post.
3. Open comment section.
4. Load comments, scrolling down.
5. Write all comments to csv.

### Problems
**Do not touch Chromium while it's working!**

**This browser or app may not be secure.** Go to Google Account Settings, go to `Security` and enable `Less secure app access`. Also disable two-factor auth. Then try again. Even with this done there still can be problems.

**Comment section doesn't open** It is a problem, just try again. Double check the link is valid.

**White screen and no video.** It is a problem, and it seems to be TikTok ban.

**OMG IT IS NOT WORKING AT ALL!** Navigate to the Issues of this repo, open an issue and describe _in full details_ what happened. We will try to help.
