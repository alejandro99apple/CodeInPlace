import tkinter as tk
import random

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 400
GROUND_Y = CANVAS_HEIGHT - 50

COLOR_SKY = "#9AD9FF"
COLOR_SKY_MID = "#DDF4FF"
COLOR_SUN = "#FFD54F"
COLOR_CLOUD = "#FFFFFF"
COLOR_MOUNTAIN = "#6E8B74"
COLOR_LEAVES = "#2E7D32"
COLOR_TRUNK = "#7A4A21"
COLOR_GRASS = "#5CB85C"

STUDENT_X = 100
STUDENT_HEIGHT = 50
STUDENT_WIDTH = 30
GRAVITY = 1
JUMP_FORCE = -20

SKIN_COLOR = "#F1C27D"
SHIRT_COLOR = "#1E88E5"
PANTS_COLOR = "#2E3A87"
SHOE_COLOR = "#4E342E"
OUTLINE_COLOR = "#1B1B1B"

OBSTACLE_SPEED = 10
OBSTACLE_TYPES = [
    {"name": "lion", "width": 58, "height_min": 36, "height_max": 42, "elevation": 0},
    {"name": "eagle", "width": 64, "height_min": 34, "height_max": 42, "elevation": 38},
    {"name": "crocodile", "width": 68, "height_min": 28, "height_max": 34, "elevation": 0},
]

FRAME_TIME_MS = 20

game_running = True
student_velocity_y = 0
score = 0
loop_job_id = None
current_obstacle_speed = OBSTACLE_SPEED
next_speed_increase_score = 5
jump_animation_frame = 0
obstacle_ids = []
obstacle_data = []
scored_obstacles = set()
game_over_frame = None
student_parts = {}
student = None
obstacle_counter = 0


def create_canvas():
    global canvas, window, score_text

    window = tk.Tk()
    window.title("Code in Place Final: Student vs Animals")

    canvas = tk.Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=COLOR_SKY)
    canvas.pack()
    draw_base_scene()


def draw_natural_background():
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, 120, fill=COLOR_SKY, outline="")
    canvas.create_rectangle(0, 120, CANVAS_WIDTH, 220, fill=COLOR_SKY_MID, outline="")

    canvas.create_oval(620, 30, 700, 110, fill=COLOR_SUN, outline="")

    for cloud_x, cloud_y in [(70, 45), (210, 35), (500, 55)]:
        canvas.create_oval(cloud_x, cloud_y, cloud_x + 40, cloud_y + 22, fill=COLOR_CLOUD, outline="")
        canvas.create_oval(cloud_x + 20, cloud_y - 8, cloud_x + 62, cloud_y + 18, fill=COLOR_CLOUD, outline="")
        canvas.create_oval(cloud_x + 40, cloud_y, cloud_x + 82, cloud_y + 22, fill=COLOR_CLOUD, outline="")

    canvas.create_polygon(0, 230, 115, 125, 230, 230, fill=COLOR_MOUNTAIN, outline="")
    canvas.create_polygon(160, 230, 280, 110, 410, 230, fill="#7C9C7F", outline="")
    canvas.create_polygon(360, 230, 510, 120, 660, 230, fill="#728A68", outline="")
    canvas.create_polygon(590, 230, 700, 135, 800, 230, fill="#829A72", outline="")

    for base_x in [40, 140, 245, 350, 470, 590, 700]:
        canvas.create_rectangle(base_x + 10, 215, base_x + 16, GROUND_Y - 6, fill=COLOR_TRUNK, outline="")
        canvas.create_polygon(base_x, 215, base_x + 13, 170, base_x + 26, 215, fill=COLOR_LEAVES, outline="")
        canvas.create_polygon(base_x - 6, 202, base_x + 13, 155, base_x + 32, 202, fill="#3F8F3E", outline="")
        canvas.create_polygon(base_x - 10, 190, base_x + 13, 145, base_x + 36, 190, fill="#4AA84A", outline="")

    canvas.create_rectangle(0, GROUND_Y - 18, CANVAS_WIDTH, CANVAS_HEIGHT, fill=COLOR_GRASS, outline="")
    canvas.create_oval(-60, 260, 250, 420, fill="#4F9E49", outline="")
    canvas.create_oval(180, 275, 520, 430, fill="#57AA4F", outline="")
    canvas.create_oval(450, 255, 860, 430, fill="#4A9644", outline="")


