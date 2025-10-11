from enum import Enum


class Intent(str, Enum):
    HISTORY = "получить историю общения"
    NEW_SCENE = "придумать новый сценарий"
    ASK_QUESTION = "вопрос о событиях, про которые говорил пользователь или которые произошли в игре"
    OTHER = "непонятный вопрос"
