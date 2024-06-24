import random
from .character import Character
from .loot import LootManager, LootItem
from .constants import ENEMIES_BY_SCENE

class Battle:
    def __init__(self, game):
        self.game = game
        self.loot_manager = LootManager()

    def choose_enemy(self):
        enemies = ENEMIES_BY_SCENE[self.game.current_scene]
        print("请选择一个敌人进行战斗：")
        for i, enemy in enumerate(enemies):
            print(f"{i + 1}. {enemy.name} (生命值: {enemy.max_health}, 力量: {enemy.strength})")
        choice = int(input("输入敌人的编号：")) - 1
        if 0 <= choice < len(enemies):
            enemy = enemies[choice]
            self.game.current_enemy = Character(enemy.name, enemy.max_health, enemy.strength, enemy.charm, enemy.intelligence, enemy.agility, enemy.skills)
            self.fight(self.game.current_enemy)
        else:
            print("无效的选择，请重新输入。")

    def fight(self, enemy):
        print(f"你遇到了一个敌人：{enemy.name}！准备战斗！")
        while self.game.player.health > 0 and enemy.health > 0:
            print("选择你的行动：")
            print("1. 普通攻击")
            print("2. 使用技能")
            if any(rel.relationship_type in ["朋友", "好友", "恋人", "配偶"] for rel in self.game.love_interests):
                print("3. 组队攻击")
            action = input("请输入选项（1-3）：")
            if action == "1":
                damage = self.game.player.attack(enemy)
                print(f"{self.game.player.name}对{enemy.name}造成了{damage}点伤害。")
            elif action == "2":
                damage = self.game.player.use_skill(enemy)
                print(f"{self.game.player.name}使用技能对{enemy.name}造成了{damage}点伤害。")
            elif action == "3":
                self.team_attack(enemy)
            else:
                print("无效的选择，请重新输入。")
                continue

            if enemy.health > 0:
                if "召唤骷髅战士" in enemy.skills:
                    print(f"{enemy.name}召唤了骷髅战士！")
                    self.fight(Character("骷髅战士", 50, 10, 1, 3, 4))
                else:
                    damage = enemy.attack(self.game.player)
                    print(f"{enemy.name}对你造成了{damage}点伤害。")

        if self.game.player.health > 0:
            print(f"你打败了{enemy.name}！")
            loot = self.loot_manager.get_loot(enemy.level)
            self.game.player.inventory.append(loot)
            print(f"你获得了：{loot}")
            self.game.player.gain_experience(random.randint(5, 15))
        else:
            print("你被敌人打败了……游戏结束。")
            exit()

    def team_attack(self, enemy):
        teammates = [rel.character for rel in self.game.love_interests if rel.relationship_type in ["朋友", "好友", "恋人", "配偶"]]
        for teammate in teammates:
            damage = teammate.attack(enemy)
            print(f"{teammate.name}对{enemy.name}造成了{damage}点伤害。")
            if enemy.health <= 0:
                print(f"{enemy.name}被打败了！")
                break
