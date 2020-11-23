from django import template
register = template.Library()

@register.simple_tag
def define_color(column, players):
    for player in players : 
        if player.userNumber == column :
            return player.color
    return "black"


@register.simple_tag
def next(number = 0):
    return int(number) + 1


@register.simple_tag
def define_variable(var=0):
    return int(var)


@register.simple_tag
def define_class(players, iLine, iColumn):
    for player in players :
        if player.posX == int(iColumn) and player.posY == int(iLine) :
            return "actual_position"
    return ""