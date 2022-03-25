from telebot import TeleBot, types
import json
import datetime


TOKEN = '5251616574:AAEXDobFGmnFRc7QN0TM1IZFhAYtoPA4r2o'

bot = TeleBot(TOKEN)



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('add deal')
    item2 = types.KeyboardButton('show deals')
    item3 = types.KeyboardButton('today')
    item4 = types.KeyboardButton('relax:)')
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, "Hello, {0.first_name}! I'm easy_organizer_bot.I can help you plan your life.Just click the button".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.text == 'add deal':
        add_new_deal(message)
    elif message.text == 'show deals':
        show_all_deals(message)
    elif message.text == 'today':
        my_deals_on_date(message)
    elif message.text == 'relax:)':
        delete_all_deals_by_date(message)


def load_all_deals_from_file():
    """func for get actual tasks"""
    with open("organizer_data.json", "r") as tasks_json:
        notebook = json.load(tasks_json)
    return notebook


def get_all_notebook_str():
    notebook = load_all_deals_from_file()
    str_result = ''

    for deal_date in notebook:
        str_result += f'{deal_date}\n'
        num_deal = 1
        for deal in notebook[deal_date]:
            str_deal = f'{num_deal} {deal}'
            str_result += f'{str_deal}\n'
            num_deal += 1
        str_result += '\n'
    return str_result

@bot.message_handler(commands=['show_all_deals'])
def show_all_deals(message):
    bot.reply_to(message, text=get_all_notebook_str())

@bot.message_handler(commands=['my_deals_on_date'])
def my_deals_on_date(message):

    all_data = load_all_deals_from_file()
    date_id = datetime.date.today().strftime('%d-%m-%Y')

    if date_id not in all_data:
        bot.reply_to(message, text="date doesn't exist")
    else:
        bot.reply_to(message, str(all_data[date_id]))


def get_new_deals(message, deal_date):
    deal = message.text
    notebook = load_all_deals_from_file()
    if deal_date not in notebook:
        notebook[deal_date] = [deal, ]
    else:
        notebook[deal_date].append(deal)

    with open('organizer_data.json', 'w', encoding='utf-8') as tasks_json:
        json.dump(notebook, tasks_json, indent=4, ensure_ascii=False)

    bot.reply_to(message, text=f'Added new deal: {deal_date} - {deal}')


def get_new_date(message):
    deal_date = message.text
    bot.reply_to(message, text=f'enter what will you do on {deal_date}')
    bot.register_next_step_handler(message, get_new_deals, deal_date)

@bot.message_handler(commands=['add_new_deal'])
def add_new_deal(message):
    bot.reply_to(message, text='Hi, enter date for your deals. Example 10-12-2022')
    bot.register_next_step_handler(message, get_new_date)

def delete_all_deals(message):
    deal_date = message.text
    if len(deal_date) == len('xx-xx-xxxx'):
        notebook = load_all_deals_from_file()
        notebook.pop(deal_date)
        with open('organizer_data.json', 'w', encoding='utf-8') as tasks_json:
            json.dump(notebook, tasks_json, indent=4, ensure_ascii=False)

        bot.reply_to(message, text='successful')
    else:
        bot.send_message(message.chat.id, text='please enter date in correct format: xx-xx-xxxx')




@bot.message_handler(commands=['delete_all_deals_by_date'])
def delete_all_deals_by_date(message):
    """deleting all deals by date"""
    bot.reply_to(message, text='Enter date for deleting')
    bot.register_next_step_handler(message, delete_all_deals)




bot.polling(none_stop=True)
