from game import players
from game import bets
from game import cards
import system
import utils


def setup ():
  cards.deck_amount = max(1, int(input("1, 6, 8... Com quantos baralhos desejas jogar? ")))

  print("")


def play ():
  players_names, players_tokens = players.register_players()

  utils.print_colored("§B§rPlacar Inicial§0\n")
  system.print_stats(players_names, players_tokens)
  print("")

  round = 1
  while True:
    utils.print_colored(f"§B§rRODADA {round}§0\n")

    players_names, players_tokens, round_bets = bets.ask_bets(players_names, players_tokens)

    utils.print_colored("§B§rDANDO AS CARTAS...§0\n")

    round_cards = cards.draw_cards(players_names)
    cards_sum = cards.sum_players_cards(round_cards)

    cards.print_cards(players_names, round_cards)

    cards_round_winners = cards.get_winners(players_names, cards_sum)

    bet_round_winners = bets.get_winners(players_names, round_bets, cards_round_winners)
    
    bet_prizes = bets.get_prizes(players.get_real_players(players_names), round_bets, bet_round_winners, cards.deck_amount)

    for i in range(0, len(bet_prizes)):
      playername = players_names[i]
      prize_amount = bet_prizes[i]

      players_tokens[i] += prize_amount

      if (prize_amount > 0):
        utils.print_success(f"{playername} ganhou a aposta e recebeu {prize_amount} fichas!")

      if (prize_amount < 0):
        utils.print_danger(f"{playername} perdeu a aposta e pagou {abs(prize_amount)} fichas!")

    i = 0
    while True:
      if not i < len(players.get_real_players(players_names)):
        break
      
      if players_tokens[i] == 0:
        player_name = players_names[i]

        del players_names[i]
        del players_tokens[i]

        utils.print_warn(f"{player_name} saiu do jogo com nenhuma ficha!")
        continue

      i += 1

    if not players.has_players(players_names):
      system.game_over()

    utils.print_colored("§B§rNovo placar§0\n")
    system.print_stats(players_names, players_tokens)
    print("")
    

    round += 1


def init ():
  system.print_greetings()
  setup()
  play()

init()
