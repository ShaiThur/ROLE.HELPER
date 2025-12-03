from enum import Enum


class Intent(str, Enum):
    HISTORY = "получить историю общения"
    NEW_SCENARIO = "придумать новый сеттинг или сценарий для игры"
    CREATE_USER = "создать ИЛИ описать новых персонажей"
    ASK_QUESTION = "вопрос о событиях, про которые говорил пользователь или которые произошли в игре"
    OTHER = "непонятный вопрос"


class ImageTheme(str, Enum):
    USER = "USER"
    LOCATION = "LOCATION"
