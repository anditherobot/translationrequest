from django import template

#from your_app.models import Language  # Import your Language model

register = template.Library()

@register.inclusion_tag('app/_languages.html')
def language_cards():
   languages = [
        {
            'name': 'Haitian Creole',
            'card_color': '#e9f2f4',
            'flag_image': 'app/images/haitian_creole.svg',
            'classification': 'Romance',
            'speakers': 'Speakers: 12M',
            'origin': 'Haiti',
            'essence': 'French-based, spoken primarily in Haiti.',
        },
        {
            'name': 'French',
            'card_color': '#ece6f2',
            'flag_image': 'app/images/french.svg',
            'classification': 'Romance',
            'speakers': 'Speakers: 274M',
            'origin': 'France',
            'essence': 'Widely spoken, influential in diplomacy, culture, and literature.',
        },
        {
            'name': 'English',
            'card_color': '#ede8e1',
            'flag_image': 'app/images/english.svg',
            'classification': 'Germanic',
            'speakers': 'Speakers: 1.3B',
            'origin': 'England',
            'essence': 'Global lingua franca, business, science, media.',
        },
       
   ]
    
   return {'languages': languages}
