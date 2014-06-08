import random
import unittest
from hsgame.agents.basic_agents import PredictableBot
from hsgame.constants import CHARACTER_CLASS
from hsgame.game_objects import Game
from tests.testing_agents import *
from tests.testing_utils import generate_game_for, StackedDeck
from hsgame.replay import SavedGame

from hsgame.cards import *

__author__ = 'Daniel'

class TestPriest(unittest.TestCase):

    def setUp(self):
        random.seed(1857)


    def test_PriestPower(self):
        game = generate_game_for(CircleOfHealing, MogushanWarden, PredictableBot, DoNothingBot)

        game.players[1].hero.health = 20

        for turn in range(0, 3):
            game.play_single_turn()

        self.assertEqual(22, game.players[1].hero.health)


    def test_CircleOfHealing(self):
        deck1 = StackedDeck([CircleOfHealing(), MogushanWarden(), CircleOfHealing(), CircleOfHealing(), CircleOfHealing(), CircleOfHealing(), CircleOfHealing()], CHARACTER_CLASS.PRIEST)
        deck2 = StackedDeck([MogushanWarden()], CHARACTER_CLASS.PALADIN)
        game = Game([deck1, deck2], [SpellTestingAgent(), MinionPlayingAgent()])
        game.pre_game()
        game.current_player = 1
        
        for turn in range(0, 8):
            game.play_single_turn()

        game.players[0].minions[0].health = 4
        game.players[1].minions[0].health = 4
        game.play_single_turn() # Circle of Healing should be played
        self.assertEqual(game.players[0].minions[0].max_health, game.players[0].minions[0].health)
        self.assertEqual(game.players[1].minions[0].max_health, game.players[1].minions[0].health)


    def test_DivineSpirit(self):
        game = generate_game_for(DivineSpirit, MogushanWarden, SpellTestingAgent, MinionPlayingAgent)
        
        for turn in range(0, 8):
            game.play_single_turn()

        self.assertEqual(1, len(game.players[1].minions))
        self.assertEqual(1, game.players[1].minions[0].attack_power)
        self.assertEqual(7, game.players[1].minions[0].health)
        self.assertEqual(7, game.players[1].minions[0].max_health)
        game.play_single_turn() # Two Divine Spirits should be played
        self.assertEqual(1, game.players[1].minions[0].attack_power)
        self.assertEqual(28, game.players[1].minions[0].health)
        self.assertEqual(28, game.players[1].minions[0].max_health)
        # Test that this spell is being silenced properly as well
        game.players[1].minions[0].silence()
        self.assertEqual(1, game.players[1].minions[0].attack_power)
        self.assertEqual(7, game.players[1].minions[0].health)
        self.assertEqual(7, game.players[1].minions[0].max_health)
        game.play_single_turn()
        # Let's say the minion got damaged
        game.players[1].minions[0].health = 4
        game.play_single_turn() # Three Divine Spirits should be played
        self.assertEqual(1, game.players[1].minions[0].attack_power)
        self.assertEqual(32, game.players[1].minions[0].health)
        self.assertEqual(35, game.players[1].minions[0].max_health)
        # Test that this spell is being silenced properly as well
        game.players[1].minions[0].silence()
        self.assertEqual(1, game.players[1].minions[0].attack_power)
        self.assertEqual(7, game.players[1].minions[0].health)
        self.assertEqual(7, game.players[1].minions[0].max_health)


    def test_HolyFire(self):
        game = generate_game_for(HolyFire, MogushanWarden, SpellTestingAgent, MinionPlayingAgent)
        
        for turn in range(0, 10):
            game.play_single_turn()

        game.players[0].hero.health = 20
        self.assertEqual(2, len(game.players[1].minions))
        self.assertEqual(1, game.players[1].minions[0].attack_power)
        self.assertEqual(7, game.players[1].minions[0].health)
        self.assertEqual(7, game.players[1].minions[0].max_health)
        game.play_single_turn() # Holy Fire should be played
        self.assertEqual(1, game.players[1].minions[0].attack_power)
        self.assertEqual(2, game.players[1].minions[0].health)
        self.assertEqual(7, game.players[1].minions[0].max_health)
        self.assertEqual(25, game.players[0].hero.health)


    def test_HolyNova(self):
        deck1 = StackedDeck([MogushanWarden(), HolyNova()], CHARACTER_CLASS.PRIEST)
        deck2 = StackedDeck([MogushanWarden()], CHARACTER_CLASS.PALADIN)
        game = Game([deck1, deck2], [SpellTestingAgent(), MinionPlayingAgent()])
        game.pre_game()
        game.current_player = 1
        
        for turn in range(0, 8):
            game.play_single_turn()

        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual(1, len(game.players[1].minions))
        game.players[0].minions[0].health = 4 # Fake damage
        self.assertEqual(4, game.players[0].minions[0].health)
        self.assertEqual(7, game.players[1].minions[0].health)
        game.play_single_turn() # Holy Nova should be played
        self.assertEqual(6, game.players[0].minions[0].health)
        self.assertEqual(5, game.players[1].minions[0].health)


    def test_HolySmite(self):
        game = generate_game_for(HolySmite, MogushanWarden, SpellTestingAgent, DoNothingBot)
        
        self.assertEqual(30, game.players[1].hero.health)
        game.play_single_turn() # Holy Smite should be played
        self.assertEqual(28, game.players[1].hero.health)


    def test_InnerFire(self):
        game = generate_game_for(InnerFire, MogushanWarden, SpellTestingAgent, MinionPlayingAgent)
        
        for turn in range(0, 8):
            game.play_single_turn()
        
        self.assertEqual(1, len(game.players[1].minions))
        self.assertEqual(1, game.players[1].minions[0].attack_power)
        self.assertEqual(7, game.players[1].minions[0].health)
        game.play_single_turn() # Inner Fire should be played
        self.assertEqual(7, game.players[1].minions[0].attack_power)
        self.assertEqual(7, game.players[1].minions[0].health)
        # Test that this spell is being silenced properly as well
        game.players[1].minions[0].silence()
        self.assertEqual(1, game.players[1].minions[0].attack_power)
        self.assertEqual(7, game.players[1].minions[0].health)


    def test_MassDispel(self):
        game = generate_game_for(MassDispel, MogushanWarden, SpellTestingAgent, MinionPlayingAgent)
        
        for turn in range(0, 8):
            game.play_single_turn()
        
        self.assertEqual(1, len(game.players[1].minions))
        self.assertTrue(game.players[1].minions[0].taunt)
        self.assertEqual(7, len(game.players[0].hand))
        game.play_single_turn() # Mass Dispel should be played
        self.assertEqual(1, len(game.players[1].minions))
        self.assertFalse(game.players[1].minions[0].taunt)
        self.assertEqual(8, len(game.players[0].hand))


    def test_MindBlast(self):
        game = generate_game_for(MindBlast, MogushanWarden, SpellTestingAgent, MinionPlayingAgent)
        
        for turn in range(0, 2):
            game.play_single_turn()
        
        self.assertEqual(30, game.players[1].hero.health)
        game.play_single_turn() # Mind Blast should be played
        self.assertEqual(25, game.players[1].hero.health)


    def test_MindControl(self):
        game = generate_game_for(MindControl, MogushanWarden, SpellTestingAgent, MinionPlayingAgent)
        
        for turn in range(0, 18):
            game.play_single_turn()
        
        self.assertEqual(0, len(game.players[0].minions))
        self.assertEqual(6, len(game.players[1].minions))
        game.play_single_turn() # Mind Control should be played
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual(5, len(game.players[1].minions))


    def test_MindVision(self):
        game = generate_game_for(MindVision, MogushanWarden, SpellTestingAgent, MinionPlayingAgent)
                
        self.assertEqual(3, len(game.players[0].hand))
        self.assertEqual(4, len(game.players[1].hand))
        game.play_single_turn() # Mind Vision should be played
        self.assertEqual(4, len(game.players[0].hand))
        self.assertEqual("Mogu'shan Warden", game.players[0].hand[-1].name)
        self.assertEqual(4, len(game.players[1].hand))


    def test_Mindgames(self):
        game = generate_game_for(Mindgames, MogushanWarden, SpellTestingAgent, DoNothingBot)
        
        # Mindgames should be played, Mogu'shan Warden will be found and put into the battlefield
        for turn in range(0, 7):
            game.play_single_turn()
        
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual("Mogu'shan Warden", game.players[0].minions[0].card.name)
        
        # Cheat
        for index in range(0, 30):
            game.players[1].deck.used[index] = True

        game.play_single_turn()
        game.play_single_turn() # Mindgames should be played, opponent have no cards left in deck so Shadow of Nothing should be summoned
        self.assertEqual(2, len(game.players[0].minions))
        self.assertEqual("Shadow of Nothing", game.players[0].minions[0].card.name)


    def test_PowerWordShield(self):
        game = generate_game_for(StonetuskBoar, PowerWordShield, MinionPlayingAgent, SpellTestingAgent)
        
        # Power Word: Shield should be played, and target the enemy Stonetusk Boar. And a card should be drawn.
        for turn in range(0, 2):
            game.play_single_turn()
        
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual(3, game.players[0].minions[0].health)
        self.assertEqual(3, game.players[0].minions[0].max_health)
        self.assertEqual(5, len(game.players[1].hand))


    def test_ShadowMadness(self):
        game = generate_game_for([MagmaRager, MogushanWarden, WarGolem], [ShadowMadness, ShadowMadness, ShadowMadness, ShadowMadness, ShadowMadness, ShadowMadness, ShadowMadness, ShadowMadness, Silence], MinionPlayingAgent, PredictableAgentWithoutHeroPower)
        
        # Magma Rager should be played
        for turn in range(0, 5):
            game.play_single_turn()
        
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual("Magma Rager", game.players[0].minions[0].card.name)
        self.assertEqual(6, len(game.players[1].hand))
        
        # Shadow Madness shouldn't be played, since Magma Rager has attack > 3
        game.play_single_turn()
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual(7, len(game.players[1].hand))
        
        # Mogu'shan Warden should be played
        game.play_single_turn()
        self.assertEqual(2, len(game.players[0].minions))
        self.assertEqual("Mogu'shan Warden", game.players[0].minions[0].card.name)
        
        # Shadow Madness should be played, targeting the Mogu'shan that will attack the Magma.
        # Results in killing the Magma, and Mogu'shan takes 5 damage before being returned to the owner.
        game.play_single_turn()
        self.assertEqual(0, len(game.players[1].minions))
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual("Mogu'shan Warden", game.players[0].minions[0].card.name)
        self.assertEqual(2, game.players[0].minions[0].health)
        
        # Nothing should happen, no mana for War Golem
        game.play_single_turn()
        
        # Shadow Madness should be played again targeting the damaged Mogu'shan. Silence should follow after, that target
        # the "mind controlled" Mogu'shan, making it stay on our side when turn ends.
        game.play_single_turn()
        self.assertEqual(0, len(game.players[0].minions))
        self.assertEqual(1, len(game.players[1].minions))
        self.assertEqual("Mogu'shan Warden", game.players[1].minions[0].card.name)
        self.assertEqual(2, game.players[1].minions[0].health)
        self.assertEqual(29, game.players[0].hero.health)


    def test_ShadowWordDeath(self):
        game = generate_game_for([IronfurGrizzly, MagmaRager], ShadowWordDeath, MinionPlayingAgent, SpellTestingAgent)

        # Ironfur Grizzly should be played
        for turn in range(0, 3):
            game.play_single_turn()

        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual("Ironfur Grizzly", game.players[0].minions[0].card.name)
        
        # Nothing should happen, since the attack of Grizzly is 3
        game.play_single_turn()
        self.assertEqual(1, len(game.players[0].minions))

        # Magma Rager should be played        
        game.play_single_turn()
        self.assertEqual(2, len(game.players[0].minions))
        self.assertEqual("Magma Rager", game.players[0].minions[0].card.name)
        
        # Shadow Word: Death should be played, targeting the Magma Rager
        game.play_single_turn()
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual("Ironfur Grizzly", game.players[0].minions[0].card.name)


    def test_ShadowWordPain(self):
        game = generate_game_for([MagmaRager, IronfurGrizzly], ShadowWordPain, MinionPlayingAgent, SpellTestingAgent)

        # Magma Rager should be played
        for turn in range(0, 5):
            game.play_single_turn()

        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual("Magma Rager", game.players[0].minions[0].card.name)
        
        # Nothing should happen, since the attack of Magma Rager is 5
        game.play_single_turn()
        self.assertEqual(1, len(game.players[0].minions))

        # Ironfur Grizzly should be played
        game.play_single_turn()
        self.assertEqual(2, len(game.players[0].minions))
        self.assertEqual("Ironfur Grizzly", game.players[0].minions[0].card.name)
        
        # Shadow Word: Pain should be played, targeting the Grizzly
        game.play_single_turn()
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual("Magma Rager", game.players[0].minions[0].card.name)


    def test_Shadowform(self):
        game = generate_game_for(IronfurGrizzly, Shadowform, MinionPlayingAgent, PredictableBot)

        for turn in range(0, 9):
            game.play_single_turn()

        self.assertEqual("Lesser Heal", game.players[1].hero.power.__str__())
        
        # Shadowform should be played
        game.play_single_turn()
        self.assertEqual("Mind Spike", game.players[1].hero.power.__str__())

        # Nothing special
        game.play_single_turn()

        # Mind Spike should be used, and Shadowform should be played
        game.play_single_turn()
        self.assertEqual(1, game.players[0].minions[0].health)
        self.assertEqual("Mind Shatter", game.players[1].hero.power.__str__())
        
        # Nothing special
        game.play_single_turn()
        self.assertEqual(6, len(game.players[0].minions))
        
        # Mind Shatter should be used, and Shadowform should be played (but nothing will happen, we are already at Mind Shatter)
        game.play_single_turn()
        self.assertEqual("Mind Shatter", game.players[1].hero.power.__str__())
        self.assertEqual(5, len(game.players[0].minions))
        
        
        # Test using the hero power, then cast Shadowform and use the new power (this is possible)
        game = SavedGame("tests/replays/card_tests/Shadowform.rep")
        game.start()
        self.assertEqual(10, game.players[0].max_mana)
        self.assertEqual(3, game.players[0].mana)
        self.assertEqual(28, game.players[1].hero.health)


    def test_Silence(self):
        game = generate_game_for(IronfurGrizzly, Silence, MinionPlayingAgent, SpellTestingAgent)

        # Ironfur Grizzly should be played
        for turn in range(0, 3):
            game.play_single_turn()

        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual("Ironfur Grizzly", game.players[0].minions[0].card.name)
        self.assertTrue(game.players[0].minions[0].taunt)
        
        # Silence should be played, targeting the grizzly
        game.play_single_turn()
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual("Ironfur Grizzly", game.players[0].minions[0].card.name)
        self.assertFalse(game.players[0].minions[0].taunt)


    def test_Thoughtsteal(self):
        game = generate_game_for(Thoughtsteal, IronfurGrizzly, SpellTestingAgent, DoNothingBot)

        # Thoughtsteal should be played, copying two grizzly
        for turn in range(0, 5):
            game.play_single_turn()

        self.assertEqual(7, len(game.players[0].hand))
        self.assertEqual("Ironfur Grizzly", game.players[0].hand[-1].name)
        self.assertEqual("Ironfur Grizzly", game.players[0].hand[-2].name)


    def test_CabalShadowPriest(self):
        game = generate_game_for(CabalShadowPriest, StonetuskBoar, MinionPlayingAgent, MinionPlayingAgent)

        for turn in range(0, 10):
            game.play_single_turn()

        self.assertEqual(5, len(game.players[1].minions))

        # Cabal Shadow Priest should be played, targeting one boar
        game.play_single_turn()
        self.assertEqual(4, len(game.players[1].minions))
        self.assertEqual(2, len(game.players[0].minions))


    def test_Lightspawn(self):
        game = generate_game_for(Lightspawn, StonetuskBoar, MinionPlayingAgent, PredictableBot)

        # Lightspawn should be played
        for turn in range(0, 7):
            game.play_single_turn()

        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual(5, game.players[0].minions[0].attack_power)
        self.assertEqual(5, game.players[0].minions[0].health)

        # Lightspawn should have taken some hits
        game.play_single_turn()
        self.assertEqual(1, len(game.players[0].minions))
        self.assertEqual(2, game.players[0].minions[0].attack_power)
        self.assertEqual(2, game.players[0].minions[0].health)

        game.players[0].minions[0].heal(2)
        self.assertEqual(4, game.players[0].minions[0].attack_power)
        self.assertEqual(4, game.players[0].minions[0].health)
        
        game.players[0].minions[0].increase_health(4)
        self.assertEqual(8, game.players[0].minions[0].attack_power)
        self.assertEqual(8, game.players[0].minions[0].health)

        game.players[0].minions[0].decrease_health(2) # max_health goes from 9 to 7
        self.assertEqual(7, game.players[0].minions[0].attack_power)
        self.assertEqual(7, game.players[0].minions[0].health)


    def test_Lightwell(self):
        game = generate_game_for(Lightwell, StonetuskBoar, MinionPlayingAgent, PredictableBot)

        for turn in range(0, 4):
            game.play_single_turn()

        self.assertEqual(29, game.players[0].hero.health)
        self.assertEqual(3, game.players[0].minions[0].health)

        # Lightwell is out, it should heal at the beginning of this turn
        game.play_single_turn()
        self.assertEqual(3, game.players[0].minions[1].health)
        self.assertEqual(30, game.players[0].hero.health)


    def test_NorthshireCleric(self):
        game = generate_game_for(NorthshireCleric, StonetuskBoar, PredictableBot, PredictableBot)

        for turn in range(0, 2):
            game.play_single_turn()

        self.assertEqual(2, game.players[0].minions[0].health)
        self.assertEqual(26, game.players[0].deck.left)

        # Northshire is damaged, should get a heal and a card should be drawn
        game.play_single_turn()
        self.assertEqual(3, game.players[0].minions[0].health)
        self.assertEqual(24, game.players[0].deck.left)
        
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        
        # Silence one Northshire, the other one should still work
        game.players[0].minions[0].silence()
        self.assertEqual(2, len(game.players[0].minions))
        self.assertEqual(22, game.players[0].deck.left)
        game.play_single_turn()
        self.assertEqual(20, game.players[0].deck.left)
