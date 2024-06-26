import random
from text_adventure_game.core.constants import BOSSES, LOVE_INTERESTS_BY_SCENE, ENEMIES_BY_SCENE
from text_adventure_game.characters.skill import SKILL_BOOKS
from text_adventure_game.gameplay.relationship import Relationship

class Explore:
    def __init__(self, game):
        self.game = game

    def explore(self):
        self.game.current_scene = random.choice(self.game.scenes)
        print(f"你探索了一下，发现了新的场景：{self.game.current_scene}。")

        # 使用多个随机事件
        events = [random.random() for _ in range(3)]

        for event in events:
            if event < 0.2:  # 20% 概率遇到敌人
                self.encounter_enemy()
            elif event < 0.3:  # 10% 概率找到宝箱
                print(f"你发现了一个宝箱！里面有一些有用的物品。")
                item = random.choice(["治疗药剂", "力量药水", "护甲"] + [book.name for book in SKILL_BOOKS])
                if item in [book.name for book in SKILL_BOOKS]:
                    skill_book = next(book for book in SKILL_BOOKS if book.name == item)
                    self.game.player.inventory.append(skill_book)
                    print(f"你获得了技能书：{item}")
                else:
                    self.game.player.inventory.append(item)
                    print(f"你获得了：{item}")
            elif event < 0.4:  # 10% 概率触发任务
                quest = self.game.quest_manager.get_new_quest()
                if quest:
                    self.game.quest_manager.list_active_quests()
            elif event < 0.9:  # 650% 概率遇到 NPC
                self.encounter_npc()
            else:  # 5% 概率遇到 Boss
                if random.random() < 0.5:
                    boss = BOSSES[self.game.current_scene]
                    print(f"你遇到了强大的首领：{boss.name}！准备战斗！")
                    self.game.battle.fight(boss)

    def encounter_enemy(self):
        enemies = ENEMIES_BY_SCENE[self.game.current_scene]
        enemy = random.choice(enemies)
        print(f"你遇到了一个敌人：{enemy.name}！准备战斗！")
        self.game.battle.fight(enemy)

    def encounter_npc(self):
        npcs = LOVE_INTERESTS_BY_SCENE[self.game.current_scene]
        npc = random.choice(npcs)
        relationship = next((rel for rel in self.game.love_interests if rel.character == npc), None)
        if relationship is None:
            relationship = Relationship(self.game.player, npc)
            self.game.love_interests.append(relationship)
        relationship.interact()
