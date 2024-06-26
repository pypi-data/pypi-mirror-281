# text_adventure_game/core/shared.py
import random
from text_adventure_game.inventory.equipment import Armor, Equipment, Weapon

class Character:
    def __init__(self, name, health, strength, charm, intelligence, agility, mana=50, luck=5, skills=None, level=1):
        self.name = name
        self.health = health
        self.max_health = health
        self.strength = strength
        self.charm = charm
        self.intelligence = intelligence
        self.agility = agility
        self.mana = mana
        self.max_mana = mana
        self.luck = luck
        self.level = level
        self.skills = skills if skills else []
        self.inventory = []
        self.equipment = Equipment()
        self.experience = 0
        self.shield = 0
        self.randomly_equip()

    def randomly_equip(self):
        weapon_pool = common_weapons
        armor_pool = common_armors
        ammo_pool=common_ammo

        if self.level >= 10:
            weapon_pool = rare_weapons
            armor_pool = rare_armors
            ammo_pool=rare_ammo
            
        if self.level >= 20:
            weapon_pool = epic_weapons
            armor_pool = epic_armors
            ammo_pool=epic_ammo
            
        if self.level >= 30:
            weapon_pool = legendary_weapons
            armor_pool = legendary_armors
            ammo_pool=legendary_ammo

        weapon = random.choice(weapon_pool)
        self.equip_item(weapon)
        if weapon.quantity:  # 远程武器需要弹药
            self.equip_item(random.choice(ammo_pool))  # 弹药也是武器池的一部分

        armor_slots = list(armor_pool[0].slot)  # 获取所有可能的装备槽位
        for slot in armor_slots:
            self.equip_item(random.choice([armor for armor in armor_pool if armor.slot == slot]))


    def equip_item(self, item):
        if isinstance(item, Weapon):
            self.equipment.equip_weapon(item)
        elif isinstance(item, Armor):
            self.equipment.equip_armor(item, item.slot)

    def attack(self, target):
        weapon = self.equipment.get_equipped_weapon()
        if weapon:
            damage = random.randint(1, self.strength) + weapon.damage
            if target.equipment.get_defense():
                damage -= target.equipment.get_defense()
                damage = max(damage + weapon.armor_penetration, 0)
            print(f"{self.name} 使用 {weapon.name} 对 {target.name} 造成了 {damage} 点伤害。")
            if weapon.quantity is not None:  # 仅对远程武器使用数量限制
                weapon.quantity -= 1
                if weapon.quantity <= 0:
                    print(f"{weapon.name} 数量用尽，已卸下。")
                    self.equipment.unequip_weapon(self.equipment.weapon_slots.index(weapon))
        else:
            damage = random.randint(1, self.strength)
            print(f"{self.name} 对 {target.name} 造成了 {damage} 点伤害。")

        if target.shield > 0:
            if damage >= target.shield:
                damage -= target.shield
                target.shield = 0
            else:
                target.shield -= damage
                damage = 0

        target.health -= damage
        return damage

    def get_defense(self):
        total_defense = 0
        for armor in self.equipment.armor_slots.values():
            if armor:
                total_defense += armor.defense
        return total_defense

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.max_health += 10
        self.health = self.max_health
        self.max_mana += 5
        self.mana = self.max_mana
        self.strength += 2
        self.charm += 1
        self.intelligence += 1
        self.agility += 1
        self.luck += 1
        print(f"{self.name} 升级了！现在的等级是：{self.level}，最大生命值增加到：{self.max_health}，最大法力值增加到：{self.max_mana}，力量增加到：{self.strength}，魅力增加到：{self.charm}，智力增加到：{self.intelligence}，敏捷增加到：{self.agility}，幸运增加到：{self.luck}。")

    def learn_skill(self, skill_book):
        if skill_book.attributes["skill"] and skill_book.requirement(self):
            self.skills.append(skill_book.attributes["skill"])
            self.inventory.remove(skill_book)
            print(f"你学习了技能：{skill_book.attributes['skill']}")
        else:
            print(f"你的属性未达到学习 {skill_book.name} 的要求。")

    def use_skill(self, target):
        if not self.skills:
            print("你没有可以使用的技能。")
            return 0

        print("选择技能：")
        for i, skill in enumerate(self.skills):
            print(f"{i + 1}. {skill['name']} - {skill['description']}")
        choice = int(input("请输入技能编号：")) - 1

        if 0 <= choice < len(self.skills):
            skill = self.skills[choice]
            if self.mana >= skill.get("mana_cost", 0):
                damage = random.randint(skill['min_damage'], skill['max_damage'])
                self.mana -= skill.get("mana_cost", 0)
                target.health -= damage
                print(f"{self.name} 使用了技能 {skill['name']}，对 {target.name} 造成了 {damage} 点伤害。")
                return damage
            else:
                print("法力不足，无法使用技能。")
                return 0
        else:
            print("无效的选择，请重新输入。")
            return 0

    def use_item(self, item):
        if item in self.inventory:
            item.use(self)
            self.inventory.remove(item)
        else:
            print(f"你没有 {item.name} 这个物品。")

