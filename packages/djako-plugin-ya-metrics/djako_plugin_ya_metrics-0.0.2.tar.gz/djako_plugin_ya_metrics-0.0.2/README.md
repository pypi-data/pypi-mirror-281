============
django-djako_plugin_ya_metrics
============

djako_plugin_ya_metrics - Это плагин для Djako, который предоставляет 
интеграцию с API Яндекс метрики и визуализирует счётчики через Chart.js

Quick start
-----------

1. Add "djako_plugin_ya_metrics" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "djako_plugin_ya_metrics",
    ]

2. Include the polls URLconf in your project urls.py like this::

    path("polls/", include("djako_plugin_ya_metrics.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit the admin to create a poll.