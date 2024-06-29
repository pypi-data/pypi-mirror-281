### Installation
```bash
$ pip install django-url2template
```

#### `settings.py`
```python
INSTALLED_APPS+=['django_url2template']
```

#### `migrate`
```bash
$ python manage.py migrate
```

#### `views.py`
```python
from django.shortcuts import render
from django_url2template.utils import get_template_name

template_name = get_template_name(request.path[1:])
if template_name:
    return render(request, template_name, {})
### Models
model|table|columns/fields
-|-|-
`Map`|`django_url2template_map`|id,url,template_name

