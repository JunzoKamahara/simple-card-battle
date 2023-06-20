import random
"""# simple-card-battle
This is a programming course material.

##Simple Card Battle Program with Object Oriented
Text based Card match battle.

This is a two-player card game where the objective is to defeat your opponent by reducing their HP (hit points) to zero. Each player has an HP value and a deck of cards. The cards in the deck have two parameters: attack power and defense power.

At the start of the game, both players draw three cards from their respective decks. These cards possess various attributes, including attack and defense, but players can only see their own cards, not their opponent's. The defending player (the latter) selects one card from their hand to place as a shield, which contributes only its defensive value.

During a player's turn, they choose a card from their hand to attack the opponent. The attack power of the selected card is compared to the opponent's defense power. If the attack power exceeds the defense power, the opponent's HP is reduced by the difference. In case the opponent's defense is higher, no damage is dealt. After attacking, the opponent draws one card from their deck into their hand, and the turn ends.

Following that, the roles of the first and second attackers are switched, and a new turn begins.
"""

class Card:

    def __init__(self,name, attack, defense):
        self.name = name
        self.attack = attack
        self.defense = defense

    def content(self): #カードの内容を文字列で取得する
        return f"{self.name}: attack={self.attack}, defense={self.defense}"

    def __str__(self):
        return self.content()

    @staticmethod
    def calcDamage(selected_card,field_card): # ダメージを計算する
        damage = selected_card.attack-field_card.defense
        if damage>0:
            return damage
        return 0 # ダメージが0以下の時は0を返す

class Cards:
    def __init__(self):
        self.cards = [] # 空のリスト

    # カードを追加する
    def add(self,card):
        self.cards.append(card)

    # カードの枚数を取得する
    def __len__(self):
        return len(self.cards) # リストの長さ

    # カードを表示する
    def print(self):
        for index in range(len(self.cards)):
            print(index,self.cards[index])

    # リストcardsの要素をself.cardsから取り除く
    def drop(self, cards):
        for card in cards:
            if card in self.cards: #もしカードがリスト(self.cards)の中にあれば
                self.cards.remove(card) # 取り除く

class Deck(Cards): # Cardsクラスを親クラスとして継承
    def __init__(self):
        super().__init__() # 親(supuer())のコンストラクタを呼ぶ
        self.add(Card("Card  1", 10, 10))
        self.add(Card("Card  2", 15,  5))
        self.add(Card("Card  3",  5, 15))
        self.add(Card("Card  4", 12,  8))
        self.add(Card("Card  5",  8, 12))
        self.add(Card("Card  6",  2, 17))
        self.add(Card("Card  7", 17,  2))
        self.add(Card("Card  8", 10, 10))
        self.add(Card("Card  9", 11,  9))
        self.add(Card("Card 10",  9, 11))
        self.add(Card("Card 11", 13,  8))
        self.add(Card("Card 12",  8, 13))
    def draw(self, num):
        picks = random.sample(self.cards, num)
        self.drop(picks) # 同じクラスのメソッドを呼ぶ場合にはself.をつける
        return picks

class Hand(Cards): # Cardsを親クラスとする
    def __init__(self,deck): #デッキを指定する
        super().__init__() # 親のコンストラクタを呼ぶ
        self.cards = deck.draw(3) # 3枚引いて手札とする(self.cardsを上書き)
        self.deck = deck # 自分のデッキに指定されたデッキを保存
    def draw(self): # デッキからカードを1枚引く
        if len(self.deck)>0: # デッキの枚数を調べる(Deckの__len__が呼ばれる)
            card = random.sample(self.deck.cards, 1)
            self.deck.drop(card) # デッキから取り除く
            self.add(card[0]) # 手札に加える
    def select(self,message):
        if len(self)<=0: # selfつまり自分(Hand)のcardsの枚数が0以下なら
            return ModuleNotFoundError  # Noneを返す (Noneは値がない時の特殊キーワード)
        self.print()
        while True:
            try:
                index = int(input(message))
                card = self.cards[index]
            except Exception as e:
                if e==KeyboardInterrupt: #エラーが中断の時だけエラーにする
                    raise KeyboardInterrupt
                print("Error. Try again.")
            else:
                self.cards.remove(card) #エラーがない時は手札から取り除く
                break
        return card


class Player:
    # コンストラクタ。hpを指定しない時は初期値10
    def __init__(self, name, hp=10):
        self.name = name
        self.hp = hp
        # デッキを持ったHandのインスタンスを持つ
        self.hand = Hand(Deck())
    def getHand(self): # handを返すメソッド
        return self.hand
    def getName(self): # nameを返すメソッド
        return self.name
    # isLivingOnDamageは、damageを与えた時に生きているかをTure/Falseで返すメソッド
    def isLivingOnDamage(self, damage=0):
        if self.hp<=damage: #ダメージの方がhpより大きければ
            return False
        else: # hpからdamageを引いても0より大きい時
            self.hp -= damage # hpからダメージを引く
            return True
    def __str__(self): # ステータス文字列
        return f"{self.name}: HP={self.hp}"

    @staticmethod # 後で説明
    def printStatus(p1, p2):
        print(p1)
        print(p2)

class Game:
    def __init__(self, p1_name, p2_name):
        self.player1 = Player(p1_name)
        self.player2 = Player(p2_name)
        Player.printStatus(self.player1, self.player2)
        self.field_card = self.player2.getHand().select("Select field card (not attack):")

    def play(self, attacker, defender):
        print(f"{attacker.getName()}'s turn")
        selected_card = attacker.getHand().select("Select attack card:")
        if selected_card==None:
            print(f"{attacker.getName()} has no card. {defender.getName()} win!")
            return False

        damage = Card.calcDamage(selected_card, self.field_card)
        print(f"Damage: {damage}")
        if not defender.isLivingOnDamage( Card.calcDamage(selected_card, self.field_card) ):
            print(f"{defender.getName()} is down. {attacker.getName()} win!")
            return False
        self.field_card = selected_card

        defender.getHand().draw()
        Player.printStatus(attacker, defender)

        return True

    def Senko(self):
        return self.play(self.player1, self.player2)
    def Koko(self):
        return self.play(self.player2, self.player1)

if __name__=="__main__":
    game = Game("Player 1", "Player 2")
    while game.Senko() and game.Koko():
        pass

