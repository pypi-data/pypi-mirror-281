import random
class LootItem:
    def __init__(self, name, description, rarity, quantity=1, item_type="generic", attributes=None, slot=None):
        self.name = name
        self.description = description
        self.rarity = rarity
        self.quantity = quantity
        self.item_type = item_type
        self.attributes = attributes if attributes else {}
        self.slot = slot

    def __str__(self):
        quantity_str = f" x{self.quantity}" if self.quantity > 1 else ""
        return f"{self.name} ({self.rarity}): {self.description}{quantity_str}"

    def use(self, character):
        if self.item_type == "potion":
            self.apply_potion_effect(character)
        elif self.item_type == "weapon":
            print(f"{self.name} 是一种武器，可以装备在装备栏中。")
        elif self.item_type == "armor":
            print(f"{self.name} 是一种护甲，可以装备在装备栏中。")
        elif self.item_type == "skill_book":
            print(f"{self.name} 是一本技能书，可以学习新的技能。")
        elif self.item_type == "mount":
            print(f"{self.name} 是一种坐骑，可以装备在坐骑栏中。")
        elif self.item_type == "ammunition":
            print(f"{self.name} 是一种消耗品，用于远程武器。")
        else:
            print(f"{self.name} 无法使用。")

    def apply_potion_effect(self, character):
        if self.name == "治疗药剂":
            character.health = min(character.max_health, character.health + 20)
            print(f"{character.name} 使用了 {self.name}，恢复了 20 点生命值。")
            self.quantity -= 1
        elif self.name == "力量药水":
            character.strength += 5
            print(f"{character.name} 使用了 {self.name}，力量增加了 5 点。")
            self.quantity -= 1
        elif self.name == "敏捷药水":
            character.agility += 5
            print(f"{character.name} 使用了 {self.name}，敏捷增加了 5 点。")
            self.quantity -= 1
        elif self.name == "智力药水":
            character.intelligence += 5
            print(f"{character.name} 使用了 {self.name}，智力增加了 5 点。")
            self.quantity -= 1
        # 添加更多药水的效果
        else:
            print(f"{self.name} 无法使用。")

from text_adventure_game.inventory.items import LootItem

# 扩展后的常见战利品
common_loot = [
    LootItem("金币", "普通的货币，可以用来购买物品。", "common"),
    LootItem("治疗药剂", "恢复少量生命值的药剂。", "common", item_type="potion"),
    LootItem("力量药水", "暂时增加力量的药水。", "common", item_type="potion"),
    LootItem("敏捷药水", "暂时增加敏捷的药水。", "common", item_type="potion"),
    LootItem("智力药水", "暂时增加智力的药水。", "common", item_type="potion"),
    LootItem("短剑", "普通的短剑。", "common", item_type="weapon", attributes={"damage": 3}),
    LootItem("木盾", "普通的木盾。", "common", item_type="weapon", attributes={"defense": 2}),
    LootItem("皮甲", "普通的皮甲。", "common", item_type="armor", attributes={"defense": 4}, slot="身"),
    LootItem("布帽", "普通的布帽。", "common", item_type="armor", attributes={"defense": 1}, slot="头"),
    LootItem("箭", "用于弓的箭。", "common", item_type="ammunition", quantity=20, attributes={"damage": 2}),
    LootItem("弩箭", "用于弩的箭。", "common", item_type="ammunition", quantity=15, attributes={"damage": 3}),
    LootItem("草药", "可以用于制作简单的药剂。", "common", item_type="ingredient"),
    LootItem("小盾牌", "简单的防御装备。", "common", item_type="shield", attributes={"defense": 3}),
]

