import random
from text_adventure_game.characters.character import Character
from text_adventure_game.core.constants import ENEMIES_BY_SCENE
from text_adventure_game.inventory.items import LootManager, LootItem
from text_adventure_game.inventory.equipment import Weapon, Armor, MountArmor, Mount
from text_adventure_game.characters.skill import SkillBook
from text_adventure_game.characters.character import common_weapons,common_armors,rare_weapons,rare_armors,epic_weapons,epic_armors,legendary_weapons,legendary_armors
class Battle:
    def __init__(self, game):
        self.game = game
        self.loot_manager = LootManager()

    def choose_enemy(self):
        enemies = ENEMIES_BY_SCENE[self.game.current_scene]
        enemy = random.choice(enemies)
        self.randomly_equip_enemy(enemy)
        self.game.current_enemy = enemy
        self.fight(self.game.current_enemy)
        
    def randomly_equip_enemy(self, enemy):
        # 根据等级选择装备池
        if enemy.level <= 5:
            weapons = common_weapons
            armors = common_armors
        elif enemy.level <= 10:
            weapons = rare_weapons
            armors = rare_armors
        elif enemy.level <= 15:
            weapons = epic_weapons
            armors = epic_armors
        else:
            weapons = legendary_weapons
            armors = legendary_armors

        # 随机装备武器
        weapon = random.choice(weapons)
        enemy.equipment.equip_weapon(weapon)

        # 如果装备了弓或弩，确保配备箭或弩箭
        if weapon.name in ["短弓", "长弓", "冰霜弓"]:
            arrow = LootItem("箭", "箭，用于弓箭。", "common", item_type="ammunition", quantity=random.randint(10, 30), attributes={"damage": 2})
            enemy.inventory.append(arrow)
        elif weapon.name in ["风暴弩"]:
            bolt = LootItem("弩箭", "弩箭，用于弩。", "common", item_type="ammunition", quantity=random.randint(5, 20), attributes={"damage": 3})
            enemy.inventory.append(bolt)

        # 随机装备盔甲
        armor = random.choice(armors)
        enemy.equipment.equip_armor(armor, armor.slot)
        

    def fight(self, enemy):
        print(f"你遇到了一个敌人：{enemy.name}！准备战斗！")
        while self.game.player.health > 0 and enemy.health > 0:
            print("选择你的行动：")
            print("1. 普通攻击")
            print("2. 使用技能")
            if any(rel.relationship_type in ["朋友", "好友", "恋人", "配偶"] for rel in self.game.love_interests):
                print("3. 组队攻击")
            print("4. 自动战斗")
            action = input("请输入选项（1-4）：")
            if action == "1":
                damage = self.game.player.attack(enemy)
            elif action == "2":
                self.use_skill(enemy)
            elif action == "3":
                self.team_attack(enemy)
            elif action == "4":
                self.auto_battle(enemy)
                break
            else:
                print("无效的选择，请重新输入。")
                continue

            if enemy.health > 0:
                damage = enemy.attack(self.game.player)
                print(f"{enemy.name}对你造成了{damage}点伤害。")
                if "召唤骷髅战士" in [skill.name for skill in enemy.skills]:
                    print(f"{enemy.name}召唤了骷髅战士！")
                    self.fight(Character("骷髅战士", 50, 10, 1, 3, 4))

            self.cooldown_tick()

        if self.game.player.health > 0:
            print(f"你打败了{enemy.name}！")
            loot = self.loot_manager.get_loot(enemy)
            self.game.player.inventory.append(self.loot_to_item(loot))
            print(f"你获得了：{loot}")
            self.game.player.gain_experience(random.randint(5, 15))
        else:
            print("你被敌人打败了……游戏结束。")
            exit()
   
    def use_skill(self, enemy):
        available_skills = [skill for skill in self.game.player.skills if skill.is_available()]
        if not available_skills:
            print("没有可用的技能！")
            return

        print("选择一个技能使用：")
        for i, skill in enumerate(available_skills):
            print(f"{i + 1}. {skill}")
        choice = int(input("输入技能编号：")) - 1
        if 0 <= choice < len(available_skills):
            skill = available_skills[choice]
            if self.game.player.mana >= skill.mana_cost:
                if skill.use():
                    if skill.skill_type == "shield":
                        self.game.player.shield += random.randint(skill.min_damage, skill.max_damage)
                        print(f"你使用了{skill.name}，生成了{self.game.player.shield}点护盾。")
                    else:
                        damage = random.randint(skill.min_damage, skill.max_damage)
                        enemy.health -= damage
                        print(f"你使用了{skill.name}，对{enemy.name}造成了{damage}点伤害。")
                    self.game.player.mana -= skill.mana_cost
                else:
                    print(f"{skill.name}仍在冷却中。")
            else:
                print("法力不足，无法使用技能。")
        else:
            print("无效的选择，请重新输入。")
   
    def auto_battle(self, enemy):
        print("进入自动战斗模式...")
        while self.game.player.health > 0 and enemy.health > 0:
            damage = self.game.player.attack(enemy)
            if enemy.health > 0:
                damage = enemy.attack(self.game.player)
            self.cooldown_tick()

        if self.game.player.health > 0:
            print(f"你打败了{enemy.name}！")
            loot = self.loot_manager.get_loot(enemy)
            self.game.player.inventory.append(self.loot_to_item(loot))
            print(f"你获得了：{loot}")
            self.game.player.gain_experience(random.randint(5, 15))
        else:
            print("你被敌人打败了……游戏结束。")
            exit()
            
    def cooldown_tick(self):
        for skill in self.game.player.skills:
            skill.cooldown_tick()

    def loot_to_item(self, loot: LootItem):
        if loot.item_type == "weapon" or loot.item_type=="shield":
            return Weapon(loot.name, loot.attributes.get("damage", 0), loot.description, loot.attributes.get("armor_penetration", 0), loot.attributes.get("quantity"))
        elif loot.item_type == "armor":
            return Armor(loot.name, loot.attributes["defense"], loot.description, loot.slot, loot.attributes.get("resistance", 0))
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
