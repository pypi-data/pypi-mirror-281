import random
from .constants import BOSSES
from .skill import SKILL_BOOKS

class Explore:
    def __init__(self, game):
        self.game = game

    def explore(self):
        self.game.current_scene = random.choice(self.game.scenes)
        print(f"你探索了一下，发现了新的场景：{self.game.current_scene}。")
        event = random.random()
        if event < 0.3:
            self.game.battle.choose_enemy()
        elif event < 0.5:
            print(f"你发现了一个宝箱！里面有一些有用的物品。")
            item = random.choice(["治疗药剂", "力量药水", "护甲"] + [book.name for book in SKILL_BOOKS])
            if item in [book.name for book in SKILL_BOOKS]:
                skill_book = next(book for book in SKILL_BOOKS if book.name == item)
                self.game.player.inventory.append(skill_book)
                print(f"你获得了技能书：{item}")
            else:
                self.game.player.inventory.append(item)
                print(f"你获得了：{item}")
        elif event < 0.7:
            quest = self.game.quest_manager.get_new_quest()
            if quest:
                self.game.quest_manager.list_active_quests()
        else:
            if random.random() < 0.5:
                boss = BOSSES[self.game.current_scene]
                print(f"你遇到了强大的首领：{boss.name}！准备战斗！")
                self.game.battle.fight(boss)
