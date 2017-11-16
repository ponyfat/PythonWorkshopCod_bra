from PIL import Image, ImageDraw
import os

LineWidth = 3


class PicField:
    def __init__(self):
        self.step = 0
        self.pic_height = 0
        self.pic_width = 0
        self.pic_name = ''

    def new_field(self, name, height, width):
        self.step = max(500 // height, 500 // width)
        self.pic_height = self.step * width
        self.pic_width = self.step * height
        self.image = Image.new('RGB', (self.pic_height, self.pic_width),
                               color='grey')
        self.draw = ImageDraw.Draw(self.image)
        self.draw_vertical_lines(height)
        self.draw_horizontal_lines(width)
        self.pic_name = 'users/{}'.format(name)
        self.image.save(self.pic_name, 'JPEG')

    def draw_vertical_lines(self, width):
        for i in range(0, width):
            self.draw.line([(0, i * self.step),
                            (self.pic_height, i * self.step)],
                           fill='black',
                           width=LineWidth)

    def draw_horizontal_lines(self, height):
        for j in range(0, height):
            self.draw.line([(j * self.step, 0),
                            (j * self.step, self.pic_width)],
                           fill='black',
                           width=LineWidth)

    def draw_number(self, x, y, number):
        num_pic = Image.open('/'.join([os.getcwd(), 'numbers/{}.jpg'.format(str(number))]))
        num_pic = num_pic.resize((self.step - 2 * LineWidth + 1, self.step -
                                  2 * LineWidth + 1))
        self.image.paste(num_pic, box=(self.step * y + 3, self.step * x + 3))
        self.image.save(self.pic_name, 'JPEG')

    def draw_bomb(self, x, y):
        bomb_pic = Image.open('/'.join([os.getcwd(), 'bombs/bomb.jpg']))
        bomb_pic = bomb_pic.resize((self.step - 2 * LineWidth + 1, self.step -
                                    2 * LineWidth + 1))
        self.image.paste(bomb_pic, box=(self.step * y + 3, self.step * x + 3))
        self.image.save(self.pic_name, 'JPEG')

    def draw_exploded_bomb(self, x, y):
        bomb_pic = Image.open('/'.join([os.getcwd(), 'bombs/ex_bomb.jpg']))
        bomb_pic = bomb_pic.resize((self.step - 2 * LineWidth + 1, self.step -
                                    2 * LineWidth + 1))
        self.image.paste(bomb_pic, box=(self.step * y + 3, self.step * x + 3))
        self.image.save(self.pic_name, 'JPEG')

    def draw_flag(self, x, y):
        flag_pic = Image.open('/'.join([os.getcwd(), 'flags/flag.jpg']))
        flag_pic = flag_pic.resize((self.step - 2 * LineWidth + 1, self.step -
                                    2 * LineWidth + 1))
        self.image.paste(flag_pic, box=(self.step * y + 3, self.step * x + 3))
        self.image.save(self.pic_name, 'JPEG')

    def remove_flag(self, x, y):
        flag_pic = Image.open('/'.join([os.getcwd(), 'flags/remove_flag.jpg']))
        flag_pic = flag_pic.resize((self.step - 2 * LineWidth + 1, self.step -
                                    2 * LineWidth + 1))
        self.image.paste(flag_pic, box=(self.step * y + 3, self.step * x + 3))
        self.image.save(self.pic_name, 'JPEG')
