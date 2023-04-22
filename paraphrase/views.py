from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_http_methods
from django.shortcuts import render
from nltk import Tree
from itertools import permutations
import json


def index(request):
    return render(request, 'paraphrase/index.html')

def paraphrase_view(request):
    # Get the tree and limit parameters from the request
    tree = request.GET.get('tree')
    limit = request.GET.get('limit', 20)

    # Paraphrase the tree and get a list of paraphrases
    paraphrases = paraphrase_tree(tree, limit)

    # Render the template with the paraphrases as a context variable
    return render(request, 'paraphrase/paraphrase.html', {'paraphrases': paraphrases})

# @require_http_methods(["GET"])
# def paraphrase(request):
#     """
#     Endpoint for paraphrasing a syntactic tree of an English text
#     """
#     # Get the syntax tree from the query parameters
#     tree_string = request.GET.get('tree', None)

#     if tree_string is None:
#         return JsonResponse({'error': 'Syntax tree not provided.'}, status=400)

#     # Parse the syntax tree string into an NLTK Tree object
#     try:
#         tree = Tree.fromstring(tree_string)
#     except ValueError:
#         return JsonResponse({'error': 'Invalid syntax tree format.'}, status=400)

#     # Get the maximum number of paraphrased sentences to generate
#     limit = int(request.GET.get('limit', 20))

#     # Paraphrase the tree
#     paraphrased_trees = paraphrase_tree(tree, limit)

#     # Return the paraphrased trees as a JSON response and save to a file
#     response_data = {'paraphrased_trees': paraphrased_trees}
#     with open('expected-result-example.json', 'w') as f:
#         json.dump(response_data, f)
#     return JsonResponse(response_data)


def paraphrase_tree(tree, limit=20):
    """
    Paraphrases the given syntax tree and returns a list of paraphrased trees.
    """
    # Find all noun phrases in the tree that consist of multiple noun phrases separated by commas or "and"
    #np_trees = [subtree for subtree in tree.subtrees(lambda t: t.label() == 'NP' and (',' in t.flatten() or 'and' in t.flatten()))]

    paraphrased_trees = []

    # Generate permutations of the noun phrases and create new trees with the permutations
    # for np_tree in np_trees:
    #     np_subtrees = list(np_tree.subtrees(lambda t: t.label() == 'NP'))
    #     np_subtree_strings = [str(np_subtree).strip()
    #                           for np_subtree in np_subtrees]

    #     for permutation in permutations(np_subtree_strings):
    #         new_np_subtrees = [Tree.fromstring(
    #             permutation[i]) for i in range(len(permutation))]
    #         new_np_tree = np_tree.copy(deep=True)
    #         for i, np_subtree in enumerate(np_subtrees):
    #             new_np_tree[tree.leaf_treeposition(
    #                 np_subtree.leaves()[0])] = new_np_subtrees[i]
    #         paraphrased_tree = tree.copy(deep=True)
    #         paraphrased_tree[tree.leaf_treeposition(
    #             np_tree.leaves()[0])] = new_np_tree
    #         paraphrased_trees.append(str(paraphrased_tree))

    #         if len(paraphrased_trees) >= limit:
    #             break

    #     if len(paraphrased_trees) >= limit:
    #         break

    # return paraphrased_trees