def draw_base_ui():
    global score_text

    score_text = canvas.create_text(15, 15, anchor="nw", text=f"Score: {score}", fill="#123524", font=("Helvetica", 18, "bold"))
    canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT - 20, text="Press [SPACE] or [↑] to jump", fill="#1F3B2C", font=("Helvetica", 10, "bold"))


def draw_base_scene():
    canvas.delete("all")
    draw_natural_background()
    canvas.create_line(0, GROUND_Y, CANVAS_WIDTH, GROUND_Y, fill="#8B4513", width=2)
    draw_base_ui()


def draw_lion(tag, x, y, width, height):
    body_y = y + 10
    canvas.create_oval(x + 10, body_y, x + width - 6, y + height, fill="#D98E3C", outline="#7B4B1F", width=2, tags=(tag,))
    canvas.create_oval(x, y, x + 26, y + 26, fill="#C97B2B", outline="#7B4B1F", width=2, tags=(tag,))
    canvas.create_oval(x + 5, y + 5, x + 21, y + 21, fill="#F2C57C", outline="", tags=(tag,))
    canvas.create_line(x + 6, y + 22, x + 1, y + 18, fill="#7B4B1F", width=2, tags=(tag,))
    canvas.create_line(x + 10, y + 22, x + 9, y + 28, fill="#7B4B1F", width=2, tags=(tag,))
    canvas.create_line(x + 16, y + 22, x + 17, y + 28, fill="#7B4B1F", width=2, tags=(tag,))
    canvas.create_line(x + 20, y + 22, x + 25, y + 18, fill="#7B4B1F", width=2, tags=(tag,))
    canvas.create_oval(x + 9, y + 10, x + 11, y + 12, fill="#1B1B1B", outline="", tags=(tag,))
    canvas.create_oval(x + 15, y + 10, x + 17, y + 12, fill="#1B1B1B", outline="", tags=(tag,))
    canvas.create_polygon(x + 12, y + 14, x + 14, y + 14, x + 13, y + 17, fill="#7B4B1F", outline="", tags=(tag,))
    canvas.create_line(x + width - 5, y + 20, x + width + 12, y + 10, fill="#7B4B1F", width=2, tags=(tag,))
    canvas.create_oval(x + width + 8, y + 5, x + width + 14, y + 11, fill="#7B4B1F", outline="", tags=(tag,))


def draw_eagle(tag, x, y, width, height):
    mid_y = y + height // 2
    canvas.create_oval(x + 20, y + 10, x + 42, y + 28, fill="#6B4F3A", outline="#2F241C", width=2, tags=(tag,))
    canvas.create_oval(x + 38, y + 12, x + 50, y + 24, fill="#F5E6C8", outline="#2F241C", width=1, tags=(tag,))
    canvas.create_polygon(x + 49, y + 18, x + 58, y + 21, x + 49, y + 24, fill="#E0A040", outline="#8B5E00", tags=(tag,))
    canvas.create_line(x + 28, mid_y, x + 8, y + 4, fill="#2F241C", width=5, tags=(tag,))
    canvas.create_line(x + 30, mid_y, x + 0, y + 16, fill="#2F241C", width=5, tags=(tag,))
    canvas.create_line(x + 34, mid_y, x + 62, y + 5, fill="#2F241C", width=5, tags=(tag,))
    canvas.create_line(x + 36, mid_y, x + 66, y + 18, fill="#2F241C", width=5, tags=(tag,))
    canvas.create_line(x + 27, y + 27, x + 23, y + 38, fill="#2F241C", width=3, tags=(tag,))
    canvas.create_line(x + 35, y + 27, x + 31, y + 38, fill="#2F241C", width=3, tags=(tag,))
    canvas.create_polygon(x + 11, y + 17, x + 0, y + 13, x + 10, y + 9, fill="#6B4F3A", outline="", tags=(tag,))
    canvas.create_polygon(x + 56, y + 17, x + 68, y + 13, x + 57, y + 9, fill="#6B4F3A", outline="", tags=(tag,))


