"""



https://www.businesswire.com/
https://www.einpresswire.com/
https://www.globenewswire.com
https://www.newswire.ca/









"""

import asyncio
from playwright.sync_api import sync_playwright
import pandas as pd
from bs4 import BeautifulSoup

def extract_a_tags_to_dataframe(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)
        content = page.content()
        browser.close()

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        a_tags = soup.find_all('a')

        # Extract data into a list of dictionaries
        data = [{'a_class': ' '.join(tag.get('class', [])), 'a_href': tag.get('href', ''), 'a_text': tag.text.strip()} 
              for tag in a_tags]

        # Create DataFrame
        df = pd.DataFrame(data, columns=['a_class', 'a_href', 'a_text'])
        return df

# Run the async function and print the DataFrame
url="https://www.businesswire.com/portal/site/home/search/?searchType=news&searchTerm=microsoft&searchPage=2"
df = extract_a_tags_to_dataframe(url)
print(df)







import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from bs4 import BeautifulSoup

async def extract_a_tags_to_dataframe(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        page.wait_for_timeout(5000)
        content = await page.content()
        await browser.close()

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        a_tags = soup.find_all('a')

        # Extract data into a list of dictionaries
        data = [{'a_class': ' '.join(tag.get('class', [])), 'a_href': tag.get('href', ''), 'a_text': tag.text.strip()} 
              for tag in a_tags]

        # Create DataFrame
        df = pd.DataFrame(data, columns=['a_class', 'a_href', 'a_text'])
        return df

def test1():
   # Run the async function and print the DataFrame
   url="https://www.businesswire.com/portal/site/home/search/?searchType=news&searchTerm=microsoft&searchPage=2"
   df = asyncio.run(extract_a_tags_to_dataframe(url))
   print(df)










##########################################################
def urls_fetch_prnweswire(keywords=" microsoft", tag_filter='microsoft', comp_name=None, pagemax=2):

    keywords = keywords.replace(" ", "+")     

    prefix   = "https://www.prnewswire.com"
    url0     = 'https://www.prnewswire.com/search/news/?keyword={keywords}&page={k}&pagesize=200'
    url0     = url0.replace("{keywords}", keywords )
    
    urls2=[]
    for k in range(1, pagemax+1):
       urlk = url0.replace("{k}", str(k))
       urls = urls_extract(urlk)

       ### Custom Filter
       urls = [ link for link in urls if link.startswith('/news-releases/')]
       urls = [ prefix + url for url in urls if ".html" in url ]
       urls = [ x for x in urls if tag_filter in x ]
       # urls = [ x for x in urls if x not in set(urls2) ]

       urls2 = urls2 + urls

    urls3 = [ {"url": url, 'name': comp_name, 'origin': 'prnewswire.com', 'keywords': comp_name,
             'art_title': '', 'art_dt': ''  }  for url in urls2 ]
    log("N_prnewsire: ", len(urls2))   
    return urls3


def urls_fetch_yahoonews( keywords="microsoft" ):

    val = { "microsoft":"MSFT"}.get(keywords)
    url = f"https://finance.yahoo.com/quote/{val}/press-releases/"
    DIV_QUERY_SELECTOR = 'div.content.svelte-j87knz'
    H3_TAG = 'h3.clamp.svelte-j87knz'
    DIV_PUBLISHING = 'div.publishing.font-condensed.svelte-1k3af9g'
    A_TAG = 'a.subtle-link'

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)

        url_list = []
        items = page.query_selector_all(DIV_QUERY_SELECTOR)

        for item in items:
            try:
                title_element = item.query_selector(H3_TAG)
                if title_element:
                    title = title_element.inner_text()
                    link  = item.query_selector(A_TAG).get_attribute('href')
                    date_element = item.query_selector(DIV_PUBLISHING)
                    if date_element:
                        date_text = date_element.inner_text()
                        url_list.append({
                            'title': title,
                            'link': link,
                            'date': date_text
                        })
            except Exception as e:
                print(f"Error: {e}")
                continue

        browser.close()

    url_list = pd.DataFrame(url_list)         
    return url_list



