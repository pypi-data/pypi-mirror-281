class SkillBook:
    def __init__(self, name, description, skill, requirement):
        self.name = name
        self.description = description
        self.skill = skill
        self.requirement = requirement

    def __str__(self):
        return f"{self.name}: {self.description} - 技能: {self.skill['name']} ({self.skill['description']})"

def basic_requirement(character):
    return character.level >= 1 and character.strength >= 5

def advanced_requirement(character):
    return character.level >= 5 and character.intelligence >= 10

def expert_requirement(character):
    return character.level >= 10 and character.agility >= 15

SKILL_BOOKS = [
    SkillBook("猛击秘籍", "学习后可以使用猛击技能。", {"name": "猛击", "description": "对敌人造成大量伤害。", "min_damage": 10, "max_damage": 20}, basic_requirement),
    SkillBook("旋风斩秘籍", "学习后可以使用旋风斩技能。", {"name": "旋风斩", "description": "对敌人造成中等伤害。", "min_damage": 5, "max_damage": 15}, basic_requirement),
    SkillBook("火球术秘籍", "学习后可以使用火球术技能。", {"name": "火球术", "description": "对敌人造成高额火焰伤害。", "min_damage": 15, "max_damage": 25}, advanced_requirement),
    SkillBook("影分身秘籍", "学习后可以使用影分身技能。", {"name": "影分身", "description": "快速攻击敌人多次。", "min_damage": 10, "max_damage": 30}, expert_requirement)
]
