# 모듈 인포트
from pico2d import *
import random

# 캔버스 오픈
TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)

# 리소스 파일 불러오기
TUK_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
hand_arrow = load_image('hand_arrow.png')

# 키보드 입력 감지 함수
def handle_events():
    global running, cursor_x, cursor_y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            cursor_x, cursor_y = event.x, TUK_HEIGHT-1-event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            hand_x.append(event.x)
            hand_y.append(event.y)
            if (len(hand_x) == 1):
                reset_line()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

# 전역변수 선언 및 초기화
running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
character_speed = 2
cursor_x = TUK_WIDTH // 2
cursor_y = TUK_HEIGHT // 2
hand_x = []
hand_y = []
line_x = [n for n in range(100//character_speed + 1)]
line_y = [n for n in range(100//character_speed + 1)]
line_x_index = 0
line_y_index = 0
character_dir = 1
frame = 0
character_frame = 0

# 커서 숨기기
hide_cursor()

# 캐릭터가 도달한 손을 지우는 함수
def reset_hand():
    global hand_x, hand_y
    hand_x.reverse()
    hand_x.pop()
    hand_x.reverse()
    hand_y.reverse()
    hand_y.pop()
    hand_y.reverse()

# 다음 손까지 이르는 경로의 좌표 집합(리스트)을 갱신하는 함수
def reset_line():
    global x, y, hand_x, hand_y, line_x, line_y, line_x_index, line_y_index
    if (len(hand_x) == 0):
        return -1
    index_x = 0
    index_y = 0
    for i in range(0, 100 + 1, character_speed):
        t = i / 100
        line_x[index_x] = int((1 - t) * x + t * hand_x[0])
        line_y[index_y] = int((1 - t) * y + t * hand_y[0])
        index_x += 1
        index_y += 1
    line_x[index_x - 1] = hand_x[0]
    line_y[index_y - 1] = hand_y[0]
    line_x_index = 0
    line_y_index = 0

# 캐릭터 위치를 다음 프레임 위치로 갱신하는 함수
def reset_character():
    global x, y, line_x, line_y, line_x_index, line_y_index
    x = line_x[line_x_index]
    y = line_y[line_y_index]
    line_x_index += 1
    line_y_index += 1


# 메인함수
while running:
    clear_canvas()
    handle_events()

    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    if (len(hand_x) == 0):
        pass
    else:
        for i in range(0, len(hand_x)): # 누적된 손 모두 그리기
            hand_arrow.draw(hand_x[i], TUK_HEIGHT - 1 - hand_y[i])
        if (hand_x[0] == x) & (hand_y[0] == y): # 첫 손에 도달했을 경우
            reset_hand()
            reset_line()
        else: # 아직 도달하지 못했을 경우
            reset_character()

    character.clip_draw(character_frame * 100, 100 * character_dir, 100, 100, x, TUK_HEIGHT - 1 - y)
    hand_arrow.draw(cursor_x, cursor_y)

    update_canvas()
    frame = (frame + 1) % 39
    character_frame = frame // 5
    delay(0.01)

# 캔버스 닫기
close_canvas()