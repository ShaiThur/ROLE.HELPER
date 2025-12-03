from enum import Enum


class Intent(str, Enum):
    HISTORY = "получить историю общения"
    NEW_SCENARIO = "придумать новый сеттинг или сценарий для игры"
    CREATE_USER = "создать ИЛИ описать новых персонажей"
    ASK_QUESTION = "вопрос о событиях, про которые говорил пользователь или которые произошли в игре"
    OTHER = "непонятный вопрос"


class ImageTheme(str, Enum):
    USER = "USER"
    THEME = "THEME"

    def value_of(self) -> str:
        if self == ImageTheme.USER:
            return "пользователя"
        if self == ImageTheme.THEME:
            return "локации, сеттинга или истории"
