import random
from otree.api import *
from otree.models import player

author = 'Jackie Chan'

doc = """
The Effect of Social Influence on Investment Decision-Making
"""


class Constants(BaseConstants):
    name_in_url = 'social_influence'
    players_per_group = 5
    num_rounds = 1
    investment_options = ['Little Risk', 'Medium Risk', 'Super-Risky']



class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for player in self.get_players():
                participant = player.participant
                participant.time_pressure = random.choice([True, False])

class Group(BaseGroup):
    pass

class Player(BasePlayer):
        # Participant demographics
    age = models.IntegerField(
        label='What is your age?',
        choices=['18_24', '24_30', '30_36','36_45','45_60'],
        widget=widgets.RadioSelect
        )
    gender = models.StringField(
        label='What is your gender?',
        choices=['Female', 'Male', 'Prefer Not to Say'],
        widget=widgets.RadioSelect
        )
    income = models.IntegerField(
        label='What is your approximate annual income?',
        choices=['10000_20000', '20000_30000','30000_100000'],
        widget=widgets.RadioSelect
        )

    # Investment decision
    
    investment_choice = models.StringField(
        choices=Constants.investment_options,
        label='Select your investment option:',
    )
    
    # leader_investment_choice_round1 = models.CharField(
    #     choices=Constants.investment_options,
    #     verbose_name="Leader's investment choice in round 1",
    #     blank=True
    # )



        
    def other_player(self):
        return self.get_others_in_group()[0]
 

    def role(self):
        if self.round_number == 1:
            if self.id_in_group == 1:
                return 'leader'
            else:
                return 'follower'
        
    
    # Confidence level
    confidence_level = models.IntegerField(
        label='Please rate your confidence in your investment choice (0-100)',
        min=1,
        max=101,
        
    )

#########PAGES##########
from otree.api import Page, WaitPage

class Introduction(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'income']

class LeaderInvestmentChoice(Page):
    def is_displayed(self):
        return self.role() == 'follower'

    def vars_for_template(self):
        leader = self.group.get_player_by_role('leader')
        leader_choice_available = leader.investment_choice is not None
        return {
            'leader': leader,
            'role': self.role(),
            'leader_choice_available': leader_choice_available
        }

class InvestmentDecision(Page):
    form_model = 'player'
    form_fields = ['investment_choice', 'confidence_level']

    def is_displayed(self):
        return self.round_number == 1 or self.role() == 'follower'
    
    def vars_for_template(self):
        if self.role() == 'follower':
            leader = self.group.get_player_by_role('leader')
            return {
                'role': self.role(),
                'investment_options': Constants.investment_options,
                'leader_investment_choice': leader.investment_choice
            }
        else:
            return {
                'role': self.role(),
                'investment_options': Constants.investment_options
            }
    
class Results(Page):
    def vars_for_template(self):
        leader = self.group.get_player_by_role('leader')
        return {
            'role': self.role(),
            'investment_choice': self.investment_choice,
            'leader_investment_choice': leader.investment_choice,
        }

    def before_next_page(self):
        if self.round_number == 1 and self.role() == 'follower':
            leader = self.group.get_player_by_role('leader')
            self.leader_investment_choice = leader.investment_choice
    
class WaitForLeader(WaitPage):
    def is_displayed(self):
        return self.role() == 'follower'

    def after_all_players_arrive(self):
        pass

    def body_text(self):
        if self.player.role() == 'follower':
            return "Please wait for the leader to make their investment decision."

    def redirect_to_page(self):
        if self.player.role() == 'follower':
            return 'LeaderInvestmentChoice'


page_sequence = [Introduction, WaitForLeader, LeaderInvestmentChoice, InvestmentDecision, Results]















#----------------- CODE/oTree/TG/models -----------------

#----------------- CODE/oTree/TG/functions -----------------

# # Assign roles to players
# def creating_session(player: Player):
#     for g in player.get_groups():
#         for p in g.get_players():
#             # Copy the treatment for each subject
   
#             if p.id_in_group == 1:
#                 first = True
#             else:
#                 first = False
#             p.first_mover = first


# # Compute payoffs
# def set_payoffs(group: Group):
#     p1 = group.get_player_by_id(1)
#     p2 = group.get_player_by_id(2)
#     if group.choice_1 == 'Option 1':
#         p1.payoff = C.P_1[0]
#         p2.payoff = C.P_1[1]
#     else:
#         if group.field_maybe_none('choice_2') == 'Option 3':
#             p1.payoff = C.P_2_3[0]
#             p2.payoff = C.P_2_3[1]
#         else:
#             p1.payoff = C.P_2_4[0]
#             p2.payoff = C.P_2_4[1]       

# #----------------- CODE/oTree/TG/functions -----------------


# #----------------- CODE/oTree/TG/pages -----------------

# class Instructions(Page):
#     @staticmethod
#     def vars_for_template(player: Player):
#         if player.session.config['treatment'] == "play":
#             return {
#                 'play': True
#             }
#         else:
#             return {
#                 'play': False
#             }


# class Choice_1(Page):
#     form_model = 'group'
#     form_fields = ['choice_1']

#     @staticmethod
#     def is_displayed(player: Player):
#         return player.first_mover == 1


# class SendWaitPage(WaitPage):
#     def is_displayed(player: Player):
#         return player.session.config['treatment'] == "play"


# class Choice_2(Page):
#     form_model = 'group'
#     form_fields = ['choice_2']

#     @staticmethod
#     def vars_for_template(player: Player):
#         if player.session.config['treatment'] == "play":
#             return {
#                 'display': True,
#                 'choice_other': player.group.choice_1
#             }
#         else:
#             return {
#                 'display': False
#             }

    
#     @staticmethod
#     def is_displayed(player: Player):
#         if player.session.config['treatment'] == "play":
#             return player.first_mover == False and player.group.choice_1 == 'Option 2'
#         else:
#             return player.first_mover == False 


# class ResultsWaitPage(WaitPage):
#     after_all_players_arrive = 'set_payoffs'


# class Results(Page):

#     @staticmethod
#     def vars_for_template(player: Player):
#         return {
#             'first_mover': player.first_mover,
#             'choice_1': player.group.choice_1,
#             'choice_2': player.group.field_maybe_none('choice_2'),
#             'payoff': player.payoff
#         }


# page_sequence = [Instructions, Choice_1,
#                  SendWaitPage, Choice_2, ResultsWaitPage, Results]