def draw_crocodile(tag, x, y, width, height):
    canvas.create_polygon(
        x + 6, y + height,
        x + 18, y + 12,
        x + 46, y + 12,
        x + 60, y + 18,
        x + width, y + height - 2,
        x + 58, y + height,
        x + 20, y + height,
        fill="#4CAF50", outline="#1B5E20", width=2, tags=(tag,)
    )
    canvas.create_polygon(x + width - 2, y + height - 6, x + width + 12, y + height - 10, x + width - 4, y + height - 2, fill="#3E8E41", outline="#1B5E20", tags=(tag,))
    canvas.create_polygon(x + 20, y + 14, x + 26, y + 6, x + 32, y + 14, fill="#2E7D32", outline="", tags=(tag,))
    canvas.create_polygon(x + 34, y + 14, x + 40, y + 6, x + 46, y + 14, fill="#2E7D32", outline="", tags=(tag,))
    canvas.create_polygon(x + 48, y + 15, x + 54, y + 8, x + 60, y + 15, fill="#2E7D32", outline="", tags=(tag,))
    canvas.create_oval(x + 12, y + 14, x + 16, y + 18, fill="#1B1B1B", outline="", tags=(tag,))
    canvas.create_oval(x + 18, y + 14, x + 22, y + 18, fill="#1B1B1B", outline="", tags=(tag,))


def draw_obstacle(obstacle_type, tag, x, y, width, height):
    if obstacle_type["name"] == "lion":
        draw_lion(tag, x, y, width, height)
    elif obstacle_type["name"] == "eagle":
        draw_eagle(tag, x, y, width, height)
    else:
        draw_crocodile(tag, x, y, width, height)


def update_character(x, y, state="idle"):
    if state == "jump_1":
        head = (x + 7, y + 1, x + 23, y + 17)
        torso = (x + 11, y + 16, x + 19, y + 32)
        left_arm = (x + 11, y + 19, x + 4, y + 9)
        right_arm = (x + 19, y + 19, x + 26, y + 9)
        left_leg = (x + 13, y + 32, x + 8, y + 45)
        right_leg = (x + 17, y + 32, x + 22, y + 45)
    elif state == "jump_2":
        head = (x + 7, y + 0, x + 23, y + 16)
        torso = (x + 11, y + 15, x + 19, y + 31)
        left_arm = (x + 11, y + 18, x + 2, y + 14)
        right_arm = (x + 19, y + 18, x + 28, y + 14)
        left_leg = (x + 13, y + 31, x + 9, y + 47)
        right_leg = (x + 17, y + 31, x + 21, y + 47)
    else:
        head = (x + 7, y + 0, x + 23, y + 16)
        torso = (x + 11, y + 16, x + 19, y + 32)
        left_arm = (x + 11, y + 19, x + 4, y + 31)
        right_arm = (x + 19, y + 19, x + 26, y + 31)
        left_leg = (x + 13, y + 32, x + 9, y + 48)
        right_leg = (x + 17, y + 32, x + 21, y + 48)

    canvas.coords(student_parts["head"], *head)
    canvas.coords(student_parts["torso"], *torso)
    canvas.coords(student_parts["left_arm"], *left_arm)
    canvas.coords(student_parts["right_arm"], *right_arm)
    canvas.coords(student_parts["left_leg"], *left_leg)
    canvas.coords(student_parts["right_leg"], *right_leg)
    canvas.coords(student_parts["left_shoe"], x + 7, y + 47, x + 11, y + 49)
    canvas.coords(student_parts["right_shoe"], x + 19, y + 47, x + 23, y + 49)