class Boss(Character):
    def __init__(self, name, health, strength, charm, intelligence, agility, mana=50, luck=5, level=1, skills=None):
        super().__init__(name, health, strength, charm, intelligence, agility, mana, luck, [], level)
        self.skills = skills if skills else []

    def use_skill(self, target):
        skill = random.choice(self.skills)
        if skill.name == "召唤骷髅战士":
            print(f"{self.name} 使用了技能 {skill.name}，召唤了一个骷髅战士！")
            return Character("骷髅战士", 50, 10, 1, 3, 4)
        else:
            if skill.use():
                damage = random.randint(skill.min_damage, skill.max_damage)
                if skill.skill_type == "shield":
                    self.shield += damage
                    print(f"{self.name} 使用了技能 {skill.name}，生成了 {damage} 点护盾。")
                else:
                    target.health -= damage
                    print(f"{self.name} 使用了技能 {skill.name}，对 {target.name} 造成了 {damage} 点伤害。")
                return damage
            else:
                print(f"{skill.name} 技能冷却中。")
                return 0



common_weapons = [
    Weapon("短剑", 3, "普通的短剑。"),
    Weapon("木盾", 2, "普通的木盾。"),
    Weapon("长矛", 4, "普通的长矛。"),
    Weapon("短弓", 4, "普通的短弓。", 0, 15)
]

common_armors = [
    Armor("皮甲", 4, "普通的皮甲。", slot="身"),
    Armor("布帽", 1, "普通的布帽。", slot="头"),
    Armor("皮靴", 2, "普通的皮靴。", slot="脚"),
    Armor("布手套", 1, "普通的布手套。", slot="手")
]

rare_weapons = [
    Weapon("钢匕首", 5, "锋利的钢匕首。"),
    Weapon("长弓", 7, "远程攻击用的长弓。", 0, 20),
    Weapon("战斧", 8, "沉重的战斧。"),
    Weapon("弯刀", 6, "快速的弯刀。")
]

rare_armors = [
    Armor("铁盔", 5, "提供额外防护的铁盔。", slot="头"),
    Armor("锁子甲", 8, "提供额外防护的锁子甲。", slot="身"),
    Armor("铁靴", 4, "提供额外防护的铁靴。", slot="脚"),
    Armor("铁手套", 3, "提供额外防护的铁手套。", slot="手")
]

epic_weapons = [
    Weapon("精钢长剑", 12, "拥有强大力量的精钢长剑。"),
    Weapon("冰霜弓", 15, "拥有冰霜力量的弓。", 0, 30),
    Weapon("烈焰锤", 14, "拥有烈焰力量的锤子。"),
    Weapon("暗影匕首", 13, "拥有暗影力量的匕首。")
]

epic_armors = [
    Armor("龙鳞甲", 15, "提供极高防护的龙鳞甲。", slot="身"),
    Armor("神圣头盔", 12, "提供极高防护的神圣头盔。", slot="头"),
    Armor("龙鳞靴", 10, "提供极高防护的龙鳞靴。", slot="脚"),
    Armor("神圣护手", 8, "提供极高防护的神圣护手。", slot="手")
]

legendary_weapons = [
    Weapon("雷霆之剑", 20, "拥有雷电力量的剑。"),
    Weapon("烈焰战斧", 25, "拥有烈焰力量的战斧。"),
    Weapon("风暴弩", 18, "射程远且威力巨大的弩。", 0, 40)
]

legendary_armors = [
    Armor("天使之铠", 20, "拥有神圣力量的铠甲。", slot="身"),
    Armor("恶魔头盔", 18, "拥有恶魔力量的头盔。", slot="头"),
    Armor("神圣护手", 12, "提供极高防护的神圣护手。", slot="手"),
    Armor("神圣长靴", 15, "提供极高防护的神圣长靴。", slot="脚")
]



common_ammo = [
    Weapon("普通箭", 0, "适用于普通弓的箭。", 0, 20),
    Weapon("普通弩箭", 0, "适用于普通弩的弩箭。", 0, 15)
]

rare_ammo = [
    Weapon("钢箭", 0, "适用于高级弓的钢箭。", 0, 20),
    Weapon("钢弩箭", 0, "适用于高级弩的钢弩箭。", 0, 15)
]

epic_ammo = [
    Weapon("冰霜箭", 0, "带有冰霜力量的箭。", 0, 25),
    Weapon("雷霆弩箭", 0, "带有雷霆力量的弩箭。", 0, 20)
]

legendary_ammo = [
    Weapon("神圣箭", 0, "带有神圣力量的箭。", 0, 30),
    Weapon("恶魔弩箭", 0, "带有恶魔力量的弩箭。", 0, 25)
]

