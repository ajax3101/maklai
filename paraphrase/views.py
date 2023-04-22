from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def paraphrase(request):
    tree = request.GET.get('tree')
    limit = request.GET.get('limit', 20)
    
    # perform paraphrasing and return results as a list of JSON objects
    results = []
    # ...
    
    # save results to file
    with open('expected-result-example.json', 'w') as f:
        json.dump(results, f)
    
    return JsonResponse(results, safe=False)
