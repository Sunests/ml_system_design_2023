from Project.Chat import Manager as manager

if __name__ == '__main__':
    chat=manager.ChatManager()
    #print(chat.getProductInfo("Банан"))
    #print(chat.getProductFact("Банан"))
    print(chat.getCustomInfo("Банан", "Какова цена?"))
    #print(chat.getRandomInfo("Банан", "Какова цена?"))
