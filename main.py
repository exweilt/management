from management_game import Player, ManagementGame, PlayerTurnData
from constants import *
from utils import fmt_dollars as d, fmt_bold as b

if __name__ == "__main__":
    mangame = ManagementGame()

    mangame.players = [
        Player("Alex", 1),
        Player("Jool", 2)
    ]
    
    while mangame.get_number_of_non_bankrupt_players() > 1:
        mangame.print_info()

        for p in mangame.get_list_of_non_bankrupt_players():
            print(f"\n{b("=====================================================")}\n")
            print(f"{b(p.name)}, its your turn!\n")

            p.print_info()

            player_turn: PlayerTurnData = {}

            print(f"\nA factory: 1 raw + {d(PRODUCTION_PRICE)} -> 1 product")
            produce_request: str = input(f"Number of factories you want to use (0-{p.get_working_factory_count()}):")
            if produce_request.isdigit():
                produce_number: int = int(produce_request)
                player_turn["request_production"] = produce_number

            print("Do you want to build a factory?")
            print(f"The factory will start operating in {b(5)} months "
                f"and will cost you {d(FACTORY_HALFPRICE)} now and {d(FACTORY_HALFPRICE)} a month before the finishing of the construction.")
            factory_build_request: str = input("(y/n): ")
            if factory_build_request.lower() == "y":
                player_turn["request_building"] = 1

            print("\nNow it's time to make the bids on the auction!")
            raw_info = mangame.get_bank_selling_info()
            good_info = mangame.get_bank_buying_info()
            print(f"Bank sells {raw_info[0]} raw materials starting at {d(raw_info[1])}.")
            print(f"Bank buys {good_info[0]} goods paying max {d(good_info[1])}.")

            # raw_num_request = input("Enter the number of raw material you are ready to buy(0-x): ")
            # raw_price_request = input("Enter the price of raw material you want to buy: ")
            try:
                raw_num_request = int(input("Raw material: how many are you ready to buy(0-x): "))
                raw_price_request = int(input("Raw material: the price you are ready to buy 1 quantity: "))
                player_turn["bid_raws"] = (raw_num_request, raw_price_request)
            except:
                pass

            try:
                product_sell_num = int(input("Product: how many do you want to sell: "))
                product_sell_price = int(input("Product: the price you want to sell 1 quantity at: "))
                player_turn["bid_products"] = (product_sell_num, product_sell_price)
            except:
                pass
            
            print(f"{b(p.name)}'s turn finished.")
            mangame.register_player_turn(p.id, player_turn)
        
    
    winner = mangame.get_list_of_non_bankrupt_players()[0]
    print(f"{winner.name} won!")