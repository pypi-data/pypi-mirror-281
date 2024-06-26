from text_adventure_game.characters.character import Boss, Character
from text_adventure_game.characters.skill import Skill
SCENES = ["森林", "村庄", "城堡", "洞穴", "山脉", "沙漠", "海岸", "火山", "冰原", "沼泽"]
ENEMIES_BY_SCENE = {
    "森林": [
        Character("小哥布林", 30, 3, 1, 2, 3),
        Character("哥布林", 50, 5, 2, 3, 4),
        Character("巨狼", 60, 7, 2, 3, 4),
        Character("树妖", 70, 6, 3, 4, 5),
        Character("毒蛇", 45, 6, 2, 2, 8),
        Character("野猪", 55, 6, 2, 3, 4),
        Character("森林精灵", 65, 8, 3, 4, 6),
    ],
    "村庄": [
        Character("小盗贼", 45, 5, 3, 2, 4),
        Character("盗贼", 65, 6, 4, 3, 5),
        Character("兽人", 80, 8, 3, 4, 5),
        Character("流氓", 55, 5, 3, 3, 6),
        Character("狂战士", 90, 9, 2, 5, 4),
        Character("黑骑士", 100, 10, 4, 5, 6),
        Character("火枪手", 75, 8, 3, 4, 7),
    ],
    "城堡": [
        Character("骷髅新兵", 50, 7, 1, 2, 3),
        Character("骷髅战士", 70, 10, 1, 3, 4),
        Character("恶龙的手下", 100, 12, 5, 3, 4),
        Character("吸血鬼", 85, 11, 3, 5, 6),
        Character("亡灵法师", 75, 10, 4, 6, 3),
        Character("鬼魂", 60, 8, 2, 6, 7),
        Character("黑暗骑士", 120, 14, 5, 4, 5),
    ],
    "洞穴": [
        Character("小蝙蝠", 30, 6, 1, 3, 8),
        Character("巨蝎", 75, 9, 3, 3, 4),
        Character("洞穴兽", 85, 10, 4, 3, 4),
        Character("洞穴蝙蝠", 50, 8, 2, 4, 9),
        Character("地精", 60, 9, 3, 3, 5),
        Character("洞穴蠕虫", 70, 10, 3, 3, 4),
        Character("洞穴巨人", 95, 12, 5, 4, 5),
    ],
    "山脉": [
        Character("山地精灵", 50, 7, 3, 4, 5),
        Character("山地巨人", 120, 15, 6, 3, 4),
        Character("恶龙", 200, 18, 8, 3, 4),
        Character("山地兽人", 110, 14, 4, 5, 5),
        Character("岩石傀儡", 130, 16, 2, 4, 3),
        Character("山鹰", 80, 10, 4, 3, 9),
        Character("山地守卫", 140, 17, 5, 4, 6),
    ],
    "沙漠": [
        Character("小沙盗", 45, 6, 2, 3, 5),
        Character("沙漠强盗", 60, 7, 3, 3, 6),
        Character("沙虫", 70, 9, 2, 4, 8),
        Character("沙漠蜥蜴", 65, 8, 3, 3, 7),
        Character("沙漠巨蝎", 80, 10, 2, 3, 5),
        Character("沙漠法师", 75, 9, 5, 6, 4),
        Character("沙漠战士", 90, 11, 4, 5, 6),
    ],
    "海岸": [
        Character("小海盗", 50, 6, 3, 3, 5),
        Character("海盗", 70, 8, 4, 3, 6),
        Character("鲨鱼", 90, 10, 1, 4, 7),
        Character("海妖", 85, 9, 5, 4, 8),
        Character("海怪", 100, 12, 3, 3, 6),
        Character("水元素", 80, 10, 4, 5, 7),
        Character("海洋巨人", 110, 13, 5, 4, 8),
    ],
    "火山": [
        Character("小火怪", 50, 8, 2, 4, 5),
        Character("火元素", 75, 10, 2, 5, 4),
        Character("岩浆怪", 90, 12, 1, 4, 3),
        Character("熔岩巨人", 110, 14, 2, 3, 4),
        Character("火山恶魔", 130, 16, 3, 4, 5),
        Character("火焰凤凰", 95, 13, 5, 6, 9),
        Character("熔岩领主", 140, 18, 4, 5, 6),
    ],
    "冰原": [
        Character("小冰狼", 40, 6, 2, 3, 8),
        Character("冰狼", 70, 8, 3, 4, 9),
        Character("冰巨人", 130, 16, 5, 4, 5),
        Character("雪怪", 100, 12, 4, 3, 5),
        Character("冰霜幽灵", 85, 10, 2, 7, 6),
        Character("冰霜元素", 75, 11, 3, 6, 4),
        Character("冰霜女王", 140, 17, 4, 6, 7),
    ],
    "沼泽": [
        Character("小沼泽怪", 45, 7, 2, 4, 6),
        Character("沼泽巨蜥", 80, 9, 3, 3, 6),
        Character("毒沼泽怪", 90, 10, 2, 5, 4),
        Character("沼泽女巫", 70, 8, 5, 7, 4),
        Character("沼泽鬼魂", 65, 7, 2, 6, 7),
        Character("毒蜘蛛", 75, 9, 2, 4, 8),
        Character("沼泽领主", 110, 12, 4, 5, 6),
    ],
}

