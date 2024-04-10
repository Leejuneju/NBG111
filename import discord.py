import discord
import os
import random
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

team_names = ["경쟁스쿼드 1팀", "경쟁스쿼드 2팀", "경쟁스쿼드 3팀", "경쟁스쿼드 4팀", "경쟁스쿼드 5팀"]
current_team_index = 0

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='팀짜기')
async def divide_teams(ctx, team_size: int):
    global current_team_index

    if team_size <= 0:
        await ctx.send("팀의 인원 수는 1 이상이어야 합니다.")
        return

    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.send("음성 채널에 연결되어 있지 않습니다.")
        return

    members = voice_channel.members

    if len(members) < team_size:
        await ctx.send("팀의 인원 수가 부족합니다.")
        return

    random.shuffle(members)
    num_teams = len(members) // team_size
    teams = [members[i:i + team_size] for i in range(0, len(members), team_size)]

    for i, team in enumerate(teams):
        team_name = team_names[current_team_index]
        current_team_index = (current_team_index + 1) % len(team_names)
        team_str = f"{team_name}: " + ', '.join([member.mention for member in team])
        await ctx.send(team_str)

@bot.command(name='랜덤뽑기')
async def pick_random_members(ctx, num_winners: int):
    voice_channel = ctx.author.voice.channel

    if not voice_channel:
        await ctx.send("음성 채널에 연결되어 있지 않습니다.")
        return

    members = voice_channel.members

    if not members:
        await ctx.send("음성 채널에 아무도 없습니다.")
        return

    if num_winners < 1 or num_winners > len(members):
        await ctx.send("유효하지 않은 당첨 인원 수입니다. 음성 채널의 참여 인원 수보다 작거나 같아야 합니다.")
        return

    winners = random.sample(members, num_winners)
    winners_names = [winner.nick or winner.name for winner in winners]

    await ctx.send(f"축하합니다! 당첨된 참여자들: {', '.join(winners_names)}")

# 디스코드 봇 토큰을 사용하여 봇 로그인
# 여기에는 본인이 발급받은 디스코드 봇 토큰을 입력해야 합니다.
accrss_token = os.environ["BOT_TOKEN"]

bot.run(accrss_token) 