def delete_character():
    for part_id in student_parts.values():
        canvas.delete(part_id)
    student_parts.clear()


def create_student():
    global student_parts

    y = GROUND_Y - STUDENT_HEIGHT
    student_id = canvas.create_rectangle(STUDENT_X, y, STUDENT_X + STUDENT_WIDTH, GROUND_Y, fill="", outline="", width=0)

    student_parts["head"] = canvas.create_oval(0, 0, 0, 0, fill=SKIN_COLOR, outline=OUTLINE_COLOR, width=2)
    student_parts["torso"] = canvas.create_rectangle(0, 0, 0, 0, fill=SHIRT_COLOR, outline=OUTLINE_COLOR, width=2)
    student_parts["left_arm"] = canvas.create_line(0, 0, 0, 0, fill=OUTLINE_COLOR, width=3)
    student_parts["right_arm"] = canvas.create_line(0, 0, 0, 0, fill=OUTLINE_COLOR, width=3)
    student_parts["left_leg"] = canvas.create_line(0, 0, 0, 0, fill=PANTS_COLOR, width=4)
    student_parts["right_leg"] = canvas.create_line(0, 0, 0, 0, fill=PANTS_COLOR, width=4)
    student_parts["left_shoe"] = canvas.create_oval(0, 0, 0, 0, fill=SHOE_COLOR, outline=OUTLINE_COLOR, width=1)
    student_parts["right_shoe"] = canvas.create_oval(0, 0, 0, 0, fill=SHOE_COLOR, outline=OUTLINE_COLOR, width=1)

    update_character(STUDENT_X, y, "idle")
    return student_id


def add_obstacle():
    global game_running, obstacle_counter
    if not game_running:
        return

    obstacle_type = random.choice(OBSTACLE_TYPES)
    width = obstacle_type["width"]
    height = random.randint(obstacle_type["height_min"], obstacle_type["height_max"])
    x = CANVAS_WIDTH
    y = GROUND_Y - height - obstacle_type["elevation"] if obstacle_type["elevation"] > 0 else GROUND_Y - height

    tag = f"obstacle_{obstacle_counter}"
    obstacle_counter += 1

    draw_obstacle(obstacle_type, tag, x, y, width, height)
    obstacle_ids.append(tag)
    obstacle_data.append({"x": x, "y": y, "w": width, "h": height, "id": tag})

    window.after(random.randint(1500, 3000), add_obstacle)


def detect_collisions(student_x, student_y):
    student_box = (student_x, student_y, student_x + STUDENT_WIDTH, student_y + STUDENT_HEIGHT)

    for obstacle in obstacle_data:
        obstacle_box = (obstacle["x"], obstacle["y"], obstacle["x"] + obstacle["w"], obstacle["y"] + obstacle["h"])
        if (
            student_box[0] < obstacle_box[2]
            and student_box[2] > obstacle_box[0]
            and student_box[1] < obstacle_box[3]
            and student_box[3] > obstacle_box[1]
        ):
            return True

    return False


