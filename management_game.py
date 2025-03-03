from math import floor
from constants import *
from utils import fmt_dollars as d, fmt_bold as b
from typing import TypedDict

class ManagementGame:
    def __init__(self):
        self.players: list[Player] = []
        self.month = 1
        self.economy_level: int = 3
        # self.raw_bids = {}            # Player id to Tuple (quantity, price)
        # self.product_bids = {}        # Player id to Tuple (quantity, price)
        # self.production_requests = {} # Player id to number of factories producing
        # self.building_requests = {}   # Player id to number of factories constructions initiated
        self.player_turns: dict[int, "PlayerTurnData"] = {}
        self.out = ""

    def to_dict(self):
        return {
            "players": [p.to_dict() for p in self.players],
            "month": self.month,
            "economy_level": self.economy_level,
            "player_turns": self.player_turns,
            "out": self.out
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        game = cls()
        game.players = [Player.from_dict(p) for p in data["players"]]
        game.month = data["month"]
        game.economy_level = data["economy_level"]
        game.player_turns = data["player_turns"]
        game.out = data["out"]

        return game
        
    def print_info(self):
        print(f"\n {b(f"=== Month {self.month} ===")}\n")

        raw_info = self.get_bank_selling_info()
        good_info = self.get_bank_buying_info()
        print(f"Economy level: {b(self.economy_level)}")
        print(f"Bank sells {raw_info[0]} raw materials starting at {d(raw_info[1])}.")
        print(f"Bank buys {good_info[0]} goods paying max {d(good_info[1])}.\n")

        print(b("===== Player info ====="))
        for player in self.players:
            print(f"{b(player.name)} has")
            print(f"{player.get_working_factory_count()} active factories")
            print(f"{d(player.money)} credits")
            print(f"{player.raw} raw materials")
            print(f"{player.product} products")
            for f in player.get_list_of_unfinished_factories():
                print(f"A factory will be ready in {f} months.")
            print()
        print("======================")

    def get_info(self):
        result = ""
        result += f"\n {b(f"=== Month {self.month} ===")}\n\n"

        raw_info = self.get_bank_selling_info()
        good_info = self.get_bank_buying_info()
        result += f"Economy level: {b(self.economy_level)}\n"
        result += f"Bank sells {raw_info[0]} raw materials starting at {d(raw_info[1])}.\n"
        result += f"Bank buys {good_info[0]} goods paying max {d(good_info[1])}.\n\n"

        result += b("===== Player info =====\n")
        for player in self.players:
            result += f"{b(player.name)} has\n"
            result += f"{player.get_working_factory_count()} active factories\n"
            result += f"{d(player.money)} credits\n"
            result += f"{player.raw} raw materials\n"
            result += f"{player.product} products\n"
            for f in player.get_list_of_unfinished_factories():
                result += f"A factory will be ready in {f} months.\n"
            result += "\n"
        result += "======================\n"

        return result

    def get_number_of_non_bankrupt_players(self) -> int:
        return len(self.get_list_of_non_bankrupt_players())
    
    def get_list_of_non_bankrupt_players(self) -> list["Player"]:
        return list(filter(lambda p : p.money > 0, self.players))
    
    def get_bank_selling_info(self) -> tuple[int, int]:
        """
        Returns (max_raw_bank_sells, min_price_bank_sells_raw_at)
        """
        match self.economy_level:
            case 1: return (floor(1.0*self.get_number_of_non_bankrupt_players()), 800)
            case 2: return (floor(1.5*self.get_number_of_non_bankrupt_players()), 650)
            case 3: return (floor(2.0*self.get_number_of_non_bankrupt_players()), 500)
            case 4: return (floor(2.5*self.get_number_of_non_bankrupt_players()), 400)
            case 5: return (floor(3.0*self.get_number_of_non_bankrupt_players()), 300)

    def get_bank_buying_info(self) -> tuple[int, int]:
        """
        Returns (max_goods_bank_buys, max_price_bank_buys_good_at)
        """
        match self.economy_level:
            case 1: return (floor(3.0*self.get_number_of_non_bankrupt_players()), 6500)
            case 2: return (floor(2.5*self.get_number_of_non_bankrupt_players()), 6000)
            case 3: return (floor(2.0*self.get_number_of_non_bankrupt_players()), 5500)
            case 4: return (floor(1.5*self.get_number_of_non_bankrupt_players()), 5000)
            case 5: return (floor(1.0*self.get_number_of_non_bankrupt_players()), 4500)
    
    def sell_raws(self):
        raws_to_sell = self.get_bank_selling_info()[0]
        bids = {p_id : turn["bid_raws"] for (p_id, turn) in self.player_turns.items() if "bid_raws" in turn}

        while raws_to_sell > 0:
            if len(bids) == 0:
                break

            # Whoose deal to fulfill
            best_player_id = max(bids, key=lambda p_id: bids[p_id][1])
            best_player = self.get_player_by_id(best_player_id)

            one_raw_price = bids[best_player_id][1]

            # Define the quantity of the sold to the player
            sold: int = min(bids[best_player_id][0], raws_to_sell)
            sold = min(sold, best_player.money // one_raw_price) 
            
            # Collect payment
            best_player.money -= sold * one_raw_price
            # Give raws to the player
            best_player.raw += sold

            self.out += f"(Bank) {sold} raws -> {
                    best_player.name
                } for { d(sold * one_raw_price) } ({d(one_raw_price)} each)\n"
            
            raws_to_sell -= sold
            bids.pop(best_player_id)

    def buy_goods(self):
        goods_to_buy = self.get_bank_buying_info()[0]
        bids: dict = {p_id : turn["bid_products"] for (p_id, turn) in self.player_turns.items() if "bid_products" in turn}

        while goods_to_buy > 0:
            if len(bids) == 0:
                break

            # Whoose deal to fulfill
            best_player_id = min(bids, key=lambda p_id: bids[p_id][1])
            best_player = self.get_player_by_id(best_player_id)
            
            # Define the quantity of the bought from the player
            bought: int = 0
            if bids[best_player_id][0] <= goods_to_buy:
                bought = bids[best_player_id][0]
            else:
                bought = goods_to_buy
            
            # Collect goods
            best_player.product -= bought
            # Pay money
            best_player.money += bought * bids[best_player_id][1]

            self.out += (f"({best_player.name}) {bought} goods -> (Bank) for "
                f"{ d(bought * bids[best_player_id][1]) } ({d(bids[best_player_id][1])} each)\n")
            
            goods_to_buy -= bought
            bids.pop(best_player_id)
    
    def handle_production_orders(self):
        self.out += b("=== Processing production orders ===") + "\n"
        production_requests = [(p_id, turn["request_production"]) for (p_id, turn) in self.player_turns.items() if "request_production" in turn]
        for p_id, prod_num in production_requests:
            player = self.get_player_by_id(p_id)
            prod_num = min(prod_num, player.get_working_factory_count())

            max_possible_order = max(0, player.money // PRODUCTION_PRICE)
            max_possible_order = min(max_possible_order, player.raw)

            actual_n = min(prod_num, max_possible_order)

            player.money -= actual_n * PRODUCTION_PRICE
            player.raw -= actual_n
            player.product += actual_n

            if actual_n >= prod_num:
                self.out += f"{player.name} produces {prod_num} products (-{d(PRODUCTION_PRICE*prod_num)}) (-{prod_num} raws)\n"
            else:
                self.out += (
                    f"{player.name} ordered production of {prod_num} products but only able "
                    f"to produce {actual_n} (-{d(PRODUCTION_PRICE*actual_n)}) (-{actual_n} raws)\n"
                )
        self.out += "=== Finished production ============\n\n"


    def finish_month(self):
        self.out = b("\n=======================================") + "\n"
        self.out += f"\nMonth {b(self.month)} end results:\n\n"

        raw_info = self.get_bank_selling_info()
        good_info = self.get_bank_buying_info()

        self.out += f"Bank was going to sell {raw_info[0]} raws starting at {d(raw_info[1])}\n"
        self.out += f"Bids were:\n=====================================\n"
        x = [ (p_id, turn["bid_raws"]) for (p_id, turn) in self.player_turns.items() if "bid_raws" in turn ]
        for player_id, bid in x:
            self.out += f"{self.get_player_by_id(player_id).name} wants to buy {bid[0]} raws for {d(bid[1])} each\n\n"
        self.out += "=====================================\n\n"

        self.sell_raws()

        self.out += "====================================\n"
        self.out += f"\nBank is looking to buy {good_info[0]} goods paying max {d(good_info[1])} per each.\n"
        self.out += f"\nBids were:\n====================\n"
        for player_id, bid in [ (p_id, turn["bid_products"]) for (p_id, turn) in self.player_turns.items() if "bid_products" in turn ]:
            self.out += f"{self.get_player_by_id(player_id).name} wants to sell {bid[0]} goods for {d(bid[1])} each\n"
        self.out += "====================\n\n"

        self.buy_goods()

        self.out += "===============================\n"
        self.order_factories()

        self.out += "\n"
        self.handle_production_orders()

        # Reset orders
        self.player_turns.clear()

        # Players pay expenses
        self.handle_expenses()

        self.out += f"\nMonth {self.month} finished!\n\n"
        self.month += 1


    def get_player_by_id(self, id: int) -> "Player":
        return next((p for p in self.players if p.id == id), None)

    def order_factories(self):
        self.out += b("=== Ordering Building Factories ===") + "\n"
        building_requests = [ (p_id, turn["request_building"]) for (p_id, turn) in self.player_turns.items() if "request_building" in turn ]
        for p_id, factory_number in building_requests:
            player = self.get_player_by_id(p_id)

            if player.money >= FACTORY_HALFPRICE:
                player.factories.append(5)
                player.money -= FACTORY_HALFPRICE
                self.out += f"{player.name} ordered a factory construction (-{d(FACTORY_HALFPRICE)})\n"
            else:
                self.out += f"{player.name} asked for factory construction but had not enough funds (only ${player.money})\n"
        self.out += "=== Factories have been ordered ===\n"

    def handle_expenses(self) -> None:
        self.out += b("=== Paying Expenses ===\n")
        nonbankrupts_before_paying = self.get_list_of_non_bankrupt_players()
        for idx, p in enumerate(nonbankrupts_before_paying):
            original_money = p.money
            expenses_str: str = ""

            if p.raw > 0:
                raws_expense = p.raw * EXPENSE_RAW
                p.money -= raws_expense
                expenses_str += f"Raw materials storage: -{d(raws_expense)} = {p.raw}pc * {d(EXPENSE_RAW)}\n"
            
            if p.product > 0:
                products_expense = p.product * EXPENSE_PRODUCT
                p.money -= products_expense
                expenses_str += f"Products storage: -{d(products_expense)} = {p.product}pc * {d(EXPENSE_PRODUCT)}\n"

            if p.get_working_factory_count() > 0:
                factory_n = p.get_working_factory_count()
                factory_expense = factory_n * EXPENSE_FACTORY
                p.money -= factory_expense
                expenses_str += f"Factories maintenance: -{d(factory_expense)} = {factory_n}pc * {d(EXPENSE_FACTORY)}"
            
            self.out += f"{p.name}: {d(original_money)} -> {d(p.money)}\n"
            self.out += f"Total: {d(-original_money + p.money)}\n"
            self.out += expenses_str + "\n"
            if idx == len(nonbankrupts_before_paying) - 1:
                self.out += "\n" # Player separator
            self.out += "=== Expenses paid ===\n"
    
    def register_player_turn(self, p_id: int, turn_data: "PlayerTurnData") -> None:
        self.player_turns[p_id] = turn_data

        players_who_didnt_turn = [p for p in self.players if (p.id not in self.player_turns)]
        
        if len(players_who_didnt_turn) == 0:
            self.finish_month()

class Player:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.money = 10000
        self.raw = 4
        self.product = 2
        # size of the list = number of factories. Each factory time to be built is number in the list
        self.factories: list[int] = [0, 0]

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "money": self.money,
            "raw": self.raw,
            "product": self.product,
            "factories": self.factories
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        p = cls(data["name"], data["id"])
        p.money = data["money"]
        p.raw = data["raw"]
        p.product = data["product"]
        p.factories = data["factories"]
        
        return p
    
    def get_working_factory_count(self) -> int:
        return len(list(filter(lambda f : f <= 0, self.factories)))
    
    def get_list_of_unfinished_factories(self) -> list[int]:
        return list(filter(lambda f : f >= 1, self.factories))
    
    def print_info(self):
        print("You have:")
        print(f"{self.get_working_factory_count()} active factories")
        print(f"{d(self.money)} dollars")
        print(f"{b(self.raw)} raw materials")
        print(f"{self.product} goods")
    
    def __repr__(self):
        return f"{self.name}:{self.id} {d(self.money)}"

class PlayerTurnData(TypedDict):
    bid_raws: tuple[int, int]           # (number, price_for_each)
    bid_products: tuple[int, int]       # (number, price_for_each)
    request_building: int               # Number of factories to build
    request_production: int             # Produce using n factories

    # @staticmethod
    # def to_dict(cls, data: "PlayerTurnData"):
    #     return {
    #         "bid_raws": data.bid_raws,
    #         "bid_products": data.bid_products,
    #         "request_building": data.request_building,
    #         "request_production": data.request
    #     }

# class Message(TypedDict):
#     bid_raws: tuple[int, int]           # (number, price_for_each)
#     bid_products: tuple[int, int]       # (number, price_for_each)
#     request_building: int               # Number of factories to build
#     request_production: int             # Produce using n factories