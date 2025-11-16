import subprocess
import sys
import os

# Автоматическая установка зависимостей
def install_dependencies():
    dependencies = [
        'pyTelegramBotAPI==4.19.1',
        'requests>=2.31.0'
    ]
    
    for package in dependencies:
        try:
            # Проверяем, установлен ли пакет
            if '==' in package:
                package_name = package.split('==')[0]
            else:
                package_name = package.split('>=')[0]
            
            __import__(package_name.replace('-', '_'))
            print(f"✅ {package_name} уже установлен")
        except ImportError:
            print(f"📦 Устанавливаем {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} успешно установлен")
            except subprocess.CalledProcessError as e:
                print(f"❌ Ошибка установки {package}: {e}")
                sys.exit(1)

# Устанавливаем зависимости перед импортом других модулей
install_dependencies()

# Теперь импортируем остальные модули
import telebot
import threading
import time
import random
import json
from datetime import datetime

# Токен бота
BOT_TOKEN = "8228625241:AAH0cNP6ggCLsh-8vQF2Jlc8NZCwidRzCLY"

# Создаем экземпляр бота
bot = telebot.TeleBot(BOT_TOKEN)

# Список пользователей, которые подписались на рассылку
subscribed_users = set()

# Файл для хранения данных пользователей
USER_DATA_FILE = "user_data.json"

# Cooldown для команды /claim (5 минут в секундах)
CLAIM_COOLDOWN = 300

