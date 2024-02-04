import httpx
import asyncio
from parsel import Selector

class AsyncEnglishScrapper:
    URL = "https://test-english.com/level-b2/"
    HEADERS={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': 'application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'identity'
    }
    ADVXPATH='//div[@class="pill hoverable"]/a/@href'
    ALLXPATH='//div[@class="dropdown-menu "]/a/@href'

    async def get_page(self):
        async with httpx.AsyncClient(headers=self.HEADERS) as client:
            response = await client.get(url=self.URL)
            links_c1=await self.c1(response=response)
            links_b2=await self.b2(response=response)
            links_b1=await self.b1(response=response)
            links_a2=await self.a2(response=response)
            links_a1=await self.a1(response=response)
            l=[links_c1,links_b2,links_b1,links_a2,links_a1]
            return l

    async def c1(self, response):
        tree = Selector(text=response.text)
        links = tree.xpath(self.ADVXPATH).extract()
        # for link in links:
        #     print(link)
        return links
    async def b2(self,response):
        tree = Selector(text=response.text)
        links = tree.xpath(self.ALLXPATH).extract()[3:29:5]
        # for i in links: print(i)
        return links
    async def b1(self,response):
        tree = Selector(text=response.text)
        links = tree.xpath(self.ALLXPATH).extract()[2:29:5]
        # for link in links: print(link)
        return links
    async def a2(self,response):
        tree = Selector(text=response.text)
        links = tree.xpath(self.ALLXPATH).extract()[1:29:5]
        # for link in links: print(link)
        return links
    async def a1(self,response):
        tree = Selector(text=response.text)
        links = tree.xpath(self.ALLXPATH).extract()[0:29:5]
        # for link in links: print(link)
        return links
if __name__ == "__main__":
    scraper = AsyncEnglishScrapper()
    asyncio.run(scraper.get_page())