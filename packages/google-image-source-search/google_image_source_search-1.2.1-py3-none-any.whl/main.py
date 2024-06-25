import requests

from google_img_source_search import ReverseImageSearcher, SafeMode

from http.cookiejar import CookieJar
from http import cookiejar  # Python 2: import cookielib as cookiejar
from http.cookiejar import DefaultCookiePolicy


class NullCookieJar(cookiejar.CookiePolicy):
    """A CookieJar that rejects all cookies."""

    def extract_cookies(self, *_):
        """For extracting and saving cookies.  This implementation does nothing"""
        pass

    def set_cookie(self, _):
        """Normally for setting a cookie.  This implementation does nothing"""
        pass


class BlockAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False


if __name__ == '__main__':
    # image_url = 'https://i.pinimg.com/originals/c4/50/35/c450352ac6ea8645ead206721673e8fb.png'
    image_url = 'https://www.on-off-on.ru/upload/medialibrary/e29/e29d2b7bf27e4f32f48321abad9ea3f0.jpg'
    # image_url = 'https://i.pinimg.com/oridginals/c4/50/35/c450352ac6ea8645ead206721673e8fb.png'

    rev_img_searcher = ReverseImageSearcher()
    rev_img_searcher.switch_safe_mode(SafeMode.DISABLED)
    res = rev_img_searcher.search_by_file('../tests/test.png')

    for search_item in res:
        print(f'Title: {search_item.page_title}')
        print(f'Site: {search_item.page_url}')
        print(f'Img: {search_item.image_url}\n')
