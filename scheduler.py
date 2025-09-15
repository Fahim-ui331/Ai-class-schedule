import random

class ClassScheduler:
    def __init__(self, database):
        self.db = database

    def generate_schedule(self):
        students = self.db.get_student_preferences()
        schedule = self.run_genetic_algorithm(students)
        return schedule

    def fitness(self, schedule):
        score = 0
        for i, student in enumerate(schedule):
            if student['preferred_section'] == student['assigned_section']:
                score += 3
            if student['cgpa'] >= 3.5:  # High priority students
                score += 2
        return score

    def crossover(self, parent1, parent2):
        point = random.randint(1, len(parent1)-1)
        child = parent1[:point] + parent2[point:]
        return child

    def mutate(self, individual):
        i = random.randint(0, len(individual)-1)
        individual[i] = random.randint(0, 3)  # Assume 4 sections

    def run_genetic_algorithm(self, students):
        # Generate an initial random population
        population = [self.generate_random_schedule(students) for _ in range(20)]
        generations = 100

        for generation in range(generations):
            population.sort(key=self.fitness, reverse=True)
            next_generation = population[:2]  # Elitism: keep top 2

            while len(next_generation) < len(population):
                p1, p2 = random.sample(population[:10], 2)
                child = self.crossover(p1, p2)
                if random.random() < 0.2:  # mutation rate
                    self.mutate(child)
                next_generation.append(child)

            population = next_generation

        return population[0]  # Return best schedule after all generations

    def generate_random_schedule(self, students):
        # Randomly assign sections to students (could be improved)
        return [{'student_id': student['student_id'], 'assigned_section': random.randint(0, 3)} for student in students]
