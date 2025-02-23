from math import floor

class ManagementGame:
    def __init__(self):
        self.players: list[Player] = []
        self.month = 1
        self.economy_level: int = 3
        self.raw_bids = {}            # Player id to Tuple (quantity, price)
        self.product_bids = {}        # Player id to Tuple (quantity, price)
        self.production_requests = {} # Player id to number of factories producing
        self.building_requests = {}   # Player id to number of factories constructions initiated
        
    def print_info(self):
        print(f"\nMonth {self.month}")
        raw_info = self.get_bank_selling_info()
        good_info = self.get_bank_buying_info()
        print(f"Bank sells {raw_info[0]} raw materials starting at ${raw_info[1]}.")
        print(f"Bank buys {good_info[0]} goods paying max ${good_info[1]}.\n")

    def get_number_of_non_bankrupt_players(self) -> int:
        return len(list(filter(lambda p : p.money > 0, self.players)))
    
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
        bids: dict = self.raw_bids.copy()

        while raws_to_sell > 0:
            if len(bids) == 0:
                break

            # Whoose deal to fulfill
            best_player_id = max(bids, key=lambda p_id: bids[p_id][1])
            best_player = self.get_player_by_id(best_player_id)

            # Define the quantity of the sold to the player
            sold: int = 0
            if bids[best_player_id][0] <= raws_to_sell:
                sold = bids[best_player_id][0]
            else:
                sold = raws_to_sell
            
            # Collect payment
            best_player.money -= sold * bids[best_player_id][1]
            # Give raws to the player
            best_player.raw += sold

            print(f"(Bank) {sold} raws -> {
                    best_player.name
                } for ${ sold * bids[best_player_id][1] } (${bids[best_player_id][1]} each)")
            
            raws_to_sell -= sold
            bids.pop(best_player_id)

    def buy_goods(self):
        goods_to_buy = self.get_bank_buying_info()[0]
        bids: dict = self.product_bids.copy()

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

            print(f"({best_player.name}) {bought} goods -> (Bank) for "
                f"${ bought * bids[best_player_id][1] } (${bids[best_player_id][1]} each)")
            
            goods_to_buy -= bought
            bids.pop(best_player_id)


    def finish_month(self):
        print(f"\nMonth {self.month} end results:\n")

        raw_info = self.get_bank_selling_info()
        good_info = self.get_bank_buying_info()

        print(f"Bank was going to sell {raw_info[0]} raws starting at ${raw_info[1]}")
        print(f"\nBids were:\n====================")
        for _, (player_id, bid) in enumerate(self.raw_bids.items()):
            print(f"{self.get_player_by_id(player_id).name} wants to buy {bid[0]} raws for ${bid[1]} each")
        print("====================\n")

        self.sell_raws()

        print(f"\nBank is looking to buy {good_info[0]} goods paying max ${good_info[1]} per each.\n")
        print(f"\nBids were:\n====================")
        for _, (player_id, bid) in enumerate(self.product_bids.items()):
            print(f"{self.get_player_by_id(player_id).name} wants to sell {bid[0]} goods for ${bid[1]} each")
        print("====================\n")

        self.buy_goods()
        
        print(f"\nMonth {self.month} finished!\n")

    def get_player_by_id(self, id: int) -> "Player":
        return next((p for p in self.players if p.id == id), None)

class Player:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.money = 10000
        self.raw = 4
        self.product = 2
        # size of the list = number of factories. Each factory time to be built is number in the list
        self.factories: list[int] = [0, 0]
    
    def get_working_factory_count(self) -> int:
        return len(list(filter(lambda f : f <= 0, self.factories)))
    
    def print_info(self):
        print("You have:")
        print(f"{self.get_working_factory_count()} active factories")
        print(f"${self.money} dollars")
        print(f"{self.raw} raw materials")
        print(f"{self.product} goods")


if __name__ == "__main__":
    mangame = ManagementGame()

    mangame.players = [
        Player("Alex", 1),
        Player("Jool", 2)
    ]

    mangame.print_info()

    # mangame.poll
    for p in mangame.players:
        print("\n\n=====================================================\n")
        print(f"{p.name}, its your turn!\n")

        p.print_info()

        print("\nA factory can produce 1 goods, using 1 raw material and $2000.")
        produce_request = input(f"How many factories do you want to produce goods (0-{p.get_working_factory_count()}):")
        
        # assert(produce_request >= 0 and produce_request <= p.get_working_factory_count())

        # print()
        p.print_info()

        print("\nWould you like to build a factory?")
        print("The factory will start operating in 5 months "
            "and will cost you $2500 now and $2500 a month before the finishing of the construction.")
        factory_build_request = input("(y/n): ")

        print("\nNow it's time to make the bids on the auction!")
        raw_info = mangame.get_bank_selling_info()
        good_info = mangame.get_bank_buying_info()
        print(f"Bank sells {raw_info[0]} raw materials starting at ${raw_info[1]}.")
        print(f"Bank buys {good_info[0]} goods paying max ${good_info[1]}.")

        # raw_num_request = input("Enter the number of raw material you are ready to buy(0-x): ")
        # raw_price_request = input("Enter the price of raw material you want to buy: ")
        try:
            raw_num_request = int(input("Raw material, how many are you ready to buy(0-x): "))
            raw_price_request = int(input("Raw material, the price you are ready to buy 1 quantity: "))
            mangame.raw_bids[p.id] = (raw_num_request, raw_price_request)
        except:
            pass

        try:
            product_sell_num = int(input("Product, how many do you want to sell: "))
            product_sell_price = int(input("Product, the price you want to sell 1 quantity at: "))
            mangame.product_bids[p.id] = (product_sell_num, product_sell_price)
        except:
            pass

        print("Turn finished.")

    mangame.finish_month()