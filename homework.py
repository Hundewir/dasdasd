from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    '''Множитель для получения кол-ва метров в километрах'''
    LEN_STEP = 0.65
    '''Расстояние преодолеваемое за один шаг'''
    MIN_IN_H = 60
    '''Множитель для получения кол-ва минут в часе'''

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.mean_speed = self.get_distance() / self.duration
        return self.mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
              'Определите метод сжигания калорий в %s.'
              % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    '''Множитель сожжённых калорий от скорости'''
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    '''Значение перепада скорости'''

    def get_spent_calories(self) -> float:
        time_in_mins = self.duration * 60
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * time_in_mins)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    '''Множитель сожжёных калорий от веса'''
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    '''Множитель сожжёных калорий от веса'''
    CM_IN_M = 100
    '''Делитель для получения роста в сантиметрах'''
    KMH_IN_MSEC = 0.278
    '''Множитель для перевода км/ч в м/с'''

    def __init__(self, action: int, duration: float,
                 weight: float, height: int):
        super().__init__(action, duration, weight)
        self.height: float = height / self.CM_IN_M

    def get_spent_calories(self) -> float:
        time_in_mins = self.duration * 60
        speed_in_msec = self.get_mean_speed() * self.KMH_IN_MSEC
        return ((self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight
                + (speed_in_msec**2 / self.height)
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight) * time_in_mins)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    '''Множитель для определения расстояния преодолеваемого за один гребок'''
    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1
    '''Множитель сжигаемых калорий за скорость'''
    CALORIES_MEAN_SPEED_SHIFT = 2
    '''Значение перепадов скорости'''

    def __init__(self, action: int, duration: int, weight: int,
                 length_pool: int, count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        return ((mean_speed
                + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                * 2 * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    classic_dict = {'SWM': Swimming,
                    'RUN': Running,
                    'WLK': SportsWalking}
    if workout_type in classic_dict:
        return classic_dict[workout_type](*data)
    raise AttributeError('Такого типа тренировки нет')


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
