from pynput import keyboard, mouse
from datetime import datetime, timedelta
import logging
import os
import time

class InputLogger:
    def __init__(self):
        self.last_move_time = time.time()
        self.last_position = (0, 0)
        self.move_threshold = 50  #
        self.time_threshold = 600  #
        self.setup_logger()

    def setup_logger(self, log_dir='logs'):
        # 创建日志目录
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 生成日志文件名（使用当前时间）
        log_file = os.path.join(log_dir, f'input_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        
        # 配置日志格式
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def calculate_distance(self, pos1, pos2):
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

    def on_press(self, key):
        try:
            # 常规按键
            logging.info(f'Key pressed: {key.char}')
        except AttributeError:
            # 特殊按键（如ctrl, shift等）
            logging.info(f'Special key pressed: {key}')

    def on_release(self, key):
        if key == keyboard.Key.esc:
            return False

    def on_click(self, x, y, button, pressed):
        action = 'pressed' if pressed else 'released'
        logging.info(f'Mouse {action} at ({x}, {y}) with {button}')
        self.last_position = (x, y)

    def on_move(self, x, y):
        current_time = time.time()
        current_pos = (x, y)
        
        # 计算距离上次记录的移动距离
        distance = self.calculate_distance(current_pos, self.last_position)
        time_diff = current_time - self.last_move_time

        # 如果移动距离超过阈值或时间超过阈值，则记录
        if distance > self.move_threshold or time_diff > self.time_threshold:
            logging.info(f'Mouse moved to ({x}, {y})')
            self.last_position = current_pos
            self.last_move_time = current_time

    def on_scroll(self, x, y, dx, dy):
        logging.info(f'Mouse scrolled {"down" if dy < 0 else "up"} at ({x}, {y})')

    def start(self):
        # 创建监听器
        keyboard_listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        
        mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )
        
        # 启动
        keyboard_listener.start()
        mouse_listener.start()
        
        print("Input logger started. Press 'esc' to stop.")
        # 等待key监听器结束（按ESC键结束）
        keyboard_listener.join()
        # 停止m监听器
        mouse_listener.stop()
        print("Input logger stopped.")

if __name__ == "__main__":
    logger = InputLogger()
    logger.start() 