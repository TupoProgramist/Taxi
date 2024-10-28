import telebot

# Telegram Bot Setup
bot_token = "8154426002:AAGudt3_gELhdDGbStcQ7GJseSgu_seEJOw"
bot = telebot.TeleBot(bot_token)

# Main menu command
@bot.message_handler(commands=['main_menu'])
def handle_main_menu(message):
    user_id = message.chat.id
    session.query(UserOpportunity).filter_by(user_id=user_id).delete()  # Delete all opportunities related to the user
    session.commit()
    bot.send_message(user_id, "All opportunities removed. You're now in the main menu.")

# Give opportunity command
@bot.message_handler(commands=['give_opportunity'])
def handle_give_opportunity(message):
    user_id = message.chat.id
    user_opp = session.query(UserOpportunity).filter_by(user_id=user_id).order_by(UserOpportunity.rating.desc()).first()

    if user_opp:
        opp = session.query(Opportunity).filter_by(opportunity_id=user_opp.opportunity_id).first()
        if opp:
            bot.send_message(user_id, f"Opportunity: {opp.keyword}")
            session.delete(user_opp)  # Remove the used opportunity
            session.commit()
        else:
            bot.send_message(user_id, "Opportunity not found.")
    else:
        bot.send_message(user_id, "No opportunities left. You're now in the main menu.")

# Start bot polling
bot.polling()
