import random


class ExerciseList():
    def __init__(self, first_exercise_idx, last_exercise_idx):
        self.num_of_exercises = last_exercise_idx - first_exercise_idx + 1
        self.index = 0
        self.exercise_list = list(xrange(first_exercise_idx, last_exercise_idx + 1))  # ordered
        random.shuffle(self.exercise_list)  # randomly ordered list

    def get_next_exercise_intensity(self):
        next_exercise = self.exercise_list[self.index]
        self.index += 1

        if self.index >= self.num_of_exercises:
            random.shuffle(self.exercise_list)
            self.index = 0

        return next_exercise


easy = ExerciseList(first_exercise_idx=0, last_exercise_idx=2)
print (easy.get_next_exercise_intensity())
print (easy.get_next_exercise_intensity())
print (easy.get_next_exercise_intensity())
print (easy.get_next_exercise_intensity())