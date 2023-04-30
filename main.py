import itertools
import json
from flask import Flask, request, jsonify, render_template
from nltk.tree import Tree

app = Flask(__name__)


def find_noun_phrases(tree, phrases):
    """
    Функция находит все именные фразы (NP) в дереве и добавляет их в список `phrases`

    :param tree: объект `Tree` - синтаксическое дерево
    :type tree: nltk.tree.Tree
    :param phrases: список, в который будут добавляться именные фразы
    :type phrases: list[str]
    """
    if tree.label() == 'NP':
        phrase = ' '.join(tree.leaves())
        phrases.append(phrase)
    for child in tree:
        if isinstance(child, Tree):
            find_noun_phrases(child, phrases)


def replace_noun_phrases(tree, phrase_permutation):
    """
    Функция заменяет именные фразы в дереве на перестановки из списка `phrase_permutation`

    :param tree: объект `Tree` - синтаксическое дерево
    :type tree: nltk.tree.Tree
    :param phrase_permutation: список перестановок именных фраз
    :type phrase_permutation: list[str]
    """
    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            for i, phrase in enumerate(phrase_permutation):
                if ' '.join(subtree.leaves()) == phrase:
                    subtree.clear()
                    subtree.insert(0, Tree.fromstring('(' + phrase + ')'))

@app.route('/')
def index():
    """
    Displays the index page with instructions on how to use the application.

    Parameters:
    None

    Returns:
    str: The HTML content of the index page.
    """
    return render_template('index.html')

@app.route('/paraphrase', methods=['GET'])
def paraphrase():
    """
    Эндпоинт, который принимает синтаксическое дерево английского текста и возвращает его перефразированные версии.
    Возвращает список перефразированных деревьев в формате JSON.

    :return: JSON-объект с ключом "paraphrases" и списком перефразированных деревьев
    :rtype: flask.Response
    """
    tree_string = request.args.get('tree')
    limit = int(request.args.get('limit', 20))
    tree = Tree.fromstring(tree_string)
    phrases = []
    find_noun_phrases(tree, phrases)
    noun_phrases = [phrase for phrase in phrases if ' ' in phrase]
    paraphrases = []
    for i in range(2, len(noun_phrases)+1):
        for combination in itertools.combinations(noun_phrases, i):
            for permutation in itertools.permutations(combination):
                new_tree = tree.copy(deep=True)
                replace_noun_phrases(new_tree, permutation)
                paraphrase = str(new_tree).replace('\n', '')
                if paraphrase not in paraphrases:
                    paraphrases.append(paraphrase)
                    if len(paraphrases) == limit:
                        break
            else:
                continue
            break
        else:
            continue
        break
    # Save the paraphrases to a file
    with open('output.json', 'w') as f:
        json.dump({'paraphrases': [{'tree': tree} for tree in paraphrases]}, f)

    return jsonify({'paraphrases': [{'tree': tree} for tree in paraphrases]})


if __name__ == '__main__':
    app.run(debug=True)