# База данных брейнротов с шансами выпадения (в процентах)
brainrots = {
    "Ancientus Artifactus": 0.5,
    "Arpa Arpegia": 1.0,
    "Arpia Aeolia": 1.0,
    "Arpo Arpegiare": 1.0,
    "Asino Riso Umano": 2.0,
    "Ballerina Cappuccina": 2.0,
    "Ballerino Lololo": 2.0,
    "Bearorito Applepitolirotito": 0.8,
    "Begalino Kotobananino": 1.5,
    "Bicicletta Del Gatto Santo": 1.2,
    "Bombardiere Lucertola": 1.8,
    "Bombardili Gorilili": 1.8,
    "Bombardiro Crocodillo": 1.5,
    "Bombombini Gusini": 2.0,
    "Boneca Ambalabu": 1.0,
    "Bri Bri Bicus Dicus": 2.5,
    "Brr brr Patapim": 3.0,
    "Brr brr Tarflem": 3.0,
    "Bruto Gialutto (RL)": 0.7,
    "Bulbito Bandito Tractorito": 1.2,
    "Bungoletti Spaghettini": 2.0,
    "Burbaloni Luliloli": 1.8,
    "Camelrino Tazzino": 1.5,
    "Cappuccino Assassino": 0.9,
    "Capybarello Cocosini": 1.3,
    "Capo Maccheroni": 1.7,
    "Catini Monkini": 2.0,
    "Cavo Vivento": 1.1,
    "Chef Crabracadabra": 0.8,
    "Chimpanzini Bananini Priestini": 0.6,
    "Chimpanzini Bananini": 0.7,
    "Coccodrilli Faerini": 1.4,
    "Coccodrillo Formaggioso": 0.9,
    "Cocosatic Bungus": 1.2,
    "Colosseumna Gladiatoria (Do not remove will be added by 5/6/25)": 0.3,
    "Crocodilo Ananasino": 1.5,
    "Crocodildo Penisini": 0.4,
    "Crocodilo Potatino": 1.6,
    "Crocodillo Robloxino": 1.3,
    "Don Coccodrillo": 1.0,
    "Drrr Traaa Toucanni Toucannus": 1.8,
    "Ecco Cavallo Virtuoso": 1.2,
    "Emo Struzzo Paparazzi": 1.4,
    "Espressona Signora": 1.1,
    "Farlynhos Cavalinhuz": 1.3,
    "Felice Volcanino": 1.5,
    "Fishinni pelmeninni": 2.0,
    "Fishano Shoebano": 1.8,
    "Formicazzo Pazzo (RL)": 0.5,
    "Frigo Camelo": 1.6,
    "Frulli Frulla": 2.2,
    "FUTURINO Dinosino": 1.0,
    "Gambero Spero": 1.7,
    "Gattino Aereoplanino": 1.8,
    "Gatto Pizza Caffè": 1.2,
    "Giraffa Celeste": 0.8,
    "Glorbo Fruttodrillo": 1.1,
    "Gorillardo Mazzuoloni": 1.0,
    "Graipussi Medussi": 1.3,
    "Guscio Metallico": 1.4,
    "Homyakini Chupa Chupsini": 1.5,
    "Horseziano Blendorzinni": 1.2,
    "Il Ragioniere del Vuoto": 0.9,
    "Inalatore Ninja": 1.6,
    "Ingonyama Enecactus (fanat page)": 0.7,
    "La Sirena Gatto Maiale": 0.8,
    "La Cavia dei Sogni": 0.9,
    "L'Ombra Illuminata": 0.7,
    "La Vacca Saturno Saturnita": 1.0,
    "La Vacca Atomo Atomita": 1.0,
    "Lightino akulino": 1.4,
    "Linguicine Serpentine": 1.7,
    "Lirilì Larilà": 2.5,
    "Los Tralaleritos": 1.8,
    "Meozad Bombardad": 1.3,
    "Mozarella di Bufala": 1.9,
    "Nuclearo Dinosauro": 0.8,
    "Oca del Rover Lunare": 1.1,
    "Orangutini Ananasini": 1.2,
    "Porcospino Stivale": 1.6,
    "Pararell Bararell": 2.0,
    "Peneçillis Implementis": 0.6,
    "Pianononi Pianofortini (Do not remove will be added by 5/6/25)": 0.3,
    "Piccione Macchina": 1.8,
    "Pinguini Zucchini": 1.9,
    "Pizza Di Cane": 1.4,
    "Platypus Boos Boos Boos": 1.5,
    "Puppini Appleini": 1.7,
    "Purri-Purrani-Nyankani": 1.3,
    "Pipi Kiwi": 1.8,
    "Quesadilla Crocodila": 1.2,
    "Ranatone Margheritus": 1.0,
    "Rantasanta Chinaranta": 1.1,
    "Rari Rutti": 1.9,
    "Ravioli Chimpanzini": 0.9,
    "Rotoliglio Rotola Srotola Srola": 1.7,
    "Rugginato LupoGT (Il Cannone Stradale)": 0.6,
    "Rupipipipipipi Streamimimimimimi": 1.4,
    "Ruota Ruota Ruota Cavallo": 2.0,
    "Sahurpalma Naufragio": 1.1,
    "Sbam Undici: Gelatòide Risorge": 0.8,
    "Scoaittolo Crittolo": 1.6,
    "Serpentini Toiletini": 1.3,
    "Sig. Gelantulone il Managero": 1.0,
    "Sombraruote Frratatà": 1.5,
    "Spiderrino rino rino? giraffa guci guci tralalino!": 1.2,
    "Talpa Di Ferro": 1.4,
    "Tarantula Hawk Due (Tarantula Hawk Tuah)": 0.9,
    "Tartaruga Turbinata Tortellini": 1.3,
    "Telefono Smemorato": 1.7,
    "Tortitilli Mortiri": 1.1,
    "Tracotocutulo": 1.8,
    "Tralachicko Jockerito": 1.4,
    "Tralalero Tralala": 2.2,
    "Tric Trac baraboom": 2.0,
    "Trippa Troppa Tralala Lirilì Rilà Tung Tung Sahur Boneca Tung Tung Tralalelo Trippi Troppa Crocodina": 0.5,
    "Bombardiro Tralalera Brr Brr": 1.0,
    "Trippi Troppi": 1.9,
    "Trulimero Truliccina": 1.3,
    "Tigerini Chickenini": 1.6,
    "Uccelloburger": 1.8,
    "Volpo Treno": 1.2,
    "Volpolina d'Uovo": 1.4,
    "Weerachino Meksachawino": 1.1,
    "Zhuzhuli Buffo": 1.7,
    "Zweino Aeroplano": 1.5,
    "Zzz zzz Patabuma": 2.1,
    "Alphabito Dinamito": 0.8,
    "Bobreo lalipopito grande pencillo spaghetti anasasillo": 0.7,
    "Coccodrillo Formaggioso": 0.9,
    "Dangerito Bearito": 1.0,
    "Detectivni Sproutini": 1.3,
    "Homyakini Chupa Chupsini": 1.5,
    "Husitia Musitia": 1.6,
    "Kioskino Girafelelenio(IT)": 1.2,
    "Meterito Bearito": 1.0,
    "Sovieto Elephino": 0.9,
    "Kravilino Čekićino": 1.1
}

# Загрузка данных пользователей
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Сохранение данных пользователей
def save_user_data(data):
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Глобальная переменная для данных пользователей
user_data = load_user_data()

# Словарь для хранения времени последнего использования /claim
user_cooldowns = {}

# Словарь для хранения активных капч
user_captchas = {}

