from management_game import Player, ManagementGame
from constants import *

if __name__ == "__main__":
    mangame = ManagementGame()

    mangame.players = [
        Player("Alex", 1),
        Player("Jool", 2)
    ]
    
    while mangame.get_number_of_non_bankrupt_players() > 1:
        mangame.print_info()

        # mangame.poll
        for p in mangame.get_list_of_non_bankrupt_players():
            print("\n=====================================================\n")
            print(f"{p.name}, its your turn!\n")

            p.print_info()

            print(f"\nA factory: 1 raw + ${PRODUCTION_PRICE} -> 1 product")
            produce_request: str = input(f"Number of factories you want to use (0-{p.get_working_factory_count()}):")
            if produce_request.isdigit():
                produce_number: int = int(produce_request)
                mangame.production_requests[p.id] = produce_number

            # assert(produce_request >= 0 and produce_request <= p.get_working_factory_count())

            # print()
            #p.print_info()

            print("Do you want to build a factory?")
            print(f"The factory will start operating in 5 months "
                "and will cost you ${FACTORY_HALFPRICE} now and ${FACTORY_HALFPRICE} a month before the finishing of the construction.")
            factory_build_request: str = input("(y/n): ")
            if factory_build_request.lower() == "y":
                mangame.building_requests[p.id] = 1

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
    
    winner = mangame.get_list_of_non_bankrupt_players()[0]
    print(f"{winner.name} won!")