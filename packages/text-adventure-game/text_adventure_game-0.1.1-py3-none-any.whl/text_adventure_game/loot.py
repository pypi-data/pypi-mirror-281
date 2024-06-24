import random

class LootItem:
    def __init__(self, name, description, rarity, quantity=1):
        self.name = name
        self.description = description
        self.rarity = rarity
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} ({self.rarity}): {self.description} x{self.quantity}"

    def use(self, character):
        if self.name == "治疗药剂":
            character.health = min(character.max_health, character.health + 20)
            print(f"{character.name}使用了{self.name}，恢复了20点生命值。")
            self.quantity -= 1
        elif self.name == "力量药水":
            character.strength += 5
            print(f"{character.name}使用了{self.name}，力量增加了5点。")
            self.quantity -= 1
        # 添加更多药水的效果
        else:
            print(f"{self.name}无法使用。")

class LootManager:
    def __init__(self):
        self.common_loot = [
            LootItem("金币", "普通的货币，可以用来购买物品。", "common"),
            LootItem("治疗药剂", "恢复少量生命值的药剂。", "common"),
            LootItem("力量药水", "暂时增加力量的药水。", "common")
        ]
        self.rare_loot = [
            LootItem("强力武器", "增加攻击力的武器。", "rare"),
            LootItem("神秘宝石", "具有神秘力量的宝石。", "rare"),
            LootItem("护甲", "提供额外防护的护甲。", "rare")
        ]
        self.epic_loot = [
            LootItem("传说武器", "拥有强大力量的传说级武器。", "epic"),
            LootItem("传奇宝石", "拥有巨大力量的宝石。", "epic"),
            LootItem("神圣护甲", "提供极高防护的护甲。", "epic")
        ]
        self.skill_books = [
            LootItem("火焰技能书", "学习火焰技能的书籍。", "rare"),
            LootItem("冰冻技能书", "学习冰冻技能的书籍。", "rare"),
            LootItem("治疗技能书", "学习治疗技能的书籍。", "rare")
        ]

    def get_loot(self, enemy_level):
        rarity_roll = random.random()
        if rarity_roll < 0.6:
            loot_list = self.common_loot
        elif rarity_roll < 0.9:
            loot_list = self.rare_loot
        else:
            loot_list = self.epic_loot

        loot = random.choice(loot_list)
        loot.quantity = random.randint(1, 3)
        if enemy_level >= 10 and random.random() < 0.2:
            loot = random.choice(self.skill_books)

        return loot