def generate_captcha():
    """Генерирует простую математическую капчу"""
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    operation = random.choice(['+', '-', '*'])
    
    if operation == '+':
        answer = a + b
        question = f"{a} + {b} = ?"
    elif operation == '-':
        # Убедимся, что результат не отрицательный
        a, b = max(a, b), min(a, b)
        answer = a - b
        question = f"{a} - {b} = ?"
    else:  # *
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        answer = a * b
        question = f"{a} × {b} = ?"
    
    return question, str(answer)

def is_on_cooldown(user_id):
    """Проверяет, находится ли пользователь на кулдауне"""
    if user_id in user_cooldowns:
        time_passed = time.time() - user_cooldowns[user_id]
        if time_passed < CLAIM_COOLDOWN:
            remaining = CLAIM_COOLDOWN - time_passed
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            return True, f"⏰ Подожди {minutes} минут {seconds} секунд перед следующим использованием /claim"
    return False, None

def needs_captcha(user_id):
    """Проверяет, нужна ли пользователю капча (каждые 3 выдачи)"""
    if user_id not in user_data:
        return False
    total_claims = user_data[user_id].get("total_received", 0)
    return total_claims > 0 and total_claims % 3 == 0

# ОБРАБОТЧИКИ КОМАНД ДОЛЖНЫ БЫТЬ ОБЪЯВЛЕНЫ ПЕРВЫМИ

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    
    # Автоматически выполняем команду /claim для новых пользователей
    if user_id not in user_data and message.text == '/start':
        # Создаем запись пользователя
        user_data[user_id] = {
            "inventory": {},
            "total_received": 0,
            "rare_count": 0,
            "last_claim": None
        }
        save_user_data(user_data)
        
        # Выполняем автоматический claim
        process_claim(message)
    else:
        # Показываем приветственное сообщение или помощь
        bot.reply_to(message, 
                    "🧠 *Brainrot Bot - Помощь*\n\n"
                    "*Основные команды:*\n"
                    "/claim - получить случайный брейнрот (раз в 5 минут)\n"
                    "/inventory - посмотреть свой инвентарь\n"
                    "/stats - ваша персональная статистика\n"
                    "/top - топ коллекционеров по уникальным брейнротам\n\n"
                    "*О боте:*\n"
                    "• Собирай уникальные брейнроты\n"
                    "• Шансы выпадения от 0.3% до 3%\n"
                    "• Каждые 3 получения - капча для защиты\n"
                    "• Соревнуйся с другими коллекционерами!\n\n"
                    "🎯 *Всего доступно брейнротов:* " + str(len(brainrots)), 
                    parse_mode='Markdown')

@bot.message_handler(commands=['claim'])
def claim_brainrot(message):
    process_claim(message)

@bot.message_handler(commands=['inventory', 'inv'])
def show_inventory(message):
    user_id = str(message.from_user.id)
    
    if user_id not in user_data or not user_data[user_id]["inventory"]:
        bot.reply_to(message, "📭 Твой инвентарь пуст! Используй /claim чтобы получить первый брейнрот.")
        return
    
    inventory = user_data[user_id]["inventory"]
    total_items = sum(inventory.values())
    unique_items = len(inventory)
    
    # Сортируем по редкости (шансу выпадения)
    sorted_items = sorted(inventory.items(), key=lambda x: brainrots.get(x[0], 100))
    
    response = f"🎒 *Твой инвентарь*\n\n"
    response += f"📊 Всего предметов: {total_items}\n"
    response += f"🎯 Уникальных: {unique_items}/{len(brainrots)}\n"
    response += f"📈 Завершено: {unique_items/len(brainrots)*100:.1f}%\n\n"
    
    # Показываем первые 15 предметов
    for i, (item, count) in enumerate(sorted_items[:15], 1):
        chance = brainrots.get(item, "N/A")
        rarity_icon = "⚡" if chance < 1.0 else "📦"
        response += f"{rarity_icon} {item} - x{count} ({chance}%)\n"
    
    if len(sorted_items) > 15:
        response += f"\n... и еще {len(sorted_items) - 15} предметов"
    
    response += f"\n\nИспользуй /stats для подробной статистики"
    
    bot.reply_to(message, response, parse_mode='Markdown')

