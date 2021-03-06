from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from user.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
import datetime
from annotation.models import Guess
from videos.models import BVH
import sys

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def scorePage(request):
		return render(request, 'score.html')


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def nextRoundPage(request):
	if	User.objects.all().first() is None:
		return HttpResponseRedirect('/userdetails')
	else:
		u = User.objects.all().first()
		u.current_round = (Guess.objects.count()-1)/5 + 1
		u.save()
		return render(request, 'nextround.html')


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def score(request):
	u = User.objects.all().first()
	return JsonResponse({'score':u.score, 'total':BVH.objects.count()})


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def score2(request):
	u = User.objects.all().first()
	return JsonResponse({'score':u.score, 'total':Guess.objects.count()-1})


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mainPage(request):
	if	User.objects.all().first() is None:
		return HttpResponseRedirect('/userdetails')
	else:
		return render(request, 'dashboard.html')

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def sendNewVideo(request):
	u = User.objects.all().first()
	pending = Guess.objects.filter(guess="")
	video = pending.first()
	if video is not None:
		return JsonResponse({'bvhPath': video.file.path, 'o1': video.file.option1, 'o2': video.file.option2, 'o3': video.file.option3, 'o4': video.file.option4, 'correct': u.score, 'total': Guess.objects.count()-1, 'round':u.current_round})
	else:
		done = Guess.objects.exclude(guess="").values('file')
		possible = BVH.objects.exclude(pk__in=done)
		video = possible.first()
		if video is None:
			return HttpResponse('/score',status=404)

		Guess.objects.create(file=video)
		return JsonResponse({'bvhPath': video.path, 'o1': video.option1, 'o2': video.option2, 'o3': video.option3, 'o4': video.option4, 'correct': u.score, 'total': Guess.objects.count()-1, 'round':u.current_round})

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def submitAnnotation(request):
	guess = request.POST.get('guess')
	print(guess)
	num_pause = request.POST.get('num_pause')
	num_replay = request.POST.get('num_replay')
	v = Guess.objects.filter(guess="").first()
	print(v)
	v.guess = guess
	v.num_replay = num_replay
	v.num_pause = num_pause
	u = User.objects.all().first()
	if guess == v.file.action:
		u.score += 1
		u.save()
	v.save()
	return JsonResponse({'correctAnswer':v.file.action, 'status':guess == v.file.action})
