import random

class Card:

    def __init__(self,name, attack, defense):
        self.name = name
        self.attack = attack
        self.defense = defense

    def content(self): #�J�[�h�̓��e�𕶎���Ŏ擾����
        return f"{self.name}: attack={self.attack}, defense={self.defense}"

    def __str__(self):
        return self.content()

    @staticmethod
    def calcDamage(selected_card,field_card): # �_���[�W���v�Z����
        damage = selected_card.attack-field_card.defense
        if damage>0:
            return damage
        return 0 # �_���[�W��0�ȉ��̎���0��Ԃ�

class Cards:
    def __init__(self):
        self.cards = [] # ��̃��X�g

    # �J�[�h��ǉ�����
    def add(self,card):
        self.cards.append(card)

    # �J�[�h�̖������擾����
    def __len__(self):
        return len(self.cards) # ���X�g�̒���

    # �J�[�h��\������
    def print(self):
        for index in range(len(self.cards)):
            print(index,self.cards[index])

    # ���X�gcards�̗v�f��self.cards�����菜��
    def drop(self, cards):
        for card in cards:
            if card in self.cards: #�����J�[�h�����X�g(self.cards)�̒��ɂ����
                self.cards.remove(card) # ��菜��

class Deck(Cards): # Cards�N���X��e�N���X�Ƃ��Čp��
    def __init__(self):
        super().__init__() # �e(supuer())�̃R���X�g���N�^���Ă�
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
        self.drop(picks) # �����N���X�̃��\�b�h���Ăԏꍇ�ɂ�self.������
        return picks

class Hand(Cards): # Cards��e�N���X�Ƃ���
    def __init__(self,deck): #�f�b�L���w�肷��
        super().__init__() # �e�̃R���X�g���N�^���Ă�
        self.cards = deck.draw(3) # 3�������Ď�D�Ƃ���(self.cards���㏑��)
        self.deck = deck # �����̃f�b�L�Ɏw�肳�ꂽ�f�b�L��ۑ�
    def draw(self): # �f�b�L����J�[�h��1������
        if len(self.deck)>0: # �f�b�L�̖����𒲂ׂ�(Deck��__len__���Ă΂��)
            card = random.sample(self.deck.cards, 1)
            self.deck.drop(card) # �f�b�L�����菜��
            self.add(card[0]) # ��D�ɉ�����
    def select(self,message):
        if len(self)<=0: # self�܂莩��(Hand)��cards�̖�����0�ȉ��Ȃ�
            return ModuleNotFoundError  # None��Ԃ� (None�͒l���Ȃ����̓���L�[���[�h)
        self.print()
        while True:
            try:
                index = int(input(message))
                card = self.cards[index]
            except Exception as e:
                if e==KeyboardInterrupt: #�G���[�����f�̎������G���[�ɂ���
                    raise KeyboardInterrupt
                print("Error. Try again.")
            else:
                self.cards.remove(card) #�G���[���Ȃ����͎�D�����菜��
                break
        return card


class Player:
    # �R���X�g���N�^�Bhp���w�肵�Ȃ����͏����l10
    def __init__(self, name, hp=10):
        self.name = name
        self.hp = hp
        # �f�b�L��������Hand�̃C���X�^���X������
        self.hand = Hand(Deck())
    def getHand(self): # hand��Ԃ����\�b�h
        return self.hand
    def getName(self): # name��Ԃ����\�b�h
        return self.name
    # isLivingOnDamage�́Adamage��^�������ɐ����Ă��邩��Ture/False�ŕԂ����\�b�h
    def isLivingOnDamage(self, damage=0):
        if self.hp<=damage: #�_���[�W�̕���hp���傫�����
            return False
        else: # hp����damage�������Ă�0���傫����
            self.hp -= damage # hp����_���[�W������
            return True
    def __str__(self): # �X�e�[�^�X������
        return f"{self.name}: HP={self.hp}"

    @staticmethod # ��Ő���
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