@bot.message_handler(commands=['stats', 'stat'])
def show_stats(message):
    user_id = str(message.from_user.id)
    
    if user_id not in user_data:
        bot.reply_to(message, "У тебя еще нет статистики! Используй /claim чтобы начать коллекцию.")
        return
    
    user_stats = user_data[user_id]
    inventory = user_stats["inventory"]
    total_items = sum(inventory.values())
    unique_items = len(inventory)
    
    # Находим самые редкие предметы
    rare_items = [(item, count) for item, count in inventory.items() if brainrots.get(item, 100) < 1.0]
    rare_count = len(rare_items)
    
    # Самый частый предмет
    most_common = max(inventory.items(), key=lambda x: x[1]) if inventory else ("Нет", 0)
    # Самый редкий предмет
    rarest_item = min(inventory.items(), key=lambda x: brainrots.get(x[0], 100)) if inventory else ("Нет", 0)
    
    response = f"📊 *Твоя статистика*\n\n"
    response += f"🎒 Всего брейнротов: {total_items}\n"
    response += f"🎯 Уникальных: {unique_items}/{len(brainrots)}\n"
    response += f"⚡ Редких: {rare_count}\n"
    response += f"📈 Завершено: {unique_items/len(brainrots)*100:.1f}%\n\n"
    
    if rare_items:
        response += f"*Твои самые редкие брейнроты:*\n"
        # Сортируем по редкости (шансу)
        rare_items_sorted = sorted(rare_items, key=lambda x: brainrots.get(x[0], 100))
        for item, count in rare_items_sorted[:5]:
            chance = brainrots[item]
            response += f"⚡ {item} - x{count} ({chance}%)\n"
    
    response += f"\n*Самый частый:* {most_common[0]} - x{most_common[1]}"
    if rarest_item[0] != "Нет":
        rarest_chance = brainrots.get(rarest_item[0], "N/A")
        response += f"\n*Самый редкий:* {rarest_item[0]} - x{rarest_item[1]} ({rarest_chance}%)"
    
    bot.reply_to(message, response, parse_mode='Markdown')

@bot.message_handler(commands=['top', 'leaderboard'])
def show_top(message):
    if not user_data:
        bot.reply_to(message, "📊 Пока нет данных для топа! Будь первым - используй /claim")
        return
    
    # Сортируем пользователей по количеству уникальных предметов
    top_users = []
    for user_id, data in user_data.items():
        unique_count = len(data["inventory"])
        total_count = sum(data["inventory"].values())
        rare_count = len([item for item in data["inventory"] if brainrots.get(item, 100) < 1.0])
        top_users.append((user_id, unique_count, total_count, rare_count))
    
    top_users.sort(key=lambda x: (x[1], x[3], x[2]), reverse=True)
    
    response = "🏆 *Топ коллекционеров*\n\n"
    
    for i, (user_id, unique_count, total_count, rare_count) in enumerate(top_users[:10], 1):
        try:
            user = bot.get_chat(int(user_id))
            username = f"@{user.username}" if user.username else user.first_name
        except:
            username = f"Пользователь {user_id[:8]}..."
        
        medal = ""
        if i == 1: medal = "🥇"
        elif i == 2: medal = "🥈" 
        elif i == 3: medal = "🥉"
        
        response += f"{medal} *{i}. {username}*\n"
        response += f"   🎯 Уникальных: {unique_count} | 📦 Всего: {total_count} | ⚡ Редких: {rare_count}\n\n"
    
    response += f"Всего коллекционеров: {len(top_users)}"
    bot.reply_to(message, response, parse_mode='Markdown')

