class Skill:
    def __init__(self, name, description, min_damage=0, max_damage=0, cooldown=0, mana_cost=0, skill_type="attack", special_effects=None):
        self.name = name
        self.description = description
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.cooldown = cooldown
        self.mana_cost = mana_cost
        self.skill_type = skill_type
        self.special_effects = special_effects or {}
        self.current_cooldown = 0

    def __str__(self):
        effects = ', '.join([f"{key}: {value}" for key, value in self.special_effects.items()])
        return f"{self.name}: {self.description} - Damage: {self.min_damage}-{self.max_damage}, Cooldown: {self.cooldown}, Mana Cost: {self.mana_cost}, Type: {self.skill_type}, Effects: {effects}"

    def is_available(self):
        return self.current_cooldown == 0

    def use(self):
        if self.is_available():
            self.current_cooldown = self.cooldown
            return True
        return False

    def cooldown_tick(self):
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

            
class SkillBook:
    def __init__(self, name, description, skill, requirement):
        self.name = name
        self.description = description
        self.skill = skill
        self.requirement = requirement

    def __str__(self):
        return f"{self.name}: {self.description} - 技能: {self.skill}"       
       
def basic_requirement(character):
    return character.level >= 1 and character.strength >= 5

def advanced_requirement(character):
    return character.level >= 5 and character.intelligence >= 10

def expert_requirement(character):
    return character.level >= 10 and character.agility >= 15   
     
SKILL_BOOKS = [
    SkillBook("猛击秘籍", "学习后可以使用猛击技能。", 
              Skill("猛击", "对敌人造成大量伤害。", 10, 20, skill_type="attack"), basic_requirement),
    SkillBook("旋风斩秘籍", "学习后可以使用旋风斩技能。", 
              Skill("旋风斩", "对敌人造成中等伤害。", 5, 15, skill_type="attack"), basic_requirement),
    SkillBook("火球术秘籍", "学习后可以使用火球术技能。", 
              Skill("火球术", "对敌人造成高额火焰伤害。", 15, 25, cooldown=3, mana_cost=20, skill_type="attack"), advanced_requirement),
    SkillBook("影分身秘籍", "学习后可以使用影分身技能。", 
              Skill("影分身", "快速攻击敌人多次。", 10, 30, skill_type="attack", special_effects={"multiple_hits": True}), expert_requirement),
    SkillBook("治疗术秘籍", "学习后可以使用治疗术技能。", 
              Skill("治疗术", "恢复一定量的生命值。", 10, 20, cooldown=2, mana_cost=15, skill_type="heal"), basic_requirement),
    SkillBook("护盾术秘籍", "学习后可以使用护盾术技能。", 
              Skill("护盾术", "为自己或队友提供一个护盾。", 0, 0, cooldown=5, mana_cost=20, skill_type="buff", special_effects={"shield": 30}), advanced_requirement),
]
