import feedparser
import asyncio


# ID YouTube канала Fluget New
CHANNEL_ID = "UC6ciAHSYsIkUfAdX7mnEKNg"


# Айди твоей группы Telegram
CHAT_ID = -1003975506717


last_video = None


async def youtube_news(bot):

    global last_video


    while True:

        try:

            url = (
                "https://www.youtube.com/feeds/videos.xml?"
                f"channel_id={CHANNEL_ID}"
            )


            feed = feedparser.parse(url)


            if not feed.entries:
                await asyncio.sleep(600)
                continue


            video = feed.entries[0]


            if video.id != last_video:


                last_video = video.id


                text = f"""
🎬 <b>НОВОЕ ВИДЕО FLUGET NEW!</b>


🔥 {video.title}


📅 {video.published}


🔗 {video.link}


💙 Не забудь поставить лайк!
"""


                await bot.send_message(
                    CHAT_ID,
                    text,
                    parse_mode="HTML"
                )


        except Exception as e:

            print(
                "Ошибка YouTube News:",
                e
            )


        await asyncio.sleep(600)