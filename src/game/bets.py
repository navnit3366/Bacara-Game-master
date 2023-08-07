from . import players
import system
import utils


house_comissions = ((1.29, 1.01, 15.75), (1.24, 1.06, 14.44), (1.24, 1.06, 14.36))


def get_bets ():
  return bets

def get_players_bets ():
  return bets[:-1]


def ask_bet_bid (input_message, player_tokens):
  while True:
    bet_bid_input = input(utils.colored(input_message))

    if bet_bid_input:
      bet_bid = int(bet_bid_input)

      if bet_bid < 0 or bet_bid > player_tokens:
        utils.print_colored("§0Não é possível apostar essa quantia!")

      else:
        return bet_bid

    else:
      return False
  

def get_betting_players (players_list, tokens, bets):
  betting_players = []
  betting_tokens = []
  betting_bet = []

  for i in range(0, len(players_list)):
    player_name = players_list[i]

    if bets[i] or player_name == "Banco":
      betting_players.append(player_name)
      betting_tokens.append(tokens[i])
      betting_bet.append(bets[i])

  return (betting_players, betting_tokens, betting_bet)


def ask_bets (players_names, players_tokens):
  players_names_tokens = list(zip(players_names, players_tokens))
  players_bets = []
  leavers = []

  for player_name_tokens in players.get_real_players(players_names_tokens):
    playername, tokens = player_name_tokens

    player_bet = []

    bet_bid = ask_bet_bid(f"§0Quanto você aposta nesta rodada, {playername}? (Ou saia sem apostar) §g", tokens)

    if bet_bid:
      player_bet.append(bet_bid)

      while True:
        bet_what = input(utils.colored(f"§0Jogador, banco ou empate. Em que você aposta {bet_bid} fichas, {playername}? §b"))
        bet_what_lower = bet_what.lower()

        if bet_what_lower in ["jogador", "j"]:
          player_bet.append("player")

          while True:
            bet_who = input(utils.colored(f"§0Em qual jogador você aposta {bet_bid} fichas, {playername}? §y"))

            bet_player = players.get_playername(bet_who, players_names)
            bet_leaver = players.get_playername(bet_who, leavers)

            if bet_player and not bet_leaver and bet_who.lower() != playername.lower():
              player_bet.append(bet_player)
              utils.print_success(f"{playername} apostou {bet_bid} fichas em {bet_player}!")
              break

            else:
              utils.print_colored("§0Não é possível apostar nesse jogador!")

          break

        elif bet_what_lower in ["banco", "b"]:
          player_bet.append("bank")
          utils.print_success(f"{playername} apostou {bet_bid} fichas no Banco!")
          break

        elif bet_what_lower in ["empate", "e"]:
          player_bet.append("tie")
          utils.print_success(f"{playername} apostou {bet_bid} fichas por um empate no jogo!")
          break

        else:
          utils.print_colored("§0Não é possível realizar esse tipo de aposta!")

    else:
      leavers.append(playername)
      utils.print_info(f"{playername} saiu do jogo com {tokens} fichas!")

    players_bets.append(player_bet)

  # Bank bet
  players_bets.append([])

  # Update players, removing who didn't bet
  players_names, players_tokens, players_bets = get_betting_players(players_names, players_tokens, players_bets)

  if not players.has_players(players_names):
    system.game_over()

  return (players_names, players_tokens, players_bets)


def get_winners (players_list, players_bets, cards_winners):
  real_players_list = players.get_real_players(players_list)
  
  players_names_bets = list(zip(real_players_list, players_bets))
  players_names_wins = list(zip(players_list, cards_winners))

  winners = []

  for player_name_bet in players_names_bets:
    player_name, player_bet = player_name_bet
    
    bet_amount = player_bet[0]
    bet_type = player_bet[1]

    if bet_type == "player" or bet_type == "bank":
      if bet_type == "player":
        bet_target = player_bet[2]

      if bet_type == "bank":
        bet_target = "Banco"
      
      target_wins = True
      
      for player_name_win in players_names_wins:
        winner_name, player_wins = player_name_win
        
        if player_wins and winner_name != bet_target:
          target_wins = False
      
      winners.append(target_wins)

    elif bet_type == "tie":
      card_winner_count = 0

      for winner in cards_winners:
        if winner:
          card_winner_count += 1

      is_winner = card_winner_count > 1

      winners.append(is_winner)

  return winners


def get_prizes (player_names, player_bets, bet_winners, deck_amount):
  if deck_amount < 6:
    house_comission_index = 0
  elif deck_amount < 8:
    house_comission_index = 1
  else:
    house_comission_index = 2

  house_comission = house_comissions[house_comission_index]

  prizes = []

  for i in range(0, len(player_names)):
    player_name = player_names[i]
    player_bet = player_bets[i]
    bet_amount = player_bet[0]
    bet_type = player_bet[1]
    player_wins = bet_winners[i]

    if player_wins:
      player_comission, bank_comission, tie_comissio = house_comission

      if bet_type == "player":
        bet_amount *= 1 - player_comission / 100

      if bet_type == "bank":
        bet_amount *= 1 - bank_comission / 100

      if bet_type == "tie":
        bet_amount *= 8
        bet_amount *= 1 - tie_comissio / 100

      bet_amount = int(bet_amount)

    elif not player_wins:
        bet_amount *= -1

    prizes.append(bet_amount)

  return prizes
