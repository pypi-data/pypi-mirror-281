import random

class Relationship:
    def __init__(self, player, character, relationship_type="陌生人"):
        self.player = player
        self.character = character
        self.relationship_type = relationship_type
        self.affection = 0 

    def interact(self):
        descriptions = {
            "陌生人": "刚刚认识你",
            "朋友": "对你有些了解",
            "好友": "对你非常信任",
            "恋人": "对你爱慕无比",
            "配偶": "与你形影不离",
            "敌人": "与你势不两立"
        }
        print(f"你遇到了{self.character.name}，他/她{descriptions[self.relationship_type]}。")
        print("选择互动方式：")
        options = self.get_interaction_options()
        for i, option in enumerate(options.keys(), 1):
            print(f"{i}. {option}")
        action = input(f"请输入选项（1-{len(options)}）：")
        if action.isdigit() and 1 <= int(action) <= len(options):
            method_name = options[list(options.keys())[int(action) - 1]]
            if hasattr(self, method_name):
                getattr(self, method_name)()
            else:
                print("无效的选择，请重新输入。")
        else:
            print("无效的选择，请重新输入。")

    def get_interaction_options(self):
        options = {"谈话": "talk"}
        if self.relationship_type in ["朋友", "好友", "恋人", "配偶"]:
            options["赠送礼物"] = "give_gift"
            options["请求帮助"] = "ask_for_help"
        if self.relationship_type in ["恋人", "配偶"]:
            options["邀请约会"] = "date"
            options["表达爱意"] = "express_love"
        if self.relationship_type == "敌人":
            options["挑衅"] = "provoke"
        if self.relationship_type == "陌生人":
            options["认识"] = "meet"
        return options

    def talk(self):
        print(f"你和{self.character.name}聊了一会儿。")
        if random.random() < (self.player.charm / 10):
            self.affection += 5
            print(f"{self.character.name}对你的好感增加了！当前好感度：{self.affection}")
            if self.affection >= 10:
                self.develop_relationship()
        else:
            print(f"{self.character.name}似乎对谈话不太感兴趣。当前好感度：{self.affection}")

    def give_gift(self):
        gifts = ["花", "巧克力", "首饰", "书籍", "香水"]
        gift = random.choice(gifts)
        print(f"你送了{self.character.name}一份礼物：{gift}。")
        if random.random() < (self.player.charm / 8):
            self.affection += 10
            print(f"{self.character.name}非常喜欢这份礼物！当前好感度：{self.affection}")
        else:
            print(f"{self.character.name}接受了礼物，但似乎不太满意。当前好感度：{self.affection}")
        if self.affection >= 10:
            self.develop_relationship()

    def date(self):
        if self.relationship_type in ["恋人", "配偶"]:
            print(f"你邀请{self.character.name}一起出去玩。")
            if random.random() < (self.player.charm / 6):
                self.affection += 15
                print(f"{self.character.name}度过了愉快的时光！当前好感度：{self.affection}")
            else:
                print(f"{self.character.name}拒绝了你的邀请。当前好感度：{self.affection}")
        else:
            print(f"你不能邀请{self.character.name}约会，因为他/她不是你的恋人或配偶。")

    def ask_for_help(self):
        print(f"你请求{self.character.name}帮助你。")
        if random.random() < (self.player.charm / 7):
            self.affection += 8
            print(f"{self.character.name}欣然同意帮助你！当前好感度：{self.affection}")
            if self.character.health > 0:
                damage = self.character.attack(self.player.current_enemy)
                print(f"{self.character.name}在战斗中对{self.player.current_enemy.name}造成了{damage}点伤害。")
            else:
                print(f"{self.character.name}状态不佳，无法提供帮助。")
        else:
            print(f"{self.character.name}拒绝了你的请求。当前好感度：{self.affection}")

    def express_love(self):
        if self.relationship_type in ["恋人", "配偶"]:
            print(f"你向{self.character.name}表达了爱意。")
            if random.random() < (self.player.charm / 5):
                self.affection += 20
                print(f"{self.character.name}被你的真情打动，对你的好感大幅提升！当前好感度：{self.affection}")
            else:
                self.affection -= 5
                print(f"{self.character.name}对你的表白并不感兴趣。当前好感度：{self.affection}")
        else:
            print(f"你不能向{self.character.name}表达爱意，因为他/她不是你的恋人或配偶。")

    def provoke(self):
        if self.relationship_type == "敌人":
            print(f"你挑衅了{self.character.name}。")
            if random.random() < (self.player.strength / 10):
                self.affection -= 10
                print(f"{self.character.name}被你的挑衅激怒了！当前好感度：{self.affection}")
            else:
                self.affection += 5
                print(f"{self.character.name}被你的挑衅激怒，但对你的好感反而增加了。当前好感度：{self.affection}")
        else:
            print(f"你不能挑衅{self.character.name}，因为他/她不是你的敌人。")

    def meet(self):
        print(f"你和{self.character.name}互相认识了一下。")
        self.affection += 5
        if self.affection >= 10:
            self.develop_relationship()
        print(f"{self.character.name}对你的好感增加了！当前好感度：{self.affection}")

    def develop_relationship(self):
        if self.affection >= 10 and self.relationship_type == "陌生人":
            print(f"{self.character.name}现在是你的朋友了！")
            self.relationship_type = "朋友"
        elif self.affection >= 50 and self.relationship_type == "朋友":
            print(f"{self.character.name}现在是你的好友了！")
            self.relationship_type = "好友"
        elif self.affection >= 100 and self.relationship_type == "好友":
            print(f"{self.character.name}现在是你的恋人了！")
            self.relationship_type = "恋人"
        elif self.affection >= 200 and self.relationship_type == "恋人":
            print(f"{self.character.name}现在是你的配偶了！")
            self.relationship_type = "配偶"
        elif self.affection <= -10 and self.relationship_type == "陌生人":
            print(f"{self.character.name}现在是你的敌人了！")
            self.relationship_type = "敌人"

    def check_affection(self):
        print(f"{self.character.name}的当前好感度：{self.affection}，关系：{self.relationship_type}")
