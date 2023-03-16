import os

try:
    import selfcord as discord
    import aiohttp
    import config
    import fade
    import asyncio
    from color import Colors
    from colorama import Fore as F

except ImportError:
    os.system("python install.py")
    
class Reporter(discord.Client):
    async def on_connect(self):
        c = Colors()
        print(f"{c.g}[+]{c.w} Logged in as {c.b}{self.user}")
        print(f"""{c.y}[?]{c.w} All the reasons:
 {c.b}[1]{c.w} Illegal content
 {c.b}[2]{c.w} Harassment
 {c.b}[3]{c.w} Spam or phishing links
 {c.b}[4]{c.w} Self-harm
 {c.b}[5]{c.w} NSFW content\n""")
        
        channel_id = int(input(f"{c.y}[?]{c.w} Enter the channel ID: "))
        user_id = int(input(f"{c.y}[?]{c.w} Enter the user ID: "))
        reason  = input(f"{c.y}[?]{c.w} Enter the reason: ")
        
        try:
            channel = self.get_channel(channel_id)
            user = await channel.guild.fetch_member(user_id)
            history = [m async for m in channel.history(limit = None) if m.author == user]
            print(f"{c.g}[+]{c.w} Found {c.b}{len(history)}{c.w} messages by {c.b}{user}")
            
        except Exception as e:
            print(f"{c.r}[-]{c.w} An error occurred whilst getting the channel.\n    Error: {c.r}{e}")
            exit()
            
        for msg in history:
            await self.send_report(channel.id, msg.id, channel.guild.id, reason)
        
    async def send_report(
        self,
        channel: str,
        message: str,
        guild: str,
        reason: str
    ):
        c = Colors()
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://discordapp.com/api/v9/report',
                json = {
                    'channel_id': channel,
                    'message_id': message,
                    'guild_id': guild,
                    'reason': reason
                }, headers={
                    'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; GO1452 Build/OPM2.171019.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.110 Mobile Safari/537.36',
                    'authorization': config.token
                }
            ) as report:
                if (status := report.status) == 201:
                    print(f"{c.g}[+]{c.w} Reported message {c.b}{message}")
                    
                elif status in (401, 403):
                    print(f"{c.r}[-] {c.w}Error: {c.r}{await report.json()['message']}")
                
                elif status == 429:
                    json = await report.json()
                    delay = json["retry_after"]
                    print(f"{c.r}[-] {c.w}We are being ratelimited. Sleeping for {c.b}{delay}s")    
                    await asyncio.sleep(delay)
                
                else:
                    print(f"{c.r}[-] {c.w}Error: {c.r}{await report.text()}\n    {c.w}Status: {c.r}{status}")

def banner():
    print(fade.water(f"""
/-\-/-\-/-\-/-\-/-\-/-\-/-\-/-\-/-\-/-\                     

▄████  ██   ███   █     ▄███▄   ██▄   
█▀   ▀ █ █  █  █  █     █▀   ▀  █  █  
█▀▀    █▄▄█ █ ▀ ▄ █     ██▄▄    █   █ 
█      █  █ █  ▄▀ ███▄  █▄   ▄▀ █  █  
 █        █ ███       ▀ ▀███▀   ███▀  
  ▀      █                            
        ▀                                                  
\-/-\-/-\-/-\-/-\-/-\-/-\-/-\-/-\-/-\-/"""))

def main():
    banner()
    reporter = Reporter()
    reporter.run(config.token)
    
if __name__ == "__main__":
    main()
    
        