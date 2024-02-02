from .models import ProductReview
from django.db.models import Count,ExpressionWrapper,FloatField

def get_rating(product_id):

    product_rating1 = ProductReview.objects.filter(product = product_id)

    rating_count=product_rating1.values('rating').annotate(count=Count('rating'),
                                                           percentage= ExpressionWrapper(100.0 * Count('rating')/product_rating1.count(),output_field=FloatField())) .order_by('-rating').annotate()
   
    rating_dict = {}
    rating_list = []
    found = 0
    for i in range(5,0,-1):
        found = 0
        for j in range(0,(rating_count.count())):
            if rating_count[j]['rating'] == i:
               found = 1
               break

        if found == 1:
            rating_list.append(rating_count[j])
            


        else:
            rating_dict['rating'] = i
            rating_dict['count'] = 0
            rating_dict['percentage'] = 0
            rating_list.append(rating_dict)
        rating_dict = {}
    return rating_list

def get_star_rating(list):
    sum = 0
    mul = 0
    star_rating = 0
    print(';lkk', list)
    try:
        for i in list:
            mul +=  i['rating'] * i['count']
            sum += i['count']
    
        
        star_rating = mul/sum
    except:
        star_rating = 0
    return star_rating
    return 0