# -*- coding: utf-8 -*-
import private_value_auction.forms as forms
from private_value_auction._builtin import Page, SubsessionWaitPage
from otree.common import Money


class Introduction(Page):

    template_name = 'private_value_auction/Introduction.html'


class Bid(Page):

    template_name = 'private_value_auction/Bid.html'

    def get_form_class(self):
        return forms.BidForm

    def variables_for_template(self):
        if self.player.private_value is None:
            self.player.private_value = self.player.generate_private_value()

        return {'private_value': self.player.private_value,
                'min_bid': Money(self.treatment.min_allowable_bid),
                'max_bid': Money(self.treatment.max_allowable_bid)}


class ResultsWaitPage(SubsessionWaitPage):

    def after_all_players_arrive(self):
        self.subsession.set_winner()


class Results(Page):

    template_name = 'private_value_auction/Results.html'

    def variables_for_template(self):
        if self.player.payoff is None:
            self.player.set_payoff()

        return {'is_winner': self.player.is_winner,
                'is_greedy': True if self.player.private_value - self.player.bid_amount < 0 else False,
                'bid_amount': self.player.bid_amount,
                'winning_bid': self.subsession.highest_bid(),
                'private_value': self.player.private_value,
                'payoff': self.player.payoff}


def pages():

    return [Introduction,
            Bid,
            ResultsWaitPage,
            Results]
