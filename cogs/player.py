import discord, sqlite3
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone
from db import db

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name='플레이어등록', description="본인을 플레이어로 등록합니다.")
    async def player_register(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        join_date = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        try: # 플레이어 등록 시도
            db.execute("INSERT INTO player (user_id, join_date) VALUES (?, ?)", user_id, join_date)
            await interaction.response.send_message("플레이어로 등록되었습니다.")
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                await interaction.response.send_message("이미 등록된 플레이어입니다.")
            else:
                await interaction.response.send_message(f"등록 중에 오류가 발생했습니다: {e}")
                
    @app_commands.command(name='플레이어탈퇴', description="플레이어 탈퇴를 진행합니다.")
    async def player_delete(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        affected_rows = db.execute("DELETE FROM player WHERE user_id = ?", user_id)
        
        if affected_rows > 0:
            await interaction.response.send_message("플레이어 탈퇴가 완료되었습니다.")
        else:
            await interaction.response.send_message("플레이어로 등록되지 않은 사용자입니다.")
                
    @app_commands.command(description="현재 보유 중인 금액을 확인합니다.")
    @app_commands.describe(플레이어="조회할 플레이어")
    async def 잔액(self, interaction: discord.Interaction, 플레이어: discord.User):
        user_id = 플레이어.id
        balance = db.field("SELECT balance FROM player WHERE user_id = ?", user_id) or None

        if balance:
            await interaction.response.send_message(f"현재 잔액은 ${balance:,}입니다.")
        else:
            await interaction.response.send_message("불러올 수 없습니다.")
            
    @app_commands.command(description="플레이어의 정보를 조회합니다.")
    @app_commands.describe(player="조회할 플레이어")
    @app_commands.rename(player='플레이어')
    async def 플레이어정보(self, interaction: discord.Interaction, player: discord.User):
        user_id = player.id
        player_info = db.record("SELECT join_date, win_count, loss_count, exp, lvl FROM player WHERE user_id = ?", user_id)
        join_date, win_count, loss_count, exp, lvl = player_info or (None, None, None, None, None)

        if player_info:
            embed = discord.Embed(
                title=f"{player.display_name}님의 정보",
                color=discord.Color.blue()
            )
            embed.add_field(name="가입일", value=join_date, inline=False)
            embed.add_field(name="도박 전적", value=f"{win_count} 승 / {loss_count} 패", inline=False)
            embed.add_field(name="레벨 / 경험치", value=f"{lvl} 레벨 / {exp}", inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("불러올 수 없습니다.")
            
    @app_commands.command(description="플레이어의 잔액을 변경합니다.")
    @app_commands.describe(player="변경할 플레이어", new_balance="설정할 잔액")
    @app_commands.rename(player='플레이어', new_balance='신규잔액')
    async def 잔액변경(self, interaction: discord.Interaction, player: discord.User, new_balance: int):
        if interaction.user.guild_permissions.administrator:
            user_id = player.id
            affected_rows = db.execute("UPDATE player SET balance = ? WHERE user_id = ?", new_balance, user_id)

            if affected_rows > 0:
                await interaction.response.send_message(f"{player.display_name}님의 잔액을 ${new_balance:,}로 변경했습니다.")
            else:
                await interaction.response.send_message("플레이어로 등록되지 않은 사용자입니다.")
        else:
            await interaction.response.send_message("권한이 없습니다.")
        
async def setup(bot):
    await bot.add_cog(Player(bot))