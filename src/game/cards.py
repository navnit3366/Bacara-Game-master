from . import players
import utils
from random import randint


suits_names = ["Paus", "Copas", "Espadas", "Ouros"]
deck_suits = len(suits_names)

cards_names = ["Ás", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Valete", "Rainha", "Rei"]
suit_values = len(cards_names)

deck_amount = 1

deck_size = suit_values * deck_suits
card_amount = deck_size * deck_amount


def get_random_card ():
  card_id = randint(0, card_amount - 1)

  return card_id


def get_card_info (card_id):
  deck = int(card_id / deck_size)
  suit = int((card_id - deck * deck_size) / suit_values)
  number = card_id % suit_values
  value = number + 1

  if value >= 10:
    value = 0

  return (card_id, deck, suit, number, value)


def get_new_random_card (cards_list):
  players_cards = [ card for player_cards in cards_list for card in player_cards ]

  while True:
    new_card = get_random_card()

    if not new_card in players_cards:
      return new_card


def sum_cards_values (cards):
  sum = 0

  for card in cards:
    card_value = get_card_info(card)[4]
    sum += card_value

  sum %= 10

  return sum

def sum_players_cards (players_cards):
  players_cards_value_sum = []

  for player_cards in players_cards:
    player_cards_value_sum = sum_cards_values(player_cards)

    players_cards_value_sum.append(player_cards_value_sum)

  return players_cards_value_sum


def draw_cards (players_list):
  cards = []

  # Draw 2 cards
  for player in players_list:
    player_cards = []

    while len(player_cards) < 2:
      card = get_new_random_card(cards)

      player_cards.append(card)

    cards.append(player_cards)

  bank_cards = cards[-1]
  bank_cards_value_sum = sum_cards_values(bank_cards)
  player_drawed_3dr_card = False

  # Draw 3dr players card
  for i in range(0, len(players.get_real_players(cards))):
    player_cards = cards[i]
    cards_value_sum = sum_cards_values(player_cards)

    if cards_value_sum <= 5 and bank_cards_value_sum < 8:
      card = get_new_random_card(cards)

      cards[i].append(card)
      player_drawed_3dr_card = True

  # Draw 3dr bank card
  if bank_cards_value_sum <= 5 and not bank_cards_value_sum >= 6:
    draw_bank_card = True

    if player_drawed_3dr_card:
      players_cards_value_sum = sum_players_cards(players.get_real_players(cards))

      for possibility in ((3, (8, 8)), (4, (0, 1, 8, 9)), (5, (0, 1, 2, 3, 8, 9))):
        bank_cards_value_sum_possibility, player_cards_value_sum_possibilityes = possibility

        if bank_cards_value_sum == bank_cards_value_sum_possibility:
          for player_cards_value_sum_possibility in player_cards_value_sum_possibilityes:
            if player_cards_value_sum_possibility in players_cards_value_sum:
              draw_bank_card = False

    if draw_bank_card:
      cards[-1].append(get_new_random_card(cards))

  return cards


def card_description (card_info):
  card_id, deck, suit, number, value = card_info

  description = f"{cards_names[number]} de {suits_names[suit]}"

  if deck_amount > 1:
    description += f" do {deck + 1}º baralho"

  description += f" ({value} pontos)"

  return description

def print_player_cards (playername, cards):
  cards_points = sum_cards_values(cards)

  utils.print_colored(f"§BCartas de §y{playername}§0:")

  for card in cards:
    card_info = get_card_info(card)

    print(f" - {card_description(card_info)}")
  
  utils.print_success(f"{playername} marcou {cards_points} pontos!")


def print_cards (players_list, tokens):
  players_names_tokens = list(zip(players_list, tokens))

  for player_name_tokens in players_names_tokens:
    player_name, player_cards = player_name_tokens

    print_player_cards(player_name, player_cards)


def get_winners (players_list, cards_sum):
  max_value = max(cards_sum)

  players_names_sums = list(zip(players_list, cards_sum))
  winners = []

  for player_name_sum in players_names_sums:
    player_name, value_sum = player_name_sum

    is_winner = value_sum == max_value

    winners.append(is_winner)

  return winners