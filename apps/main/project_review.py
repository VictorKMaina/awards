from apps.api.models import Project, Review
import math as m

def review_average(project):
    reviews = Review.find_by_project(project)
    design = 0
    usability = 0
    content = 0

    for review in reviews:
        design += review.design
        usability += review.usability
        content += review.content

    if design > 0:
        design = round(design/len(reviews), 1)
    if usability > 0:
        usability = round(usability/len(reviews), 1)
    if content > 0:
        content = round(content/len(reviews), 1)

    average = (design + usability + content)

    if average > 0:
        average = round(average/3, 1)

    return {"design": design, "usability": usability, "content": content, "average":average}

    
