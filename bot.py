import requests
import datetime
url = "https://api.telegram.org/bot568200205:AAHEzc2c0TfywZwzdxEGYPRv1COUfvBFDmI/"


def get_updates_json(request):  
    params = {'timeout': 100, 'offset': None}
    response = requests.get(request + 'getUpdates', data=params)
    return response.json()
    
def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):  
    chat_id = update['message']['chat']['id']
    return chat_id

def send_mess(chat, text):  
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response

def main():  
    update_id = last_update(get_updates_json(url))['update_id']
    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:
            now = datetime.datetime.now()
            
            send_mess(get_chat_id(last_update(get_updates_json(url))),("Date: " + str(now)))
            day = str(now.day)
            if len(day) == 1:
                day = "0" + day 
            month = now.month
            timetable = []
            f = open("exams.txt")
            for line in f:
                timetable.append(line)
            f.close()
            counter = 0
            messages = []
            test = True
            while counter != 254:
                if counter % 7 == 0:
                    timetable_date = str(timetable[counter])
                    daynumber = timetable_date[4] + timetable_date[5]
        
                if (now.strftime("%b") in timetable_date) and (day == daynumber):
                    newcounter = counter
                    while newcounter != (counter + 1):
                        line=timetable[newcounter]
                        line = line.strip('\n')
                        messages.append(line)
                        newcounter += 1
                counter += 1
            messages_length = len(messages)
            exams = []
            if messages_length == 0:
                final_message = "There are no scheduled examinations, for today."
            else:
                final_message = "There are scheduled examinations today. Please note the following exams will be taking place today: " 
                anumber = 0
                counter = 0
                examinationboard = ""
                subject = ""
                
               
                print(messages_length)
                print(messages)
                while anumber <= (messages_length-6):
                    examinationboard = (messages[anumber+3])
                    subject = (messages[anumber+6])
                    my_time = messages[anumber+2]
                    my_time = (str(sum(i*j for i, j in zip(map(int, my_time.split(':')), [60, 1, 1/60])))) + " mins"
                    setting = messages[anumber+1]
                    exams.append(examinationboard + " " + subject + " - " + setting + " - " + my_time)
                    anumber = anumber + 7
            send_mess(get_chat_id(last_update(get_updates_json(url))), final_message)
            
            if len(exams) != 0:
                print(exams)

                counter = 0
                examsmessage = ""
                examslen = len(exams)-1
                while counter != examslen + 1:
                    send_mess(get_chat_id(last_update(get_updates_json(url))), exams[counter])
                    counter += 1
            update_id += 1
    sleep(1)       

if __name__ == '__main__':  
    main()

chat_id = get_chat_id(last_update(get_updates_json(url)))

send_mess(chat_id, 'Your message goes here')


