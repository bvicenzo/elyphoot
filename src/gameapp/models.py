# coding=utf-8

from django.db import models

PLAYER_POSITION = (
    (0, u'Goalkeeper'),
    (1, u'Defense'),
    (2, u'Midfield'),
    (3, u'Forward'),
)

TEAM_FORMATION = (
    (0, u'3-3-4'),
    (1, u'3-4-3'),
    (2, u'3-5-2'),
    (3, u'3-6-1'),
    (4, u'2-3-5'),
    (5, u'4-2-4'),
    (6, u'4-3-3'),
    (7, u'4-3-2-1'),
    (8, u'4-4-2'),
    (9, u'4-5-1'),
    (10, u'4-6-0'),
    (11, u'5-3-2'),
    (12, u'5-4-1'),
    (13, u'5-5-0'),
    (14, u'4-1-3-2'),
    (15, u'Carrossel'),
)

TEAM_SERIE = (
    (0, u'Série A'),
    (1, u'Série B'),
    (2, u'Série C'),
    (3, u'Série D'),
)

# blank is only used for validations on django's admin tool
# null is intended to be used for nullable fields on the database

class Player(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    country = models.CharField(max_length=20)
    wage = models.IntegerField(blank=True)
    position = models.IntegerField(choices=PLAYER_POSITION)
    kick = models.IntegerField(blank=True)
    dribble = models.IntegerField(blank=True)
    strength = models.IntegerField(blank=True)
    brave = models.IntegerField(blank=True)
    luck = models.IntegerField(blank=True)
    health = models.IntegerField(blank=True)
    
    def __unicode__(self):
        return self.name + ' [' + self.nickname + ']'
    
class Team(models.Model):
    name = models.CharField(max_length=100)
    money = models.IntegerField(blank=True, default=0)
    color1 = models.IntegerField(default=255)
    color2 = models.IntegerField(default=255)
    color3 = models.IntegerField(default=255)
    serie = models.IntegerField(choices=TEAM_SERIE)
    player = models.ManyToManyField(Player, related_name='players')
    squad = models.ManyToManyField(Player, related_name='squad_members')
    
    def __unicode__(self):
        return self.name
    
class PlayerInstance(models.Model):
    base_player = models.ForeignKey(Player)
    kick = models.IntegerField(blank=True)
    dribble = models.IntegerField(blank=True)
    strength = models.IntegerField(blank=True)
    brave = models.IntegerField(blank=True)
    luck = models.IntegerField(blank=True)
    health = models.IntegerField(blank=True)
    
    def __unicode__(self):
        return self.base_player.name
    
class TeamInstance(models.Model):
    base_team = models.ForeignKey(Team)
    player = models.ManyToManyField(PlayerInstance, related_name='players')
    squad = models.ManyToManyField(PlayerInstance, related_name='squad_members')
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.base_team.name
    
class Match(models.Model):
    team_a = models.ForeignKey(TeamInstance, null=True, blank=True, related_name='team_a')
    team_b = models.ForeignKey(TeamInstance, null=True, blank=True, related_name='team_b')
    goals_a = models.IntegerField(default=0)
    goals_b = models.IntegerField(default=0)
    resolved = models.BooleanField(default=False) # was the match played already?
    
    def __unicode__(self):
        if self.resolved:
            return self.team_a.base_team.name + ' ' + str(self.goals_a) + ' X ' + str(self.goals_b) + ' ' + self.team_b.base_team.name
        else:
            return self.team_a.base_team.name + ' ? X ? ' + self.team_b.base_team.name

class Round(models.Model):
    match = models.ManyToManyField(Match, null=True, blank=True, related_name='matches')
    resolved = models.BooleanField(default=False) # was the round completed?
    
    def __unicode__(self):
        return 'DONE? ' + str(self.resolved)

class Season(models.Model):
    current_round = models.ForeignKey(Round, null=True, blank=True)
    winner = models.ForeignKey(TeamInstance, blank=True, null=True, related_name='winner_team')
    my_team = models.ForeignKey(TeamInstance, blank=True, null=True, related_name='manager_team')
    team = models.ManyToManyField(TeamInstance, blank=True, null=True, related_name='season_teams')
    year = models.IntegerField()
    completed = models.BooleanField(default=False)
    
    def __unicode__(self):
        return str(self.year) + ' | COMPLETED? ' + str(self.complete)

class Manager(models.Model):
    current_season = models.ForeignKey(Season, null=True, blank=True) # if current_season is null we have to create one before the user is able to play
    nickname = models.CharField(max_length=20, default='Manager')
    total_points = models.IntegerField(default=0)
    season = models.ManyToManyField(Season, null=True, blank=True, related_name='seasons')
    
    def __unicode__(self):
        return self.nickname