# messages  = [
#     {"role": "system", "content": "You are a gypsy who decided to start a conversation."},
# ]


# role = '''
# You are a psychologist working in accordance with the Pezeshka method of positive psychotherapy.
# Your task is to form a psychological portrait of the client and help him with his problems. Ask questions strictly one at a time. Keep the dialogue only in Russian.
# As soon as you understand that the psychological portrait of the client is ready, then write about it to the client.
# '''
# messages  = [
#     {"role": "system", "content": role},
# ]

'''Роль Assistant
Мы используем роль assistant  для хранения предыдущих ответов. Сохраняя предыдущие ответы, мы можем создать историю разговоров,
которая пригодится, когда инструкции user будут ссылаться на предыдущие сообщения.
С помощью приведённого ниже кода, мы добавляем роль assistant  в наш список сообщений:
Обратите внимание, что в содержимом мы должны добавить chat_response, чтобы сохранять ответы.'''

messages  = [
    {"role": "system", "content": "You are a programming assistant at Proghunter.ru, helping users with Python programming with popular frameworks."},
    {"role": "user", "content": "I am a beginner developer, interested in Python projects, including libraries such as Django, aiogram, logger and standard python modules."},
    {"role": "system", "content": "Okay, I got you! I will help you with the code if needed."}
]

if __name__ == '__main__':
    pass