# 扩展后的稀有战利品
rare_loot = [
    LootItem("钢匕首", "锋利的钢匕首。", "rare", item_type="weapon", attributes={"damage": 5}),
    LootItem("长弓", "远程攻击用的长弓。", "rare", item_type="weapon", attributes={"damage": 7}),
    LootItem("弩", "强力的弩。", "rare", item_type="weapon", attributes={"damage": 8}),
    LootItem("铁盔", "提供额外防护的铁盔。", "rare", item_type="armor", attributes={"defense": 5}, slot="头"),
    LootItem("锁子甲", "提供额外防护的锁子甲。", "rare", item_type="armor", attributes={"defense": 8}, slot="身"),
    LootItem("火焰技能书", "学习火焰技能的书籍。", "rare", item_type="skill_book", attributes={"skill": {"name": "火焰喷射", "description": "对敌人造成火焰伤害", "min_damage": 10, "max_damage": 20}}),
    LootItem("战马", "强壮的战马，可以增加移动速度。", "rare", item_type="mount", attributes={"speed": 10}),
    LootItem("箭", "高质量的箭。", "rare", item_type="ammunition", quantity=30, attributes={"damage": 4}),
    LootItem("弩箭", "高质量的弩箭。", "rare", item_type="ammunition", quantity=20, attributes={"damage": 5}),
    LootItem("魔法卷轴", "可以施放一次性魔法的卷轴。", "rare", item_type="scroll"),
    LootItem("治疗药水", "恢复大量生命值的药水。", "rare", item_type="potion"),
]

# 扩展后的史诗级战利品
epic_loot = [
    LootItem("精钢长剑", "拥有强大力量的精钢长剑。", "epic", item_type="weapon", attributes={"damage": 12}),
    LootItem("冰霜弓", "拥有冰霜力量的弓。", "epic", item_type="weapon", attributes={"damage": 15}),
    LootItem("龙鳞甲", "提供极高防护的龙鳞甲。", "epic", item_type="armor", attributes={"defense": 15}, slot="身"),
    LootItem("冰冻技能书", "学习冰冻技能的书籍。", "epic", item_type="skill_book", attributes={"skill": {"name": "冰冻冲击", "description": "对敌人造成冰冻伤害并减速", "min_damage": 15, "max_damage": 25}}),
    LootItem("神圣头盔", "提供极高防护的神圣头盔。", "epic", item_type="armor", attributes={"defense": 12}, slot="头"),
    LootItem("战斗马", "强壮的战斗马，可以增加移动速度和攻击力。", "epic", item_type="mount", attributes={"speed": 15, "attack": 5}),
    LootItem("箭", "传说中的箭。", "epic", item_type="ammunition", quantity=50, attributes={"damage": 6}),
    LootItem("弩箭", "传说中的弩箭。", "epic", item_type="ammunition", quantity=40, attributes={"damage": 7}),
    LootItem("神圣卷轴", "可以施放强大魔法的卷轴。", "epic", item_type="scroll"),
    LootItem("力量之戒", "增加佩戴者的力量。", "epic", item_type="ring", attributes={"strength": 5}),
    LootItem("守护护符", "提供额外防护的护符。", "epic", item_type="amulet", attributes={"defense": 5}),
]

# 扩展后的技能书定义
skill_books = [
    LootItem("治疗技能书", "学习治疗技能的书籍。", "rare", item_type="skill_book", attributes={"skill": {"name": "治疗术", "description": "恢复生命值", "heal": 20}}),
    LootItem("旋风斩技能书", "学习旋风斩技能的书籍。", "epic", item_type="skill_book", attributes={"skill": {"name": "旋风斩", "description": "对敌人造成旋风斩伤害", "min_damage": 20, "max_damage": 30}}),
    LootItem("闪电箭技能书", "学习闪电箭技能的书籍。", "epic", item_type="skill_book", attributes={"skill": {"name": "闪电箭", "description": "对敌人造成闪电伤害", "min_damage": 15, "max_damage": 25}}),
    LootItem("隐身技能书", "学习隐身技能的书籍。", "rare", item_type="skill_book", attributes={"skill": {"name": "隐身术", "description": "使你在短时间内隐身", "duration": 5}}),
]


class LootManager:
    def __init__(self):
        self.common_loot = common_loot
        self.rare_loot = rare_loot
        self.epic_loot = epic_loot
        self.skill_books = skill_books

    def get_loot(self, enemy):
        loot_list = []
        if enemy.level < 10:
            loot_list = self.common_loot
        elif enemy.level < 20:
            loot_list = self.common_loot + self.rare_loot
        else:
            loot_list = self.common_loot + self.rare_loot + self.epic_loot

        if enemy.skills:
            loot_list += self.skill_books

        # 增加金币的掉落
        if random.random() < 0.5:  # 50%的概率掉落金币
            loot_list.append(LootItem("金币", "普通的货币，可以用来购买物品。", "common", quantity=random.randint(1, 5)))

        loot = random.choice(loot_list)
        if loot.item_type in ["ammunition", "potion"]:
            loot.quantity = random.randint(1, 3)

        return loot

