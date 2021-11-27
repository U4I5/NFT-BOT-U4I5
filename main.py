import json
import time
import random
import urllib.request
import praw




global config, metakey, emojis, reddit, subreddit, webhook_url
config = json.load(open("config.json", "r"))
metakey = config["metakey"]
emojis = ("🤞", "🙏", "❤️", "💯", "▶️", "🔔", "🆔", "💸")
reddit = praw.Reddit(client_id=config["reddit"]["client"]["id"],
                     client_secret=config["reddit"]["client"]["secret"],
                     user_agent="<console:HAPPY:1.0>",
                     username=config["reddit"]["username"],
                     password=config["reddit"]["password"])
subreddit = reddit.subreddit("NFTsMarketplace")
webhook_url = config["discord_webhook_url"]


def execute_webhook(data: dict) -> str:
    http = urllib.request.Request(url=webhook_url, data=json.dumps(data).encode("utf-8"), headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(http) as response:
            content = response.read().decode("utf-8")
        response.close()
        return content
    except:
        return ''


def bot():
    comment = reddit.comment("t3_qsj32h")
    comment.upvote()
    comment.reply(metakey)

    posted_messages = 0
   
    giveaways_limit = 200

    bot_username = "NFT Bot"
    bot_avatar = "https://cdn.discordapp.com/avatars/755734583005282334/f50603ab57beb11b22be7500742aea6b.png?size=1024"

    for submission in subreddit.hot(limit=giveaways_limit):
        reply = random.choice(config["replies"])
        emoji = random.choice(emojis)
        data = dict(username=bot_username, avatar_url=bot_avatar, embeds=[
            dict(title="[>] **Reply posted !**", description=f"**Post's URL :** {submission.url}\n\n**Post's Name :** ``{submission.title}``\n\n**Post's ID :** ``{submission.id}``\n\n**Content :** ``{config['metakey']} - {reply}``\n\n**Sent messages :** ``{posted_messages}``\n\n**Support :** [Join discord](https://discord.gg/3JWKnxydHz)", thumbnail=dict(
                url=submission.url), footer=dict(text="Good luck."))
        ])

        posted_messages += 1
        try:
            submission.reply(f"{emoji} Metamask > {metakey} !\n{reply}  | discord : U4I5#6947")  #MAIS ICI LE MESSAGE QUI VAS ETRE ENVOYER PAR LE boT SUR REDDIT
            submission.upvote()
            print(
                f"---------------------------------\n[+] New comment posted ! \n[>] Post ID | {submission.id}\n[>] Content | {metakey} - {reply}\n[>] Upvote | True\n[>] Webhook endpoint | True")
            response = execute_webhook(data)
            if response == '':
                raise Exception("HTTP Error")
            time.sleep(random.randint(20, 40))
        except Exception as err:
            error = dict(username=bot_username, avatar_url=bot_avatar, embeds=[
                dict(title="[>] **An error occured !**",
                     description=f"You might being ratelimited by Reddit or being blacklist from the subreddit !\n\n**Posted messages :**  ``{posted_messages}``\n\n```Read the README.md file to see what you can do !```\n\n **Support :** [Join discord](https://discord.gg/3JWKnxydHz)", thumbnail=dict(url=bot_avatar))
            ])
            print(f"---------------------------------\n[-] {err}")
          ##  execute_webhook(error)
            time.sleep(360)

    task_ended = dict(username=bot_username, avatar_url=bot_avatar, embeds=[
        dict(title="[>] **Task ended !**",
             description=f"**Check your OpenSea account, you might receive some NFT !**\n\n**Posted messages :**  ``{posted_messages}``\n\n**Support :** [Join discord](https://discord.gg/3JWKnxydHz)",
             thumbnail=dict(url=bot_avatar))
    ])

    execute_webhook(task_ended)
    time.sleep(10)


if __name__ == "__main__":
    while True:
        bot()
