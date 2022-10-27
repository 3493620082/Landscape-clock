# --coding=utf-8
import sys

import pygame

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("demo_1")
        self.f1 = pygame.font.Font("AGENCYR.TTF", 75)
        self.f2 = pygame.font.Font("bahnschrift.ttf", 20)
        self.watches = pygame.Surface((256, 144)).convert_alpha()
        self.watches_rect = self.watches.get_rect()
        # print(self.watches_rect)  # (0, 0, 128, 72)
        self.background = pygame.image.load("peaks-of-mount-whitney-zn-1280x720.jpg").convert()
        pygame.mixer.music.load("midnight city.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()

        self.clock = pygame.time.Clock()

        self.time_0_count = 0  # 秒，可修改
        self.time_1_count = 0  # 分钟，可修改
        self.time_1_count_real = 0  # 实际显示
        self.time_2_count = 0  # 小时，可修改
        self.date_0_count = 1  # 天，可修改
        self.date_1_count = 1  # 月，可修改
        self.date_2_count = 1990  # 年，可修改
        # self.season_text = ""  # 春夏秋冬供选择，因为不用参与计算所以不当做数值变量
        self.week_count = 1  # 代表星期几的数字，不要轻易修改

        while True:
            self.clock.tick(60)  # 帧率，可以修改，加速的话推荐600帧。好像不能超过1000，否则后面的数就无效了，该多少帧还是多少帧
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.watch_time_text = self.time_change()
            self.watch_date_text = self.date_change()

            self.watch_time = self.f1.render(self.watch_time_text, True, (255, 255, 255))
            self.watch_time_rect = self.watch_time.get_rect()
            self.watch_date = self.f2.render(self.watch_date_text, True, (255, 255, 255))
            self.watch_date_rect = self.watch_date.get_rect()

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.watches, (1280 / 2 - self.watches_rect[2] / 2, 720 / 2 - self.watches_rect[3] / 2))
            self.watches.fill((0, 0, 0, 85))
            pygame.draw.rect(self.watches, (255, 255, 255), (0, 0, self.watches_rect[2], self.watches_rect[3]), 1)
            # self.watches.blit(self.watch_time, (self.watches_rect[2] / 2 - self.watch_time_rect[2] / 2, self.watches_rect[3] / 2 - self.watch_time_rect[3] / 2))
            self.watches.blit(self.watch_time, (self.watches_rect[2] / 2 - self.watch_time_rect[2] / 2, 0))
            self.watches.blit(self.watch_date, (self.watches_rect[2] / 2 - self.watch_date_rect[2] / 2, self.watches_rect[3] / 2 + self.watch_date_rect[3]))

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()

            pygame.display.update()

    def time_change(self):
        self.time_0_count += 10  # 一帧加1秒，可以修改，最多60
        if self.time_0_count == 60:  # 如果达到了60秒，则归0
            self.time_0_count = 0  # 将秒数归0
            self.time_1_count += 1  # 将分钟加1
        if self.time_1_count == 60:  # 如果时间到了60分钟，则归0进1
            self.time_1_count = 0  # 将分钟归0
            self.time_2_count += 1  # 将小时加1
        if self.time_1_count % 10 == 0:  # 如果分钟能整除10就将给time_1_count_real变量改变值
            if self.time_1_count == 0:  # 如果是0分钟的话就在前面加上一个0再显示，这样会美观一些
                self.time_1_count_real = "0" + str(self.time_1_count)
            else:  # 不为0的话就正常显示
                self.time_1_count_real = str(self.time_1_count)
        if self.time_2_count == 24:  # 时间到了24小时，归0进1
            self.time_2_count = 0  # 小时数归0
            self.date_0_count += 1  # 将日期加1
            self.week_count += 1  # 将星期加1
            if self.week_count == 8:
                self.week_count = 1
        if self.time_2_count < 10:
            return "0" + str(self.time_2_count) + " : " + str(self.time_1_count_real)
        else:
            return str(self.time_2_count) + " : " + str(self.time_1_count_real)

    def date_change(self):
        if self.date_1_count == 1 or self.date_1_count == 3 or self.date_1_count == 5 or self.date_1_count == 7 or self.date_1_count == 8 or self.date_1_count == 10 or self.date_1_count == 12:
            if self.date_0_count == 32:
                self.date_0_count = 1
                self.date_1_count += 1
        elif self.date_1_count == 4 or self.date_1_count == 6 or self.date_1_count == 9 or self.date_1_count == 11:
            if self.date_0_count == 31:
                self.date_0_count = 1
                self.date_1_count += 1
        elif self.date_1_count == 2:  # 2月特殊情况的计算
            if self.date_2_count % 4 == 0 and self.date_2_count % 100 != 0:
                if self.date_0_count == 29:
                    self.date_0_count = 1
                    self.date_1_count += 1
            elif self.date_2_count % 400 == 0:
                if self.date_0_count == 30:
                    self.date_0_count = 1
                    self.date_1_count += 1
            else:
                if self.date_0_count == 29:
                    self.date_0_count = 1
                    self.date_1_count += 1
        if self.date_1_count == 13:  # 如果月份到达了13月则归1，然后年份加1
            self.date_1_count = 1
            self.date_2_count += 1
        # if self.date_1_count == 3 or self.date_1_count == 4 or self.date_1_count == 5:
        #     self.season_text = "Spring"
        # elif self.date_1_count == 6 or self.date_1_count == 7 or self.date_1_count == 8:
        #     self.season_text = "Summer"
        # elif self.date_1_count == 9 or self.date_1_count == 10 or self.date_1_count == 11:
        #     self.season_text = "Autumn"
        # elif self.date_1_count == 12 or self.date_1_count == 1 or self.date_1_count == 2:
        #     self.season_text = "Winter"
        if  self.week_count == 1:
            self.week_text = "Monday"
        elif  self.week_count == 2:
            self.week_text = "Tuesday"
        elif  self.week_count == 3:
            self.week_text = "Wednesday"
        elif  self.week_count == 4:
            self.week_text = "Thursday"
        elif  self.week_count == 5:
            self.week_text = "Friday"
        elif  self.week_count == 6:
            self.week_text = "Saturday"
        elif  self.week_count == 7:
            self.week_text = "Sunday"

        if self.date_1_count < 10 and self.date_0_count < 10:
            return str(self.date_2_count) + " / 0" + str(self.date_1_count) + " / 0" + str(self.date_0_count) + "    " + self.week_text
        elif self.date_1_count < 10:
            return str(self.date_2_count) + " / 0" + str(self.date_1_count) + " / " + str(self.date_0_count) + "    " + self.week_text
        elif self.date_0_count < 10:
            return str(self.date_2_count) + " / " + str(self.date_1_count) + " / 0" + str(self.date_0_count) + "    " + self.week_text

App()