# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants


def vars_for_all_templates(self):

    return {
            'total_q': 1
            }


class Introduction(Page):

    template_name = 'stackelberg_competition/Introduction.html'


class Question1(Page):

    template_name = 'stackelberg_competition/Question.html'

    form_model = models.Player
    form_fields = ['training_question_1']

    def vars_for_template(self):
        return {'num_q': 1}


class Feedback1(Page):

    template_name = 'stackelberg_competition/Feedback.html'

    def vars_for_template(self):
        return {'num_q': 1,
                'question': """Suppose firm A first decided to produce 20 units. Then firm B would be informed of firm A's production and decided to produce 30 units.
                               What would be the profit for firm B?""",
              #  'answer': self.player.training_question_1,
               # 'correct': Constants.training_1_correct,
                'explanation': """Total units produced were 20 + 30 = 50. The unit selling price was 60 – 50 = 10.
                                  The profit for firm B would be the product of the unit selling price and the unit produced by firm B, that is 10 × 30 = 300""",
              #  'is_correct': self.player.is_training_question_1_correct()
              }


class ChoiceOne(Page):

    def participate_condition(self):
        return self.player.id_in_group == 1

    template_name = 'stackelberg_competition/ChoiceOne.html'

    form_model = models.Player
    form_fields = ['quantity']


class ChoiceTwoWaitPage(WaitPage):



    def body_text(self):
        if self.player.id_in_group == 1:
            return "Waiting for the other participant to decide."
        else:
            return 'You are to decide second. Waiting for the other participant to decide first.'


class ChoiceTwo(Page):

    def participate_condition(self):
        return self.player.id_in_group == 2

    template_name = 'stackelberg_competition/ChoiceTwo.html'

    form_model = models.Player
    form_fields = ['quantity']

    # def vars_for_template(self):
    #     return {'other_quantity': self.player.other_player().quantity}
    #

class ResultsWaitPage(WaitPage):



    def body_text(self):
        return "Waiting for the other participant to decide."

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):

    template_name = 'stackelberg_competition/Results.html'

    def vars_for_template(self):
        self.player.set_payoff()

        return {
                'total_quantity': self.player.quantity + self.player.other_player().quantity,
                'total_plus_base': self.player.payoff + Constants.fixed_pay

                }


page_sequence = [Introduction,
            Question1,
            Feedback1,
            ChoiceOne,
            ChoiceTwoWaitPage,
            ChoiceTwo,
            ResultsWaitPage,
            Results]
