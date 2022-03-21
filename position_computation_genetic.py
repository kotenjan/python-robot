import random
from queue import PriorityQueue
from metric import *
from constants import *


def update_current_position(low, high, current, ratio):
    curr_lo = current + ratio*(low-current)
    curr_hi = current + ratio*(high-current)
    rand_number = random.random()
    return (curr_hi-curr_lo)*rand_number + curr_lo


def get_shoulder_pitch(current, ratio):
    return update_current_position(SHOULDER_PITCH_LO, SHOULDER_PITCH_HI, current, ratio)


def get_shoulder_roll(current, ratio):
    return update_current_position(SHOULDER_ROLL_LO, SHOULDER_ROLL_HI, current, ratio)


def get_elbow_roll(current, ratio):
    return update_current_position(ELBOW_ROLL_LO, ELBOW_ROLL_HI, current, ratio)


def get_elbow_yaw(current, ratio):
    return update_current_position(ELBOW_YAW_LO, ELBOW_YAW_HI, current, ratio)


def get_wrist_yaw(current, ratio):
    return update_current_position(WRIST_YAW_LO, WRIST_YAW_HI, current, ratio)

def modify_random_state(state, ratio):
    return np.array([
        get_shoulder_pitch(state[0], ratio),
        get_shoulder_roll(state[1], ratio),
        get_elbow_roll(state[2], ratio),
        get_elbow_yaw(state[3], ratio),
        get_wrist_yaw(state[4], ratio)
    ])


def create_population(current_rotations_arr, all_count, top_count, position_start, position_dest, init_distance):
    population = PriorityQueue()
    for current_rotations in current_rotations_arr:
        for _ in range(all_count):
            ratio = abs(max(current_rotations[0]/init_distance, 0.01))
            rotations = modify_random_state(current_rotations[1], ratio)
            distance = get_relative_distance(
                position_start, position_dest, rotations)
            try:
                population.put((distance, rotations), False)
            except:
                pass

    return population.queue[:top_count]


def cross_elements(x, y):
    state = np.random.rand(5)
    return x*state + y*(1-state)


def mutate_population(current_rotations_arr, top_count, position_start, position_dest):
    population = PriorityQueue()
    for x in current_rotations_arr:
        for y in current_rotations_arr:
            rotations = cross_elements(x[1], y[1])
            distance = get_relative_distance(
                position_start, position_dest, rotations)
            try:
                population.put((distance, rotations), False)
            except:
                pass

    return population.queue[:top_count]


def create_queue(queue, data):
    for x in data:
        try:
            queue.put(x, False)
        except:
            pass
    return queue


def rotations_to_position(position_start, position_dest, current_rotations, population_count, top_count, generations):
    
    position_start = np.array(position_start)
    position_dest = np.array(position_dest)
    current_rotations = np.array(current_rotations)

    init_distance = get_relative_distance(position_start, position_dest, current_rotations)

    population = PriorityQueue()

    population_0 = create_population([(init_distance, current_rotations)], population_count, top_count, position_start, position_dest, init_distance)

    bad_cycle_count = 0

    while bad_cycle_count < generations:
        population = create_queue(population, population_0)

        current_min = population.queue[0][0]

        population_1 = mutate_population(
            population_0, top_count, position_start, position_dest)
        population = create_queue(population, population_1)
        population_2 = create_population(population_1, int(
            population_count/top_count), top_count, position_start, position_dest, init_distance)
        population = create_queue(population, population_2)
        population_0 = population.queue[:top_count]

        new_min = population.queue[0][0]

        population = PriorityQueue()

        if current_min >= new_min:
            bad_cycle_count += 1
        else:
            bad_cycle_count = 0

    # distance from object and rotation
    return population_0[0][0], population_0[0][1]
