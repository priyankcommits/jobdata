import urllib2
import argparse
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
from base_crawler import BaseCrawler

parser = argparse.ArgumentParser(description='Arguments for agenlistscript.py')
parser.add_argument('-i', '--id', help='Input crawler agent id', required=True)
args = parser.parse_args()
crawler_id = args.id
key = 'django'
locations = ['Hyderabad', 'Bangalore', 'Chennai', 'Delhi', 'Mumbai']
tld = 'angellist.co'


class AngelListScript(BaseCrawler):

    def main(self):
        import ipdb;ipdb.set_trace();
        br = mechanize.Browser()
        # Enable cookie support for urllib2
        cookiejar = cookielib.LWPCookieJar()
        br.set_cookiejar( cookiejar )
        # Broser options
        br.set_handle_equiv( True )
        br.set_handle_gzip( True )
        br.set_handle_redirect( True )
        br.set_handle_referer( True )
        br.set_handle_robots( False )
        # ??
        br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 )
        br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ]
        # authenticate
        br.open('https://angel.co/login?utm_source=top_nav_home')
        forms = [f for f in br.forms()]
        br.form = forms[2]
        # these two come from the code you posted
        # where you would normally put in your username and password
        br.form.find_control(id="user_email").__setattr__('value', 'priyank@beautifulcode.in')
        br.form.find_control(id="user_password").__setattr__('value', 'priyank123')
        res = br.submit()
        for location in locations:
            u = 'https://angel.co/jobs\#find/f\!%7B%22keywords%22%3A%5B%22' + key + '%22%5D%2C%22locations%22%3A%5B%22' + location + '%22%5D%7D'
            url = br.open(u)
            text = url.read()
            text = str(text.encode('utf-8'))
            text_file = open("something.html", "wb")
            text_file.write(text)
            text_file.close()
            #opener = urllib2.build_opener()
            #opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            #response = opener.open(url)
            #text = response.read()
            soup = BeautifulSoup(text)
            data = soup.findAll('div', attrs={'class': 'listing-row'})
            for i in data:
                page = str(i.div.div.a.get('href'))
                page_new = page
                if page_new and page_new != 'None':
                    print page_new
if __name__ == "__main__":
    script = AngelListScript()
    script.main()
