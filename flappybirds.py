import pygame, sys, random


def main(width, height):
    res = (width, height)

    pygame.init()
    screen = pygame.display.set_mode(res, 0, 32)
    pygame.display.set_caption("Flappy Square")
    clock = pygame.time.Clock()
    obstacle_speed = 3
    obstacle_width = 30
    obstacle_gap = height / 5
    distance_between_obstacles = int(width / 3)
    i = width
    j = width + distance_between_obstacles
    k = width + distance_between_obstacles*2
    bird_y = height//2
    bird_x = width//5
    falling_speed = 0.1
    accel = falling_speed
    offset1, offset2, offset3 = random.randint(-height/3, height/3), random.randint(-height/3, height/3), random.randint(-height/3, height/3)
    obstacle_counter = 0

    small_jump_counter = 0
    medium_jump_counter = 0
    big_jump_counter = 0
    score_overall = 0

    myfont = pygame.font.SysFont('Arial', height//15)

    running = True
    while running:
        screen.fill((0, 0, 0))
        clock.tick(60)

        obstacle_counter_text = myfont.render(str(obstacle_counter), False, (255, 0, 0))
        screen.blit(obstacle_counter_text, (0,0))
        score_text = myfont.render(str(score_overall), False, (255, 0, 0))
        screen.blit(score_text, (0, height//16+1))
        
        if bird_y >= height:
            running = False

        bird = pygame.Rect(bird_x, int(bird_y), height//obstacle_width, height//obstacle_width)
        pygame.draw.rect(screen, (255, 255, 255), bird, 0)

        # game start move obstacles in from the side
        if k > width:
            i -= width//(obstacle_speed*100)
            j -= width//(obstacle_speed*100)
            k -= width//(obstacle_speed*100)
        else:
            # normal movement
            i_old = i
            i = (i - width//(obstacle_speed * 100)) % width
            j_old = j
            j = (j - width//(obstacle_speed * 100)) % width
            k_old = k
            k = (k - width //(obstacle_speed * 100)) % width
            # check if obstacle was passed
            if i_old + obstacle_width > bird_x >= i + obstacle_width or j_old + obstacle_width> bird_x >= j + obstacle_width or k_old + obstacle_width > bird_x >= k + obstacle_width:
                obstacle_counter += 1
                score_for_obstacle = 100 * big_jump_counter + 20 * medium_jump_counter - small_jump_counter
                score_overall += score_for_obstacle
                small_jump_counter = 0
                medium_jump_counter = 0
                big_jump_counter = 0
            # generating new obstacle offset
            if i_old < width//2 < i:
                offset1 = random.randint(-height / 3, height / 3)
            if j_old < width//2 < j:
                offset2 = random.randint(-height / 3, height / 3)
            if k_old < width // 2 < k:
                offset3 = random.randint(-height / 3, height / 3)

        lower_obstacle1 = pygame.Rect(i, height/2+obstacle_gap/2+offset1, obstacle_width, height-obstacle_gap/2-offset1)
        upper_obstacle1 = pygame.Rect(i, 0, obstacle_width, height/2-obstacle_gap/2+offset1)
        lower_obstacle2 = pygame.Rect(j, height/2+obstacle_gap/2+offset2, obstacle_width, height-obstacle_gap/2-offset2)
        upper_obstacle2 = pygame.Rect(j, 0, obstacle_width, height/2-obstacle_gap/2+offset2)
        lower_obstacle3 = pygame.Rect(k, height/2+obstacle_gap/2+offset3, obstacle_width, height-obstacle_gap/2-offset3)
        upper_obstacle3 = pygame.Rect(k, 0, obstacle_width, height/2-obstacle_gap/2+offset3)
        obstacles = [lower_obstacle1, upper_obstacle1, lower_obstacle2, upper_obstacle2, lower_obstacle3, upper_obstacle3]
        for obs in obstacles:
            pygame.draw.rect(screen, (255, 255, 255), obs, 0)
            if bird.colliderect(obs):
                running = False

        bird_y += falling_speed
        falling_speed += accel

        keys = pygame.key.get_pressed()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if keys[pygame.K_SPACE]:
                falling_speed = -accel*50
            if keys[pygame.K_a]:
                falling_speed = -accel*70
                big_jump_counter += 1
            if keys[pygame.K_s]:
                falling_speed = -accel*50
                medium_jump_counter += 1
            if keys[pygame.K_d]:
                falling_speed = -accel*30
                small_jump_counter += 1
            if keys[pygame.K_k]:
                offset1, offset2, offset3 = random.randint(-height / 3, height / 3), random.randint(-height / 3, height / 3), random.randint(-height / 3, height / 3)
        pygame.display.update()


    textsurface = myfont.render('GAME OVER', False, (255, 0, 0))
    screen.blit(textsurface, (width//6, height//6))
    pygame.display.update()
    pygame.time.wait(4000)
    pygame.quit()




main(1260, 720)
