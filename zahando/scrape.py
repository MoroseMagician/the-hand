from mimetypes import guess_extension
from urllib.parse import urlparse
import aiomysql
import asyncio
import aiohttp
import config
import util

class Scrape():
    def __init__(self, loop):
        self.loop = loop
        connector = aiohttp.TCPConnector(verify_ssl = True)
        self.session = aiohttp.ClientSession(loop=self.loop, connector=connector)

    def __del__(self):
        if not self.session.closed:
            self.session.close()

    async def connect(self):
        self.dbconnector  = await aiomysql.connect(
            host     = config.login["host"],
            port     = config.login["port"],
            user     = config.login["user"],
            password = config.login["pass"],
            db       = config.login["database"],
            charset  = "utf8mb4",
            loop     = self.loop)

    async def check_message(self, message):
        valid_urls = []
        messages = []
        for s in message.clean_content.split():
            if self.is_url(s):
                extension = await self.get_head(s)
                if extension is not False:
                    valid_urls.append((s, extension))
                else:
                    messages.append(s)
            else:
                messages.append(s)
        attach = message.attachments[0]
        if "width" in attach and "height" in attach:
            valid_urls.append((attach["url"], "." + attach["filename"].split(".")[-1]))
        text = " ".join(messages)
        await self.insert(valid_urls, message, text)

    async def insert(self, urls, message, text):
        query = "INSERT INTO haha_nice_meme_my_friend("    \
                "user, url, message, filename, timestamp)" \
                "VALUES(%s, %s, %s, %s, NOW());"
        for url in urls:
            filename = None
            if config.download_images:
                filename = util.generate_filename(url[1])
                with open(filename, "wb") as f:
                    f.write(await self.download(url[0]))
            async with self.dbconnector.cursor() as cursor:
                await cursor.execute(query, 
                    (str(message.author), url[0], text, filename))
        await self.dbconnector.commit()

    def is_url(self, url):
        u = urlparse(url)
        if u.scheme and u.netloc:
            return True
        return False

    async def get_head(self, url):
        async with self.session.head(url, timeout=30) as resp:
            if resp.status == 200:
                try:
                    head = resp.headers["Content-Type"].split("/")
                    if head[0] == "image":
                        if head[1] == "jpeg":
                            return ".jpeg"
                        return guess_extension(resp.headers["Content-Type"])
                except KeyError: pass
            return False

    async def download(self, url, parameters={}):
        async with self.session.get(url, params=parameters, timeout=30) as resp:
            return await resp.read()
