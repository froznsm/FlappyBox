import pygame, sys, random, os

def main(width, height, tickrate):
    res = (width, height)
    pygame.init()
    screen = pygame.display.set_mode(res, 0, 32)
    pygame.display.set_caption("Flappy Square")
    clock = pygame.time.Clock()
    player = os.getlogin()
    game_font = pygame.font.SysFont('Arial', height // 15)
    player_name_text = game_font.render("Hello There! General {}".format(player), False, (255, 0, 0))

    while True:
        obstacle_speed = 3
        obstacle_width = width // 28
        obstacle_gap = height / 5
        distance_between_obstacles = width // 3
        i = width
        j = width + distance_between_obstacles
        k = width + distance_between_obstacles * 2
        bird_y = height // 2
        bird_x = width // 5
        falling_speed = 0.1
        accel = falling_speed
        offset1, offset2, offset3 = random.randint(-height / 3, height / 3), random.randint(-height / 3, height / 3), random.randint(-height / 3, height / 3)
        obstacle_counter = 0

        small_jump_counter = 0
        medium_jump_counter = 0
        big_jump_counter = 0
        score_overall = 0



        running = True
        while running:
            screen.fill((0, 0, 0))
            clock.tick(tickrate)

            # Hello There! General Kenobi!
            # screen.blit(player_name_text, (width // 8, height - height//8))

            obstacle_counter_text = game_font.render(str(obstacle_counter), False, (255, 0, 0))
            screen.blit(obstacle_counter_text, (0,0))
            score_text = game_font.render(str(score_overall), False, (255, 0, 0))
            screen.blit(score_text, (0, height//16+1))

            # establish floor
            if bird_y >= height:
                running = False

            bird = pygame.Rect(bird_x, int(bird_y), obstacle_width * (2/3), obstacle_width * (2/3))
            pygame.draw.rect(screen, (255, 255, 255), bird, 0)

            # at game start move obstacles in from the side
            if k > width:
                i -= width // (obstacle_speed * 100)
                j -= width // (obstacle_speed * 100)
                k -= width // (obstacle_speed * 100)
            else:
                # normal obstacle movement
                i_old = i
                i = (i - width//(obstacle_speed * 100)) % width
                j_old = j
                j = (j - width//(obstacle_speed * 100)) % width
                k_old = k
                k = (k - width //(obstacle_speed * 100)) % width
                # check if obstacle was passed
                if i_old + obstacle_width > bird_x >= i + obstacle_width or j_old + obstacle_width > bird_x >= j + obstacle_width or k_old + obstacle_width > bird_x >= k + obstacle_width:
                    # scoring system
                    score_for_obstacle = 1100 - 100 * big_jump_counter - 200 * medium_jump_counter - 300 * small_jump_counter
                    # no negative score
                    if score_for_obstacle < 0:
                        score_for_obstacle = 0
                    # first obstacle does not give any points
                    if obstacle_counter == 0:
                        score_for_obstacle = 0
                    # establish obstacles being infinitely high
                    if bird_y < 0:
                        running = False
                    # increment obstacle counter
                    obstacle_counter += 1
                    # add up obstacle score to overall score
                    score_overall += score_for_obstacle
                    # reset counters
                    small_jump_counter = 0
                    medium_jump_counter = 0
                    big_jump_counter = 0

                # generating new obstacle offset each time the obstacle moves out of screen
                if i_old < width//2 < i:
                    offset1 = random.randint(-height / 3, height / 3)
                if j_old < width//2 < j:
                    offset2 = random.randint(-height / 3, height / 3)
                if k_old < width // 2 < k:
                    offset3 = random.randint(-height / 3, height / 3)

            # generate obstacle objects
            lower_obstacle1 = pygame.Rect(i, height/2+obstacle_gap/2+offset1, obstacle_width, height-obstacle_gap/2-offset1)
            upper_obstacle1 = pygame.Rect(i, 0, obstacle_width, height/2-obstacle_gap/2+offset1)
            lower_obstacle2 = pygame.Rect(j, height/2+obstacle_gap/2+offset2, obstacle_width, height-obstacle_gap/2-offset2)
            upper_obstacle2 = pygame.Rect(j, 0, obstacle_width, height/2-obstacle_gap/2+offset2)
            lower_obstacle3 = pygame.Rect(k, height/2+obstacle_gap/2+offset3, obstacle_width, height-obstacle_gap/2-offset3)
            upper_obstacle3 = pygame.Rect(k, 0, obstacle_width, height/2-obstacle_gap/2+offset3)
            obstacles = [lower_obstacle1, upper_obstacle1, lower_obstacle2, upper_obstacle2, lower_obstacle3,
                         upper_obstacle3]
            for obs in obstacles:
                pygame.draw.rect(screen, (255, 255, 255), obs, 0)
                if bird.colliderect(obs):
                    running = False

            # bird gravity
            bird_y += falling_speed
            falling_speed += accel

            keys = pygame.key.get_pressed()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if keys[pygame.K_SPACE]:
                    falling_speed = -accel * 50
                if keys[pygame.K_a]:
                    falling_speed = -accel * 70
                    big_jump_counter += 1
                if keys[pygame.K_s]:
                    falling_speed = -accel * 50
                    medium_jump_counter += 1
                if keys[pygame.K_d]:
                    falling_speed = -accel * 30
                    small_jump_counter += 1
                if keys[pygame.K_k]:
                    offset1, offset2, offset3 = random.randint(-height / 3, height / 3), random.randint(-height / 3, height / 3), random.randint(-height / 3, height / 3)
            pygame.display.update()


        game_over = game_font.render('GAME OVER', False, (255, 0, 0))
        obstacle_text = game_font.render('You have passed {} obstacles'.format(obstacle_counter), False, (255, 0, 0))
        score_text = game_font.render('and scored {} points'.format(score_overall), False, (255, 0, 0))
        screen.blit(game_over, (width//2 - width // 18, height//6))
        screen.blit(obstacle_text, ((width // 6) * 2, (height // 6) * 2))
        screen.blit(score_text, ((width // 6) * 2 + (width // 20), (height // 6) * 2 + (height // 12)))
        pygame.display.update()
        pygame.time.wait(2000)

    #pygame.quit()




main(640, 480, 60)
