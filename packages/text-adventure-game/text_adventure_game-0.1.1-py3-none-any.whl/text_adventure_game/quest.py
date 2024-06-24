import random

class Quest:
    def __init__(self, name, description, reward, experience, difficulty):
        self.name = name
        self.description = description
        self.reward = reward
        self.experience = experience
        self.difficulty = difficulty
        self.completed = False

    def start(self):
        print(f"任务开始：{self.name}")
        print(f"描述：{self.description}")

    def complete(self):
        self.completed = True
        print(f"任务完成：{self.name}")
        return self.reward, self.experience

class QuestManager:
    def __init__(self):
        self.quests = [
            Quest("寻找失踪的戒指", "帮助村民寻找失踪的戒指。", "神秘宝石", 20, "简单"),
            Quest("消灭洞穴中的兽人", "前往洞穴消灭所有的兽人。", "强力武器", 30, "中等"),
            Quest("解救被困的村民", "在森林中解救被困的村民。", "健康药剂", 25, "中等"),
            Quest("讨伐恶龙", "前往山顶讨伐恶龙。", "传说武器", 50, "困难")
        ]
        self.active_quests = []

    def get_new_quest(self):
        if not self.quests:
            print("目前没有可用的新任务。")
            return None
        quest = random.choice(self.quests)
        self.quests.remove(quest)
        self.active_quests.append(quest)
        quest.start()
        return quest

    def complete_quest(self, quest):
        if quest in self.active_quests:
            reward, experience = quest.complete()
            self.active_quests.remove(quest)
            return reward, experience
        else:
            print("这个任务未被接受或已完成。")
            return None, None

    def list_active_quests(self):
        if not self.active_quests:
            print("目前没有进行中的任务。")
        else:
            print("进行中的任务：")
            for quest in self.active_quests:
                print(f"{quest.name} - {quest.description} (难度：{quest.difficulty})")

    def list_completed_quests(self):
        completed = [quest for quest in self.active_quests if quest.completed]
        if not completed:
            print("目前没有完成的任务。")
        else:
            print("已完成的任务：")
            for quest in completed:
                print(f"{quest.name} - {quest.description} (难度：{quest.difficulty})")

    def manage_quests(self):
        print("任务管理：")
        print("1. 查看进行中的任务")
        print("2. 接受新任务")
        print("3. 完成任务")
        print("4. 查看已完成的任务")
        action = input("请输入选项（1-4）：")
        if action == "1":
            self.list_active_quests()
        elif action == "2":
            quest = self.get_new_quest()
            if quest:
                self.list_active_quests()
        elif action == "3":
            quest_name = input("请输入要完成的任务名称：")
            for quest in self.active_quests:
                if quest.name == quest_name:
                    reward, experience = self.complete_quest(quest)
                    if reward and experience:
                        self.game.player.inventory.append(reward)
                        self.game.player.gain_experience(experience)
                    break
            else:
                print("未找到对应的任务。")
        elif action == "4":
            self.list_completed_quests()
        else:
            print("无效的选择，请重新输入。")