# ОБЩИЙ ОБРАБОТЧИК ДОЛЖЕН БЫТЬ ПОСЛЕДНИМ
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Обработчик всех сообщений (капча и текстовые команды)"""
    user_id = str(message.from_user.id)
    text = message.text.strip().lower()
    
    # Обработка капчи
    if user_id in user_captchas:
        correct_answer = user_captchas[user_id]
        if text == correct_answer:
            # Капча пройдена, выдаем брейнрот
            del user_captchas[user_id]
            give_brainrot(user_id, message.chat.id)
        else:
            # Неправильный ответ, новая капча
            question, answer = generate_captcha()
            user_captchas[user_id] = answer
            bot.reply_to(message,
                        f"❌ *Неправильный ответ!*\n\n"
                        f"Попробуй еще раз:\n`{question}`",
                        parse_mode='Markdown')
        return
    
    # Обработка текстовых команд
    if text in ['brainrot', 'брейнрот', 'мозг', 'brain', 'брейн', 'инвентарь']:
        brainrot = get_random_brainrot()
        user_id = str(message.from_user.id)
        add_to_inventory(user_id, brainrot)
        
        chance = brainrots[brainrot]
        rarity = "⚡ РЕДКИЙ" if chance < 1.0 else "📦 ОБЫЧНЫЙ"
        
        bot.reply_to(message, 
                    f"🧠 {brainrot}\n"
                    f"*Редкость:* {rarity}\n"
                    f"*Шанс:* {chance}%\n\n"
                    f"Добавлено в инвентарь! 📥", 
                    parse_mode='Markdown')

def process_claim(message):
    """Обрабатывает запрос на получение брейнрота"""
    user_id = str(message.from_user.id)
    
    # Проверяем кулдаун
    cooldown, cooldown_message = is_on_cooldown(user_id)
    if cooldown:
        bot.reply_to(message, cooldown_message)
        return
    
    # Проверяем, нужна ли капча
    if needs_captcha(user_id) and user_id not in user_captchas:
        question, answer = generate_captcha()
        user_captchas[user_id] = answer
        bot.reply_to(message, 
                    f"🔒 *Требуется проверка*\n\n"
                    f"Реши пример:\n`{question}`\n\n"
                    f"Отправь ответ числом в чат",
                    parse_mode='Markdown')
        return
    
    # Выдаем брейнрот
    give_brainrot(user_id, message.chat.id)

def give_brainrot(user_id, chat_id):
    """Выдает брейнрот пользователю"""
    brainrot = get_random_brainrot()
    add_to_inventory(user_id, brainrot)
    
    # Обновляем время последнего использования
    user_cooldowns[user_id] = time.time()
    
    rarity = "⚡ РЕДКИЙ" if brainrots[brainrot] < 1.0 else "📦 ОБЫЧНЫЙ"
    chance = brainrots[brainrot]
    
    response = (f"🧠 *Новый брейнрот!*\n\n"
               f"*{brainrot}*\n"
               f"*Редкость:* {rarity}\n"
               f"*Шанс выпадения:* {chance}%\n\n"
               f"Добавлено в твой инвентарь! 📥\n\n"
               f"⏰ Следующий /claim через 5 минут")
    
    bot.send_message(chat_id, response, parse_mode='Markdown')

def get_random_brainrot():
    """Возвращает случайный брейнрот с учетом шансов"""
    items = list(brainrots.keys())
    chances = list(brainrots.values())
    
    # Нормализуем шансы
    total = sum(chances)
    normalized_chances = [chance/total for chance in chances]
    
    return random.choices(items, weights=normalized_chances)[0]

def add_to_inventory(user_id, brainrot):
    """Добавляет брейнрот в инвентарь пользователя"""
    if user_id not in user_data:
        user_data[user_id] = {
            "inventory": {},
            "total_received": 0,
            "rare_count": 0
        }
    
    if brainrot not in user_data[user_id]["inventory"]:
        user_data[user_id]["inventory"][brainrot] = 0
    
    user_data[user_id]["inventory"][brainrot] += 1
    user_data[user_id]["total_received"] += 1
    
    # Увеличиваем счетчик редких, если предмет редкий
    if brainrots.get(brainrot, 100) < 1.0:
        user_data[user_id]["rare_count"] = user_data[user_id].get("rare_count", 0) + 1
    
    save_user_data(user_data)

def send_brainrot_to_all():
    """Отправляет брейнрот всем подписанным пользователям"""
    if subscribed_users:
        brainrot = get_random_brainrot()
        for user_id in list(subscribed_users):
            try:
                add_to_inventory(user_id, brainrot)
                
                chance = brainrots[brainrot]
                rarity = "⚡ РЕДКИЙ" if chance < 1.0 else "📦 ОБЫЧНЫЙ"
                
                bot.send_message(
                    user_id, 
                    f"🧠 *Новый брейнрот!* 🧠\n\n"
                    f"*{brainrot}*\n"
                    f"*Редкость:* {rarity}\n"
                    f"*Шанс выпадения:* {chance}%\n\n"
                    f"_Следующий через 5 минут..._\n"
                    f"Используй /inventory чтобы посмотреть коллекцию",
                    parse_mode='Markdown'
                )
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
                subscribed_users.discard(user_id)

def brainrot_scheduler():
    """Планировщик для отправки брейнротов каждые 5 минут"""
    while True:
        try:
            send_brainrot_to_all()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Отправлен брейнрот {len(subscribed_users)} пользователям")
        except Exception as e:
            print(f"Ошибка при отправке брейнротов: {e}")
        
        time.sleep(300)

# Запускаем планировщик в отдельном потоке
def start_scheduler():
    scheduler_thread = threading.Thread(target=brainrot_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

if __name__ == "__main__":
    print("=" * 50)
    print("🧠 Brainrot Bot запускается...")
    print("=" * 50)
    print(f"Загружено {len(brainrots)} брейнротов с разными шансами выпадения")
    print(f"Загружено данных {len(user_data)} пользователей")
    print("Бот готов к работе...")
    print("=" * 50)
    
    start_scheduler()
    
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ Ошибка при работе бота: {e}")
