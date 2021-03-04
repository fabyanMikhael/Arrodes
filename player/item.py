import json

item_list = dict()

with open("player/item_list.json") as open_file:
    item_list = json.load(open_file)

item_list['0']["icon"] = '🍎'
item_list['1']["icon"] ='🫐'

item_icon_to_name = dict()
item_icon_to_name = {item_list[key]["icon"]:key for key in item_list}

class item():
    def __init__(self, amount, name="base_name", id=-1, usable=False):
        self.amount = amount

        if str(id) in item_list:
            self.name = item_list[str(id)]["name"]
            self.icon = item_list[str(id)]["icon"]
        else: 
            self.name = "unknown item"
            self.icon = ":x:"

        self.id = id
        self.usable = bool(item_list[str(id)]["usable"])
        self.use = self.__use__
    

    def __use__(self, player, game, count=1):
        if not self.usable: return
        if hasattr(self, "use_"+self.name):
            
            result = self.__getattribute__("use_"+self.name)
            self.amount -= count
            return result(player, game, count)


    #item use-functions. in the format of "use_{item name}"

    def use_apple(self, player, game, count=1):
        self.__heal__(player,amount=2)
        return f"**[{player.name}]** healed for **2** ❤️!"


    def __heal__(self, player, amount=1):
        player.health = min(player.health + amount, player.stats["Health"])
