import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"{member.display_name}님이 서버에 참가하셨습니다.")
    
    @app_commands.command(name='hello', description="인사를 합니다")
    async def hello(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=":raised_hands: 반갑습니다!",
            description="서버에 오신 것을 환영합니다.",
            color=discord.Color.gold(),
            timestamp=datetime.now(),
            url='https://sunwoo-j.github.io/'
        )
        embed.add_field(name="동해물과 백두산이", value="마르고 닳도록 하느님이 보우하사 우리나라 만세", inline=False)

        embed.add_field(name="무궁화 삼천리", value="화려강산", inline=True)
        embed.add_field(name="대한사람", value="대한으로", inline=True)
        embed.add_field(name="길이 보전하세", value="(간주)", inline=True)
        
        file = discord.File('./icon.gif')
        
        embed.set_author(name="디스코드 봇 DIY", icon_url='attachment://icon.gif')
        embed.set_thumbnail(url='https://picsum.photos/100/100')
        embed.set_field_at
        embed.set_image(url='https://picsum.photos/600/400')
        embed.set_footer(text="Footer가 들어가는 공간", icon_url='attachment://icon.gif')
    
        await interaction.response.send_message("안녕하세요", embed=embed, file=file)
    
async def setup(bot):
    await bot.add_cog(Welcome(bot))