import argparse

greetings_parser = argparse.ArgumentParser()
greetings_parser.add_argument('--salutation', action='store', type=str, required=True)
greetings_parser.add_argument('--name', action='store', type=str, required=True)
greetings_parser.add_argument('--lang', type=str, help='Mention the language in which your operation is written. In this case it is python', required=True)


args = greetings_parser.parse_args()

print(f"Hello { args.salutation}.{ args.name }! This is the { args.lang } world!")
