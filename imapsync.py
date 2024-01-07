import os, csv
import asyncio
import time
from loguru import logger as logging

logging.add("imapsync.log", format="{time} {level} {message}", level="DEBUG", rotation="20 MB")

# def imapsync_csv():
#     logging.info("Start ImapSync")
#     #mode = input("Interactive mode or Read CSV file ? (1/2) ")
#     mode = "2"
#     if mode == "2":
#         #host1;user1;password1;host2;user2;password2
#         #file = input("File path : ")
#         file = "test_imapsync.csv"
#         if file:
#             print("Reading file")
#             with open(file, 'r') as csvfile:
#                 reader = csv.reader(csvfile, delimiter=';', quotechar='|')
#                 for row in reader:
#                     command = f"imapsync --host1 {row[0]} --user1 {row[1]} --password1 {row[2]} --host2 {row[3]} --user2 {row[4]} --password2 {row[5]}"
#                     #command = "imapsync --host1 " + row[0] + " -user1 " + row[1] + " --password1 " + row[2] +\
#                     #        " --ssl1 --host2 " + row[3] + " --user2 " + row[4] + " --password2 " + row[5] + " --ssl2"
#                     print(command)
#                     #os.system(command)
#imapsync_csv()

# async def start_imapsync(host1, user1, password1, host2, user2, password2):
#     try:
#         logging.info(f'start transfer for user: {user1}')
#         command = f"imapsync --host1 {host1} --user1 {user1} --password1 {password1} --host2 {host2} --user2 {user2} --password2 {password2}"
#         await os.system(command)
#         logging.info(f'success transfer for user: {user1}')
#     except Exception as e:
#         logging.exception(f'error transfer for user: {user1}\n{e}')

async def start_imapsync(host1, user1, password1, host2, user2, password2):
    try:
        logging.info(f'start transfer for user: {user1}')
        command = f'imapsync --host1 {host1} --user1 {user1} --password1 "{password1}" --host2 {host2} --user2 {user2} --password2 "{password2}"'
        logging.debug(f"{command}")
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if stdout:
            logging.info(f"Output for user {user1}:\n{stdout.decode()}")
        if stderr:
            logging.error(f"Error for user {user1}:\n{stderr.decode()}")
        await process.communicate()
        logging.info(f'success transfer for user: {user1}')
    except Exception as e:
        logging.exception(f'error transfer for user: {user1}\n{e}')

async def main_imapsync_csv(csv_path):
    try:
        logging.info(f'Start ImapSync')
        tasks = []
        with open(csv_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in reader:
                host1 = row[0]
                user1 = row[1]
                password1 = row[2]
                host2 = row[3]
                user2 = row[4]
                password2 = row[5]
                tasks.append(asyncio.create_task(start_imapsync(host1, user1, password1, host2, user2, password2)))

        for task in tasks:
            await task
        logging.info(f'Finish ImapSync')
    except Exception as e:
        logging.exception(f'error: {e}')

csv_file = "test_imapsync.csv"
asyncio.run(main_imapsync_csv(csv_file))


# async def test(url):
#     command = f"curl {url}"
#     print(f'start for {url}')
#     os.system(command)
#     await asyncio.sleep(3)
#     print(f'finish for {url}')
    
# urls = ["ipinfo.io/ip", "ipecho.net/plain", "icanhazip.com", "https://ipecho.net/plain", "ident.me", "api.ipify.org"]

# async def main(urls):
#     tasks = []
#     for url in urls:
#         tasks.append(asyncio.create_task(test(url)))

#     for task in tasks:
#         await task

# print(time.strftime('%X'))

# asyncio.run(main(urls))

# print(time.strftime('%X'))