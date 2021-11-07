import view_count

def view(name: str):
    x = int(view_count.get(name)['view_count'])
    print(name, x)
    return x

def pageview_sort(lst: list):
    return sorted(lst,key=view,reverse=True)
