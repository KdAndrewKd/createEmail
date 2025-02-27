import requests
import random
import string
import time
import os

# Sources:
# https://www.1secmail.com/api/

# код работает. В папке 'all_mails' сохранен результат 

API = 'https://www.1secmail.com/api/v1/'
domain_list = [
  "1secmail.com",
  "1secmail.org",
  "1secmail.net",
#   "wwjmp.com",
#   "esiix.com",
#   "xojxe.com",
#   "yoggm.com"
]
domain = random.choice(domain_list)
count = 0

def generate_username():
    name = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(name) for i in range(10))
    return username


def check_mail(mail=''):
    req_link = f'{API}?action=getMessages&login={mail.split("@")[0]}&domain={mail.split("@")[1]}'
    r = requests.get(req_link).json()
    length = len(r)

    if length == 0:
        global count
        count += 1
        print(f'{count}) [INFO] На почте пока нет новых сообщений. Проверка происходит автоматически каждые 5 сек.')
    else:
        id_list = []

        for i in r:
            for k, v in i.items():
                if k == 'id':
                    id_list.append(v)

        print(f'[+] У вас {length} входящих! Почта обновляется каждые 5 сек.')

        current_dir = os.getcwd()
        final_dir = os.path.join(current_dir, 'all_mails')

        if not os.path.exists(final_dir):
            os.makedirs(final_dir)

        for i in id_list:
            read_msg = f'{API}?action=readMessage&login={mail.split("@")[0]}&domain={mail.split("@")[1]}&id={i}'
            r = requests.get(read_msg).json()

            sender = r.get('from')
            subject = r.get('subject')
            date = r.get('date')
            content = r.get('textBody')

            mail_file_path = os.path.join(final_dir, f'{i}.txt')

            with open(mail_file_path, "w") as file:
                file.write(f'Sender: {sender}\nTo: {mail}\nSubject: {subject}\nDate: {date}\nContent: {content}')


def delete_mail(mail=''):
    url = 'https://www.1secmail.com/mailbox'

    data = {
        'action': 'deleteMailbox',
        'login': mail.split('@')[0],
        'domain': mail.split('@')[1],
    }

    r = requests.post(url, data=data)
    print(f'[X] Почтовый фврес {mail} - удален!\n')


def main():
    try:
        username = generate_username()
        mail = f'{username}@{domain}'
        print(f'[+] Ваш почтвый адрес: {mail}')

        mail_req = requests.get(f'{API}?login={mail.split("@")[0]}&domain={mail.split("@")[1]}')

        while True:
            check_mail(mail=mail)
            time.sleep(5)
    
    except(KeyboardInterrupt): # Исключение сробатывает при нажатии клавиш прерывающих прооцесс выполнения программы Ctrl + c
        delete_mail(mail=mail)
        print("Программа прервана")

if __name__ == '__main__':
    main()



