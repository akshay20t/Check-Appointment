import requests
from bs4 import BeautifulSoup
from time import sleep


def telegram_bot_sendtext(bot_message):
    bot_token = ''#Enter bot token
    bot_chatID = ''#Enter bot chatID
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response.json()

def check_appointment(refresh_time, dates, flag):
    done= []
    response = requests.get('https://goo.gl/RdS6A4', headers={
        'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find_all('table')

    for date in dates:
        month = date.partition(' ')[0]
        available = []
        for t in table:
            child = t.findChildren('th', class_='month')[0].string.partition(' ')[0]
            if (child == month):
                tr = t.tbody.find_all('tr')
                for r in tr:
                    try:
                        td = r.find_all('td', class_='buchbar')
                        for d in td:
                            available.append(d.a.string)
                    except:
                        continue
        if (date.partition(' ')[2] in available):
            msg= telegram_bot_sendtext('Appointment is available on '+date)
            done.append(date)
            print(msg)
            print('Message Sent on Telegram')

    for d in done:
        index_= dates.index(d)
        dates.pop(index_)
    if (len(dates)==0):
        flag= 1
        del response
        return flag
    else:
        sleep(refresh_time)
        del response
        print('refreshing')
        sleep(10)
        return flag

if __name__=='__main__':
    dates= list(input('Enter Date: ').split(','))
    refresh_time= int(input('Enter Refresh Time: '))
    flag= 0
    while (flag!= 1):
        flag= check_appointment(refresh_time, dates, flag)