@diskcache_decorator
def urls_fetch_microsoftnews(url = "https://news.microsoft.com/category/press-releases/"):
    TAG_ARTICLE = 'article.category-press-releases'
    TAG_DIV = 'div.c-paragraph-3.c-meta-text'
    A_TAG = 'a.f-post-link.c-heading-6.m-chevron'

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)

        url_list = []
        items = page.query_selector_all(TAG_ARTICLE)

        for item in items:
            try:
                date_element = item.query_selector(TAG_DIV)
                title_element = item.query_selector(A_TAG)
                if title_element and date_element:
                    date  = date_element.inner_text().strip()
                    title = title_element.inner_text().strip()
                    link  = title_element.get_attribute('href')
                    url_list.append({
                        'title': title,
                        'url': link,
                        'date': date
                    })
            except Exception as e:
                print(f"Error: {e}")
                continue

        browser.close()

    urls2 = [ {"url": str(x['url']), 'name': 'microsoft', 'origin': 'news.microsoft.com/category/press-releases/', 'keywords': "",
               'art_title' : x['title'],
               'art_dt' :    x['date']
             }  for x in url_list ]       
    return urls2


def urls_fetch_googlenews(keywords="microsoft funding", comp_name="microsoft", pagemax=2,):

    prefix = 'https://news.google.com'
    dt0 = date_now(fmt="%Y/%m/%d ")
    urlp = "https://news.google.com/search?q="
    keys = keywords.split(" ")
    keys = [  f"%22{x}%22" for x in keys   ]
    keys = "%20".join(keys)
    #keys = keywords.replace(" ", "%20" )
    url = f"{urlp}{keys}&hl=en-US&when%3A15d&gl=US&ceid=US%3Aen"         ##√
    ## https://news.google.com/search?q=%22microsoft%22%20%22partner%22%20when%3A7d&hl=en-US&gl=US&ceid=US%3Aen
    ## https://news.google.com/search?q=microsoft%20%22acquisition%22%20when%3A7d&hl=en-US&gl=US&ceid=US%3Aen
    ### "https://news.google.com/search?q=". &hl=en-US&gl=US&ceid=US%3Aen"
    log(url)

    ARTICLE_SELECTOR = 'article.IFHyqb'
    TITLE_SELECTOR = 'a.JtKRv'
    LINK_SELECTOR = 'a.JtKRv'
    DATE_SELECTOR = 'time.hvbAAd'

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)

        url_list = []
        items = page.query_selector_all(ARTICLE_SELECTOR)

        for item in items:
            try:
                title_element = item.query_selector(TITLE_SELECTOR)
                link_element = item.query_selector(LINK_SELECTOR)
                date_element = item.query_selector(DATE_SELECTOR)
                #text_element = item.query_selector(TEXT_SELECTOR)

                if title_element and link_element and date_element:
                    title = title_element.inner_text().strip()
                    link = link_element.get_attribute('href')
                    date = date_element.inner_text().strip()
                    #text = TEXT_element.inner_text().strip()

                    url_list.append({
                        'title': title,
                        'url':   link,
                        'date':   date,
                        'origin': url
                    })
            except Exception as e:
                print(f"Error: {e}")
                continue

        browser.close()

    urls2 = [ {"url": str(prefix + x['url']), 'name': comp_name,  'keywords': comp_name, 
                 'art_title': x['title'], 'art_dt': dt0 + x['date'],
                 'origin': x['origin']
              }  for x in url_list   ]      
    return urls2




#####################################################################################
def np_remove_dup(xlist):
    l2= []
    for x in xlist:
        if x not in l2:
              l2.append(x)
    return l2


def urls_extract(base_url ):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    urls = [link['href'].lower() for link in links ]

    urls = np_remove_dup(urls)
    log(str(urls)[:100] )
    log("N_urls:", len(urls))
    return urls


      




###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()



















