import random
from text_adventure_game.characters.character import Character
from text_adventure_game.core.constants import ENEMIES_BY_SCENE
from text_adventure_game.inventory.items import LootManager,LootItem
from text_adventure_game.inventory.equipment import Weapon,Armor,MountArmor,Mount
from text_adventure_game.characters.skill import SkillBook

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
            elif action == "2":
                damage = self.game.player.use_skill(enemy)
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

        if self.game.player.health > 0:
            print(f"你打败了{enemy.name}！")
            loot = self.loot_manager.get_loot(enemy)
            self.game.player.inventory.append(self.loot_to_item(loot))
            print(f"你获得了：{loot}")
            self.game.player.gain_experience(random.randint(5, 15))
        else:
            print("你被敌人打败了……游戏结束。")
            exit()
            
    def loot_to_item(self, loot: LootItem):
        if loot.item_type == "weapon":
            return Weapon(loot.name, loot.attributes["damage"], loot.description, loot.attributes.get("armor_penetration", 0), loot.attributes.get("quantity"))
        elif loot.item_type == "armor":
            return Armor(loot.name, loot.attributes["defense"], loot.description, loot.attributes.get("resistance", 0))
        elif loot.item_type == "mount":
            return Mount(loot.name, loot.attributes["speed"], loot.attributes["health"], loot.description)
        elif loot.item_type == "mount_armor":
            return MountArmor(loot.name, loot.attributes["defense"], loot.description)
        elif loot.item_type == "skill_book":
            skill = loot.attributes["skill"]
            requirement = loot.attributes["requirement"]
            return SkillBook(loot.name, loot.description, skill, requirement)
        else:
            return loot

    def team_attack(self, enemy):
        teammates = [rel.character for rel in self.game.love_interests if rel.relationship_type in ["朋友", "好友", "恋人", "配偶"]]
        for teammate in teammates:
            damage = teammate.attack(enemy)
            print(f"{teammate.name}对{enemy.name}造成了{damage}点伤害。")
            if enemy.health <= 0:
                print(f"{enemy.name}被打败了！")
                break
