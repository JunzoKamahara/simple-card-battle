# simple-card-battle
This is a programming course material.

##Simple Card Battle Program with Object Oriented
Text based Card match battle.

This is a two-player card game where the objective is to defeat your opponent by reducing their HP (hit points) to zero. Each player has an HP value and a deck of cards. The cards in the deck have two parameters: attack power and defense power.

At the start of the game, both players draw three cards from their respective decks. These cards possess various attributes, including attack and defense, but players can only see their own cards, not their opponent's. The defending player (the latter) selects one card from their hand to place as a shield, which contributes only its defensive value.

During a player's turn, they choose a card from their hand to attack the opponent. The attack power of the selected card is compared to the opponent's defense power. If the attack power exceeds the defense power, the opponent's HP is reduced by the difference. In case the opponent's defense is higher, no damage is dealt. After attacking, the opponent draws one card from their deck into their hand, and the turn ends.

Following that, the roles of the first and second attackers are switched, and a new turn begins.