def game_loop():
    global game_running, student_velocity_y, score, loop_job_id
    global current_obstacle_speed, next_speed_increase_score, jump_animation_frame

    if not game_running:
        return

    student_velocity_y += GRAVITY

    coords = canvas.coords(student)
    student_x = coords[0]
    student_y = coords[1]
    next_y = student_y + student_velocity_y

    if next_y + STUDENT_HEIGHT >= GROUND_Y:
        next_y = GROUND_Y - STUDENT_HEIGHT
        student_velocity_y = 0
        jump_animation_frame = 0

    canvas.coords(student, student_x, next_y, student_x + STUDENT_WIDTH, next_y + STUDENT_HEIGHT)

    if student_velocity_y < 0:
        jump_animation_frame = (jump_animation_frame + 1) % 8
        update_character(student_x, next_y, "jump_1" if jump_animation_frame < 4 else "jump_2")
    else:
        update_character(student_x, next_y, "idle")

    updated_score = score
    remaining_ids = []
    remaining_data = []

    for obstacle_id, obstacle in zip(obstacle_ids, obstacle_data):
        canvas.move(obstacle_id, -current_obstacle_speed, 0)
        obstacle["x"] -= current_obstacle_speed

        if obstacle["x"] + obstacle["w"] > 0:
            remaining_ids.append(obstacle_id)
            remaining_data.append(obstacle)

            if obstacle["x"] + obstacle["w"] < STUDENT_X and obstacle["id"] not in scored_obstacles:
                updated_score += 1
                scored_obstacles.add(obstacle["id"])
        else:
            canvas.delete(obstacle_id)

    obstacle_ids[:] = remaining_ids
    obstacle_data[:] = remaining_data

    if updated_score != score:
        score = updated_score
        canvas.itemconfig(score_text, text=f"Score: {score}")

        while score >= next_speed_increase_score:
            current_obstacle_speed *= 1.1
            next_speed_increase_score += 5

    if detect_collisions(student_x, next_y):
        end_game()
        return

    loop_job_id = window.after(FRAME_TIME_MS, game_loop)


def jump(event):
    global student_velocity_y, game_running, jump_animation_frame
    if not game_running:
        return

    coords = canvas.coords(student)
    student_y = coords[1]

    if student_y + STUDENT_HEIGHT >= GROUND_Y - 5:
        student_velocity_y = JUMP_FORCE
        jump_animation_frame = 0


def end_game():
    global game_running, loop_job_id, game_over_frame
    game_running = False

    if loop_job_id is not None:
        window.after_cancel(loop_job_id)

    if game_over_frame is not None:
        game_over_frame.destroy()

    canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 55, text="GAME OVER", fill="red", font=("Helvetica", 40, "bold"))
    canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 5, text=f"Final Score: {score}", fill="black", font=("Helvetica", 20))

    game_over_frame = tk.Frame(window, bg="#F0F0F0")
    canvas.create_window(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 + 55, window=game_over_frame)

    restart_button = tk.Button(game_over_frame, text="Restart", font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white", activebackground="#45A049", padx=18, pady=8, command=restart_game)
    quit_button = tk.Button(game_over_frame, text="Quit", font=("Helvetica", 14, "bold"), bg="#C62828", fg="white", activebackground="#AD1F1F", padx=18, pady=8, command=window.destroy)
    restart_button.grid(row=0, column=0, padx=10)
    quit_button.grid(row=0, column=1, padx=10)


def restart_game():
    global game_running, student_velocity_y, score, loop_job_id
    global obstacle_ids, obstacle_data, scored_obstacles, student, game_over_frame
    global current_obstacle_speed, next_speed_increase_score, jump_animation_frame, obstacle_counter

    game_running = True
    student_velocity_y = 0
    score = 0
    current_obstacle_speed = OBSTACLE_SPEED
    next_speed_increase_score = 5
    jump_animation_frame = 0
    obstacle_counter = 0
    scored_obstacles.clear()
    obstacle_ids.clear()
    obstacle_data.clear()

    if loop_job_id is not None:
        try:
            window.after_cancel(loop_job_id)
        except tk.TclError:
            pass
        loop_job_id = None

    if game_over_frame is not None:
        game_over_frame.destroy()
        game_over_frame = None

    draw_base_scene()
    student_parts.clear()
    student = create_student()
    add_obstacle()
    game_loop()


create_canvas()
student = create_student()

window.bind("<space>", jump)
window.bind("<Up>", jump)

add_obstacle()
game_loop()

window.mainloop()