# 为每个BOSS定义独特的技能
fire_boss_skills = [
    Skill("火焰喷射", "对敌人造成火焰伤害。", 15, 25, cooldown=2, mana_cost=20),
    Skill("火焰护盾", "生成火焰护盾，减少接下来的伤害。", 10, 20, cooldown=3, mana_cost=15, skill_type="shield")
]

ice_boss_skills = [
    Skill("冰霜冲击", "对敌人造成冰霜伤害并减速。", 10, 20, cooldown=2, mana_cost=20),
    Skill("冰霜护盾", "生成冰霜护盾，减少接下来的伤害。", 10, 20, cooldown=3, mana_cost=15, skill_type="shield")
]

earth_boss_skills = [
    Skill("地震", "对敌人造成地震伤害。", 20, 30, cooldown=4, mana_cost=25),
    Skill("石肤术", "生成石质护盾，减少接下来的伤害。", 15, 25, cooldown=3, mana_cost=20, skill_type="shield")
]

# 更新BOSSES定义
BOSSES = {
    "森林": Boss("森林之王", 200, 15, 6, 8, 5, skills=[
        Skill("树根缠绕", "用树根缠绕敌人造成伤害。", 10, 20, cooldown=2, mana_cost=15),
        Skill("树皮护盾", "生成树皮护盾，减少接下来的伤害。", 10, 20, cooldown=3, mana_cost=15, skill_type="shield")
    ]),
    "村庄": Boss("盗贼头目", 220, 17, 7, 7, 6, skills=[
        Skill("毒刃", "用毒刃攻击敌人，造成额外毒性伤害。", 15, 25, cooldown=2, mana_cost=20),
        Skill("闪避", "增加自己的闪避率。", 0, 0, cooldown=3, mana_cost=10, skill_type="buff")
    ]),
    "城堡": Boss("恶龙", 300, 20, 8, 10, 5, skills=fire_boss_skills),
    "洞穴": Boss("洞穴领主", 250, 18, 5, 9, 4, skills=earth_boss_skills),
    "山脉": Boss("巨魔王", 350, 22, 5, 15, 8, skills=[
        Skill("巨力挥击", "用巨力攻击敌人，造成大量伤害。", 20, 30, cooldown=3, mana_cost=25),
        Skill("巨人护盾", "生成巨人护盾，减少接下来的伤害。", 15, 25, cooldown=3, mana_cost=20, skill_type="shield")
    ]),
    "沙漠": Boss("沙漠之主", 270, 19, 6, 11, 7, skills=[
        Skill("沙尘暴", "召唤沙尘暴对敌人造成伤害。", 15, 25, cooldown=3, mana_cost=20),
        Skill("沙漠护盾", "生成沙漠护盾，减少接下来的伤害。", 10, 20, cooldown=3, mana_cost=15, skill_type="shield")
    ]),
    "海岸": Boss("海洋之王", 280, 20, 7, 12, 6, skills=[
        Skill("水流冲击", "用水流冲击敌人，造成伤害。", 15, 25, cooldown=2, mana_cost=20),
        Skill("水之护盾", "生成水之护盾，减少接下来的伤害。", 10, 20, cooldown=3, mana_cost=15, skill_type="shield")
    ]),
    "火山": Boss("火山之主", 320, 21, 6, 13, 8, skills=fire_boss_skills),
    "冰原": Boss("冰霜之王", 300, 18, 5, 14, 7, skills=ice_boss_skills),
    "沼泽": Boss("沼泽之王", 280, 17, 5, 12, 8, skills=[
        Skill("毒液喷射", "喷射毒液对敌人造成伤害。", 15, 25, cooldown=3, mana_cost=20),
        Skill("毒雾护盾", "生成毒雾护盾，减少接下来的伤害。", 10, 20, cooldown=3, mana_cost=15, skill_type="shield")
    ]),
}

LOVE_INTERESTS_BY_SCENE = {
    "森林": [
        Character("艾米丽", 100, 8, 8, 10, 5),
        Character("伊丽莎白", 100, 7, 9, 10, 5)
    ],
    "村庄": [
        Character("凯瑟琳", 100, 9, 7, 10, 5),
        Character("朱莉娅", 100, 6, 10, 10, 5)
    ],
    "城堡": [
        Character("维多利亚", 100, 8, 8, 10, 5),
        Character("安娜", 100, 7, 9, 10, 5)
    ],
    "洞穴": [
        Character("索菲亚", 100, 9, 7, 10, 5),
        Character("克莱尔", 100, 6, 10, 10, 5)
    ],
    "山脉": [
        Character("玛丽亚", 100, 8, 9, 10, 5),
        Character("艾琳", 100, 9, 8, 10, 5)
    ],
    "沙漠": [
        Character("露西", 100, 7, 9, 10, 5),
        Character("奥莉薇亚", 100, 8, 8, 10, 5)
    ],
    "海岸": [
        Character("米娅", 100, 9, 7, 10, 5),
        Character("艾莉西亚", 100, 6, 10, 10, 5)
    ],
    "火山": [
        Character("贝拉", 100, 8, 8, 10, 5),
        Character("艾莉", 100, 9, 9, 10, 5)
    ],
    "冰原": [
        Character("娜塔莎", 100, 7, 8, 10, 5),
        Character("凯特", 100, 8, 9, 10, 5)
    ],
    "沼泽": [
        Character("丽莎", 100, 9, 7, 10, 5),
        Character("伊娃", 100, 6, 10, 10, 5)
    ]
}
