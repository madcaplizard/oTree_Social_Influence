from otree.api import *


author = 'Your name here'

doc = """
A mini trust game
"""

#----------------- CODE/oTree/TG/models -----------------

class C(BaseConstants):
    NAME_IN_URL = 'TG'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    P_1=[10,0] #payoffs exit
    P_2_3=[0,40] # payoffs entry, exploitation
    P_2_4 = [22, 18]  # payoffs entry, reciprocity


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    choice_1 = models.CharField(choices=[['Option 1','Option 1'], ['Option 2', 'Option 2']], widget=widgets.RadioSelectHorizontal, label="")
    choice_2 = models.CharField(choices=[['Option 3','Option 3'], ['Option 4', 'Option 4']], widget=widgets.RadioSelectHorizontal, label="")

class Player(BasePlayer):
    first_mover = models.BooleanField()
    treatment=  models.CharField()

#----------------- CODE/oTree/TG/models -----------------

#----------------- CODE/oTree/TG/functions -----------------

# Assign roles to players
def creating_session(player: Player):
    for g in player.get_groups():
        for p in g.get_players():
            # Copy the treatment for each subject
   
            if p.id_in_group == 1:
                first = True
            else:
                first = False
            p.first_mover = first


# Compute payoffs
def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    if group.choice_1 == 'Option 1':
        p1.payoff = C.P_1[0]
        p2.payoff = C.P_1[1]
    else:
        if group.field_maybe_none('choice_2') == 'Option 3':
            p1.payoff = C.P_2_3[0]
            p2.payoff = C.P_2_3[1]
        else:
            p1.payoff = C.P_2_4[0]
            p2.payoff = C.P_2_4[1]       

#----------------- CODE/oTree/TG/functions -----------------


#----------------- CODE/oTree/TG/pages -----------------

class Instructions(Page):
    @staticmethod
    def vars_for_template(player: Player):
        if player.session.config['treatment'] == "play":
            return {
                'play': True
            }
        else:
            return {
                'play': False
            }


class Choice_1(Page):
    form_model = 'group'
    form_fields = ['choice_1']

    @staticmethod
    def is_displayed(player: Player):
        return player.first_mover == 1


class SendWaitPage(WaitPage):
    def is_displayed(player: Player):
        return player.session.config['treatment'] == "play"


class Choice_2(Page):
    form_model = 'group'
    form_fields = ['choice_2']

    @staticmethod
    def vars_for_template(player: Player):
        if player.session.config['treatment'] == "play":
            return {
                'display': True,
                'choice_other': player.group.choice_1
            }
        else:
            return {
                'display': False
            }

    
    @staticmethod
    def is_displayed(player: Player):
        if player.session.config['treatment'] == "play":
            return player.first_mover == False and player.group.choice_1 == 'Option 2'
        else:
            return player.first_mover == False 


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'first_mover': player.first_mover,
            'choice_1': player.group.choice_1,
            'choice_2': player.group.field_maybe_none('choice_2'),
            'payoff': player.payoff
        }


page_sequence = [Instructions, Choice_1,
                 SendWaitPage, Choice_2, ResultsWaitPage, Results]

