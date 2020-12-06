from chatterbot import ChatBot
from chatterbot.response_selection import get_first_response, get_most_frequent_response
from chatterbot.comparisons import levenshtein_distance

taylorchatbot = ChatBot(
    "Taylor",
    storage_adapter = "chatterbot.storage.SQLStorageAdapter",
    database = "./db.sqlite3",
    input_adapter = "chatterbot.input.VariableInputTypeAdapter",
    output_adapter = "chatterbot.output.OutputAdapter",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
        }
    ],
    statement_comparison_function = levenshtein_distance,
    response_selection_method = get_first_response
)
