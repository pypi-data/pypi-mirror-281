import random

class Character:
    def __init__(self, name, health, strength, charm, intelligence, agility, skills=None, level=1):
        self.name = name
        self.health = health
        self.max_health = health
        self.strength = strength
        self.charm = charm
        self.intelligence = intelligence
        self.agility = agility
        self.level = level
        self.skills = skills if skills else []
        self.experience = 0
        self.inventory = []

    def attack(self, target):
        damage = random.randint(1, self.strength)
        target.health -= damage
        return damage

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.level * 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.max_health += 10
        self.health = self.max_health
        self.strength += 2
        self.charm += 1
        self.intelligence += 1
        self.agility += 1
        print(f"{self.name}升级了！现在的等级是：{self.level}，最大生命值增加到：{self.max_health}，力量增加到：{self.strength}，魅力增加到：{self.charm}，智力增加到：{self.intelligence}，敏捷增加到：{self.agility}。")

    def learn_skill(self, skill_book):
        if skill_book.requirement(self):
            self.skills.append(skill_book.skill)
            print(f"{self.name}学习了新技能：{skill_book.skill['name']}。")
        else:
            print(f"{self.name}未能学习技能：{skill_book.skill['name']}。需要更高的属性。")

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
            damage = random.randint(skill['min_damage'], skill['max_damage'])
            target.health -= damage
            print(f"{self.name}使用了技能 {skill['name']}，对{target.name}造成了{damage}点伤害。")
            return damage
        else:
            print("无效的选择，请重新输入。")
            return 0

class Boss(Character):
    def __init__(self, name, health, strength, charm, intelligence, agility, level=1):
        super().__init__(name, health, strength, charm, intelligence, agility, [], level)
        self.skills = ["火焰喷射", "地震", "召唤骷髅战士"]

    def use_skill(self, target):
        skill = random.choice(self.skills)
        if skill == "召唤骷髅战士":
            print(f"{self.name}使用了技能 {skill}，召唤了一个骷髅战士！")
            return Character("骷髅战士", 50, 10, 1, 3, 4)
        else:
            damage = random.randint(10, 25)
            target.health -= damage
            print(f"{self.name}使用了技能 {skill}，对{target.name}造成了{damage}点伤害。")
            return damage
