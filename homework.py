class Training:
    LEN_STEP = 0.65
    M_IN_H = 60
    M_IN_KM = 1000  # метров в километры

    def __init__(self, action, duration, weight):
        self.action = action
        self.duration = duration  # в часах
        self.weight = weight

    def get_distance(self):
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self):
        return self.get_distance() / self.duration

    def get_spent_calories(self):
        pass  # метод будет реализован в дочерних классах

    def show_training_info(self):
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


class InfoMessage:
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )


class Running(Training):
    M_IN_KM = 1000

    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)
        self.LEN_STEP = 0.65

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed()
        time_in_minutes = self.duration * 60  # преобразование в минуты
        calories = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM * time_in_minutes
        )
        return calories


class SportsWalking(Training):
    MULTI_WEIGHT = 0.035
    MULTI_HEIGHT = 0.029
    KM_H_IN_M_S = 0.278
    M_IN_SM = 100
    SEC_IN_MIN = 60

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.LEN_STEP = 0.65
        self.height = height  # рост

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed() * self.KM_H_IN_M_S
        height_in_meters = self.height / self.M_IN_SM  # преобразование в метры

        calories = ((self.MULTI_WEIGHT * self.weight + (mean_speed ** 2 / height_in_meters) * self.MULTI_HEIGHT *
                     self.weight) * self.duration * self.SEC_IN_MIN)

        return calories


class Swimming(Training):
    LEN_STEP = 1.38
    MID_SPEED = 1.1
    MULTI_SPEED = 2
    M_IN_KM = 1000

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool) / self.M_IN_KM / self.duration

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed()
        calories = (mean_speed + self.MID_SPEED) * self.MULTI_SPEED * self.weight * self.duration
        return calories


def read_package(workout_type, data):
    workout_classes = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    return workout_classes[workout_type](*data)


def main(training_instance):
    info = training_instance.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),  # 25 м, 40 раз
        ('RUN', [15000, 1, 75]),  # 75 кг
        ('WLK', [9000, 1, 75, 180]),  # 180 см
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
